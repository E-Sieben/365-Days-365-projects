celsius_to_fahrenheit = lambda c: (c * 9/5) + 32
fahrenheit_to_celsius = lambda f: (f - 32) * 5/9

CELSIUS: int = 21
FAHRENHEIT: int = 70
print(f"{CELSIUS}°C are {celsius_to_fahrenheit(CELSIUS)}°F")
print(f"and {FAHRENHEIT}°F are {fahrenheit_to_celsius(FAHRENHEIT):.2f}°C")