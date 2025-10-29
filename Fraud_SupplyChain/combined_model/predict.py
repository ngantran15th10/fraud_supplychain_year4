## Model Evaluation and Prediction for Combined Model

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    roc_curve, precision_recall_curve
)
import matplotlib.pyplot as plt
import seaborn as sns
import os

def find_optimal_threshold_with_constraint(y_true, y_pred_proba, min_recall=0.60):
    """
    Find optimal threshold that maintains minimum Recall while maximizing Precision/F1
    
    Args:
        y_true: True labels
        y_pred_proba: Predicted probabilities
        min_recall: Minimum acceptable recall (default 0.60 = 60%)
    
    Returns:
        Optimal threshold value, metrics at that threshold
    """
    thresholds = np.arange(0.05, 0.95, 0.01)
    best_f1 = 0
    optimal_threshold = 0.3
    best_metrics = {}
    
    results = []
    
    for thresh in thresholds:
        y_pred = (y_pred_proba >= thresh).astype(int)
        
        recall = recall_score(y_true, y_pred, zero_division=0)
        precision = precision_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        
        # Only consider thresholds that meet minimum recall constraint
        if recall >= min_recall:
            results.append({
                'threshold': thresh,
                'recall': recall,
                'precision': precision,
                'f1': f1
            })
            
            # Update best if F1 is higher
            if f1 > best_f1:
                best_f1 = f1
                optimal_threshold = thresh
                best_metrics = {
                    'threshold': thresh,
                    'recall': recall,
                    'precision': precision,
                    'f1': f1
                }
    
    if not results:
        # If no threshold meets min_recall, find threshold with highest recall
        print(f"WARNING: No threshold achieves Recall >= {min_recall:.1%}")
        print("Finding threshold with maximum Recall instead...")
        
        for thresh in thresholds:
            y_pred = (y_pred_proba >= thresh).astype(int)
            recall = recall_score(y_true, y_pred, zero_division=0)
            precision = precision_score(y_true, y_pred, zero_division=0)
            f1 = f1_score(y_true, y_pred, zero_division=0)
            
            results.append({
                'threshold': thresh,
                'recall': recall,
                'precision': precision,
                'f1': f1
            })
        
        # Sort by F1-score descending
        results.sort(key=lambda x: x['f1'], reverse=True)
        best_metrics = results[0]
        optimal_threshold = best_metrics['threshold']
    
    return optimal_threshold, best_metrics

def find_optimal_threshold(y_true, y_pred_proba, metric='f1'):
    """
    Find optimal threshold based on F1-score or other metrics
    
    Args:
        y_true: True labels
        y_pred_proba: Predicted probabilities
        metric: 'f1', 'precision', 'recall', or 'balanced'
    
    Returns:
        Optimal threshold value
    """
    if metric == 'balanced':
        # Find threshold that balances precision and recall
        precision, recall, thresholds = precision_recall_curve(y_true, y_pred_proba)
        f1_scores = 2 * (precision * recall) / (precision + recall + 1e-10)
        optimal_idx = np.argmax(f1_scores)
        optimal_threshold = thresholds[optimal_idx] if optimal_idx < len(thresholds) else 0.5
    else:
        # Try different thresholds and find best F1
        thresholds = np.arange(0.1, 0.9, 0.05)
        best_score = 0
        optimal_threshold = 0.3
        
        for thresh in thresholds:
            y_pred = (y_pred_proba > thresh).astype(int)
            
            if metric == 'f1':
                score = f1_score(y_true, y_pred, zero_division=0)
            elif metric == 'precision':
                score = precision_score(y_true, y_pred, zero_division=0)
            elif metric == 'recall':
                score = recall_score(y_true, y_pred, zero_division=0)
            
            if score > best_score:
                best_score = score
                optimal_threshold = thresh
    
    return optimal_threshold

def evaluate_model(model, X_test, y_test, config, threshold='auto'):
    """
    Evaluate the trained model on test set
    
    Args:
        model: Trained Keras model
        X_test: Test features
        y_test: Test labels
        config: Configuration module
        threshold: 'auto' to find optimal, or float value
    
    Returns:
        Dictionary of evaluation metrics
    """
    print("\n" + "="*60)
    print("Evaluating Combined Model...")
    print("="*60)
    
    # Get predictions
    y_pred_proba = model.predict(X_test, verbose=0).flatten()
    
    # Find optimal threshold if auto
    if threshold == 'auto':
        threshold = find_optimal_threshold(y_test, y_pred_proba, metric='balanced')
        print(f"\nOptimal threshold found: {threshold:.3f}")
    else:
        print(f"\nUsing threshold: {threshold}")
    
    y_pred = (y_pred_proba > threshold).astype(int)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
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
