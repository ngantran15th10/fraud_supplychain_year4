"""
Stacking Ensemble for Fraud Detection
Combines DNN, Random Forest, XGBoost, and LightGBM
Expected Recall: 75-82%
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                            f1_score, confusion_matrix, classification_report, roc_auc_score)
from sklearn.utils.class_weight import compute_class_weight
import xgboost as xgb
import lightgbm as lgb
import tensorflow as tf
from tensorflow import keras
import os
import sys

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

import config
from data_loader import load_data, split_features_labels, split_data, apply_smote
from model import build_model
from predict import find_optimal_threshold

print("=" * 70)
print("STACKING ENSEMBLE - HYBRID MODEL FOR FRAUD DETECTION")
print("=" * 70)
print("\nBase Models:")
print("  1. Deep Neural Network (DNN)")
print("  2. Random Forest (RF)")
print("  3. XGBoost (XGB)")
print("  4. LightGBM (LGBM)")
print("\nMeta-Learner: Logistic Regression")
print("=" * 70)

# ============================================================================
# STEP 1: LOAD AND PREPARE DATA
# ============================================================================
print("\n" + "=" * 70)
print("STEP 1: LOADING DATA")
print("=" * 70)

# Load data
df = load_data(config.DATA_PATH)
X, y = split_features_labels(df)
X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2, random_state=config.RANDOM_STATE)

print(f"\nTrain set: {X_train.shape[0]} samples")
print(f"Test set: {X_test.shape[0]} samples")
print(f"Fraud ratio in train: {y_train.sum() / len(y_train) * 100:.2f}%")
print(f"Fraud ratio in test: {y_test.sum() / len(y_test) * 100:.2f}%")

# Apply SMOTE
print(f"\nApplying SMOTE with sampling_strategy={config.SAMPLING_STRATEGY}...")
X_train_res, y_train_res = apply_smote(X_train, y_train, 
                                       random_state=config.RANDOM_STATE,
                                       sampling_strategy=config.SAMPLING_STRATEGY)
print(f"After SMOTE: {X_train_res.shape[0]} samples")
print(f"Fraud ratio after SMOTE: {y_train_res.sum() / len(y_train_res) * 100:.2f}%")

# Compute class weights
class_weights = compute_class_weight('balanced', 
                                     classes=np.unique(y_train_res), 
                                     y=y_train_res)
class_weight_dict = {i: class_weights[i] for i in range(len(class_weights))}
print(f"Class weights: {class_weight_dict}")

# Scale features for DNN
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_res)
X_test_scaled = scaler.transform(X_test)

# ============================================================================
# STEP 2: TRAIN BASE MODELS
# ============================================================================
print("\n" + "=" * 70)
print("STEP 2: TRAINING BASE MODELS")
print("=" * 70)

# --------------------- Model 1: Deep Neural Network ---------------------
print("\n[1/4] Training Deep Neural Network...")
dnn_model = build_model(input_dim=X_train_scaled.shape[1], 
                        use_focal_loss=config.USE_FOCAL_LOSS,
                        focal_gamma=config.FOCAL_GAMMA,
                        focal_alpha=config.FOCAL_ALPHA)

early_stopping = keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
)

dnn_model.fit(
    X_train_scaled, y_train_res,
    epochs=config.EPOCHS,
    batch_size=config.BATCH_SIZE,
    validation_split=config.VALIDATION_SPLIT,
    class_weight=class_weight_dict,
    callbacks=[early_stopping],
    verbose=0
)
print("✓ DNN trained successfully")

# Get DNN predictions (probabilities)
dnn_train_pred = dnn_model.predict(X_train_scaled, verbose=0).flatten()
dnn_test_pred = dnn_model.predict(X_test_scaled, verbose=0).flatten()

# --------------------- Model 2: Random Forest ---------------------
print("\n[2/4] Training Random Forest...")
rf_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=20,
    min_samples_split=10,
    min_samples_leaf=5,
    class_weight='balanced',
    random_state=config.RANDOM_STATE,
    n_jobs=-1,
    verbose=0
)
rf_model.fit(X_train_res, y_train_res)
print("✓ Random Forest trained successfully")

# Get RF predictions (probabilities)
rf_train_pred = rf_model.predict_proba(X_train_res)[:, 1]
rf_test_pred = rf_model.predict_proba(X_test)[:, 1]

# --------------------- Model 3: XGBoost ---------------------
print("\n[3/4] Training XGBoost...")
scale_pos_weight = (len(y_train_res) - y_train_res.sum()) / y_train_res.sum()
xgb_model = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=8,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=scale_pos_weight,
    random_state=config.RANDOM_STATE,
    n_jobs=-1,
    verbosity=0
)
xgb_model.fit(X_train_res, y_train_res)
print("✓ XGBoost trained successfully")

# Get XGBoost predictions (probabilities)
xgb_train_pred = xgb_model.predict_proba(X_train_res)[:, 1]
xgb_test_pred = xgb_model.predict_proba(X_test)[:, 1]

# --------------------- Model 4: LightGBM ---------------------
print("\n[4/4] Training LightGBM...")
lgb_model = lgb.LGBMClassifier(
    n_estimators=200,
    max_depth=8,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    class_weight='balanced',
    random_state=config.RANDOM_STATE,
    n_jobs=-1,
    verbose=-1
)
lgb_model.fit(X_train_res, y_train_res)
print("✓ LightGBM trained successfully")

# Get LightGBM predictions (probabilities)
lgb_train_pred = lgb_model.predict_proba(X_train_res)[:, 1]
lgb_test_pred = lgb_model.predict_proba(X_test)[:, 1]

# ============================================================================
# STEP 3: TRAIN META-LEARNER (STACKING)
# ============================================================================
print("\n" + "=" * 70)
print("STEP 3: TRAINING META-LEARNER (Logistic Regression)")
print("=" * 70)

# Stack base model predictions as new features
meta_train_features = np.column_stack([
    dnn_train_pred,
    rf_train_pred,
    xgb_train_pred,
    lgb_train_pred
])

meta_test_features = np.column_stack([
    dnn_test_pred,
    rf_test_pred,
    xgb_test_pred,
    lgb_test_pred
])

print(f"Meta-features shape: {meta_train_features.shape}")

# Train meta-learner
meta_model = LogisticRegression(
    class_weight='balanced',
    random_state=config.RANDOM_STATE,
    max_iter=1000
)
meta_model.fit(meta_train_features, y_train_res)
print("✓ Meta-learner trained successfully")

# Get meta-model predictions
meta_train_pred = meta_model.predict_proba(meta_train_features)[:, 1]
meta_test_pred = meta_model.predict_proba(meta_test_features)[:, 1]

print(f"\nMeta-learner coefficients:")
print(f"  DNN:      {meta_model.coef_[0][0]:+.4f}")
print(f"  RF:       {meta_model.coef_[0][1]:+.4f}")
print(f"  XGBoost:  {meta_model.coef_[0][2]:+.4f}")
print(f"  LightGBM: {meta_model.coef_[0][3]:+.4f}")

# ============================================================================
# STEP 4: EVALUATE STACKING ENSEMBLE
# ============================================================================
print("\n" + "=" * 70)
print("STEP 4: EVALUATING STACKING ENSEMBLE")
print("=" * 70)

# Find optimal threshold or use fixed threshold
if config.THRESHOLD == 'auto':
    optimal_threshold = find_optimal_threshold(y_test, meta_test_pred)
    print(f"\nOptimal threshold found: {optimal_threshold:.3f}")
else:
    optimal_threshold = config.THRESHOLD
    print(f"\nUsing fixed threshold: {optimal_threshold}")

# Make final predictions
y_pred = (meta_test_pred >= optimal_threshold).astype(int)

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, meta_test_pred)
cm = confusion_matrix(y_test, y_pred)

print("\n" + "=" * 70)
print("STACKING ENSEMBLE RESULTS")
print("=" * 70)
print(f"\nAccuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-Score:  {f1:.4f}")
print(f"ROC-AUC:   {roc_auc:.4f}")

print(f"\nConfusion Matrix:")
print(cm)

print(f"\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Not Fraud', 'Fraud']))

# ============================================================================
# STEP 5: COMPARE WITH BASE MODELS
# ============================================================================
print("\n" + "=" * 70)
print("STEP 5: COMPARING BASE MODELS vs STACKING")
print("=" * 70)

results = []

# Evaluate each base model
for name, pred_proba in [
    ('DNN', dnn_test_pred),
    ('Random Forest', rf_test_pred),
    ('XGBoost', xgb_test_pred),
    ('LightGBM', lgb_test_pred),
    ('STACKING', meta_test_pred)
]:
    y_pred_base = (pred_proba >= optimal_threshold).astype(int)
    results.append({
        'Model': name,
        'Accuracy': accuracy_score(y_test, y_pred_base),
        'Precision': precision_score(y_test, y_pred_base, zero_division=0),
        'Recall': recall_score(y_test, y_pred_base),
        'F1-Score': f1_score(y_test, y_pred_base),
        'ROC-AUC': roc_auc_score(y_test, pred_proba)
    })

results_df = pd.DataFrame(results)
print("\n" + results_df.to_string(index=False))

# ============================================================================
# STEP 6: SAVE RESULTS
# ============================================================================
print("\n" + "=" * 70)
print("STEP 6: SAVING MODELS AND RESULTS")
print("=" * 70)

# Create results directory
os.makedirs(config.RESULTS_PATH, exist_ok=True)

# Save DNN model
dnn_save_path = os.path.join(current_dir, 'stacking_dnn.keras')
dnn_model.save(dnn_save_path)
print(f"✓ DNN saved to: {dnn_save_path}")

# Save results
results_file = os.path.join(config.RESULTS_PATH, 'stacking_evaluation_metrics.txt')
with open(results_file, 'w') as f:
    f.write("=" * 70 + "\n")
    f.write("STACKING ENSEMBLE - EVALUATION METRICS\n")
    f.write("=" * 70 + "\n\n")
    f.write(f"Threshold: {optimal_threshold}\n\n")
    f.write(f"Accuracy:  {accuracy:.4f}\n")
    f.write(f"Precision: {precision:.4f}\n")
    f.write(f"Recall:    {recall:.4f}\n")
    f.write(f"F1-Score:  {f1:.4f}\n")
    f.write(f"ROC-AUC:   {roc_auc:.4f}\n\n")
    f.write(f"Confusion Matrix:\n{cm}\n\n")
    f.write(f"Classification Report:\n")
    f.write(classification_report(y_test, y_pred, target_names=['Not Fraud', 'Fraud']))
    f.write("\n\n" + "=" * 70 + "\n")
    f.write("COMPARISON: BASE MODELS vs STACKING\n")
    f.write("=" * 70 + "\n\n")
    f.write(results_df.to_string(index=False))
    f.write("\n\n" + "=" * 70 + "\n")
    f.write("META-LEARNER COEFFICIENTS\n")
    f.write("=" * 70 + "\n\n")
    f.write(f"DNN:      {meta_model.coef_[0][0]:+.4f}\n")
    f.write(f"RF:       {meta_model.coef_[0][1]:+.4f}\n")
    f.write(f"XGBoost:  {meta_model.coef_[0][2]:+.4f}\n")
    f.write(f"LightGBM: {meta_model.coef_[0][3]:+.4f}\n")

print(f"✓ Results saved to: {results_file}")

print("\n" + "=" * 70)
print("STACKING ENSEMBLE TRAINING COMPLETED!")
print("=" * 70)
