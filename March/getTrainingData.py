from sklearn import preprocessing as pp
import numpy as np
import pandas as pd
from getData import getProducts
from sys import path
path.append('../..')


def getData():
    products = getProducts()
    justProducts = []
    categories = list(products.keys())
    category_to_id = {category: idx for idx, category in enumerate(categories)}

    for category in products:
        category_id = category_to_id[category]
        for name, price in products[category]:
            justProducts.append((category, category_id, name, price))

    normalizedProducts = []
    for i in range(len(justProducts)):
        normalizedProducts.append({
            "product_id": i,
            "category_name": justProducts[i][0],
            "category_id": justProducts[i][1],
            "product_name": justProducts[i][2],
            "product_price": justProducts[i][3]
        })
    products = normalizedProducts
    # Reformat the products
    reformattedProducts = {
        "category_name": [],
        "product_name": [],
        "product_price": []
    }
    for product in products:
        reformattedProducts["category_name"].append(product["category_name"])
        reformattedProducts["product_name"].append(product["product_name"])
        reformattedProducts["product_price"].append(product["product_price"])

    # Create Data frame
    df = pd.DataFrame(data=reformattedProducts)
    # Create and configure encoder
    ohe = pp.OneHotEncoder(handle_unknown="ignore",
                           sparse_output=False).set_output(transform="pandas")
    # Use encoder by fiting and transforming the data
    oheTransformed = ohe.fit_transform(df[["category_name"]])
    # Put both Data Frames together and delete the original category_name column
    df = pd.concat([df, oheTransformed], axis=1).drop(
        columns=["category_name"])
    from sklearn.feature_extraction.text import TfidfVectorizer

    vectorizer = TfidfVectorizer(max_features=100)
    tfidf_matrix = vectorizer.fit_transform(df["product_name"])
    product_names_encoded = vectorizer.fit_transform(df["product_name"])
    product_names_df = pd.DataFrame(
        product_names_encoded.toarray(),
        columns=vectorizer.get_feature_names_out()
    )
    df = pd.concat([df, product_names_df], axis=1).drop(
        columns=["product_name"])
    train_size = int(len(df) * 0.8)
    training = df.iloc[:train_size].reset_index(drop=True)
    testing = df.iloc[train_size:].reset_index(drop=True)
    return (training, testing)
