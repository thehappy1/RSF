import xgboost as xgb
import pandas as pd
import numpy as np
from app.core.config import DATA_PATH, MODEL_PATH


import xgboost as xgb
import numpy as np

class XGBoostModel():
    def __init__(self, model_path="xgboost_final.json"):
        self.xgb_model = self.load_xgb_model(model_path)

    def load_xgb_model(self, path):
        '''
        Load XGBoost model
        '''
        xgb_model = xgb.Booster()
        xgb_model.load_model(path)
        return xgb_model

    def get_predictions_for_store(self, input_data, store_id, future_steps):
        # Select Test Data for store_id
        # Das hier sollte sogar noch ein Schritt vorher erfolgen

        dtest_store = xgb.DMatrix(input_data, enable_categorical=True)

        # Get prediction
        predictions_xgb = self.xgb_model.predict(dtest_store)

        # Transform 
        predictions_xgb = np.expm1(predictions_xgb)

        return predictions_xgb

def load_data(path):
    """
    Load data from the specified CSV file path.

    Args:
        path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded and preprocessed data.
    """
    try:
        df = pd.read_csv(path, low_memory=False)
        df = df.drop(columns='Unnamed: 0')
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values(by='Date')
        print('Daten erfolgreich geladen')
    except Exception as e:
        print('Data Loading fehlgeschlagen!')
        df = pd.DataFrame()  # Return an empty DataFrame in case of failure

    return df

def create_holdout_set(dataframe, store_id, feature_list, anzahl_wochen, get_dates=False):
    """
    Create a holdout set for model training and testing.

    Args:
        dataframe (pd.DataFrame): The input data.
        store_id (int): The ID of the store to filter data for.
        feature_list (list): The list of features to be used.
        anzahl_wochen (int): The number of weeks for the test set.
        get_dates (bool): Whether to return the dates of the training and test sets.

    Returns:
        tuple: Depending on the value of get_dates, returns either:
               - (pd.DataFrame, pd.Series, pd.DataFrame, pd.Series): The training features, training targets, test features, and test targets.
               - (pd.DataFrame, pd.Series, pd.DataFrame, pd.Series, pd.Series, pd.Series): The training features, training targets, test features, test targets, training dates, and test dates.
    """
    train_list = []
    test_list = []
    
    dataframe = dataframe[dataframe['Store'] == store_id]
    dataframe = dataframe[feature_list]
    dataframe = dataframe[dataframe["Open"] != 0]
    dataframe = dataframe[dataframe["Sales"] > 0]
    
    dataframe = dataframe.sort_values(by=['Store', 'Date'])
    grouped = dataframe.groupby('Store')

    for store_id, group in grouped:
        train_list.append(group[:-7 * anzahl_wochen])
        test_list.append(group[-7 * anzahl_wochen:])

    train = pd.concat(train_list)
    test = pd.concat(test_list)
    
    if get_dates: 
        train_dates = train.Date
        test_dates = test.Date 

    y_train = np.log1p(train['Sales'])
    X_train = train
    y_test = np.log1p(test['Sales'])  
    X_test = test.drop(columns=['Sales', 'Open', 'Date'])

    if get_dates:
        return X_train, y_train, X_test, y_test, train_dates, test_dates
    else:
        return X_train, y_train, X_test, y_test
