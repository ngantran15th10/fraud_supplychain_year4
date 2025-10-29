## Ensemble Model Training and Evaluation

import config
import data_loader
import model
import train
import predict

from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
import numpy as np
import os

def train_ensemble_models():
    """
    Train multiple models with different random seeds and ensemble predictions
    """
    print("="*70)
    print("ENSEMBLE TRAINING - COMBINED FRAUD DETECTION MODEL")
    print("="*70)
    
    # 1. Load and prepare data (same for all models)
    print("\n" + "="*70)
    print("STEP 1: DATA PREPARATION")
    print("="*70)
    
    df = data_loader.load_data(config.DATA_PATH)
    X, y = data_loader.split_features_labels(df)
    
    # Split with fixed seed for consistency
    X_train, X_test, y_train, y_test = data_loader.split_data(
        X, y, test_size=0.2, random_state=42  # Fixed seed for test set
    )
    
    # Scale
    X_train_scaled, X_test_scaled, scaler = data_loader.scale_data(X_train, X_test)
    
    # Store models and predictions
    models = []
    predictions_proba = []
    
    # 2. Train multiple models with different seeds
    print("\n" + "="*70)
    print("STEP 2: TRAINING ENSEMBLE MODELS")
    print("="*70)
    
    for i, seed in enumerate(config.ENSEMBLE_SEEDS, 1):
        print(f"\n{'='*70}")
        print(f"TRAINING MODEL {i}/{len(config.ENSEMBLE_SEEDS)} (seed={seed})")
        print(f"{'='*70}")
        
        # Apply SMOTE with this seed
        X_train_res, y_train_res = data_loader.apply_smote(
            X_train_scaled, y_train, 
            random_state=seed,
            sampling_strategy=config.SAMPLING_STRATEGY
        )
        
        # Clean NaN/Inf
        X_train_res = np.nan_to_num(X_train_res, nan=0.0, posinf=0.0, neginf=0.0)
        X_test_scaled_clean = np.nan_to_num(X_test_scaled, nan=0.0, posinf=0.0, neginf=0.0)
        
        # Apply PCA
        print(f"\nApplying PCA: {X_train_res.shape[1]} → {config.N_COMPONENTS} components")
        pca = PCA(n_components=config.N_COMPONENTS, random_state=seed)
        X_train_pca = pca.fit_transform(X_train_res)
        X_test_pca = pca.transform(X_test_scaled_clean)
        
        explained_variance = pca.explained_variance_ratio_.sum()
        print(f"Explained variance: {explained_variance*100:.2f}%")
        
        # Split train/validation
        X_train_final, X_val, y_train_final, y_val = train_test_split(
            X_train_pca, y_train_res,
            test_size=config.VALIDATION_SPLIT,
            random_state=seed
        )
        
        # Build model
        input_dim = X_train_pca.shape[1]
        fraud_model = model.build_model(input_dim, use_focal_loss=config.USE_FOCAL_LOSS)
        
        # Create model-specific save path
        model_save_path = os.path.join(
            os.path.dirname(config.MODEL_SAVE_PATH),
            f'combined_model_seed{seed}.keras'
        )
        
        # Update config for this model
        class ModelConfig:
            pass
        model_config = ModelConfig()
        for attr in dir(config):
            if not attr.startswith('_'):
                setattr(model_config, attr, getattr(config, attr))
        model_config.MODEL_SAVE_PATH = model_save_path
        
        # Train
        trained_model, history = train.train_model(
            fraud_model, X_train_final, y_train_final, X_val, y_val, model_config
        )
        
        # Get predictions on test set
        y_pred_proba = trained_model.predict(X_test_pca, verbose=0).flatten()
        
        # Store
        models.append(trained_model)
        predictions_proba.append(y_pred_proba)
        
        print(f"\nModel {i} training completed!")
    
    # 3. Ensemble predictions
    print("\n" + "="*70)
    print("STEP 3: ENSEMBLE PREDICTIONS")
    print("="*70)
    
    # Average predictions from all models
    ensemble_pred_proba = np.mean(predictions_proba, axis=0)
    
    print(f"\nEnsemble combines {len(models)} models")
    print(f"Prediction method: Average probability")
    
    # 4. Evaluate ensemble
    print("\n" + "="*70)
    print("STEP 4: EVALUATING ENSEMBLE MODEL")
    print("="*70)
    
    # Find optimal threshold
    if config.THRESHOLD == 'auto':
        threshold = predict.find_optimal_threshold(y_test, ensemble_pred_proba, metric='balanced')
        print(f"\nOptimal threshold found: {threshold:.3f}")
    else:
        threshold = config.THRESHOLD
        print(f"\nUsing threshold: {threshold}")
    
    # Make predictions
    y_pred = (ensemble_pred_proba > threshold).astype(int)
    
    # Calculate metrics
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score, f1_score,
        roc_auc_score, confusion_matrix, classification_report
    )
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    roc_auc = roc_auc_score(y_test, ensemble_pred_proba)
    cm = confusion_matrix(y_test, y_pred)
    
    # Print results
    print(f"\n{'='*70}")
    print("ENSEMBLE MODEL RESULTS")
    print(f"{'='*70}")
    print(f"\nAccuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print(f"ROC-AUC:   {roc_auc:.4f}")
    
    print("\nConfusion Matrix:")
    print(cm)
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Not Fraud', 'Fraud']))
    
    # Save results
    os.makedirs(config.RESULTS_PATH, exist_ok=True)
    results_file = os.path.join(config.RESULTS_PATH, 'ensemble_evaluation_metrics.txt')
    
    with open(results_file, 'w') as f:
        f.write("="*70 + "\n")
        f.write("ENSEMBLE COMBINED MODEL EVALUATION RESULTS\n")
        f.write(f"(Transaction + Network Features - {len(models)} models ensemble)\n")
        f.write("="*70 + "\n\n")
        f.write(f"Number of models: {len(models)}\n")
        f.write(f"Random seeds: {config.ENSEMBLE_SEEDS}\n")
        f.write(f"Threshold: {threshold:.3f}\n\n")
        f.write(f"Accuracy:  {accuracy:.4f}\n")
        f.write(f"Precision: {precision:.4f}\n")
        f.write(f"Recall:    {recall:.4f}\n")
        f.write(f"F1-Score:  {f1:.4f}\n")
        f.write(f"ROC-AUC:   {roc_auc:.4f}\n\n")
        f.write("Confusion Matrix:\n")
        f.write(str(cm) + "\n\n")
        f.write("Classification Report:\n")
        f.write(classification_report(y_test, y_pred, target_names=['Not Fraud', 'Fraud']))
    
    print(f"\nResults saved to: {results_file}")
    
    print("\n" + "="*70)
    print("ENSEMBLE TRAINING COMPLETED!")
    print("="*70)
    
    return models, ensemble_pred_proba, {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'roc_auc': roc_auc,
        'confusion_matrix': cm,
        'threshold': threshold
    }

if __name__ == "__main__":
    models, predictions, metrics = train_ensemble_models()
