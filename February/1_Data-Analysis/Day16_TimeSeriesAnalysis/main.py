import pandas
import numpy
from datetime import datetime

# stolen
dates = pandas.date_range(start='2022-01-01', end='2023-12-31')
n = len(dates)
temperature = 15 + 10 * numpy.sin(numpy.linspace(0, 2*numpy.pi*2, n)) + \
    numpy.random.normal(0, 2, n) + numpy.linspace(0, 1, n)


df = pandas.DataFrame({'temperature': temperature}, index=dates)
print("===== Weather Pattern Analysis =====")
print(f"Data period: {df.index.min().date()} to {df.index.max().date()}")
print(
    f"Temperature stats: min={df.temperature.min():.1f}°C, max={df.temperature.max():.1f}°C, avg={df.temperature.mean():.1f}°C")

print("\nSeasonal Patterns:")
seasonal_data = df.groupby(df.index.month).mean()
for month, data in seasonal_data.iterrows():
    month_name = datetime(2022, month, 1).strftime('%B')
    print(f"{month_name}: {data.temperature:.1f}°C")
