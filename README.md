# Raman ML Classification Tool

A machine learning classification tool for Raman spectroscopy data that supports multiple algorithms (Random Forest, SVM, KNN) with cross-validation and optional external testing.

## Features

- **Multiple ML Algorithms**: Random Forest, Support Vector Machine (SVM), and K-Nearest Neighbors (KNN)
- **Cross-Validation**: K-fold cross-validation or Leave-One-Out Cross-Validation (LOOCV)
- **Feature Selection**: Automatic feature selection using mutual information for SVM and KNN
- **External Testing**: Optional external test set evaluation
- **Visualization**: Confusion matrix plots for model performance assessment
- **Flexible Configuration**: Command-line arguments and configurable parameters

## Quick Start with Docker (Recommended)

The easiest way to run this tool is using Docker, which provides a consistent Python 3.11 environment:

Install docker


```bash
# Build and start the container
./run_docker.sh

# Inside the container, run your analysis
python ml-classification_v2.0.py --models rf --cv loocv --train EXAMPLE_CSV.csv
```

## Docker Usage

### First Time Setup

```bash
# Build the Docker image (first time only)
docker-compose build

# Start the container
docker-compose up -d

# Get into the container
docker-compose exec ml-classification bash
```

### Running Analysis

```bash
# Inside the Docker container
python ml-classification_v2.0.py --models rf --cv loocv --train EXAMPLE_CSV.csv
```

### Viewing Results

```bash
# List generated plot files
python view_plots.py

# Copy plots to your host machine
docker cp raman-ml:/app/cv_results_loocv.png .
docker cp raman-ml:/app/external_test_results.png .
```

### Restarting After Code Changes

```bash
# For Python code changes (most common)
docker-compose down
docker-compose up -d
docker-compose exec ml-classification bash

# For dependency changes (requirements.txt, Dockerfile)
./run_docker.sh --rebuild
```

## Local Installation (Alternative)

If you prefer to run locally without Docker:

```bash
pip install -r requirements.txt
python ml-classification_v2.0.py --models rf --cv loocv --train EXAMPLE_CSV.csv
```

## Usage Examples

### Basic Usage

```bash
python ml-classification_v2.0.py --models rf --cv loocv --train EXAMPLE_CSV.csv
```

### Run All Models with K-fold CV

```bash
python ml-classification_v2.0.py --models rf,svm,knn --cv kfold --splits 5 --train data.csv
```

### With External Test Set

```bash
python ml-classification_v2.0.py --models rf,svm --train train.csv --test test.csv
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

## Docker Troubleshooting

### Common Issues

**Container won't start:**
```bash
# Check if port is in use
docker-compose down
docker-compose up -d
```

**Permission issues:**
```bash
# Make sure the script is executable
chmod +x run_docker.sh
```

**Plots not showing:**
- Plots are saved as PNG files in the container
- Use `python view_plots.py` to list available plots
- Copy plots to host: `docker cp raman-ml:/app/plot_name.png .`

**Need to rebuild after dependency changes:**
```bash
./run_docker.sh --rebuild
```

### Docker Commands Reference

**Using the helper script (recommended):**
```bash
./docker_helpers.sh start     # Start container
./docker_helpers.sh stop      # Stop container
./docker_helpers.sh restart   # Restart container
./docker_helpers.sh logs      # View container logs
./docker_helpers.sh status    # Check container status
./docker_helpers.sh clean     # Clean up everything
./docker_helpers.sh copy-plots # Copy plot files to host
```

**Manual Docker commands:**
```bash
# Start container
docker-compose up -d

# Stop container
docker-compose down

# Get into container
docker-compose exec ml-classification bash

# View container logs
docker-compose logs ml-classification

# Rebuild image
docker-compose build

# Remove everything (clean slate)
docker-compose down --volumes --remove-orphans
docker system prune -a
```

## Output

The script provides:
- Cross-validation accuracy scores
- Classification reports with precision, recall, and F1-score
- Confusion matrix visualizations (saved as PNG files in Docker)
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