## Define the Deep Neural Network model for Combined Fraud Detection

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import tensorflow.keras.backend as K

def focal_loss(gamma=2.0, alpha=0.75):
    """
    Focal Loss for imbalanced classification
    
    Args:
        gamma: focusing parameter (higher = more focus on hard examples)
        alpha: balance parameter (higher = more weight on positive class)
    
    Returns:
        Focal loss function
    """
    def focal_loss_fixed(y_true, y_pred):
        epsilon = K.epsilon()
        y_pred = K.clip(y_pred, epsilon, 1. - epsilon)
        
        # Calculate cross entropy
        cross_entropy = -y_true * K.log(y_pred) - (1 - y_true) * K.log(1 - y_pred)
        
        # Calculate focal weight
        weight = alpha * y_true * K.pow((1 - y_pred), gamma) + \
                 (1 - alpha) * (1 - y_true) * K.pow(y_pred, gamma)
        
        # Apply focal weight
        focal_loss_value = weight * cross_entropy
        
        return K.mean(focal_loss_value)
    
    return focal_loss_fixed

def build_model(input_dim, use_focal_loss=True):
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
    
    # Compile model with Focal Loss or Binary Crossentropy
    if use_focal_loss:
        print("Using Focal Loss (gamma=2.0, alpha=0.75)")
        loss_function = focal_loss(gamma=2.0, alpha=0.75)
    else:
        print("Using Binary Crossentropy")
        loss_function = 'binary_crossentropy'
    
    clf.compile(
        optimizer='adam',
        loss=loss_function,
        metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
    )
    
    return clf
