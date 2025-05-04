import pandas as pd


class DataProfiler:
    #A utility class for profiling and analyzing pandas DataFrames.

    def __init__(self, df):
        self.df = df

    def get_basic_info(self):
        #Returns basic information about the dataset.
        info = f"""
        Shape: {self.df.shape}
        Columns: {', '.join(self.df.columns)}
        Total Rows: {len(self.df)}
        """
        return info

    def get_summary_stats(self):
        #Returns summary statistics for numeric columns.
        return self.df.describe()

    def get_missing_values(self):
        #Returns a DataFrame with missing value counts and percentages.
        missing_count = self.df.isnull().sum()
        missing_percent = (missing_count / len(self.df) * 100).round(2)
        return pd.DataFrame({
            'Missing Count': missing_count,
            'Missing Percent': missing_percent
        })

    def get_numeric_columns(self):
        #Returns a list of numeric column names.
        return self.df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    def get_categorical_columns(self):
        """Returns a list of categorical column names."""
        return self.df.select_dtypes(include=['object', 'category']).columns.tolist()