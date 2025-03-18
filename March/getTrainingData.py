import numpy as np
import pandas as pd
from sklearn import preprocessing as pp
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer


def getTrainingData(test_size=0.2, random_state=42, scale_features=True, max_text_features=100):
    """
    Prepare training and testing data for regression tasks.

    Parameters:
    -----------
    test_size : float, default=0.2
        The proportion of the dataset to include in the test split.
    random_state : int, default=42
        Controls the shuffling applied to the data before applying the split.
    scale_features : bool, default=True
        Whether to scale numerical features.
    max_text_features : int, default=100
        Maximum number of text features to extract.

    Returns:
    --------
    dict : A dictionary containing X_train, X_test, y_train, y_test, and other metadata
    """
    # Load data from CSV
    csv_path = '/workspaces/365-Days-365-projects/February/CANDA_webscraper/listings/all_products.csv'
    df = pd.read_csv(csv_path)

    # Clean and convert price column
    df['price_numeric'] = df['price'].apply(lambda x:
                                            float(str(x).replace(
                                                ',', '.').replace('"', ''))
                                            if x != 'Price not found' else np.nan)

    # Drop rows with missing prices for regression task
    df_clean = df.dropna(subset=['price_numeric']).copy()

    # Feature engineering
    # Encode categorical variables
    cat_columns = ['category', 'type']
    encoder = pp.OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    encoded_cats = encoder.fit_transform(df_clean[cat_columns])
    encoded_cats_df = pd.DataFrame(
        encoded_cats,
        columns=encoder.get_feature_names_out(),
        index=df_clean.index
    )

    # Process product titles with TF-IDF
    vectorizer = TfidfVectorizer(max_features=max_text_features)
    tfidf_matrix = vectorizer.fit_transform(df_clean['title'])
    tfidf_df = pd.DataFrame(
        tfidf_matrix.toarray(),
        columns=vectorizer.get_feature_names_out(),
        index=df_clean.index
    )

    # Extract date features
    df_clean['scrape_date'] = pd.to_datetime(df_clean['scrape_date'])
    df_clean['day_of_week'] = df_clean['scrape_date'].dt.dayofweek
    df_clean['month'] = df_clean['scrape_date'].dt.month

    # Combine features
    features_df = pd.concat([
        encoded_cats_df,
        tfidf_df,
        df_clean[['day_of_week', 'month']]
    ], axis=1)

    # Scale features if requested
    if scale_features:
        numeric_columns = features_df.select_dtypes(
            include=[np.number]).columns
        scaler = pp.StandardScaler()
        features_df[numeric_columns] = scaler.fit_transform(
            features_df[numeric_columns])

    # Define target
    target = df_clean['price_numeric']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        features_df, target, test_size=test_size, random_state=random_state
    )

    # Return data as dict for easy access
    return {
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test,
        'feature_names': list(features_df.columns),
        'encoder': encoder,
        'vectorizer': vectorizer,
        'scaler': scaler if scale_features else None,
        'original_data': df_clean
    }


def getData():
    """Legacy function for backward compatibility"""
    result = getTrainingData(test_size=0.2)
    training_data = pd.concat([result['X_train'], result['y_train']], axis=1)
    testing_data = pd.concat([result['X_test'], result['y_test']], axis=1)
    return (training_data, testing_data)
