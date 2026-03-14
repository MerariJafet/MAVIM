# Patrón 00: Design System & UI (Shadcn/Tailwind)

**Objetivo:** Garantizar que todas las aplicaciones construidas bajo la metodología MAVIM tengan un diseño visual de nivel *Premium / Senior* ("Out of the box"), evitando UIs genéricas, planas o disonantes.

## 1. Stack Obligatorio
El agente frontend DEBE utilizar el siguiente stack visual:
- **Tailwind CSS:** Para utilidades rápidas y responsivas.
- **shadcn/ui:** Como biblioteca base de componentes (Radix UI + Tailwind). NO instalar bibliotecas de componentes acopladas genéricas gigantes que sean difíciles de sobreescribir.
- **Lucide Icons:** Para la iconografía del sistema.

## 2. Paleta de Colores y Variables CSS (Jerarquía Visual)
- Configurar siempre el `globals.css` / `tailwind.config.ts` con variables CSS unificadas (`--background`, `--foreground`, `--primary`, `--muted`, `--border`).
- **Dark Mode First / Ready:** Todos los componentes deben testearse y soportar modo oscuro usando la utilidad `dark:` de Tailwind.
- NUNCA usar colores genéricos absolutos como `bg-red-500` para fondos estructurales. Usar la paleta semántica (`bg-destructive`, `text-destructive-foreground`).

## 3. Micro-Interacciones (El 'Vibe' Premium)
Diferenciar un MVP amateur de un producto real:
- **Estados de Interacción:** Todo botón o enlace interactivo DEBE tener estilos `hover:`, `focus:`, y `disabled:`.
- **Transiciones:** Utilizar clases como `transition-all duration-200 ease-in-out` para suavizar cualquier cambio visual de color o posición.
- **Skeletons (UX):** Para cargas de datos asíncronos en el cliente, PROHIBIDO dejar la pantalla en blanco. Utilizar el componente `<Skeleton>` de shadcn para dibujar el layout pendiente.
