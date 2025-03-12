import pandas

STD_PATH = "/workspaces/365-Days-365-projects/February/CANDA_webscraper/listings/all_products.csv"


def getProducts(file_path: str = STD_PATH, time: bool = False):
    cleaned_data: dict[str, list[tuple[str, int]]] = {}
    try:
        ds = pandas.read_csv(file_path)
        for _, row in ds.iterrows():
            dateTime = str(row.get("scrape_date", ""))
            product_name = str(row.get("title", ""))
            category = str(row.get("category", ""))
            try:
                price = float(row.get("price", "").replace(",", "."))
            except ValueError:
                continue
            if category not in cleaned_data:
                cleaned_data[category] = []
            if time:
                cleaned_data[category].append(
                    (product_name, price, str(dateTime)))
            else:
                cleaned_data[category].append((product_name, price))
    except Exception as e:
        print(f"! Error: {e}")
    return cleaned_data
