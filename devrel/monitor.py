"""
MAVIM DevRel Intelligence System — Main Monitor
═══════════════════════════════════════════════
Scans Reddit, Stack Overflow, and GitHub for threads where MAVIM provides
genuine technical value. Generates opportunity reports with response drafts
for human review. Never posts automatically.

Usage:
    python monitor.py              # Single scan + report
    python monitor.py --watch      # Continuous monitoring (every N minutes)
    python monitor.py --dry-run    # Scan without saving or emailing

Requirements:
    pip install -r requirements.txt
    cp .env.example .env && fill in credentials
"""
import sys
import time
import argparse
from datetime import datetime, timezone
from pathlib import Path

# Add devrel root to path
sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import schedule

from intelligence.relevance import filter_relevant
from reports.generator import generate_report
from notifications.email_notifier import send_opportunity_alert, check_inbox_for_replies
from config import SCAN_INTERVAL_MINUTES, HIGH_PRIORITY_SCORE

console = Console()


def run_scan(dry_run: bool = False) -> None:
    """Execute a full scan across all sources and generate report."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    console.print(Panel(
        f"[bold blue]MAVIM DevRel Intelligence Scan[/bold blue]\n"
        f"[dim]{now}[/dim]",
        border_style="blue"
    ))

    all_threads = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:

        # ── Reddit ────────────────────────────────────────────────────────
        task = progress.add_task("Scanning Reddit...", total=None)
        try:
            from sources.reddit_monitor import fetch_threads as reddit_fetch
            reddit_threads = reddit_fetch()
            all_threads.extend(reddit_threads)
            progress.update(task, description=f"Reddit ✓ ({len(reddit_threads)} new)")
        except Exception as e:
            progress.update(task, description=f"Reddit ✗ ({e})")

        # ── Stack Overflow ────────────────────────────────────────────────
        task = progress.add_task("Scanning Stack Overflow...", total=None)
        try:
            from sources.stackoverflow_monitor import fetch_threads as so_fetch
            so_threads = so_fetch()
            all_threads.extend(so_threads)
            progress.update(task, description=f"Stack Overflow ✓ ({len(so_threads)} new)")
        except Exception as e:
            progress.update(task, description=f"Stack Overflow ✗ ({e})")

        # ── GitHub ────────────────────────────────────────────────────────
        task = progress.add_task("Scanning GitHub...", total=None)
        try:
            from sources.github_monitor import fetch_threads as gh_fetch, fetch_mavim_feedback
            gh_threads = gh_fetch()
            mavim_feedback = fetch_mavim_feedback()
            all_threads.extend(gh_threads + mavim_feedback)
            progress.update(task, description=f"GitHub ✓ ({len(gh_threads)} + {len(mavim_feedback)} MAVIM feedback)")
        except Exception as e:
            progress.update(task, description=f"GitHub ✗ ({e})")

        # ── Inbox ─────────────────────────────────────────────────────────
        task = progress.add_task("Checking inbox...", total=None)
        try:
            inbox_replies = check_inbox_for_replies()
            progress.update(task, description=f"Inbox ✓ ({len(inbox_replies)} community replies)")
        except Exception as e:
            inbox_replies = []
            progress.update(task, description=f"Inbox ✗ ({e})")

        # ── Scoring ───────────────────────────────────────────────────────
        task = progress.add_task("Scoring relevance...", total=None)
        relevant = filter_relevant(all_threads)
        progress.update(task, description=f"Scored ✓ ({len(relevant)} relevant / {len(all_threads)} total)")

    # ── Display Results ───────────────────────────────────────────────────
    _display_summary(relevant)

    if not relevant:
        console.print("[dim]No relevant threads found in this scan.[/dim]")
        return

    # ── Generate Report ───────────────────────────────────────────────────
    if not dry_run:
        _, report_path = generate_report(relevant, inbox_replies)
        console.print(f"\n[green]Report saved:[/green] {report_path}")

        # Email alert for high-priority threads
        high_threads = [t for t in relevant if t.relevance_score >= HIGH_PRIORITY_SCORE]
        if high_threads:
            sent = send_opportunity_alert(high_threads, report_path)
            if sent:
                console.print(f"[green]Email alert sent:[/green] {len(high_threads)} high-priority threads")
    else:
        console.print("\n[yellow][dry-run] Report and email skipped[/yellow]")

    # ── Top 3 Actionable ──────────────────────────────────────────────────
    _display_top_opportunities(relevant[:3])


def _display_summary(threads: list) -> None:
    table = Table(title="Scan Results", border_style="dim")
    table.add_column("Priority", style="bold")
    table.add_column("Count", justify="right")
    table.add_column("Sources")

    by_priority = {"CRITICAL": [], "HIGH": [], "MEDIUM": []}
    for t in threads:
        if t.priority in by_priority:
            by_priority[t.priority].append(t)

    colors = {"CRITICAL": "red", "HIGH": "yellow", "MEDIUM": "cyan"}
    for p, items in by_priority.items():
        if items:
            sources = ", ".join(set(t.source for t in items))
            table.add_row(
                f"[{colors[p]}]{p}[/{colors[p]}]",
                str(len(items)),
                sources,
            )

    console.print(table)


def _display_top_opportunities(threads: list) -> None:
    if not threads:
        return
    console.print("\n[bold]Top Opportunities (open the full report for drafts):[/bold]")
    for i, t in enumerate(threads, 1):
        sop = t.mapped_sops[0]["sop"] if t.mapped_sops else "general"
        console.print(
            f"  {i}. [{t.priority}] [link={t.url}]{t.title[:65]}[/link]\n"
            f"     {t.source.upper()} | Score: {t.relevance_score} | SOP: {sop}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="MAVIM DevRel Intelligence Monitor")
    parser.add_argument("--watch", action="store_true",
                        help=f"Run continuously every {SCAN_INTERVAL_MINUTES} minutes")
    parser.add_argument("--dry-run", action="store_true",
                        help="Scan without saving reports or sending emails")
    parser.add_argument("--interval", type=int, default=SCAN_INTERVAL_MINUTES,
                        help="Scan interval in minutes (with --watch)")
    args = parser.parse_args()

    if args.watch:
        console.print(f"[blue]Starting continuous monitoring (every {args.interval} min)[/blue]")
        run_scan(dry_run=args.dry_run)  # Run immediately on start
        schedule.every(args.interval).minutes.do(run_scan, dry_run=args.dry_run)
        while True:
            schedule.run_pending()
            time.sleep(30)
    else:
        run_scan(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
