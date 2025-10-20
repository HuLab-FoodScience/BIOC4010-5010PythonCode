#!/usr/bin/env python3
# Raman ML: selectable RF/SVM/KNN, CV/LOOCV, optional external test

from pathlib import Path
from collections import Counter
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import StratifiedKFold, LeaveOneOut, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

# -------------------- DEFAULT CONFIG (edit these) --------------------
TRAIN_CSV = Path(r"C:\Users\Hwoar\OneDrive - Carleton University\Desktop\PBMA\Without Pe and Ha\Reshuffled (Separate Scaling)\Combined_AUC_scaled.csv")     # rows = samples; col0 = class; col1.. = features
TEST_CSV  = None                                    # e.g., Path(r"C:\path\to\your\external_test.csv") or None

CV_MODE   = "kfold"   # "kfold" or "loocv"
N_SPLITS  = 5         # used only for kfold
RANDOM_STATE = 13

# Choose algorithms here (any subset of {"rf","svm","knn"})
MODELS_TO_RUN = {"rf", "svm", "knn"}

# Model hyperparams
TOP_K = 3                 # feature count for SVM/KNN (SelectKBest with mutual info)
# TOP_K = "all"                 # feature count for SVM/KNN (SelectKBest with mutual info)
KNN_NEIGHBORS = 4
SVM_C = 1.0
SVM_GAMMA = "scale"
RF_TREES = 500
# --------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(description="Raman ML with selectable models")
    p.add_argument("--models", type=str, default=None,
                   help="Comma-separated list of models to run from {rf,svm,knn} (e.g. rf,svm)")
    p.add_argument("--cv", type=str, default=None, choices=["kfold","loocv"],
                   help="Override CV mode (kfold or loocv)")
    p.add_argument("--splits", type=int, default=None, help="Override n_splits for kfold")
    p.add_argument("--train", type=str, default=None, help="Override train CSV path")
    p.add_argument("--test", type=str, default=None, help="Optional external test CSV path")
    return p.parse_args()

def load_xy(csv_path: Path):
    df = pd.read_csv(csv_path).dropna(axis=0, how="all").dropna(axis=1, how="all")
    y = df.iloc[:, 0].astype(str).values
    X = df.iloc[:, 1:].apply(pd.to_numeric, errors="coerce")
    X = X.loc[:, X.notna().any(axis=0)].fillna(0.0)
    return X.values.astype(float), y, [str(c) for c in X.columns]

def get_cv(y, mode: str, splits: int):
    if mode.lower() == "loocv":
        counts = Counter(y)
        bad = [cls for cls, c in counts.items() if c < 2]
        if bad:
            raise ValueError(f"LOOCV requires ≥2 samples per class. Offending classes: {bad}")
        return LeaveOneOut()
    return StratifiedKFold(n_splits=splits, shuffle=True, random_state=RANDOM_STATE)

def plot_cm(ax, cm, labels, title):
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(ax=ax, values_format="d", cmap="Blues", colorbar=False)
    ax.set_title(title, fontsize=10)
    ax.tick_params(axis="x", labelrotation=45)
    ax.set_xlabel("Predicted"); ax.set_ylabel("True")

def build_models(n_features: int, selected: set[str]):
    if not selected:
        raise ValueError("No models selected. Choose from {'rf','svm','knn'}.")

    models = {}
    if "rf" in selected:
        models["Random Forest"] = Pipeline([
            ("clf", RandomForestClassifier(
                n_estimators=RF_TREES, bootstrap=True, random_state=RANDOM_STATE, n_jobs=-1
            ))
        ])

    if "svm" in selected:
        k = min(TOP_K, n_features)

        models["SVM (RBF)"] = Pipeline([
            ("scale", StandardScaler()),
            ("select", SelectKBest(mutual_info_classif, k=k)),
            ("clf", SVC(kernel="rbf", C=SVM_C, gamma=SVM_GAMMA))
        ])

    if "knn" in selected:
        k = min(TOP_K, n_features)

        models["KNN"] = Pipeline([
            ("scale", StandardScaler()),
            ("select", SelectKBest(mutual_info_classif, k=k)),
            ("clf", KNeighborsClassifier(n_neighbors=KNN_NEIGHBORS))
        ])
    return models

def main():
    args = parse_args()

    # Resolve config (CLI overrides are optional)
    train_csv = Path(args.train) if args.train else TRAIN_CSV
    test_csv  = Path(args.test) if args.test else TEST_CSV
    cv_mode   = args.cv if args.cv else CV_MODE
    splits    = args.splits if args.splits else N_SPLITS

    selected = MODELS_TO_RUN
    if args.models:
        selected = {args.models} & {"rf","svm","knn"} if args.models else selected

    # Load data
    X, y, feat_names = load_xy(train_csv)
    print(f"Train shape: X={X.shape}, y={len(y)}, classes={sorted(set(y))}")

    cv = get_cv(y, cv_mode, splits)
    models = build_models(n_features=X.shape[1], selected=selected)
    class_labels = np.unique(y)

    # CV predictions and plots
    n = len(models)
    fig, axes = plt.subplots(1, n, figsize=(4.8 * n, 4), squeeze=False)
    axes = axes[0]

    for ax, (name, pipe) in zip(axes, models.items()):
        print(f"\n=== {name} ({cv_mode.upper()}) ===")
        y_pred = cross_val_predict(pipe, X, y, cv=cv, n_jobs=-1)
        acc = accuracy_score(y, y_pred)
        print(f"Accuracy: {acc:.4f}")
        print(classification_report(y, y_pred, zero_division=0))
        cm = confusion_matrix(y, y_pred, labels=class_labels)
        plot_cm(ax, cm, labels=class_labels, title=f"{name}\n{cv_mode.upper()} Acc={acc*100:.2f}%")
    fig.tight_layout()
    plt.show()

    # External test (optional)
    if test_csv:
        Xtest, ytest, _ = load_xy(test_csv)
        print(f"\nExternal test shape: X={Xtest.shape}, y={len(ytest)}")
        n = len(models)
        fig, axes = plt.subplots(1, n, figsize=(4.8 * n, 4), squeeze=False)
        axes = axes[0]
        for ax, (name, pipe) in zip(axes, models.items()):
            pipe.fit(X, y)
            yhat = pipe.predict(Xtest)
            acc = accuracy_score(ytest, yhat)
            print(f"\n=== {name} (External Test) ===")
            print(f"Accuracy: {acc:.4f}")
            print(classification_report(ytest, yhat, zero_division=0))
            cm = confusion_matrix(ytest, yhat, labels=class_labels)
            plot_cm(ax, cm, labels=class_labels, title=f"{name}\nTest Acc={acc*100:.2f}%")
        fig.tight_layout()
        plt.show()

if __name__ == "__main__":
    main()
