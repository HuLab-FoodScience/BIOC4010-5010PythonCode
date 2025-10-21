# Raman ML Classification Tool

A machine learning classification tool for Raman spectroscopy data that supports multiple algorithms (Random Forest, SVM, KNN) with cross-validation and optional external testing.

## Features

- **Multiple ML Algorithms**: Random Forest, Support Vector Machine (SVM), and K-Nearest Neighbors (KNN)
- **Cross-Validation**: K-fold cross-validation or Leave-One-Out Cross-Validation (LOOCV)
- **Feature Selection**: Automatic feature selection using mutual information for SVM and KNN
- **External Testing**: Optional external test set evaluation
- **Visualization**: Confusion matrix plots for model performance assessment
- **Flexible Configuration**: Command-line arguments and configurable parameters

## Requirements

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python ml-classification_v2.0.py --models rf --cv loocv --train EXAMPLE_CSV.csv
```

### Command Line Arguments

- `--models`: Comma-separated list of models to run (rf, svm, knn)
- `--cv`: Cross-validation mode (kfold or loocv)
- `--splits`: Number of splits for k-fold CV (default: 5)
- `--train`: Path to training CSV file
- `--test`: Optional path to external test CSV file

## Configuration

Key parameters can be modified in the script:

- `TOP_K`: Number of features to select for SVM/KNN (default: 3)
- `KNN_NEIGHBORS`: Number of neighbors for KNN (default: 4)
- `SVM_C`: SVM regularization parameter (default: 1.0)
- `SVM_GAMMA`: SVM kernel coefficient (default: "scale")
- `RF_TREES`: Number of trees in Random Forest (default: 500)
- `N_SPLITS`: Number of folds for k-fold CV (default: 5)
- `RANDOM_STATE`: Random seed for reproducibility (default: 13)

## Output

The script provides:
- Cross-validation accuracy scores
- Classification reports with precision, recall, and F1-score
- Confusion matrix visualizations
- External test results (if test set provided)

## Model Details

### Random Forest
- Uses all features
- 500 trees by default
- Bootstrap sampling enabled

### SVM (RBF Kernel)
- Feature selection using mutual information
- Standard scaling applied
- RBF kernel with configurable C and gamma

### K-Nearest Neighbors
- Feature selection using mutual information
- Standard scaling applied
- 4 neighbors by default