import pandas as pd
import logging
from sklearn.model_selection import train_test_split

def load_data(filepath: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        logging.error(f"Fehler beim Laden der Daten: {e}")
        return None

def create_holdout_set(df: pd.DataFrame, features: list, anzahl_wochen: int, get_dates=False):
    try:
        X = df[features]
        y = df['Sales']

        # Dummy Implementierung für den Holdout
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        train_dates, test_dates = None, None  # Setze hier echte Datum-Daten, falls nötig

        if get_dates:
            return X_train, y_train, X_test, y_test, train_dates, test_dates
        else:
            return X_train, y_train, X_test, y_test
    except Exception as e:
        logging.error(f"Fehler beim Erstellen des Holdout-Sets: {e}")
        return None, None, None, None, None, None
