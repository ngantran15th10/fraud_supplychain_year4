## Main script for Network-based Fraud Detection Model

import config
import data_loader
import model
import train
import predict

from sklearn.model_selection import train_test_split
import os

def main():
    print("="*60)
    print("NETWORK-BASED FRAUD DETECTION MODEL")
    print("="*60)
    
    # 1. Load data
    df = data_loader.load_data(config.DATA_PATH)
    
    # 2. Split features and labels
    X, y = data_loader.split_features_labels(df)
    
    # 3. Split into train and test sets
    X_train, X_test, y_train, y_test = data_loader.split_data(
        X, y, test_size=0.2, random_state=config.RANDOM_STATE
    )
    
    # 4. Scale data
    X_train_scaled, X_test_scaled, scaler = data_loader.scale_data(X_train, X_test)
    
    # 5. Apply SMOTE to training data
    X_train_res, y_train_res = data_loader.apply_smote(
        X_train_scaled, y_train, random_state=config.RANDOM_STATE
    )
    
    # 6. Clean NaN/Inf values
    import numpy as np
    X_train_res = np.nan_to_num(X_train_res, nan=0.0, posinf=0.0, neginf=0.0)
    X_test_scaled = np.nan_to_num(X_test_scaled, nan=0.0, posinf=0.0, neginf=0.0)
    
    # 7. No PCA for network features (only 4 features)
    print(f"\nSkipping PCA - using all {X_train_res.shape[1]} network features")
    X_train_final_data = X_train_res
    X_test_final_data = X_test_scaled
    
    # 7. Split training data into train and validation
    X_train_final, X_val, y_train_final, y_val = train_test_split(
        X_train_final_data, y_train_res,
        test_size=config.VALIDATION_SPLIT,
        random_state=config.RANDOM_STATE
    )
    
    print(f"\nFinal train set: {X_train_final.shape}")
    print(f"Validation set: {X_val.shape}")
    print(f"Test set: {X_test_final_data.shape}")
    
    # 8. Build model
    input_dim = X_train_final_data.shape[1]
    fraud_model = model.build_model(input_dim)
    
    print("\nModel Architecture:")
    fraud_model.summary()
    
    # 9. Train model
    trained_model, history = train.train_model(
        fraud_model, X_train_final, y_train_final, X_val, y_val, config
    )
    
    # 10. Evaluate model on test set
    metrics = predict.evaluate_model(trained_model, X_test_final_data, y_test, config)
    
    print("\n" + "="*60)
    print("NETWORK-BASED MODEL COMPLETED!")
    print("="*60)
    print(f"Model saved: {config.MODEL_SAVE_PATH}")
    print(f"Results saved: {config.RESULTS_PATH}")
    
    return metrics

if __name__ == "__main__":
    main()
