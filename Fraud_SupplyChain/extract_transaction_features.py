"""
Extract Transaction-based Features from DataCo Supply Chain Dataset
Aggregates features per customer for fraud detection
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import os

def load_dataset(file_path):
    """Load the main dataset"""
    print(f"Loading dataset from {file_path}...")
    df = pd.read_csv(file_path, encoding='latin1')
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

def select_features(df):
    """Select relevant features for fraud detection"""
    
    # Define feature columns
    feature_columns = [
        # Fraud indicators
        'Late_delivery_risk',
        'Benefit per order',
        'Order Profit Per Order',
        'Order Item Profit Ratio',
        
        # Transaction values
        'Sales',
        'Order Item Total',
        'Order Item Quantity',
        'Order Item Discount',
        'Order Item Discount Rate',
        
        # Time features
        'order month',
        'order day',
        'Days for shipping (real)',
        
        # Payment & Delivery
        'Type',
        'Delivery Status',
        'Shipping Mode',
        
        # Customer info
        'Customer Segment',
        'Market',
        
        # Product info
        'Category Name',
        'Department Name',
        
        # Target
        'Order Status',
        
        # Customer ID for grouping
        'Customer Id'
    ]
    
    # Check which columns exist
    missing_cols = [col for col in feature_columns if col not in df.columns]
    if missing_cols:
        print(f"Warning: Missing columns: {missing_cols}")
        feature_columns = [col for col in feature_columns if col in df.columns]
    
    df_selected = df[feature_columns].copy()
    print(f"Selected {len(feature_columns)} columns")
    
    return df_selected

def encode_categorical(df):
    """Encode categorical variables"""
    print("\nEncoding categorical variables...")
    
    categorical_cols = [
        'Type', 'Delivery Status', 'Shipping Mode',
        'Customer Segment', 'Market', 
        'Category Name', 'Department Name'
    ]
    
    # Label encoding for each categorical column
    le_dict = {}
    for col in categorical_cols:
        if col in df.columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            le_dict[col] = le
            print(f"  - {col}: {len(le.classes_)} classes")
    
    return df, le_dict

def create_fraud_label(df):
    """Create binary fraud label from Order Status"""
    print("\nCreating fraud label...")
    
    # SUSPECTED_FRAUD = 1, others = 0
    df['is_fraud'] = (df['Order Status'] == 'SUSPECTED_FRAUD').astype(int)
    
    fraud_count = df['is_fraud'].sum()
    total_count = len(df)
    fraud_rate = fraud_count / total_count * 100
    
    print(f"  Fraud transactions: {fraud_count} ({fraud_rate:.2f}%)")
    print(f"  Normal transactions: {total_count - fraud_count} ({100-fraud_rate:.2f}%)")
    
    return df

def aggregate_by_customer(df):
    """Aggregate features by Customer Id"""
    print("\nAggregating features by customer...")
    
    # Numerical features to aggregate
    numerical_features = [
        'Late_delivery_risk',
        'Benefit per order',
        'Order Profit Per Order',
        'Order Item Profit Ratio',
        'Sales',
        'Order Item Total',
        'Order Item Quantity',
        'Order Item Discount',
        'Order Item Discount Rate',
        'order month',
        'order day',
        'Days for shipping (real)',
    ]
    
    # Categorical features (already encoded) - take mode
    categorical_features = [
        'Type', 'Delivery Status', 'Shipping Mode',
        'Customer Segment', 'Market',
        'Category Name', 'Department Name'
    ]
    
    # Aggregation dictionary
    agg_dict = {}
    
    # Numerical: mean, sum, std, min, max
    for col in numerical_features:
        if col in df.columns:
            agg_dict[col] = ['mean', 'sum', 'std', 'min', 'max']
    
    # Categorical: mode (most frequent)
    for col in categorical_features:
        if col in df.columns:
            agg_dict[col] = lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0]
    
    # Fraud label: max (if any transaction is fraud, customer is fraud)
    agg_dict['is_fraud'] = 'max'
    
    # Group by customer
    df_agg = df.groupby('Customer Id').agg(agg_dict)
    
    # Flatten column names
    df_agg.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col 
                      for col in df_agg.columns.values]
    
    # Rename is_fraud column
    df_agg.rename(columns={'is_fraud_max': 'is_fraud'}, inplace=True)
    
    # Reset index to make Customer Id a column
    df_agg.reset_index(inplace=True)
    
    print(f"  Aggregated to {len(df_agg)} unique customers")
    print(f"  Total features: {df_agg.shape[1] - 2} (excluding Customer Id and is_fraud)")
    
    return df_agg

def main():
    """Main execution"""
    # Paths - adjust based on current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(current_dir, '..', 'data', 'DataCoSupplyChainDataset.csv')
    output_path = os.path.join(current_dir, 'data', 'transaction_features.csv')
    
    # Check if dataset exists
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset not found at {dataset_path}")
        print("Please ensure DataCoSupplyChainDataset.csv is in the data/ folder")
        return
    
    # Step 1: Load dataset
    df = load_dataset(dataset_path)
    
    # Step 2: Select features
    df = select_features(df)
    
    # Step 3: Create fraud label
    df = create_fraud_label(df)
    
    # Step 4: Encode categorical variables
    df, le_dict = encode_categorical(df)
    
    # Step 5: Aggregate by customer
    df_customer = aggregate_by_customer(df)
    
    # Step 6: Save to CSV
    print(f"\nSaving transaction features to {output_path}...")
    df_customer.to_csv(output_path, index=False)
    print(f"Saved {len(df_customer)} customers with {df_customer.shape[1]} columns")
    
    # Show sample
    print("\nSample of transaction features:")
    print(df_customer.head())
    
    # Show fraud distribution
    fraud_customers = df_customer['is_fraud'].sum()
    total_customers = len(df_customer)
    print(f"\nFraud distribution:")
    print(f"  Fraud customers: {fraud_customers} ({fraud_customers/total_customers*100:.2f}%)")
    print(f"  Normal customers: {total_customers - fraud_customers} ({(total_customers-fraud_customers)/total_customers*100:.2f}%)")
    
    print("\n✅ Transaction features extraction complete!")

if __name__ == '__main__':
    main()
