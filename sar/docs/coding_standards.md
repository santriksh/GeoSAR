# Coding Standards

## Naming

Functions

- snake_case

Classes

- PascalCase

Private Functions

- _leading_underscore

---

## Function Structure

Every public function should follow:

1. Docstring
2. Input Validation
3. Computation
4. Metadata Preservation
5. Return SARImage

---

## Input Validation

Always validate:

- image type
- dimensions
- value scale
- parameters

---

## Metadata

Never discard:

- CRS
- transform
- mask
- history

---

## Inputs

Never modify input objects.

Always return a new SARImage.

---

## Documentation

Use NumPy-style docstrings.

---

## Exceptions

Raise informative exceptions.

Preferred:

- ValueError
- TypeError

Avoid silent failures.

---

## Testing

Every public function should include:

- Unit Tests
- Edge Cases
- Integration Tests
