import pandas as pd
import os

def extractDataFromMETA():
    data = pd.read_excel(r'COVID-CT-MetaInfo.xlsx')
    df = pd.DataFrame(data, columns=[
        'File name', 'Age', 'Gender', 'Location', 'Medical history', 'Severity'])
    return df


def extractTrainedFileName():
    trainedPath = []
    for filename in os.listdir('data/CT_COVID'):
        trainedPath.append(filename)
    return trainedPath


# This method return a list of dicts with the extracted, crossed data of images in training
def extractTrainedData():
    df = extractDataFromMETA()
    trainedPaths = extractTrainedFileName()
    for index, row in df.iterrows():
        if row['File name'] not in trainedPaths:
            df.drop(index, inplace=True)
    dataDict = df.to_dict('records')
    ctr = 0
    for each in dataDict:
        ctr += 1
        each.update({'index': ctr})
    return dataDict
