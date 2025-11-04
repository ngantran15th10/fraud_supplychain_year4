======================================================================
BEST MODELS - ENSEMBLE CONFIGURATION
Supply Chain Fraud Detection System
======================================================================

OVERVIEW
--------
This folder contains the 3 best-performing models that form the 
production ensemble for fraud detection. These models achieved 
74.83% Recall on the test set, exceeding the industry target of 70%.

MODEL FILES
-----------
1. combined_model_seed42.keras
   - Random seed: 42
   - Architecture: DNN (256->128->64->1)
   - Training: Cost-Sensitive Focal Loss

2. combined_model_seed123.keras
   - Random seed: 123
   - Architecture: DNN (256->128->64->1)
   - Training: Cost-Sensitive Focal Loss

3. combined_model_seed456.keras
   - Random seed: 456
   - Architecture: DNN (256->128->64->1)
   - Training: Cost-Sensitive Focal Loss

ENSEMBLE PREDICTION METHOD
---------------------------
To make predictions using the ensemble:

1. Load all 3 models
2. Preprocess input data:
   - Scale features using StandardScaler
   - Apply PCA (45 components)
3. Get predictions from each model
4. Average the 3 predictions: (pred1 + pred2 + pred3) / 3
5. Apply threshold = 0.20
   - If average_probability > 0.20: Predict FRAUD
   - Otherwise: Predict NOT FRAUD

PERFORMANCE METRICS
-------------------
Ensemble Performance (Test Set):
- Accuracy:  77.73%
- Precision: 20.15%
- Recall:    74.83% (TARGET ACHIEVED)
- F1-Score:  31.75%
- ROC-AUC:   82.16%

Confusion Matrix:
- True Positives (Frauds Caught): 214 / 286 (74.83%)
- False Negatives (Frauds Missed): 72 (25.17%)
- False Positives (False Alerts): 848 / 3845 (22.05%)
- True Negatives (Correct): 2997 (77.95%)

HOW TO USE FOR API/PRODUCTION
------------------------------

Example Python code for loading and using the ensemble:

```python
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Load the 3 models
model1 = keras.models.load_model('best_models/combined_model_seed42.keras')
model2 = keras.models.load_model('best_models/combined_model_seed123.keras')
model3 = keras.models.load_model('best_models/combined_model_seed456.keras')

# Preprocess new data
# Assuming X_new has 61 features (57 transaction + 4 network)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_new)

pca = PCA(n_components=45)
X_pca = pca.fit_transform(X_scaled)

# Get predictions from all 3 models
pred1 = model1.predict(X_pca).flatten()
pred2 = model2.predict(X_pca).flatten()
pred3 = model3.predict(X_pca).flatten()

# Ensemble prediction (average)
ensemble_pred = (pred1 + pred2 + pred3) / 3

# Apply threshold
THRESHOLD = 0.20
final_prediction = (ensemble_pred > THRESHOLD).astype(int)

# Result:
# 0 = Not Fraud
# 1 = Fraud
```

IMPORTANT NOTES FOR API DEPLOYMENT
-----------------------------------
1. You MUST use all 3 models together (ensemble)
   - Do NOT use only 1 model
   - Performance degrades significantly with single model

2. Preprocessing is CRITICAL:
   - Must apply StandardScaler on features
   - Must apply PCA to reduce to 45 components
   - Save and reuse the same scaler and PCA from training

3. Threshold = 0.20 is optimized for maximum Recall
   - Do NOT change this threshold without re-evaluation
   - Lower threshold = more fraud detected but more false alarms
   - Higher threshold = fewer false alarms but miss more frauds

4. Input Features Required (61 total):
   Transaction Features (57):
   - Order details, customer behavior, shipping info, etc.
   
   Network Features (4):
   - degree: Customer's network degree centrality
   - betweenness: Betweenness centrality
   - closeness: Closeness centrality
   - pagerank: PageRank score

5. Expected API Response Time:
   - Each model inference: ~10-50ms
   - Total ensemble prediction: ~30-150ms per order
   - Can batch process for better performance

RECOMMENDED API STRUCTURE
--------------------------
For FastAPI or Flask deployment:

Input:
{
  "order_id": "12345",
  "transaction_features": [...57 values...],
  "network_features": [...4 values...]
}

Output:
{
  "order_id": "12345",
  "prediction": "FRAUD" or "NOT_FRAUD",
  "fraud_probability": 0.XX,
  "confidence_level": "HIGH/MEDIUM/LOW",
  "alert_priority": 1-5
}

MAINTENANCE
-----------
- Model Version: 1.0 (November 2025)
- Last Training Date: November 2025
- Recommended Retraining: Every 3-6 months with new data
- Monitor Recall metric in production (should stay >70%)

For questions or issues, refer to:
- CONSOLIDATED_EVALUATION_RESULTS.txt (performance details)
- main_ensemble.py (training code)
- config.py (configuration settings)

======================================================================
