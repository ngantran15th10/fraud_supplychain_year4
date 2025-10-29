## Configuration for Network-based Fraud Detection Model

import os

# Paths
current_dir = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(current_dir, '..', 'data', 'network_only.csv')
MODEL_SAVE_PATH = os.path.join(current_dir, 'network_model.keras')
RESULTS_PATH = os.path.join(current_dir, 'results')

# PCA Components - Use all 4 features (no PCA needed for small feature set)
N_COMPONENTS = None  # Set to None to skip PCA

# Model hyperparameters
EPOCHS = 50
BATCH_SIZE = 32
VALIDATION_SPLIT = 0.2

# Random state
RANDOM_STATE = 42
