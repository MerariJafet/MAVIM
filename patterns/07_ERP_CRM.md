# Blueprint 07: ERP & CRM Integrado

**Objetivo:** Arquitectura robusta para sistemas internos empresariales y gestión de la relación con clientes (CRM), garantizando flujos operativos estrictos (ERP) sin acoplar fuertemente los procesos de ventas.

## Mapa de Módulos

| Módulo | Responsabilidad | Interface (API Síncrona) | Eventos (Asíncronos) |
| :--- | :--- | :--- | :--- |
| **Identity/HR** | Gestión de empleados, roles corporativos y accesos. | `GET /hr/employee/{id}` | `EmployeeHired`, `EmployeeTerminated`, `RoleAssigned` |
| **CRM (Sales)** | Gestión de leads, oportunidades de venta y clientes. | `POST /crm/lead` | `LeadConverted`, `OpportunityWon`, `OpportunityLost` |
| **ERP (Operations)** | Control de compras, manufactura y despachos. | `POST /erp/order` | `MaterialsRequested`, `OrderDispatched` |
| **Finance** | Contabilidad, cuentas por cobrar y pagar. | `POST /finance/invoice`| `InvoiceGenerated`, `PaymentReceived` |

## Esquema de Datos (Entidades Clave)

Todas las entidades **DEBEN** utilizar `UUID v4` como identificador primario.

- **Identity/HR:** `Employee (id: UUID, department: String, role: String)`
- **CRM:** `Lead (id: UUID, status: String)`, `Customer (id: UUID, company_name: String)`
- **ERP:** `WorkOrder (id: UUID, requirements: JSON, status: String)`
- **Finance:** `Invoice (id: UUID, customer_id: UUID, amount: Decimal, due_date: Date)`

## Detalles Críticos de Implementación (Senior Level)

### 1. Logística y On-Demand (Mapas y Rutas)
Si el ERP integra despachos físicos, logística, tracking de vehículos o "Surge Pricing" estilo Uber:
- **Indexación Espacial:** **No** utilices simples radios geográficos y queries de distancia geo-espacial pesadas. Utiliza el sistema **H3 (Hexagonal Hierarchical Spatial Indexing de Uber)**.
- Agrupa a los agentes y órdenes en polígonos hexagonales para pre-calcular precios dinámicos y densidades de demanda de forma ultra-rápida.

### 2. Relaciones Polimórficas Estructuradas
- Un documento contable o un ticket puede estar asociado a N tipos de entidades (`Order`, `Lead`, `Employee`).
- En bases de datos relacionales, prefiere tablas asociativas específicas antes que usar un modelo puramente polimórfico (`entity_id`, `entity_type`) ciego que rompe la integridad referencial de las llaves foráneas. Si el volumen no es crítico, encapsula referenciales en columnas JSONB tipadas.

## Cuidados Críticos (Trampas a Evitar)

> [!CAUTION]
> 1. **El Vendedor NO debe emitir facturas (Invoices):** El `CRM` solo registra que la Oportunidad fue ganada (`OpportunityWon`). Es el módulo de `Finance` el que escucha el evento para registrar cuentas por cobrar.
> 2. **Base de datos compartida:** Es un antipatrón tener la tabla de `Customers` compartida entre CRM, ERP y Finance. Pasa el `Customer ID` (UUID) en el evento y cada módulo guarda solo los datos que necesita del cliente.
> 3. **Acoplamiento de Procesos:** No atar un WorkOrder (ERP) a la aprobación final de la venta usando consultas directas al módulo de CRM, hazlo mediante un estado suscrito a eventos para soportar caídas de módulos.
