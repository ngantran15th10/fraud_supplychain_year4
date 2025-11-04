## Model Training for Combined Fraud Detection

from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, CSVLogger
from sklearn.utils.class_weight import compute_class_weight
import numpy as np
import os

def train_model(model, X_train, y_train, X_val, y_val, config):
    """
    Train the fraud detection model
    
    Args:
        model: Compiled Keras model
        X_train: Training features
        y_train: Training labels
        X_val: Validation features
        y_val: Validation labels
        config: Configuration module
    
    Returns:
        Trained model and training history
    """
    # Create results directory if not exists
    os.makedirs(config.RESULTS_PATH, exist_ok=True)
    
    # Calculate class weights to handle imbalance
    class_weights = compute_class_weight(
        'balanced',
        classes=np.unique(y_train),
        y=y_train
    )
    class_weight_dict = {0: class_weights[0], 1: class_weights[1]}
    
    print(f"\nClass weights: {class_weight_dict}")
    print(f"Fraud class weight is {class_weights[1]/class_weights[0]:.2f}x higher")
    
    # Callbacks
    checkpoint = ModelCheckpoint(
        filepath=config.MODEL_SAVE_PATH,
        monitor='val_loss',
        save_best_only=True,
        mode='min',
        verbose=1
    )
    
    early_stop = EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True,
        verbose=1
    )
    
    csv_logger = CSVLogger(
        os.path.join(config.RESULTS_PATH, 'training_log.csv'),
        append=False
    )
    
    print("\n" + "="*60)
    print("Training Combined Model (Transaction + Network)...")
    print("="*60)
    
    # Train the model with class weights
    history = model.fit(
        X_train, y_train,
        epochs=config.EPOCHS,
        batch_size=config.BATCH_SIZE,
        validation_data=(X_val, y_val),
        class_weight=class_weight_dict,  # Add class weight
        callbacks=[checkpoint, early_stop, csv_logger],
        verbose=1
    )
    
    print("\nTraining completed!")
    print(f"Best model saved to: {config.MODEL_SAVE_PATH}")
    
    return model, history
