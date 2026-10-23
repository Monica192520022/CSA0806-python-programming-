# TASK 2 – Python Data Types and Floating-Point Precision

## Aim
To study Python data types and compare floating-point arithmetic with decimal arithmetic for accurate milk payment calculations.

## 1. Python Data Types
Python provides different data types to store values.

- `int`: Stores whole numbers, such as the number of farmers.
- `float`: Stores decimal numbers, such as milk quantity.
- `str`: Stores text, such as a farmer's name.
- `bool`: Stores `True` or `False`.
- `Decimal`: Represents decimal values more accurately for financial calculations.

## 2. Floating-Point Calculation

```python
amount = 1000 * 33.40 + 3 * 0.10
print(amount)
print(amount == 33400.30)
```

Floating-point numbers may produce small precision errors because many decimal fractions cannot be represented exactly in binary.

## 3. Decimal Calculation

```python
from decimal import Decimal

amount = Decimal("1000") * Decimal("33.40")
amount += Decimal("3") * Decimal("0.10")

print(amount)
print(amount == Decimal("33400.30"))
```

Expected output:

```text
33400.30
True
```

## 4. Comparison

- `float` is convenient for general calculations but can introduce precision errors.
- `Decimal` is suitable for financial calculations requiring decimal accuracy.
- Decimal values should be created from strings, such as `Decimal("33.40")`, rather than from floats.

## Conclusion
Python data types have different purposes. For a milk payment calculator, `Decimal` is preferable for monetary calculations because it supports exact decimal representation for values such as rupees and paise.
