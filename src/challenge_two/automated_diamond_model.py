# In this file we'll have the automated model that will take the weight of the trained model, new data and result in a
# new model trained on new data
import logging
import os
import random
import string
import time
from datetime import datetime
from typing import Optional, Tuple

import pandas as pd
import xgboost as xgb
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

logger = logging.getLogger(__name__)
logger_level = logging.DEBUG

# The features of the datasets, always the same, used in multiple functions
categorical_features = ['cut', 'color', 'clarity']
numerical_features = ['carat', 'depth', 'table', 'price', 'x', 'y', 'z']

random_number_for_consistency = random.randint(0, 4294967295)

directory_model_evaluation = 'model_weights'
dataset_directory = os.path.join('..', '..', 'datasets')

# Set this variable to False if you don't want the print of the evaluation
print_model_evaluation = True

X_test_original, y_test_original = None, None


def load_model() -> Optional[xgb.XGBRegressor]:
    """
    Load the newest XGBoost model found.

    Returns:
    - Optional[xgb.XGBRegressor]:
        Loaded XGBoost model if found, otherwise None.
    """

    # Check if the directory with weights already exists
    if not os.path.exists(directory_model_evaluation):
        # Create the directory if it doesn't exist
        os.makedirs(directory_model_evaluation)
        logger.debug(f"Directory '{directory_model_evaluation}' created successfully")
    else:
        # Get the list of files in the directory
        files = os.listdir(directory_model_evaluation)

        # Filter files for those starting with 'xgboost_model_' and having extension '.json' and sort them
        files = [f for f in files if f.startswith('xgboost_model_') and f.endswith('.json')]
        files.sort(reverse=True)

        # Get the first file (the newest model)
        if files:
            newest_model_file = os.path.join(directory_model_evaluation, files[0])  # Add directory path to the filename
            logger.debug(f"Newest model found: {newest_model_file}")

            # Load the XGBoost model
            model = xgb.XGBRegressor()
            model.load_model(newest_model_file)
            logger.info("Last XGBoost model loaded successfully")
            return model
    logger.info(f"No model was found, a new model will be trained")
    return None


def load_new_data(file_name: str) -> Optional[pd.DataFrame]:
    """
    Load a new dataset from a CSV file.

    Returns:
    - Optional[pd.DataFrame]:
        DataFrame containing the loaded dataset if successful, otherwise None.
    """
    choice = input(f'File {file_name} has been uploaded.\n'
                   'Do you want to train the model with this file? (y/n): ')
    if choice == 'y':
        # Load a new dataset of diamonds
        if len(file_name) > 0:
            try:
                df = pd.read_csv(os.path.join(dataset_directory, file_name))
                logger.info(f'Loaded new data to train from {file_name}')

                if not set(categorical_features).issubset(df.columns) or not set(numerical_features).issubset(
                        df.columns):
                    logger.info(f'The columns in the provided CSV file do not match the expected columns.\n'
                                f'Upload a CSV file compatible with the following columns:\n'
                                f'cut, color, clarity, carat, depth, table, price, x, y and z\n')
                else:
                    return df
            except FileNotFoundError:
                logger.info(f'No file with this name {file_name} was found')
    else:
        logger.info(f'No file has been loaded')
        return None


