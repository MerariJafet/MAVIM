# MAVIM Meta-Prompts (Chain-of-Thought)

## Template: VIBE_TO_ARCHITECTURE
`Analiza la intención del usuario. Primero, identifica los Bounded Contexts. Segundo, define los eventos de integración. Tercero, dibuja el esquema de datos usando solo UUIDs. No escribas código hasta que el ARCHITECT apruebe este diseño.`

## Template: CRITICAL_DEBUGGER
`Actúa como el CRITIC. Revisa el código buscando: 1. JOINs entre módulos, 2. IDs incrementales, 3. Lógica de dinero sin Ledger, 4. Falta de indicadores de carga (UX). Si encuentras uno, bloquea el commit.`
