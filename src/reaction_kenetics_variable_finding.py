import pandas as pd
import plotly.express as px


def import_csv(filepath):
    """
    Import data from a CSV file into a pandas DataFrame.

    This function assumes the CSV file has a specific format where the actual
    data starts from the third row, and the columns represent time and absorption values.

    :param filepath: str, the path to the CSV file.
    :return: pandas.DataFrame, contains the time and absorption values.
    """
    df = pd.read_csv(filepath)
    return df


def plot_data(df):
    """
    Plot the time series data using Plotly.

    :param df: pandas.DataFrame, the DataFrame containing the time and absorption data to plot.
    """
    fig = px.line(df, x='Time (min)', y='Abs', title='Absorption over Time', labels={'Abs': 'Absorption'})
    fig.show()


if __name__ == "__main__":
    FILEPATH = '../40-1-cleaned.csv'  # Change this variable to the path of your CSV file
    data = import_csv(FILEPATH)
    plot_data(data)
