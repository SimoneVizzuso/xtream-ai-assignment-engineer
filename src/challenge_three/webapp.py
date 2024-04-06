import string
from typing import Optional

import model.diamond_model as adm

import streamlit as st
import pandas as pd
import xgboost as xgb


# Function for the retrain of the model
def train_model(new_data_to_train: Optional[pd.DataFrame] = None, retrain: Optional[bool] = False) -> xgb.XGBRegressor:
    """
    Train the XGBoost model.

    Parameters:
    - new_data_to_train: pd.DataFrame
        New data to train the model.
    - retrain: bool
        Whether to retrain the model.

    Returns:
    - xgb.XGBRegressor
        Trained XGBoost model.
    """
    model_state = st.empty()
    model_state.write("Training the model...")

    try:
        xgb_regressor = adm.load_model()

        if retrain or (xgb_regressor is None):
            if new_data_to_train is not None:
                xgb_regressor, metrics = adm.train(xgb_regressor, new_data_to_train, retrain=True)
            else:
                xgb_regressor, metrics = adm.train(retrain=True)
            model_state.write(f'Model trained successfully! New Percentage: {round(metrics[2] * 100, 2)}')
        else:
            metrics = adm.load_metrics()
            model_state.write(
                f'Model has been trained! Percentage of the variance (higher is better): {round(metrics[2] * 100, 2)}')
        return xgb_regressor
    except Exception as e:
        model_state.write(f'Could not load because -> {e}')


@st.cache_data
def plot_prices(input_data_list=None):
    """
    Plot price history.

    Parameters:
    - input_data_list: List[pd.DataFrame]
        List of input data.
    """
    if len(input_data_list) > 0:
        # Create a DataFrame to display the predicted prices and input data in a table
        price_history_df = pd.DataFrame(input_data_list)
        price_history_df['Predicted Price'] = st.session_state["predicted_prices"]

        st.table(price_history_df)
    else:
        st.write('No price predictions yet.')


def main():
    st.title('Diamond Price Predictor')

    st.header('Model Training')
    model = train_model()

    if st.button("Retrain the model!"):
        model = train_model(retrain=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.header('Price Prediction')

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        cut = st.selectbox('Cut', ['Ideal', 'Premium', 'Very Good', 'Good', 'Fair'])
    with col2:
        color = st.selectbox('Color', [letter for letter in string.ascii_uppercase[3:10]])
    with col3:
        clarity = st.selectbox('Clarity', ['IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2', 'I1'])
    with col4:
        carat = st.number_input('Carat', min_value=0.01, max_value=5.0, value=1.0, step=0.1)

    col5, col6, col7, col8, col9 = st.columns(5)

    with col5:
        depth = st.number_input('Depth', min_value=0.01, max_value=80.0, value=0.01, step=0.01)
    with col6:
        table = st.number_input('Table', min_value=0.01, max_value=80.0, value=0.01, step=0.01)
    with col7:
        x = st.number_input('X', min_value=0.01, max_value=10.0, value=0.01, step=0.01)
    with col8:
        y = st.number_input('Y', min_value=0.01, max_value=10.0, value=0.01, step=0.01)
    with col9:
        z = st.number_input('Z', min_value=0.01, max_value=10.0, value=0.01, step=0.01)

    # Initialize an empty list to store predicted prices
    if 'predicted_prices' not in st.session_state:
        st.session_state["predicted_prices"] = []
    if 'input_data_list' not in st.session_state:
        st.session_state["input_data_list"] = []
    if 'price' not in st.session_state:
        st.session_state["price"] = 0

    if st.button('Predict'):
        input_data = pd.DataFrame({
            'cut': [cut],
            'color': [color],
            'clarity': [clarity],
            'carat': [carat],
            'depth': [depth],
            'table': [table],
            'x': [x],
            'y': [y],
            'z': [z]
        })

        data = adm.preprocessing_evaluation(input_data)
        prediction = model.predict(data)
        st.session_state["price"] = round(prediction[0])
        st.write(f'Predicted Price: ${round(st.session_state["price"])}')

        st.session_state["predicted_prices"].append(round(prediction[0]))
        st.session_state["input_data_list"].append(input_data.iloc[0][:-3])

    st.markdown("<hr>", unsafe_allow_html=True)

    # Display the Price History header
    st.header('Price History')
    if st.button('Clean History'):
        st.session_state["input_data_list"] = []
        st.session_state["predicted_prices"] = []

    plot_prices(st.session_state["input_data_list"])

    st.markdown("<hr>", unsafe_allow_html=True)

    # Display the Price History header
    st.header('Train with new data')
    st.write("Insert new data below if you want to train the model with those new data. The accepted format is CSV.")

    # File uploader for CSV
    uploaded_file = st.file_uploader("Upload CSV", type=['csv'])

    if uploaded_file is not None:
        input_data = pd.read_csv(uploaded_file)
        col10, col11 = st.columns(2)
        with col10:
            show_data = st.checkbox('Show loaded Data')

        if show_data:
            st.write(input_data)

        with col11:
            if st.button('Train the model with this new data'):
                model = train_model(new_data_to_train=input_data, retrain=True)


if __name__ == '__main__':
    main()
