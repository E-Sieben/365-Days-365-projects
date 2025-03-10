import pandas

STD_PATH = "February/CANDA_webscraper/listings/all_products.csv"
STD_PATH_OUT = "February/1_Data-Analysis/Day13_DataAggregation/aggregated.csv"


def cleanAllProducts(file_path: str = STD_PATH):
    cleaned_data: list[tuple[str, int]] = []
    try:
        ds = pandas.read_csv(file_path)
        for _, row in ds.iterrows():
            product_category = str(row.get("category", ""))
            product_name = str(row.get("title", ""))
            try:
                price = float(row.get("price", "").replace(",", "."))
            except ValueError:
                continue
            cleaned_data.append((product_category, product_name, price))
    except Exception as e:
        print(f"! Error: {e}")
    return cleaned_data


def save_to_csv(cleaned_data: list[tuple[str, str, float]] = cleanAllProducts(), output_path: str = STD_PATH_OUT):
    try:
        df = pandas.DataFrame(cleaned_data, columns=[
                              "category", "name", "price"])
        df.to_csv(output_path, index=False)
        print(f"Data successfully saved to {output_path}")
    except Exception as e:
        print(f"! Error saving data: {e}")


if __name__ == "__main__":
    save_to_csv()
