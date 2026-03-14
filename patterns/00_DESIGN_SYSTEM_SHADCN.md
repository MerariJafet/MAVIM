# MAVIM Design System: shadcn/ui + Tailwind
Cualquier Front-end bajo MAVIM debe ser profesional, accesible y estéticamente superior.

## 1. Stack Obligatorio
- **Framework:** Next.js (App Router).
- **Styling:** Tailwind CSS.
- **Componentes:** shadcn/ui (Radix UI).
- **Iconos:** Lucide-react.

## 2. Reglas de Interfaz
- **Skeletons:** Todo fetch de datos debe mostrar un `Skeleton` de shadcn mientras carga. Prohibido el uso de spinners simples.
- **Dark Mode:** Implementar soporte nativo para `next-themes`.
- **Formularios:** Usar `react-hook-form` + `zod` para validación estricta en el cliente.
- **Toasts:** Notificaciones de éxito/error obligatorias para cada acción del usuario.
