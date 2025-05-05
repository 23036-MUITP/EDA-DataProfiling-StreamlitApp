import pandas as pd

class DataProfiler:
    def __init__(self, df):
        self.df = df

    def get_basic_info(self):
        """Returns basic information about the dataset."""
        info = f"Dataset Shape: {self.df.shape}\n"
        info += f"Columns: {list(self.df.columns)}\n"
        info += f"Data Types:\n{self.df.dtypes}"
        return info

    def get_summary_stats(self):
        """Returns summary statistics for numeric columns."""
        return self.df.describe()

    def get_missing_values(self):
        """Returns a dataframe with the count and percentage of missing values per column."""
        missing_count = self.df.isnull().sum()
        missing_percent = (missing_count / len(self.df)) * 100
        missing_df = pd.DataFrame({
            "Missing Count": missing_count,
            "Missing Percent": missing_percent
        })
        return missing_df[missing_df["Missing Count"] > 0]

    def get_numeric_columns(self):
        """Returns a list of numeric columns."""
        return list(self.df.select_dtypes(include=['int64', 'float64']).columns)

    def get_categorical_columns(self):
        """Returns a list of categorical columns."""
        return list(self.df.select_dtypes(include=['object', 'category']).columns)