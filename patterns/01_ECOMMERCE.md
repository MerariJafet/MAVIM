# Blueprint 01: E-Commerce Architecture

**Objetivo:** Definir la arquitectura para plataformas de comercio electrónico transaccionales de alto volumen, garantizando la consistencia y escalabilidad a través de la separación de módulos.

## Mapa de Módulos

| Módulo | Responsabilidad | Interface (API Síncrona) | Eventos (Asíncronos) |
| :--- | :--- | :--- | :--- |
| **Catalog** | Gestión de productos, categorías y precios. | `GET /products/{id}` | `ProductPriceUpdated`, `ProductActivated` |
| **Cart** | Gestión de la canasta de compras temporal del usuario. | `POST /cart/items` | `CartAbandoned` |
| **Checkout/Payments**| Procesamiento de pagos y generación de la orden. | `POST /checkout/pay` | `OrderPlaced`, `PaymentSucceeded`, `PaymentFailed` |
| **Inventory** | Control de stock físico y reservas. | `POST /inventory/reserve`| `StockReserved`, `StockDepleted` |

## Esquema de Datos (Entidades Clave)

Todas las entidades **DEBEN** utilizar `UUID v4` como identificador primario.

- **Catalog:** `Product (id: UUID, skus: JSON, details: JSON)`
- **Cart:** `Cart (id: UUID, session_id: UUID, items: JSON)`
- **Checkout:** `Order (id: UUID, customer_id: UUID, total_amount: Decimal, status: String)`
- **Inventory:** `StockItem (id: UUID, product_id: UUID, quantity_available: Int)`

## Detalles Críticos de Implementación (Senior Level)

### 1. Sistema Financiero Incorruptible (Doble-Entrada)
Todo sistema que maneje balances de usuarios, pagos o escrow en un Marketplace **NUNCA** debe usar una simple columna `balance: float` que se actualiza. Debe usarse un **Ledger de Doble Entrada**.
- **Regla:** Cada transacción financiera genera al menos dos líneas inmutables (`Debit` y `Credit`) que sumadas siempre deben dar `0`.
- **Tipo de Dato:** Manejar todo el dinero utilizando **ENTEROS (Integers/BigInts) que representen las fracciones más pequeñas (ej: centavos)**. NUNCA usar `float` o `double` por los errores de redondeo en coma flotante.

### 2. Flujo de Escrow (Depósito en Garantía)
En marketplaces C2C/B2C, el comprador no le paga directamente al vendedor. 
1. `UserA` paga -> Fondos van a cuenta `Escrow_Marketplace`.
2. Se confirma recepción del servicio/producto.
3. Se liberan fondos -> De `Escrow_Marketplace` a `UserB` (menos comisión de plataforma).

## Cuidados Críticos (Trampas a Evitar)

> [!CAUTION]
> 1. **Prohibido JOINs entre Cart e Inventory:** El módulo `Cart` no lee directamente de la base de datos de `Inventory`. `Cart` debe llamar al API de `Inventory` para verificar la disponibilidad en el momento del checkout.
> 2. **IDs Incrementales:** Nunca uses `id: 1` para un `Product` u `Order`. Los competidores podrían deducir tu volumen de ventas usando IDs secuenciales. Siempre usa `UUIDv4`.
> 3. **Consistencia Eventual en Checkout:** El pago no debe restar stock secuencialmente en la misma transacción SQL. Se emite `PaymentSucceeded` y el módulo `Inventory` lo escucha para ajustar el stock definitivo.
