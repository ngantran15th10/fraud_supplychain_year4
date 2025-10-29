## Define the Deep Neural Network model for Combined Fraud Detection

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

def build_model(input_dim):
    """
    Build a Deep Neural Network for fraud detection using combined features
    
    Args:
        input_dim: Number of input features (after PCA)
    
    Returns:
        Compiled Keras Sequential model
    """
    clf = Sequential(name='Combined_Model')
    
    # Input layer + Hidden layer 1
    clf.add(Dense(256, activation='relu', input_dim=input_dim, name='dense_1'))
    clf.add(Dropout(0.3, name='dropout_1'))
    
    # Hidden layer 2
    clf.add(Dense(128, activation='relu', name='dense_2'))
    clf.add(Dropout(0.3, name='dropout_2'))
    
    # Hidden layer 3
    clf.add(Dense(64, activation='relu', name='dense_3'))
    clf.add(Dropout(0.2, name='dropout_3'))
    
    # Output layer (binary classification)
    clf.add(Dense(1, activation='sigmoid', name='output'))
    
    # Compile model
    clf.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
    )
    
    return clf
