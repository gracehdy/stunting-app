import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)
import pickle
import os


def train_model(verbose=True):
    try:
        df = pd.read_csv("data_balita.csv")
    except FileNotFoundError:
        return None

    stunting_categories = ['stunted', 'severely stunted']
    df['is_stunted'] = df['Status Gizi'].apply(lambda x: 1 if x in stunting_categories else 0)

    X = df[['Umur (bulan)', 'Tinggi Badan (cm)']]
    y = df['is_stunted']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)

    if verbose:
        evaluate_model(model, X_test, y_test)

    if not os.path.exists("model"):
        os.makedirs("model")

    with open("model/model.pkl", "wb") as f:
        pickle.dump(model, f)

    return model


def evaluate_model(model, X_test, y_test):
    """Print classification metrics for a binary stunting classifier (0 = normal, 1 = stunted).

    MAE/RMSE are not used here since this is a classification task, not regression.
    """
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba)
    cm = confusion_matrix(y_test, y_pred)

    print("\n=== Model Evaluation (test set, n =", len(y_test), ") ===")
    print(f"Accuracy : {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall   : {rec:.4f}")
    print(f"F1 Score : {f1:.4f}")
    print(f"ROC AUC  : {auc:.4f}")

    print("\nConfusion Matrix:")
    print("                 Predicted Normal   Predicted Stunted")
    print(f"Actual Normal    {cm[0][0]:>16}   {cm[0][1]:>18}")
    print(f"Actual Stunted   {cm[1][0]:>16}   {cm[1][1]:>18}")

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Normal", "Stunted"]))

    return {
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1": f1,
        "roc_auc": auc,
        "confusion_matrix": cm,
    }


if __name__ == "__main__":
    train_model()
    print("\nModel trained and saved successfully to model/model.pkl.")