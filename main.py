import datetime
import os
import shutil
import json

import pandas as pd

with open("config.json", "r") as f:
    CONFIG = json.load(f)
    
KAGGLE_USERNAME = os.getenv("KAGGLE_USERNAME")
KAGGLE_KEY = os.getenv("KAGGLE_KEY")


def get_update_lines(df_last, df_actual, pk, date_field):

    df_update = df_last.merge(
        df_actual,
        how="left",
        on=[pk],
        suffixes=('_x', '_y')
    )

    update_flag = df_update[date_field + '_y'] > df_update[date_field + '_x']
    ids_updated = df_update[update_flag][pk].tolist()

    df_update = df_actual[df_actual[pk].isin(ids_updated)].copy()
    df_update["op"] = "U"
    return df_update


def get_insert_lines(df_last, df_actual, pk):
    df_insert = df_actual[~df_actual[pk].isin(df_last[pk])].copy()
    df_insert["op"] = "I"
    return df_insert


def get_delete_lines(df_last, df_actual, pk):
    df_delete = df_last[~df_last[pk].isin(df_actual[pk])].copy()
    df_delete["op"] = "D"
    return df_delete


def create_cdc(df_last, df_actual, pk, date_field):
    df_update = get_update_lines(df_last, df_actual, pk, date_field)
    df_insert = get_insert_lines(df_last, df_actual, pk)
    df_delete = get_delete_lines(df_last, df_actual, pk)
    df_cdc = pd.concat([df_update, df_insert, df_delete], ignore_index=True)
    return df_cdc

def process_cdc(tables):

    print("Processando CDC de todas tabelas...")

    for t in tables:
        df_last = pd.read_csv(f"./data/last/{t['name']}.csv", sep=t["sep"])
        df_actual = pd.read_csv(f"./data/actual/{t['name']}.csv", sep=t["sep"])
        df_cdc = create_cdc(df_last, df_actual, t["pk"], t["date_field"])

        if df_cdc.shape[0] == 0:
            print(f"Nenhuma alteração encontrada para a tabela {t['name']}.")
            continue
        
        if not os.path.exists("./data/cdc"):
            os.makedirs("./data/cdc")

        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"./data/cdc/{t['name']}_{now}.csv"

        df_cdc.to_csv(filename, index=False, sep=t["sep"])

    print("CDC processado com sucesso!")


def download_kaggle_dataset(dataset_name):
    
    from kaggle.api.kaggle_api_extended import KaggleApi
    api = KaggleApi()
    api.authenticate()

    print(f"Baixando o dataset {dataset_name} para ./data/actual/...")
    api.dataset_download_files(dataset_name, path="data/actual/", unzip=True)
    print("Download concluído!")


def move_from_actual_to_last():
    
    actual_path = "./data/actual"
    last_path = "./data/last"

    if not os.path.exists(last_path):
        os.makedirs(last_path)

    print("Movendo arquivos de ./data/actual para ./data/last...")

    for item in os.listdir(actual_path):
        source = os.path.join(actual_path, item)
        destination = os.path.join(last_path, item)
        shutil.move(source, destination)

    print("Arquivos movidos com sucesso!")

if __name__ == "__main__":

    dataset_name = CONFIG["dataset_name"]
    
    move_from_actual_to_last()
    download_kaggle_dataset(dataset_name)
    process_cdc(CONFIG["tables"])
    
