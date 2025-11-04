# Supply Chain Fraud Detection System

Year 4 Research Project

## Project Structure

```
fraud_supplychain/
├── Fraud_SupplyChain/
│   ├── combined_model/          # Main fraud detection models
│   │   ├── config.py            # Configuration settings
│   │   ├── model.py             # Neural network architecture
│   │   ├── data_loader.py       # Data preprocessing
│   │   ├── train.py             # Training logic
│   │   ├── predict.py           # Prediction utilities
│   │   ├── main_ensemble.py     # MAIN: Ensemble training script
│   │   └── results/
│   │       ├── best_models/     # Production models (.keras files)
│   │       └── CONSOLIDATED_EVALUATION_RESULTS.txt
│   └── documentation/           # Comprehensive project documentation
│       ├── README.txt           # Documentation index
│       ├── 01_PROJECT_OVERVIEW.txt
│       ├── 02_MODEL_ARCHITECTURE.txt
│       ├── 03_EXPERIMENTAL_RESULTS.txt
│       └── 04_DEPLOYMENT_GUIDE.txt
├── SNA/                         # Social Network Analysis scripts
└── data/
    └── DataCoSupplyChainDataset.csv
```

## Installation

```bash
pip install tensorflow scikit-learn imbalanced-learn numpy pandas
```

## Training

```bash
cd Fraud_SupplyChain/combined_model
python main_ensemble.py
```

## Using Models for Prediction

```python
import numpy as np
from tensorflow import keras

# Load 3 ensemble models
model1 = keras.models.load_model('results/best_models/combined_model_seed42.keras')
model2 = keras.models.load_model('results/best_models/combined_model_seed123.keras')
model3 = keras.models.load_model('results/best_models/combined_model_seed456.keras')

# Preprocess input (61 features -> StandardScaler -> PCA to 45 components)
# X_preprocessed = your preprocessing pipeline

# Ensemble prediction
pred1 = model1.predict(X_preprocessed)
pred2 = model2.predict(X_preprocessed)
pred3 = model3.predict(X_preprocessed)
ensemble_pred = (pred1 + pred2 + pred3) / 3

# Apply threshold
THRESHOLD = 0.20
is_fraud = (ensemble_pred > THRESHOLD).astype(int)
```

## Documentation

**For detailed information**, see `Fraud_SupplyChain/documentation/`:
- `README.txt` - Documentation index
- `01_PROJECT_OVERVIEW.txt` - Project description and methodology
- `02_MODEL_ARCHITECTURE.txt` - Technical specifications
- `03_EXPERIMENTAL_RESULTS.txt` - Performance analysis
- `04_DEPLOYMENT_GUIDE.txt` - Production deployment guide

**For consolidated results**, see:
- `Fraud_SupplyChain/combined_model/results/CONSOLIDATED_EVALUATION_RESULTS.txt`

**For production models**, see:
- `Fraud_SupplyChain/combined_model/results/best_models/`

## Contact

Year 4 Research Project - November 2025

