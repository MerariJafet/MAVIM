# Patrón Avanzado: Marketplace con Ledger de Doble Entrada

## 1. El Motor Financiero (The Ledger)
No usar floats para dinero. Implementar un **Ledger de Doble Entrada** inmutable.
- **Entidades:** `Accounts` (Balance), `Transactions` (Débito/Crédito), `JournalEntries`.
- **Regla:** La suma de débitos y créditos en un `JournalEntry` siempre debe ser CERO.

## 2. Catálogo Polimórfico
Usar **JSONB** para atributos específicos de categoría. 
- **Listing Table:** `id (UUID)`, `seller_id`, `base_price`, `attributes (JSONB)`.

## 3. Escrow y Workflows
Usar **Temporal.io** para orquestar la liberación de fondos. El dinero no se mueve al vendedor hasta que el `CRITIC` o el `USER` confirmen la entrega (14 días de guarda).
