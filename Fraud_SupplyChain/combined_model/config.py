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
EPOCHS = 100  # Increased from 50 (with early stopping)
BATCH_SIZE = 32
VALIDATION_SPLIT = 0.2

# Evaluation
THRESHOLD = 0.3  # Lower threshold for better recall (default 0.5)

# SMOTE
SAMPLING_STRATEGY = 0.5  # Fraud = 50% of Not Fraud

# Model settings
USE_FOCAL_LOSS = True  # Use Focal Loss instead of Binary Crossentropy

# Random state
RANDOM_STATE = 42
