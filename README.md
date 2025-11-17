# Análisis de Antipatrones y Refactorización
Juan Camilo Mosquera Palomino - 20241020120

Andres Felipe Lopez Martinez - 20241020052

## Antipatrón 1: **Magic Numbers (Números Mágicos)**

### Ubicación
- Líneas con valores literales: `100`, `42`, `5`, `7`, `0.25`, `300`, `20`, `3`, `4`, `0.15`, `0.07`
- Método `discount_for_order()`: umbrales de descuento (`100`, `42`) y porcentajes (`0.15`, `0.07`)
- Métodos `ship_cost_domestic()` y `ship_cost_international()`: costos base y factores de cálculo
- Método `run()`: total ficticio `123.45`

### Descripción
Los **números mágicos** son valores literales que aparecen directamente en el código sin contexto ni explicación. Esto reduce la legibilidad, dificulta el mantenimiento y hace que cambiar estos valores requiera buscar todas sus ocurrencias en el código.

### Refactorización
- Extraer todos los valores literales como **constantes con nombres descriptivos**
- Agrupar constantes relacionadas en clases de configuración
- Usar diccionarios o estructuras de datos para reglas de negocio (descuentos por tier)

---

## Antipatrón 2: **Código Duplicado (Copy-Paste Programming)**

### Ubicación
- Métodos `ship_cost_domestic()` y `ship_cost_international()`
- Ambos métodos comparten la misma estructura y lógica casi idéntica
- Diferencias sutiles: `base` (5 vs 7), condición (`>` vs `>=`), cargo extra (3 vs 4)

### Descripción
El **código duplicado** ocurre cuando la misma lógica se repite en múltiples lugares con variaciones mínimas. Esto viola el principio DRY (Don't Repeat Yourself) y crea problemas de mantenimiento: si se encuentra un bug o se necesita un cambio, hay que modificarlo en múltiples lugares.

### Refactorización
- Crear un método genérico `calculate_shipping_cost()` que acepte parámetros de configuración
- Usar un diccionario o clase de configuración para almacenar los parámetros específicos de cada tipo de envío
- Los métodos específicos delegan al método genérico con sus parámetros correspondientes

---

## Antipatrón 3: **Long Method con Múltiples Responsabilidades**

### Ubicación
- Clase `AppManager` completa
- El método `run()` mezcla diferentes responsabilidades
- La clase gestiona: persistencia de datos, formateo de salida, lógica de negocio (descuentos y envíos)

### Descripción
El antipatrón **Long Method** y **God Class** ocurre cuando una clase o método tiene demasiadas responsabilidades, violando el Principio de Responsabilidad Única (SRP). `AppManager` maneja almacenamiento, presentación, cálculo de descuentos y cálculo de envíos, todo en una sola clase.

### Refactorización
- **Separar responsabilidades** en clases especializadas:
  - `UserRepository`: manejo de persistencia de usuarios
  - `DiscountCalculator`: lógica de cálculo de descuentos
  - `ShippingCalculator`: lógica de cálculo de envíos
  - `UserPrinter`: formateo y presentación de información
- Usar **inyección de dependencias** para que cada clase sea testeable
- El `AppManager` refactorizado solo orquesta las diferentes componentes

---

## Beneficios de la Refactorización

1. **Mantenibilidad**: Cambios en reglas de negocio solo requieren modificar constantes
2. **Testabilidad**: Cada clase tiene una responsabilidad clara y puede ser testeada independientemente
3. **Legibilidad**: El código es autodocumentado con nombres descriptivos
4. **Escalabilidad**: Fácil agregar nuevos tiers, tipos de envío o reglas de negocio
5. **Reutilización**: Las clases especializadas pueden usarse en otros contextos

---

## Principios SOLID Aplicados

- **S**RP (Single Responsibility): Cada clase tiene una única responsabilidad
- **O**CP (Open/Closed): Abierto para extensión (nuevos tiers/envíos), cerrado para modificación
- **D**IP (Dependency Inversion): Dependencias inyectadas, no hardcodeadas
