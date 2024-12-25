import json
import pandas as pd
from pathlib import Path


def column_renaming(df: pd.DataFrame, json_renamers_path: Path) -> pd.DataFrame:

    with open(json_renamers_path) as json_renamers:
        dict_renamers = json.load(json_renamers)
        selected_columns = list(dict_renamers.keys())
        df = df.filter(items=selected_columns, axis=1)
        df.rename(columns=dict_renamers, inplace=True)

    return df
