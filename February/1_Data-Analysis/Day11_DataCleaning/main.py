import pandas

STD_PATH = "February/CANDA_webscraper/listings/all_products.csv"


def cleanAllProducts(file_path: str = STD_PATH):
    cleaned_data: dict[str, int] = {}
    try:
        ds = pandas.read_csv(file_path)
        for _, row in ds.iterrows():
            product_name = str(row.get("title", ""))
            try:
                price = float(row.get("price", "").replace(",", "."))
            except ValueError:
                continue
            cleaned_data[product_name] = price
    except Exception as e:
        print(f"! Error: {e}")
    return cleaned_data


print(cleanAllProducts())
