## Configuration for Combined Fraud Detection Model (Transaction + Network)

import os

# Paths
current_dir = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(current_dir, '..', 'data', 'combined_features.csv')
MODEL_SAVE_PATH = os.path.join(current_dir, 'combined_model.keras')
RESULTS_PATH = os.path.join(current_dir, 'results')

# PCA Components
N_COMPONENTS = 35  # Reduce from 61 features to 35 components

# Model hyperparameters
EPOCHS = 50
BATCH_SIZE = 32
VALIDATION_SPLIT = 0.2

# Random state
RANDOM_STATE = 42
