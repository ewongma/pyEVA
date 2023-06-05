import os
from pathlib import Path

if __name__ == '__main__':
    if not (Path(__file__).parent / "input").exists():
        raise RuntimeError("Create an Input folder and place the data into it")
    (Path(__file__).parent / "output").mkdir(exist_ok=True)
    os.system('python config.py')
    os.system('python LoadCSV.py')
    print('Feature table has already been loaded and saved as “InputFeatureTable.csv” under the output folder.')
    print('\nIn the next step, you will need to input a smoothing level, which is an integer.')
    os.system('python PlotData.py')
    print('All EIC plots have been generated under the folder .../classifier/EICplots')
    os.chdir('classifier')
    os.system('python main.py -m test')
    os.chdir('..')
    os.system('python FinalOutput.py')
    print('Data processing is complete. The EIC evaluation result is in "PredictionOutcome.csv" and the final result '
          'is in "FinalTable.csv". Both files are found under the output folder.\nThank you for using pyEVA!')



