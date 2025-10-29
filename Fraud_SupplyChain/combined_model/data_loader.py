## Data loading and preprocessing for Combined Model

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

def load_data(data_path):
    """Load combined features dataset"""
    print(f"Loading data from {data_path}...")
    df = pd.read_csv(data_path)
    print(f"Data loaded: {df.shape}")
    return df

def split_features_labels(df):
    """Split features and labels"""
    # Remove Customer Id and is_fraud
    X = df.drop(['Customer Id', 'is_fraud'], axis=1)
    y = df['is_fraud']
    
    print(f"Features shape: {X.shape}")
    print(f"Transaction features: 57")
    print(f"Network features: 4")
    print(f"Total combined features: {X.shape[1]}")
    print(f"Labels distribution:\n{y.value_counts()}")
    print(f"Fraud rate: {y.mean()*100:.2f}%")
    
    return X, y

def split_data(X, y, test_size=0.2, random_state=42):
    """Split data into train and test sets"""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    print(f"\nTrain set: {X_train.shape}")
    print(f"Test set: {X_test.shape}")
    
    return X_train, X_test, y_train, y_test

def scale_data(X_train, X_test):
    """Scale features using StandardScaler"""
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"\nData scaled successfully")
    
    return X_train_scaled, X_test_scaled, scaler

def apply_smote(X_train, y_train, random_state=42, sampling_strategy=0.5):
    """
    Apply SMOTE to handle class imbalance
    
    Args:
        sampling_strategy: float, target ratio of minority/majority class
                          0.5 = minority will be 50% of majority (recommended)
                          1.0 = fully balanced (default SMOTE)
    """
    print(f"\nBefore SMOTE: {X_train.shape}")
    print(f"Class distribution: {pd.Series(y_train).value_counts().to_dict()}")
    
    # Check and handle NaN values
    if np.isnan(X_train).any():
        print("WARNING: Found NaN values in training data. Replacing with 0...")
        X_train = np.nan_to_num(X_train, nan=0.0)
    
    # Check for infinite values
    if np.isinf(X_train).any():
        print("WARNING: Found infinite values in training data. Replacing with 0...")
        X_train = np.nan_to_num(X_train, posinf=0.0, neginf=0.0)
    
    smote = SMOTE(random_state=random_state, sampling_strategy=sampling_strategy)
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
    
    print(f"After SMOTE (strategy={sampling_strategy}): {X_train_res.shape}")
    print(f"Class distribution: {pd.Series(y_train_res).value_counts().to_dict()}")
    
    return X_train_res, y_train_res
