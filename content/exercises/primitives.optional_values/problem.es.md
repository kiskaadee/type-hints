# Ejercicio 0102 — Valores Opcionales y Guardas de Tipo

## Objetivo

Aprender a anotar variables que pueden ser de un tipo específico o `None` (representando valores ausentes u opcionales), y cómo usar guardas de tipo (type guards / narrowing) para satisfacer el análisis estático estricto.

## Enunciado

En nuestro sistema de tickets de soporte, algunos campos son obligatorios al crear un ticket (como `ticket_id` y `customer_name`), pero otros (como `assigned_agent` y `resolution_notes`) comienzan vacíos (`None`) y se completan más tarde.

Bajo el modo de verificación de tipo estricto, si una variable se anota como `str | None`, no se puede pasar directamente a una función que espera un `str` estricto. Debes verificar que la variable no sea `None` antes de usarla. Esto se llama **Reducción de Tipo** (Type Narrowing) o **Guarda de Tipo** (Type Guard).

1. Reemplaza las anotaciones `"???"` de `assigned_agent` y `resolution_notes` con el tipo de unión correcto que represente una cadena o `None`.
2. Envuelve la llamada a `close_ticket` en una sentencia `if` que verifique que `assigned_agent` no es `None`.

Ejemplo:

```python
assigned_agent: "???" = None
```

debe convertirse en:

```python
assigned_agent: str | None = None
```

Y:

```python
close_ticket(assigned_agent)
```

debe convertirse en:

```python
if assigned_agent is not None:
    close_ticket(assigned_agent)
```

## Criterio de Éxito

El ejercicio se considera completado cuando:
- Tanto `assigned_agent` como `resolution_notes` están anotados como `str | None`.
- El código pasa la verificación estricta de Pyright sin ningún error.
