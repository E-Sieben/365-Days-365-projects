import pandas
import numpy
from scipy import stats

STD_PATH = "February/CANDA_webscraper/listings/all_products.csv"


def cleanAllProducts(file_path: str = STD_PATH, category: str = "jeans"):
    cleaned_data: list[tuple[str, int]] = []
    try:
        ds = pandas.read_csv(file_path)
        for _, row in ds.iterrows():
            if str(row.get("category", "")) != category:
                continue
            product_name = str(row.get("title", ""))
            try:
                price = float(row.get("price", "").replace(",", "."))
            except ValueError:
                continue
            cleaned_data.append((product_name, price))
    except Exception as e:
        print(f"! Error: {e}")
    return cleaned_data


def averagePriceOfCategory(category: str = "shirts"):
    products = cleanAllProducts(category=category)
    aV: list[int] = []
    for product in products:
        aV.append(product[1])
    return numpy.mean(aV)


def medianPriceOfCategory(category: str = "shirts"):
    products = cleanAllProducts(category=category)
    aV: list[int] = []
    for product in products:
        aV.append(product[1])
    return numpy.median(aV)


def modePriceOfCategory(category: str = "shirts"):
    products = cleanAllProducts(category=category)
    aV: list[int] = []
    for product in products:
        aV.append(product[1])
    return stats.mode(aV).mode


if __name__ == "__main__":
    print(averagePriceOfCategory())
    print(medianPriceOfCategory())
    print(modePriceOfCategory())
