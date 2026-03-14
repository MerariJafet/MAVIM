# MAVIM Anti-Patrones (Lista Negra OBLIGATORIA)

El agente **MAVIM-Critic** tiene autoridad para rechazar inmediatamente cualquier Pull Request que contenga uno de los siguientes anti-patrones de diseño. **Estas son faltas letales a la arquitectura Senior.**

## 1. Fraude Contable
- **[PROHIBIDO]** Usar tipos de dato `float`, `double` o `decimal` sueltos para representar dinero/moneda base.  
  *Solución:* Usar **Enteros (Integers/BigInts)** para representar los centavos más pequeños y aplicar un **Ledger Inmutable**.

## 2. Leakage Operacional
- **[PROHIBIDO]** Usar IDs autoincrementales (`1`, `2`, `3`) en rutas, URLs o APIs visuales (ej. `/users/45`).  
  *Solución:* Utilizar **UUIDv4**, **ULID**, o **Snowflakes** para no revelar metadatos competitivos (fuga de volumen).

## 3. Caos de Responsabilidad (Fat Controllers)
- **[PROHIBIDO]** Escribir lógica de negocio (consultas SQL complejas, validaciones pesadas, envíos de emails) directamente adentro de los Controladores o Resolvers (GraphQL).  
  *Solución:* El controlador solo recibe la petición, inyecta la dependencia a la capa de "Service" (Casos de Uso) y retorna la respuesta serializada.

## 4. Spaghetti Relacional
- **[PROHIBIDO]** Ejecutar clausulas `JOIN` o referencias de Base de Datos extranjeras (`Foreign Keys` duras a nivel SQL) **entre dos Bounded Contexts (Módulos)** distintos.  
  *Solución:* Duplicación intencionada de datos referenciales mediante eventos de dominio (`UserCreatedEvent`) o llamadas de API internas estrictas síncronas.

## 5. Ceguera Transaccional
- **[PROHIBIDO]** Procesar pagos o descontar stock sin usar **Transacciones de Base de Datos (BEGIN...COMMIT)**.  
  *Solución:* Todo flujo que muta más de un estado crítico simultáneamente, debe estar envuelto en transacciones atómicas seguras mediante `ACID` properties.
