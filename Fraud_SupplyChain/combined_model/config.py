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
THRESHOLD = 0.20  # AGGRESSIVE: Lower threshold for maximum Recall

# SMOTE
SAMPLING_STRATEGY = 1.0  # FULLY BALANCED: Fraud = 100% of Not Fraud

# Model settings
USE_FOCAL_LOSS = False  # Disable standard focal loss
USE_COST_SENSITIVE = True  # Enable cost-sensitive focal loss
FOCAL_GAMMA = 0.8  # AGGRESSIVE: Even less aggressive focusing
FOCAL_ALPHA = 0.80  # AGGRESSIVE: Focus even more on fraud class
FN_COST = 15.0  # AGGRESSIVE: False Negative costs 15x more than False Positive

# Ensemble
USE_ENSEMBLE = True  # Train multiple models with different seeds
ENSEMBLE_SEEDS = [42, 123, 456]  # 3 random seeds for ensemble

# Random state
RANDOM_STATE = 42
