from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)
from utils import get_db_connection
from mlxtend.plotting import plot_confusion_matrix
import matplotlib.pyplot as plt
import numpy as np


def get_metrics(
    model_prefix: str,
    table_name: str,
    cursor,
    split: bool = False,
    split_word_count: int = 0,
) -> None:
    try:
        prompt_strategy = ["zs", "fs", "cot"]

        for strategy in prompt_strategy:
            sql = ""
            if split:
                sql = f"SELECT aristotelian_rhetoric, {model_prefix}_{strategy} FROM {table_name} WHERE transcription_word_count >= {split_word_count}"
            else:
                sql = f"SELECT aristotelian_rhetoric, {model_prefix}_{strategy} FROM {table_name} WHERE profile = 'bolsonaromessiasjair'"
            cursor.execute(sql)
            rows = cursor.fetchall()

            true = [row[0].strip().lower() for row in rows]
            prediction = [row[1].strip().lower() for row in rows]

            accuracy = accuracy_score(true, prediction)
            precision = precision_score(true, prediction, average="macro")
            recall = recall_score(true, prediction, average="macro")
            f1 = f1_score(true, prediction, average="macro")

            if split:
                print(f"{model_prefix} {strategy} {split_word_count} words: ")
            else:
                print(f"{model_prefix} {strategy}: ")
            print(f"Accuracy: {accuracy:.2f}")
            print(f"Precision: {precision:.2f}")
            print(f"Recall: {recall:.2f}")
            print(f"F1 Score: {f1:.2f}")
            print(" ")
    except Exception as e:
        print(e)


try:
    connection, cursor = get_db_connection(
        "video_transcription", "postgres", "localhost", "28240907", 5432
    )
    models = ["gemini", "llama", "deepseek"]
    for model in models:
        get_metrics(model, "data", cursor)
except Exception as e:
    print(e)
finally:
    if connection:
        cursor.close()
        connection.close()
