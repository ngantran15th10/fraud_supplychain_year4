## Configuration for Combined Fraud Detection Model (Transaction + Network)

import os

# Paths
current_dir = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(current_dir, '..', 'data', 'combined_features.csv')
MODEL_SAVE_PATH = os.path.join(current_dir, 'combined_model.keras')
RESULTS_PATH = os.path.join(current_dir, 'results')

# PCA Components
N_COMPONENTS = 45  # Increased from 35 to retain more information

# Model hyperparameters
EPOCHS = 100  # Increased from 50 (with early stopping)
BATCH_SIZE = 32
VALIDATION_SPLIT = 0.2

# Evaluation
THRESHOLD = 0.3  # Fixed threshold to prioritize Recall in fraud detection

# SMOTE
SAMPLING_STRATEGY = 0.6  # Increased from 0.5: Fraud = 60% of Not Fraud

# Model settings
USE_FOCAL_LOSS = True  # Use Focal Loss instead of Binary Crossentropy
FOCAL_GAMMA = 1.5  # Reduced from 2.0 for less aggressive focusing
FOCAL_ALPHA = 0.65  # Adjusted from 0.75 for better balance

# Ensemble
USE_ENSEMBLE = True  # Train multiple models with different seeds
ENSEMBLE_SEEDS = [42, 123, 456]  # 3 random seeds for ensemble

# Random state
RANDOM_STATE = 42
