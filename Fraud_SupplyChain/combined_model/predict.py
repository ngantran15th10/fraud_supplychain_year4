## Model Evaluation and Prediction for Combined Model

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)
import matplotlib.pyplot as plt
import seaborn as sns
import os

def evaluate_model(model, X_test, y_test, config):
    """
    Evaluate the trained model on test set
    
    Args:
        model: Trained Keras model
        X_test: Test features
        y_test: Test labels
        config: Configuration module
    
    Returns:
        Dictionary of evaluation metrics
    """
    print("\n" + "="*60)
    print("Evaluating Combined Model...")
    print("="*60)
    
    # Predictions
    y_pred_proba = model.predict(X_test, verbose=0)
    y_pred = (y_pred_proba > 0.5).astype(int).flatten()
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    
    # Print results
    print(f"\nAccuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print(f"ROC-AUC:   {roc_auc:.4f}")
    
    print("\nConfusion Matrix:")
    print(cm)
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Not Fraud', 'Fraud']))
    
    # Save metrics to file
    os.makedirs(config.RESULTS_PATH, exist_ok=True)
    metrics_file = os.path.join(config.RESULTS_PATH, 'evaluation_metrics.txt')
    
    with open(metrics_file, 'w') as f:
        f.write("="*60 + "\n")
        f.write("COMBINED MODEL EVALUATION RESULTS\n")
        f.write("(Transaction + Network Features)\n")
        f.write("="*60 + "\n\n")
        f.write(f"Accuracy:  {accuracy:.4f}\n")
        f.write(f"Precision: {precision:.4f}\n")
        f.write(f"Recall:    {recall:.4f}\n")
        f.write(f"F1-Score:  {f1:.4f}\n")
        f.write(f"ROC-AUC:   {roc_auc:.4f}\n\n")
        f.write("Confusion Matrix:\n")
        f.write(str(cm) + "\n\n")
        f.write("Classification Report:\n")
        f.write(classification_report(y_test, y_pred, target_names=['Not Fraud', 'Fraud']))
    
    print(f"\nMetrics saved to: {metrics_file}")
    
    # Plot confusion matrix
    plot_confusion_matrix(cm, config)
    
    # Return metrics dictionary
    metrics = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'roc_auc': roc_auc,
        'confusion_matrix': cm
    }
    
    return metrics

def plot_confusion_matrix(cm, config):
    """Plot and save confusion matrix"""
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Oranges', cbar=False)
    plt.title('Confusion Matrix - Combined Model')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.tight_layout()
    
    cm_file = os.path.join(config.RESULTS_PATH, 'confusion_matrix.png')
    plt.savefig(cm_file, dpi=300, bbox_inches='tight')
    print(f"Confusion matrix plot saved to: {cm_file}")
    plt.close()
