import pandas as pd


def column_selection_and_renaming(df: pd.DataFrame, dict_renamers: dict) -> pd.DataFrame:

    selected_columns = list(dict_renamers.keys())
    df = df.filter(items=selected_columns, axis=1)
    df.rename(columns=dict_renamers, inplace=True)

    return df
