# MAVIM Proyecto Piloto: Arquitectura de "FixR" (Marketplace de Servicios Generales On-Demand)

**Problema Real a Resolver:**
Se requiere una plataforma (FixR) donde usuarios puedan solicitar servicios de mantenimiento urgentes (plomería, electricidad, cerrajería) y profesionales cercanos ("Fixers") puedan aceptar estos trabajos en tiempo real, garantizando pagos seguros y precios dinámicos según la demanda por zona.

## 1. Fase de Intención (`VIBE_TO_SPEC` -> `INTENT_MANIFEST`)

- **El Problema:** Falta de confianza y lentitud al contratar profesionales de mantenimiento para emergencias en el hogar.
- **Los Actores:**
  - `Client`: Usuario que solicita el servicio.
  - `Fixer`: Profesional verificado que atiende la solicitud.
  - `Admin`: Personal de soporte y resolución de disputas.
- **Casos de Éxito (Definition of Done):**
  1. Un Client puede solicitar un servicio y el sistema lo empareja con un Fixer cercano en menos de 5 minutos.
  2. El pago del Client se retiene de forma segura hasta que el Fixer confirma la finalización del trabajo.
  3. Los precios se ajustan dinámicamente si hay muchos Clients y pocos Fixers en una zona específica.

## 2. Fase de Arquitectura (`MAPA_LEGO.md` & `DATA_SCHEMA.md`)

**Modelo Base:** Híbrido entre `02_MARKETPLACE_ADVANCED` y `08_ONDEMAND_LOGISTICS`.
**Patrón Invariante:** Monolito Modular con UUIDs, sin JOINs entre Bounded Contexts.

### Bounded Contexts (Módulos)

| Módulo | Responsabilidad | Eventos Emitidos |
| :--- | :--- | :--- |
| **1. Identity / Auth** | Autenticación, Roles, Perfiles (Client/Fixer) y verificación de identidad. | `UserRegistered`, `FixerVerified` |
| **2. Catalog & Pricing**| Definición de servicios base (`attributes JSONB`), indexación H3 (Zonas) y algoritmo de Surge Pricing (`Demand/Supply > 1.5 = x1.2`). | `PriceCalculated`, `SurgeActivated` |
| **3. Matching Engine** | Agrupación de solicitudes (Batched Matching cada 5s) y asignación al Fixer óptimo usando Hungarian Match. | `JobMatched`, `JobAccepted`, `JobStarted`, `JobCompleted` |
| **4. Escrow & Ledger** | Sistema de Doble Entrada inmutable. Retención de fondos (Escrow gestionado vía Temporal.io) hasta la finalización. | `PaymentHeld`, `FundsReleased`, `PayoutIssued` |

### Esquema de Datos Crítico (Solo UUIDs)

- `Identity.User`: `id (UUIDv4)`, `role (ENUM)`, `metadata (JSONB)`
- `Catalog.ServiceType`: `id (UUIDv4)`, `base_price (Int - Centavos)`, `attributes (JSONB)`
- `Matching.Job`: `id (UUIDv4)`, `client_id (UUIDv4)`, `fixer_id (UUIDv4 nullable)`, `h3_index (String)`, `status (ENUM)`
- `Ledger.JournalEntry`: `id (UUID)`, `job_id (UUID)`, `debit_account (UUID)`, `credit_account (UUID)`, `amount (Int - Centavos)`

## 3. Fase de Evaluación (The Gatekeeper Checklist)

Antes de cualquier PR, el agente **MAVIM-Critic** verifica:
1. **[X] Ledger Check:** La tabla de `JournalEntry` usa Enteros para centavos y no `floats`. Un trabajo finalizado emite `FundsReleased` que a su vez inserta un Debit del Escrow y un Credit al Fixer.
2. **[X] Anti-Data Bleeding:** `Matching Engine` NO hace JOIN con `Identity.User` para sacar el nombre del Fixer. Se debe comunicar por API síncrona / eventos.
3. **[X] UX Check:** La aplicación del Client debe tener un _Skeleton Loader_ y Websockets mientras espera el estado `JobAccepted`.
4. **[X] Sec-Evals:** Si la app integra un chatbot de soporte (LLM), tiene sanitización activa contra Prompt Injection y ofuscación de la dirección física del Client en los logs.
