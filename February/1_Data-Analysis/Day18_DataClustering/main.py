import pandas
import numpy

STD_PATH = "February/CANDA_webscraper/listings/all_products.csv"


def getProducts(file_path: str = STD_PATH):
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


def clusterPrices() -> dict[str, list[tuple[str, int]]]:
    categories: dict[str, list[tuple[str, int]]] = {
        "cheap": [],
        "mid": [],
        "expensive": []
    }
    products: dict[str, int] = getProducts()
    prices = list(products.values())
    meanPrice = numpy.mean(prices)
    standardDeviation = numpy.std(prices)
    for name, price in products.items():
        zScore: float = (price - meanPrice) / standardDeviation
        if zScore < -0.5:
            isCat = "cheap"
        elif zScore > 0.5:
            isCat = "expensive"
        else:
            isCat = "mid"
        categories[isCat].append((name, price))
    return categories


def prettyPrint(o):
    for i in o:
        print(f"=> {i}:\n")
        for j in o[i]:
            print(f"Name: {j[0]}\nPrice: {j[1]}")
            print("-----")
        print("\n==o==\n")


if __name__ == "__main__":
    prettyPrint(clusterPrices())
