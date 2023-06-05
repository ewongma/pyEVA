import pandas as pd
import numpy as np
from glob import iglob
from pathlib import Path

class LoadCSV:

    def __init__(self):
        self.featureTable = pd.read_csv(
            next(iglob("input/*.csv")),
            header=0)
        self.csv_modify()

    def csv_modify(self):
        df = self.featureTable
        df.columns.values[0:2] = ["mz", "rt"]
        df["maxo"] = np.nan
        df["sample"] = np.nan
        from PlotData import PlotData
        for i in range(df.shape[0]):
            row = df.iloc[i, :]
            int_values = np.array(row[2:2 + len(PlotData(level=1).files)], dtype=float)
            max_value = np.max(int_values)
            max_index = int_values.argmax()
            df.loc[i, "maxo"] = max_value
            df.loc[i, "sample"] = max_index + 1
        df = df[["mz", "rt", "maxo", "sample"]]
        df = df.sort_values("mz", ascending=True)
        df.index = ["F" + str(i) for i in range(1, df.shape[0] + 1)]
        featuretablepath = Path(__file__).parent / "output" / "FinalTable.csv"
        df.to_csv(featuretablepath)
        self.featureTable = df


if __name__ == '__main__':
    a = LoadCSV()

