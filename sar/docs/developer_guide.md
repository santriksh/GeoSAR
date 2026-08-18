# Developer Guide

## Adding a New Algorithm

Every new algorithm should follow the GeoSAR workflow.

### Step 1

Write the NumPy-style docstring.

### Step 2

Validate all inputs.

### Step 3

Perform the computation.

### Step 4

Preserve:

- metadata
- CRS
- affine transform
- masks
- history

### Step 5

Return a new SARImage.

### Step 6

Write unit tests.

### Step 7

Write integration tests.

---

## Standard Function Template

```python
def algorithm(
    image: SARImage,
):
    """
    Description.

    Parameters
    ----------
    ...

    Returns
    -------
    SARImage
    """

    _validate(...)

    ...

    return _create_result(...)
```

---

## Coding Workflow

Design

↓

Implementation

↓

Unit Tests

↓

Edge Case Validation

↓

Integration Tests

↓

Documentation