def preprocessing_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Preprocess the input DataFrame.

    Drops rows with missing values and negative prices, and those with zero dimensions.
    Encodes categorical features 'cut', 'color', and 'clarity'.
    Splits the dataset into features (X) and target variable (y) for training and testing.

    Parameters:
    - df : pd.DataFrame
        Input DataFrame containing diamond data.

    Returns:
    - Optional[Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]]:
        Tuple containing X_train, X_test DataFrames and y_train, y_test Series if preprocessing is successful,
        otherwise None.
    """
    logger.debug(f'Preprocessing data on the training set...')
    # Drop the rows with null values
    df = df.dropna()
    # Remove the rows with price null (equal 0 or negative value)
    df = df[df['price'] >= 0]
    # Drop the rows with dimensions null (equal 0 or negative value)
    row_with_no_dimensions = df[(df['x'] <= 0) | (df['y'] <= 0) | (df['z'] <= 0)]
    df = df.drop(row_with_no_dimensions.index)

    # Define the order for encoding for each feature
    cut_order = ['Ideal', 'Premium', 'Very Good', 'Good', 'Fair']
    color_order = [letter for letter in string.ascii_uppercase[3:]]
    clarity_order = ['IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2', 'I1']

    # Create a mapping dictionary for each feature
    cut_mapping = {category: i + 1 for i, category in enumerate(cut_order)}
    color_mapping = {category: i + 1 for i, category in enumerate(color_order)}
    clarity_mapping = {category: i + 1 for i, category in enumerate(clarity_order)}

    # Map the categories to their encoded values in the DataFrame
    df['cut_encoded'] = df['cut'].map(cut_mapping)
    df['color_encoded'] = df['color'].map(color_mapping)
    df['clarity_encoded'] = df['clarity'].map(clarity_mapping)

    # Define the features (X) removing the target variable and the categorical features, and target variable (y)
    X = df.drop(columns=['price', 'cut', 'color', 'clarity'])
    y = df['price']

    # Split the dataset into training and testing sets (70/30)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=random_number_for_consistency)
    logger.debug(f'Preprocessing on data was successful')
    return X_train, X_test, y_train, y_test


def evaluate_model(predictions: pd.Series, ground_truth: pd.Series) -> Tuple[float, float, float]:
    """
    Evaluate the performance of the model.

    Calculates RMSE, MAE, and R-squared between predicted and ground truth values.

    Parameters:
    - predictions : pd.Series
        Series containing predicted values.
    - ground_truth : pd.Series
        Series containing ground truth values.

    Returns:
    - Tuple[float, float, float]:
        Tuple containing RMSE, MAE, and R-squared values.
    """
    logger.info(f'Evaluating the model...')
    rmse = root_mean_squared_error(ground_truth, predictions)
    mae = mean_absolute_error(ground_truth, predictions)
    r_squared = r2_score(ground_truth, predictions)
    return rmse, mae, r_squared


def save_model_evaluation(model_name: str, random_number: int, evaluation_results: Tuple[float, float, float]) -> None:
    """
    Save model evaluation results to a file.

    Parameters:
    - model_name : str
        Name of the model, typically containing the training date.
    - random_number : int
        Random number used during training.
    - evaluation_results : Tuple[float, float, float]
        Tuple containing evaluation results (RMSE, MAE, R-squared).
    """

    # Check if the directory with evaluation already exists
    if not os.path.exists(directory_model_evaluation):
        # Create the directory if it doesn't exist
        os.makedirs(directory_model_evaluation)
        logger.debug(f"Directory '{directory_model_evaluation}' created successfully")

    filename = os.path.join(directory_model_evaluation, f"xgboost_model_{model_name}_evaluation.txt")

    with open(filename, "w") as file:
        file.write(f"Model Name: {model_name}\n")
        file.write(f"Random Number: {random_number}\n")
        file.write(f"RMSE: {evaluation_results[0]}\n")
        file.write(f"MAE: {evaluation_results[1]}\n")
        file.write(f"R-squared: {evaluation_results[2]}\n")

    logger.info(f"Model evaluation results saved to {filename}")


def train(xgb_regressor: Optional[xgb.XGBRegressor] = None,
          new_data_to_train: Optional[pd.DataFrame] = None) -> Optional[xgb.XGBRegressor]:
    """
    Train an XGBoost regressor model.

    If new data is provided, preprocess it and train the model. Otherwise, load the default dataset.
    Evaluate and save the trained model and the evaluation.

    Parameters:
    - xgb_regressor : Optional[xgb.XGBRegressor]
        Pre-trained XGBoost regressor model. If None, a new model will be initialized.
    - new_data_to_train : Optional[pd.DataFrame]
        New data to train the model. If None, default dataset will be used.

    Returns:
    - Optional[xgb.XGBRegressor]:
        Trained XGBoost regressor model if successful, otherwise None.
    """
    global X_test_original, y_test_original
    logger.info(f'Start training XGBoost...')

    if X_test_original is None or y_test_original is None:
        df = pd.read_csv(os.path.join(dataset_directory, 'diamonds', 'diamonds.csv'))
        X_train, X_test_original, y_train, y_test_original = preprocessing_data(df)
        xgb_regressor = xgb.XGBRegressor(random_state=random_number_for_consistency)
        start_time = time.time()
        xgb_regressor.fit(X_train, y_train)
        end_time = time.time()
    if new_data_to_train is not None and xgb_regressor is not None:
        X_train, X_test, y_train, y_test = preprocessing_data(new_data_to_train)
        start_time = time.time()
        xgb_regressor.fit(X_train, y_train, xgb_model=xgb_regressor)
        end_time = time.time()

    timestamp_trained_model = datetime.now().strftime("%Y%m%d_%H%M%S")
    logger.info(f'Model trained correctly in {end_time - start_time}. Saving the model...')
    model_filename = os.path.join(directory_model_evaluation, f'xgboost_model_{timestamp_trained_model}.json')
    xgb_regressor.save_model(model_filename)

    logger.info(f'Making prediction...')
    xgb_prediction = xgb_regressor.predict(X_test_original)
    xgb_rmse, xgb_mae, xgb_r2 = evaluate_model(xgb_prediction, y_test_original)
    save_model_evaluation(timestamp_trained_model, random_number_for_consistency, (xgb_rmse, xgb_mae, xgb_r2))
    if print_model_evaluation:
        logger.info(f'--- XGBoost Regression Performance --- RMSE: {xgb_rmse:} - MAE: {xgb_mae:} - R2: {xgb_r2:}')
    return xgb_regressor


class FileModifiedHandler(FileSystemEventHandler):
    def __init__(self, xgb_regressor):
        super().__init__()
        self.xgb_regressor = xgb_regressor

    def on_modified(self, event):
        if event.is_directory:
            return
        logging.info(f'File {event.src_path} modified. Starting training...')
        file_name = os.path.basename(event.src_path)
        new_data_to_train = load_new_data(file_name)
        if new_data_to_train is not None:
            if len(new_data_to_train) != 0:
                train(self.xgb_regressor, new_data_to_train)


def start_watchdog(directory, xgb_regressor):
    event_handler = FileModifiedHandler(xgb_regressor)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=False)
    observer.start()
    logging.info(f'Watching directory {directory} for file modifications...')

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()


def main():
    logging.basicConfig(level=logger_level)
    logger.info('Process automated_diamond_model started')

    xgb_regressor = load_model()
    if xgb_regressor is None:
        xgb_regressor = train()

    while True:
        choice = input('Do you want to keep process alive to watch the folder for new data? (y/n): ')
        if choice == 'y':
            start_watchdog(dataset_directory, xgb_regressor)
        elif choice == 'n':
            print('Exiting...')
            break
        else:
            print('Invalid input. Please reply with "y" or "n"')

    logger.info('Process automated_diamond_model finished')


if __name__ == '__main__':
    main()
