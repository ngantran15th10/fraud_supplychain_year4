## Configuration for Transaction-based Fraud Detection Model

import os

# Paths
current_dir = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(current_dir, '..', 'data', 'transaction_only.csv')
MODEL_SAVE_PATH = os.path.join(current_dir, 'transaction_model.keras')
RESULTS_PATH = os.path.join(current_dir, 'results')

# PCA Components
N_COMPONENTS = 30  # Reduce from 57 features to 30 components

# Model hyperparameters
EPOCHS = 50
BATCH_SIZE = 32
VALIDATION_SPLIT = 0.2

# Random state
RANDOM_STATE = 42
