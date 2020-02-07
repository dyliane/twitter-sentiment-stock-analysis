# -*- coding:utf-8 -*-
import os
import glob
import json
import io
import argparse
import pandas as pd


def main(data_path):

    files = glob.glob(os.path.join(data_path, '*'))
    print(len(files))

    dictlist = []

    for file in files:

        json_string = io.open(file, 'r', encoding="utf-8").read()
        # print(json_string)
        json_dict = json.loads(json_string)
        dictlist.append(json_dict)

    df = pd.DataFrame(dictlist)

    df = df.replace({'\n': ' '}, regex=True)
    df = df.replace({'\t': ' '}, regex=True)
    #df = df.replace({'\r', ' '}, regex=True)

    df.to_csv("data-full-pt.csv", index=False, encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('data_path')
    args = parser.parse_args()

    main(args.data_path)
