import pandas as pd
from pathlib import Path

class FinalOutput:
    def __init__(self):
        self.featureTable = pd.read_csv(
            "output/FinalTable.csv")
        self.prediction = pd.read_csv(
            "output/PredictionOutcome.csv")
        self._modify()
        featuretablepath = Path(__file__).parent / "output" / "FinalTable.csv"
        self.featureTable.to_csv(
            featuretablepath,
            index=False, header=True)

    def _modify(self):
        feature_table = self.featureTable.sort_values(self.featureTable.columns[0], ascending=True)
        prediction = self.prediction.sort_values(by=["image"], ascending=True)
        feature_table = feature_table.rename(columns={'Unnamed: 0': 'ID'})
        feature_table = pd.concat(
            [feature_table["ID"], feature_table["mz"], feature_table["rt"], feature_table["maxo"],
             prediction["prediction"], feature_table["sample"]],
            axis=1)
        feature_table.columns = ["ID", "mz", "rt", "intensity", "prediction", "sample"]
        feature_table["mz"] = pd.to_numeric(feature_table["mz"])
        feature_table["rt"] = pd.to_numeric(feature_table["rt"])
        feature_table["intensity"] = pd.to_numeric(feature_table["intensity"])
        feature_table["mz"] = feature_table["mz"].round(4).apply(lambda x: '{:.4f}'.format(x))
        feature_table["rt"] = feature_table["rt"].round(0).astype(int)
        feature_table["intensity"] = feature_table["intensity"].round(0).astype(int)
        feature_table["sample"] = feature_table["sample"].astype(int)
        feature_table = feature_table.sort_values(by=["mz"], ascending=False)
        self.featureTable = feature_table


if __name__ == '__main__':
    a = FinalOutput()
