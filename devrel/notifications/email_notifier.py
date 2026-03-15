"""
MAVIM DevRel — Email Notification System
SMTP for outbound alerts. IMAP for reading community notifications/replies.
"""
from __future__ import annotations
import smtplib
import imaplib
import email
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone
from typing import Optional
from config import (
    NOTIFY_EMAIL, NOTIFY_SMTP_HOST, NOTIFY_SMTP_PORT,
    NOTIFY_SMTP_USER, NOTIFY_SMTP_PASS, NOTIFY_IMAP_HOST
)


def send_opportunity_alert(threads: list, report_path: str) -> bool:
    """
    Send email digest when high-priority threads are found.
    Called only when threads with priority HIGH or CRITICAL are detected.
    """
    if not NOTIFY_SMTP_USER or not NOTIFY_SMTP_PASS:
        print("[Email] SMTP not configured — skipping notification.")
        return False

    critical = [t for t in threads if t.priority == "CRITICAL"]
    high = [t for t in threads if t.priority == "HIGH"]

    if not critical and not high:
        return False  # Don't send digest for only MEDIUM threads

    subject = f"MAVIM DevRel — {len(critical)} CRITICAL + {len(high)} HIGH opportunities"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Build HTML body
    html_rows = ""
    for t in (critical + high):
        sops = ", ".join(t.mapped_sops[0]["sop"] if t.mapped_sops else ["general"])
        html_rows += f"""
        <tr style="border-bottom: 1px solid #eee;">
            <td style="padding:8px; color:{'#dc2626' if t.priority == 'CRITICAL' else '#d97706'}">
                <strong>{t.priority}</strong>
            </td>
            <td style="padding:8px;">{t.source.upper()}</td>
            <td style="padding:8px;">
                <a href="{t.url}" style="color:#2563eb;">{t.title[:80]}...</a>
            </td>
            <td style="padding:8px;">{t.relevance_score:.1f}</td>
            <td style="padding:8px; font-size:11px; color:#666;">{sops}</td>
        </tr>
        """

    html = f"""
    <html><body style="font-family: monospace; max-width: 800px; margin: 0 auto;">
        <h2 style="color: #1e40af;">MAVIM DevRel — Opportunity Report</h2>
        <p style="color: #666;">{now} | Full report: <code>{report_path}</code></p>
        <table style="width:100%; border-collapse:collapse;">
            <thead>
                <tr style="background:#f3f4f6;">
                    <th style="padding:8px; text-align:left;">Priority</th>
                    <th style="padding:8px; text-align:left;">Source</th>
                    <th style="padding:8px; text-align:left;">Thread</th>
                    <th style="padding:8px; text-align:left;">Score</th>
                    <th style="padding:8px; text-align:left;">MAVIM SOP</th>
                </tr>
            </thead>
            <tbody>{html_rows}</tbody>
        </table>
        <p style="margin-top:24px; color:#666; font-size:12px;">
            MAVIM DevRel Intelligence System — github.com/MerariJafet/MAVIM
        </p>
    </body></html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = NOTIFY_SMTP_USER
    msg["To"] = NOTIFY_EMAIL
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(NOTIFY_SMTP_HOST, NOTIFY_SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(NOTIFY_SMTP_USER, NOTIFY_SMTP_PASS)
            server.sendmail(NOTIFY_SMTP_USER, NOTIFY_EMAIL, msg.as_string())
        print(f"[Email] Alert sent: {len(critical)} CRITICAL + {len(high)} HIGH")
        return True
    except Exception as e:
        print(f"[Email] Send failed: {e}")
        return False


def check_inbox_for_replies() -> list[dict]:
    """
    Read IMAP inbox for community reply notifications.
    Returns list of subjects/senders for logging in the report.
    Useful for tracking when your community responses get replies.
    """
    if not NOTIFY_IMAP_HOST or not NOTIFY_SMTP_USER or not NOTIFY_SMTP_PASS:
        return []

    replies = []
    try:
        mail = imaplib.IMAP4_SSL(NOTIFY_IMAP_HOST)
        mail.login(NOTIFY_SMTP_USER, NOTIFY_SMTP_PASS)
        mail.select("INBOX")

        # Search for unread messages in last 24h from community sources
        _, data = mail.search(None, "(UNSEEN)")
        ids = data[0].split()[-20:]  # Check last 20 unread

        for num in ids:
            _, msg_data = mail.fetch(num, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])
            subject = msg.get("Subject", "")
            sender = msg.get("From", "")

            # Tag community notifications
            source = "unknown"
            if "reddit" in sender.lower() or "reddit" in subject.lower():
                source = "reddit"
            elif "stackoverflow" in sender.lower() or "stack" in subject.lower():
                source = "stackoverflow"
            elif "github" in sender.lower():
                source = "github"

            if source != "unknown":
                replies.append({
                    "source": source,
                    "subject": subject[:100],
                    "from": sender[:60],
                    "received": msg.get("Date", ""),
                })

        mail.logout()
    except Exception as e:
        print(f"[IMAP] Error reading inbox: {e}")

    return replies
