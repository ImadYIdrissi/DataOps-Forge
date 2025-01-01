"""Columns staging transformations."""

import pandas as pd


def column_selection_and_renaming(df: pd.DataFrame, dict_renamers: dict) -> pd.DataFrame:
    """Filter and rename columns in a Pandas DataFrame based on a dictionary mapping.

    Args:
      df(pd.DataFrame): The input DataFrame to process.
      dict_renamers(dict): A dictionary where keys represent the column names to select,
    and values represent the new names for those columns.

    Returns:
      pd.DataFrame: A DataFrame with only the selected columns, renamed according to the dictionary.

    """
    selected_columns = list(dict_renamers.keys())
    df = df.filter(items=selected_columns, axis=1)
    df.rename(columns=dict_renamers, inplace=True)

    return df
