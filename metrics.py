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


try:
    connection, cursor = get_db_connection(
        "db_name", "username", "host", "root_password", 5432
    )

    # Substituir para gerar as métricas para diferentes modelos e estratégia de prompt
    sql = "SELECT aristotelian_rhetoric, gemini_zs FROM data"
    cursor.execute(sql)
    results = cursor.fetchall()

    # Normalização
    true = [row[0].strip().lower() for row in results]
    prediction = [row[1].strip().lower() for row in results]

    # Verificar classes únicas
    unique_labels = sorted(set(true) | set(prediction))
    print("Rótulos encontrados:", unique_labels)

    # Criar matriz de confusão
    cm = confusion_matrix(true, prediction, labels=unique_labels)
    print(f"Matriz de confusão:\n{cm}")

    correct_predictions = np.trace(cm)
    total_predictions = np.sum(cm)
    incorrect_predictions = total_predictions - correct_predictions

    cm_simplified = np.array(
        [
            [correct_predictions, incorrect_predictions],
            [incorrect_predictions, correct_predictions],
        ]
    )

    print(f"Acertos: {correct_predictions}, Erros: {incorrect_predictions}")

    # Plotar matriz de confusão simplificada
    fig, ax = plot_confusion_matrix(
        conf_mat=cm_simplified, show_absolute=True, show_normed=True, colorbar=True
    )
    plt.xticks([0, 1], ["Acertos", "Erros"])
    plt.yticks([0, 1], ["Acertos", "Erros"])
    plt.show()

    # Calcular métricas
    accuracy = accuracy_score(true, prediction)
    precision = precision_score(true, prediction, average="weighted")
    recall = recall_score(true, prediction, average="weighted")
    f1 = f1_score(true, prediction, average="weighted")

    print(f"Accuracy: {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1 Score: {f1:.2f}")

except Exception as e:
    print(e)
finally:
    if connection:
        cursor.close()
        connection.close()
