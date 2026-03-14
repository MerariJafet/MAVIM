# Patrón: Logística On-Demand y Surge Pricing

## 1. Indexación Espacial (H3)
Dividir el mapa en **Hexágonos H3**. 
- **Uso:** Calcular la densidad de oferta/demanda por celda hexagonal para evitar distorsiones de distancia.

## 2. Surge Pricing Algorithm
Si `Demand (Users en celda) / Supply (Drivers en celda) > 1.5`, aplicar multiplicador de precio `x1.2` automáticamente.

## 3. Matching de Ventana (Batched Matching)
No asignar al primer conductor disponible. Agrupar pedidos cada 5 segundos y usar el algoritmo de 'Hungarian Match' para optimizar la distancia global del sistema.
