import pandas as pd
import numpy as np

# Read CSV file
df = pd.read_csv(
    '/workspaces/365-Days-365-projects/February/CANDA_webscraper/listings/all_products.csv')

df['price'] = df['price'].replace('Price not found', np.nan)
df['price'] = df['price'].str.replace(',', '.').astype(float)

# Create features for correlation analysis
df['title_length'] = df['title'].str.len()
df['product_id'] = pd.to_numeric(df['product_id'])

# Dynamically create binary features for all categories
category_dummies = pd.get_dummies(df['category'], prefix='is')
df = pd.concat([df, category_dummies], axis=1)

# Get numerical columns for correlation analysis
numerical_cols = ['price', 'product_id', 'title_length']
# Add the category dummy columns
numerical_cols.extend(category_dummies.columns.tolist())

# Calculate correlation matrix for numerical columns
corr = df[numerical_cols].corr().round(2)

# Print correlation matrix
print("Correlation Matrix:")
print(corr)

# Visualize correlations with price using ASCII bars
print("\nPrice Correlations:")
for col in corr.index:
    if col != 'price':
        value = corr.loc['price', col]
        bar = '█' * int(abs(value) * 50)
        direction = '+' if value >= 0 else '-'
        print(f"{col.ljust(25)}: {direction} {bar} ({value})")

# Display average price by category
print("\nAverage price by category:")
cat_avg = df.groupby('category')['price'].mean().sort_values(ascending=False)
print(cat_avg.round(2))
