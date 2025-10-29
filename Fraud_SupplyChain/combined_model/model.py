## Define the Deep Neural Network model for Combined Fraud Detection

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
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

def cost_sensitive_focal_loss(gamma=1.0, alpha=0.75, fn_cost=10.0):
    """
    Cost-Sensitive Focal Loss - Heavily penalize False Negatives (missing frauds)
    
    Args:
        gamma: focusing parameter (lower = less aggressive than standard focal)
        alpha: balance parameter for fraud class
        fn_cost: cost multiplier for False Negatives (default: 10x)
    
    Philosophy:
        - Missing a fraud (FN) costs ~$1000 in real money
        - False alarm (FP) costs ~$20 in investigation
        - FN should be penalized 50x more than FP
    
    Returns:
        Cost-sensitive focal loss function
    """
    def cs_focal_loss_fixed(y_true, y_pred):
        epsilon = K.epsilon()
        y_pred = K.clip(y_pred, epsilon, 1. - epsilon)
        
        # Standard focal loss component
        cross_entropy = -y_true * K.log(y_pred) - (1 - y_true) * K.log(1 - y_pred)
        
        p_t = y_true * y_pred + (1 - y_true) * (1 - y_pred)
        focal_weight = K.pow((1 - p_t), gamma)
        focal = alpha * focal_weight * cross_entropy
        
        # Extra penalty for False Negatives
        # When y_true=1 (actual fraud) but y_pred is low (model misses it)
        fn_penalty = y_true * (1 - y_pred) * fn_cost
        
        # Combined loss
        total_loss = focal + fn_penalty
        
        return K.mean(total_loss)
    
    return cs_focal_loss_fixed

def build_model(input_dim, use_focal_loss=True, focal_gamma=1.5, focal_alpha=0.65, use_cost_sensitive=False, fn_cost=10.0):
    """
    Build a Deep Neural Network for fraud detection using combined features
    
    Args:
        input_dim: Number of input features (after PCA)
        use_focal_loss: Whether to use Focal Loss (default True)
        focal_gamma: Focal loss gamma parameter (default 1.5)
        focal_alpha: Focal loss alpha parameter (default 0.65)
        use_cost_sensitive: Whether to use cost-sensitive focal loss (default False)
        fn_cost: Cost multiplier for False Negatives when use_cost_sensitive=True
    
    Returns:
        Compiled Keras model
    """
    model = Sequential([
        # Input layer with BatchNormalization
        Dense(256, activation='relu', input_shape=(input_dim,)),
        BatchNormalization(),
        Dropout(0.3),
        
        # Hidden layer 1
        Dense(128, activation='relu'),
        BatchNormalization(),
        Dropout(0.3),
        
        # Hidden layer 2
        Dense(64, activation='relu'),
        BatchNormalization(),
        Dropout(0.2),
        
        # Output layer
        Dense(1, activation='sigmoid')
    ])
    
    # Choose loss function
    if use_cost_sensitive:
        loss_fn = cost_sensitive_focal_loss(gamma=focal_gamma, alpha=focal_alpha, fn_cost=fn_cost)
        print(f"Using Cost-Sensitive Focal Loss (gamma={focal_gamma}, alpha={focal_alpha}, fn_cost={fn_cost})")
    elif use_focal_loss:
        loss_fn = focal_loss(gamma=focal_gamma, alpha=focal_alpha)
        print(f"Using Focal Loss (gamma={focal_gamma}, alpha={focal_alpha})")
    else:
        loss_fn = 'binary_crossentropy'
        print("Using Binary Crossentropy")
    
    Returns:
        Compiled Keras Sequential model
    """
    clf = Sequential(name='Combined_Model')
    
    # Input layer + Hidden layer 1
    clf.add(Dense(256, activation='relu', input_dim=input_dim, name='dense_1'))
    clf.add(BatchNormalization(name='bn_1'))
    clf.add(Dropout(0.3, name='dropout_1'))
    
    # Hidden layer 2
    clf.add(Dense(128, activation='relu', name='dense_2'))
    clf.add(BatchNormalization(name='bn_2'))
    clf.add(Dropout(0.3, name='dropout_2'))
    
    # Hidden layer 3
    clf.add(Dense(64, activation='relu', name='dense_3'))
    clf.add(BatchNormalization(name='bn_3'))
    clf.add(Dropout(0.2, name='dropout_3'))
    
    # Output layer (binary classification)
    clf.add(Dense(1, activation='sigmoid', name='output'))
    
    # Compile model with Focal Loss or Binary Crossentropy
    if use_focal_loss:
        print(f"Using Focal Loss (gamma={focal_gamma}, alpha={focal_alpha})")
        loss_function = focal_loss(gamma=focal_gamma, alpha=focal_alpha)
    else:
        print("Using Binary Crossentropy")
        loss_function = 'binary_crossentropy'
    
    clf.compile(
        optimizer='adam',
        loss=loss_function,
        metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
    )
    
    return clf
