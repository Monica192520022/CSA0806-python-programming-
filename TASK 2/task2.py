from decimal import Decimal

# Floating-point calculation
amount_float = 1000 * 33.40 + 3 * 0.10
print("Float amount:", amount_float)
print("Float matches expected:", amount_float == 33400.30)

# Decimal calculation
amount_decimal = Decimal("1000") * Decimal("33.40")
amount_decimal += Decimal("3") * Decimal("0.10")

print("Decimal amount:", amount_decimal)
print("Decimal matches expected:", amount_decimal == Decimal("33400.30"))
