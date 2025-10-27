# 🔍 Supply Chain Fraud Detection using Social Network Analysis# 🔍 Supply Chain Fraud Detection using Social Network Analysis



**Project:** Application of Social Network Analysis (SNA) for fraud detection in supply chains  **Project:** Application of Social Network Analysis (SNA) for fraud detection in supply chains

**Dataset:** DataCo Supply Chain Dataset (Kaggle)  

**Status:** ✅ Complete (All Q1-Q8 answered)**Dataset:** DataCo Supply Chain Dataset (Kaggle)  



> ⚠️ **NOTE:** This repository does NOT contain data files. See [DOWNLOAD_DATA.md](DOWNLOAD_DATA.md) to download the dataset from Kaggle before running the code.

> ⚠️ **NOTE:** This repository does NOT contain data files. See [DOWNLOAD_DATA.md](DOWNLOAD_DATA.md) to download the dataset from Kaggle before running the code.

---

---

## 🚀 Quick Start

## � Hướng dẫn sử dụng

### **1. View Analysis Results**

```powershell### **1. Xem kết quả phân tích**

# Q1-Q2: Dataset & Network Construction```powershell

Get-Content results/RESULTS_Q1_Q2_COMPLETE.txt# Q1-Q2: Dataset và Network Construction

Get-Content results/RESULTS_Q1_Q2_COMPLETE.txt

# Q3: Centrality Measures

Get-Content results/RESULTS_Q3_CENTRALITY.txt# Q3: Centrality Measures

Get-Content results/RESULTS_Q3_CENTRALITY.txt

# Q4-Q8: Communities, Patterns, Visualization, Implications

Get-Content results/RESULTS_Q4_Q5_Q6_Q7_Q8.txt# Q4-Q8: Communities, Patterns, Visualization, Implications

```Get-Content results/RESULTS_Q4_Q5_Q6_Q7_Q8.txt

```

### **2. Visualize in Gephi**

### **2. Visualize network trong Gephi**

**Full network:**

1. Open Gephi → File → Open → Select: `data/network_for_gephi.gexf`#### **Full network (tất cả 20,770 nodes):**

2. Apply layout: ForceAtlas2 (Prevent Overlap ON)```

3. Color: Customer (blue), Product (red), Fraud (yellow/orange)1. Mở Gephi

2. File → Open → Chọn: data/network_for_gephi.gexf

**Fraud rings (4 communities):**3. Import as "Undirected graph"

- `data/subgraphs/community_26.gexf` (fraud_rate=11.5%)4. Apply layout: ForceAtlas2 (with Prevent Overlap ON)

- `data/subgraphs/community_1.gexf` (fraud_rate=10.4%)5. Color nodes:

- `data/subgraphs/community_3.gexf` (fraud_rate=10.2%)   - Customer nodes = blue

- `data/subgraphs/community_7.gexf` (fraud_rate=10.0%)   - Product nodes = red

   - Fraud customers (fraud_count > 0) = yellow/orange

### **3. Re-run Analysis**6. Size nodes by degree (products phổ biến → lớn hơn)

```powershell```

python analyze_dataset.py

python create_edgelist.py#### **Candidate fraud rings (4 communities):**

python build_network.py```

python calculate_network_features.py1. Mở Gephi

```2. File → Open

3. Chọn file:

---   - data/subgraphs/community_26.gexf (fraud_rate=11.5%)

   - data/subgraphs/community_1.gexf (fraud_rate=10.4%)

## 🔄 Workflow   - data/subgraphs/community_3.gexf (fraud_rate=10.2%)

   - data/subgraphs/community_7.gexf (fraud_rate=10.0%)

```4. Import as "Undirected graph"

RAW DATA (180k transactions)5. Visualize để xem fraud patterns trong mỗi community

    ↓ analyze_dataset.py```

EDGE LIST (customer-product pairs)

    ↓ create_edgelist.py### **3. Chạy lại phân tích từ đầu**

NETWORK (20,770 nodes, 101,196 edges)

    ↓ build_network.pyNếu bạn có dataset mới hoặc muốn tái tạo kết quả:

FEATURES (degree, betweenness, closeness)

    ↓ calculate_network_features.py```powershell

ANALYSIS (27 communities, 4 fraud rings)# Bước 1: Phân tích dataset gốc

    ↓python analyze_dataset.py

RESULTS (Q1-Q8 answered)

```# Bước 2: Tạo edge list

python create_edgelist.py

---

# Bước 3: Build bipartite network

## 📂 Directory Structurepython build_network.py



```# Bước 4: Tính network features

fraud_supplychain/python calculate_network_features.py

├── data/```

│   ├── DataCoSupplyChainDataset.csv (95.9 MB)

│   ├── edgelist.csv**Lưu ý:** Files Gephi export (`.gexf`) đã được tạo sẵn trong `data/` và `data/subgraphs/`.

│   ├── bipartite_graph.gpickle

│   ├── network_features.csv---

│   ├── network_for_gephi.gexf

│   └── subgraphs/ (4 fraud ring exports)## �🔄 Workflow

├── results/

│   ├── RESULTS_Q1_Q2_COMPLETE.txt```

│   ├── RESULTS_Q3_CENTRALITY.txt┌─────────────────┐

│   └── RESULTS_Q4_Q5_Q6_Q7_Q8.txt│  1. RAW DATA    │  DataCoSupplyChainDataset.csv (180k transactions)

├── analyze_dataset.py└────────┬────────┘

├── create_edgelist.py         │ analyze_dataset.py

├── build_network.py         ↓

├── calculate_network_features.py┌─────────────────┐

└── README.md│  2. EDGE LIST   │  edgelist.csv (customer-product pairs + fraud labels)

```└────────┬────────┘

         │ create_edgelist.py

---         ↓

┌─────────────────┐

## 🎯 Research Objectives│  3. NETWORK     │  bipartite_graph.gpickle (20,770 nodes, 101,196 edges)

└────────┬────────┘

1. **RQ1:** Can SNA be adapted for supply chain fraud detection?         │ build_network.py

2. **RQ2:** How do network centrality measures compare to traditional features?         ↓

3. **RQ3:** Does combining features improve accuracy?┌─────────────────┐

│  4. FEATURES    │  network_features.csv (degree, betweenness, closeness)

---└────────┬────────┘

         │ calculate_network_features.py

## 📊 Key Findings         ↓

┌─────────────────┐

### **Dataset & Network**│  5. ANALYSIS    │  • Communities detected (27 communities via Louvain)

- 180,519 transactions, 20,652 customers, 118 products│                 │  • Fraud rings identified (4 communities with fraud_rate>10%)

- Fraud rate: 2.25% (Order Status = "SUSPECTED_FRAUD")│                 │  • Gephi exports created

- Bipartite network: sparse (density=0.000469), scale-free└────────┬────────┘

         ↓

### **Centrality Measures**┌─────────────────┐

| Measure | Fraud | Normal | Difference | Rank |│  6. RESULTS     │  RESULTS_Q1_Q2_COMPLETE.txt (Dataset & Network)

|---------|-------|--------|------------|------|│                 │  RESULTS_Q3_CENTRALITY.txt (Centrality Measures)

| **Betweenness** | 0.00000085 | 0.00000047 | **+82%** | 🥇 |│                 │  RESULTS_Q4_Q5_Q6_Q7_Q8.txt (Communities & Patterns)

| **Degree** | 7.40 | 4.71 | **+57%** | 🥈 |└─────────────────┘

| **Closeness** | 0.259 | 0.175 | **+48%** | 🥉 |```



All measures: p-value < 0.001 (highly significant)### **Step-by-step Explanation:**



### **Communities & Fraud Rings****Step 1: Analyze dataset**

- Detected: 27 communities (Louvain algorithm)- Input: `DataCoSupplyChainDataset.csv` (180,519 rows, 53 columns)

- Top 4 fraud rings (fraud_rate > 10%):- Output: Understand data structure, select fraud label (Order Status = "SUSPECTED_FRAUD")

  - Community 26: 1,550 members, 11.5% fraud- Script: `analyze_dataset.py`

  - Community 1: 1,604 members, 10.4% fraud

  - Community 3: 1,659 members, 10.2% fraud**Step 2: Create edge list**

  - Community 7: 1,609 members, 10.0% fraud- Input: Original dataset

- Output: `edgelist.csv` (7 columns: customer_id, product_id, sales, quantity, order_date, order_status, is_fraud)

---- Script: `create_edgelist.py`

- Purpose: Simplify data, keep only necessary information for network

## 📈 Network Features

**Step 3: Build bipartite network**

Each customer has 7 features in `network_features.csv`:- Input: `edgelist.csv`

- Output: `bipartite_graph.gpickle` (NetworkX graph object)

| Feature | Description | Fraud Detection Value |- Script: `build_network.py`

|---------|-------------|----------------------|- Purpose: Create network with 2 types of nodes (customers & products)

| **betweenness_centrality** | Bridge role | ⭐ Strongest (+82%) |

| **degree_centrality** | Activity level | High activity indicator |**Step 4: Calculate network features**

| **closeness_centrality** | Network proximity | Network connectivity |- Input: `bipartite_graph.gpickle`

| **community_id** | Group assignment | Behavior patterns |- Output: `network_features.csv` (20,652 customers × 7 features)

| **degree** | Products purchased | Activity count |- Script: `calculate_network_features.py`

| **is_fraud** | Label (0/1) | Ground truth |- Features: degree, betweenness, closeness, community_id



---**Step 5: Detect fraud patterns**

- Community detection: Louvain algorithm → 27 communities

## 💡 Practical Applications- Fraud ring identification: Communities 26, 1, 3, 7 (fraud_rate 10-11.5%)

- Export for Gephi: `.gexf` files for visualization

**Real-world use:**

- Monitor betweenness & degree in real-time**Step 6: Write results**

- Flag customers with degree > 10 or high betweenness- Q1-Q2: Is the dataset suitable? What is the network structure?

- Investigate communities with fraud_rate > 10%- Q3: Do centrality measures distinguish fraud vs normal?

- Analyze product patterns in fraud rings- Q4-Q8: Communities, fraud patterns, visualization, implications



**Advantages:**

✅ Detect organized fraud (rings)  The Louvain algorithm detected **27 communities** (IDs from 0-26). We selected 4 communities with the **highest fraud rates**:

✅ Capture relational patterns  - Community 26: fraud_rate = **11.5%** (highest)

✅ Identify hubs & anomalies  - Community 1: fraud_rate = **10.4%** (2nd)

✅ Scalable for large networks- Community 3: fraud_rate = **10.2%** (3rd)

- Community 7: fraud_rate = **10.0%** (4th)

**Limitations:**

⚠️ High computational cost (betweenness = O(n³))  → These are the most suspicious "fraud rings" for detailed analysis.

⚠️ Requires quality data (accurate IDs)  

⚠️ No temporal/dynamic analysis yet  ---

⚠️ Possible false positives

## 📂 Directory Structure

---

```

## 📚 Technical Detailsfraud_supplychain/

│

**Network Statistics:**├── data/                          # Data and network files

- Nodes: 20,770 (20,652 customers + 118 products)│   ├── DataCoSupplyChainDataset.csv         # Original dataset from Kaggle (95.9 MB)

- Edges: 101,196 unique pairs│   ├── DescriptionDataCoSupplyChain.csv     # Description of dataset columns

- Components: 19 (largest = 12,431 nodes)│   ├── edgelist.csv                         # Edge list for network (7 main columns)

- Communities: 27 (modularity = 0.1898)│   ├── bipartite_graph.gpickle              # Network object (20,770 nodes, 101,196 edges)

│   ├── graph_info.pkl                       # Metadata summary about network

**Dependencies:**│   ├── network_features.csv                 # Network features for each customer

- pandas, numpy, networkx│   ├── community_stats_nopandas.csv         # Community statistics

- python-louvain (community)│   ├── community_top_products_nopandas.json # Top products per community

- scipy (statistical tests)│   ├── network_for_gephi.gexf               # Network export for Gephi (full)

- Gephi (visualization)│   └── subgraphs/                           # Subgraphs of candidate fraud rings

│       ├── community_26.gexf                # Community 26 (fraud_rate=11.5%)

---│       ├── community_1.gexf                 # Community 1 (fraud_rate=10.4%)

│       ├── community_3.gexf                 # Community 3 (fraud_rate=10.2%)

## 📝 Research Questions Coverage│       └── community_7.gexf                 # Community 7 (fraud_rate=10.0%)

│

All Q1-Q8 answered ✅ (see `results/` folder)├── results/                       # Analysis results (Q1-Q8)

│   ├── RESULTS_Q1_Q2_COMPLETE.txt           # Dataset & Network Construction

---│   ├── RESULTS_Q3_CENTRALITY.txt            # Centrality Measures Analysis

│   └── RESULTS_Q4_Q5_Q6_Q7_Q8.txt           # Communities, Patterns, Viz, Implications

## 🔗 Links│

├── analyze_dataset.py             # Script: analyze dataset, create fraud labels

- **Repository:** https://github.com/ngantran15th10/fraud_supplychain_year4├── create_edgelist.py             # Script: create edge list from dataset

- **Dataset:** https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis├── build_network.py               # Script: build bipartite network

- **Gephi:** https://gephi.org/├── calculate_network_features.py  # Script: calculate network features

├── .gitignore                     # Git ignore file

---│

└── README.md                      # This guide file

**🎓 Academic Project - Year 4 | Social Network Analysis for Fraud Detection**```


---

## 🎯 Project Summary

### **Research Objectives:**
Answer 3 main research questions:
1. **RQ1:** Can SNA code be adapted for supply chain fraud detection?
2. **RQ2:** How do network centrality measures compare to traditional features?
3. **RQ3:** Does combining features improve accuracy?

### **Dataset:**
- **Source:** DataCo Supply Chain (Kaggle)
- **Size:** 180,519 transactions, 20,652 customers, 118 products
- **Fraud definition:** Order Status = "SUSPECTED_FRAUD" (2.25% fraud rate)

### **Network type:**
- **Bipartite network:** Customer nodes (20,652) ↔ Product nodes (118)
- **Total nodes:** 20,770
- **Total edges:** 101,196 (unique customer-product pairs)
- **Structure:** 19 connected components, largest = 12,431 nodes
- **Density:** 0.000469 (sparse network - GOOD for fraud detection)

---

## 📊 Key Findings

### **Q1-Q2: Dataset & Network Construction**
✅ Dataset suitable for building bipartite network  
✅ Network has power-law distribution (scale-free)  
✅ Fraud customers have higher degree (+57%)  
📄 **Details:** `results/RESULTS_Q1_Q2_COMPLETE.txt`

### **Q3: Centrality Measures**
| Measure | Fraud Mean | Normal Mean | % Difference | Ranking |
|---------|-----------|-------------|--------------|---------|
| **Betweenness** | 0.00000085 | 0.00000047 | **+82.16%** | 🥇 #1 |
| **Degree** | 7.40 | 4.71 | **+56.93%** | 🥈 #2 |
| **Closeness** | 0.259 | 0.175 | **+48.43%** | 🥉 #3 |

✅ Tất cả 3 measures có p-value < 0.001 (highly significant)  
✅ Betweenness có discrimination power cao nhất  
📄 **Chi tiết:** `results/RESULTS_Q3_CENTRALITY.txt`

### **Q4-Q8: Communities & Fraud Patterns**
✅ Phát hiện 27 communities (Louvain algorithm)  
✅ Tìm thấy 4 candidate fraud rings với fraud_rate 10-11.5%  
✅ Các fraud communities mua cùng nhóm products (P_365, P_403, P_502)  
📄 **Chi tiết:** `results/RESULTS_Q4_Q5_Q6_Q7_Q8.txt`

**Top Candidate Fraud Rings:**
- **Community 26:** 1,550 members, 179 fraud (11.5% fraud rate)
- **Community 1:** 1,604 members, 167 fraud (10.4% fraud rate)
- **Community 3:** 1,659 members, 170 fraud (10.2% fraud rate)
- **Community 7:** 1,609 members, 161 fraud (10.0% fraud rate)

---

## 📈 Network Features

---

## �🚀 Hướng dẫn sử dụng

### **1. Xem kết quả phân tích**
```powershell
# Q1-Q2: Dataset và Network Construction
Get-Content results/RESULTS_Q1_Q2_COMPLETE.txt

# Q3: Centrality Measures
Get-Content results/RESULTS_Q3_CENTRALITY.txt

# Q4-Q8: Communities, Patterns, Visualization, Implications
Get-Content results/RESULTS_Q4_Q5_Q6_Q7_Q8.txt
```

### **2. Visualize network trong Gephi**

#### **Full network (tất cả 20,770 nodes):**
```
1. Mở Gephi
2. File → Open → Chọn: data/network_for_gephi.gexf
3. Import as "Undirected graph"
4. Apply layout: ForceAtlas2 (with Prevent Overlap ON)
5. Color nodes:
   - Customer nodes = blue
   - Product nodes = red
   - Fraud customers (fraud_count > 0) = yellow/orange
6. Size nodes by degree (products phổ biến → lớn hơn)
```

#### **Candidate fraud rings (4 communities):**
```
1. Mở Gephi
2. File → Open
3. Chọn file:
   - data/subgraphs/community_26.gexf (fraud_rate=11.5%)
   - data/subgraphs/community_1.gexf (fraud_rate=10.4%)
   - data/subgraphs/community_3.gexf (fraud_rate=10.2%)
   - data/subgraphs/community_7.gexf (fraud_rate=10.0%)
4. Import as "Undirected graph"
5. Visualize để xem fraud patterns trong mỗi community
```

### **3. Chạy lại phân tích từ đầu**

Nếu bạn có dataset mới hoặc muốn tái tạo kết quả:

```powershell
# Bước 1: Phân tích dataset gốc
python analyze_dataset.py

# Bước 2: Tạo edge list
python create_edgelist.py

# Bước 3: Build bipartite network
python build_network.py

# Bước 4: Tính network features
python calculate_network_features.py
```

**Lưu ý:** Files Gephi export (`.gexf`) đã được tạo sẵn trong `data/` và `data/subgraphs/`.

---

## 📈 Network Features

Mỗi customer có 7 features trong `data/network_features.csv`:

| Feature | Mô tả | Ý nghĩa fraud detection |
|---------|-------|-------------------------|
| **customer_id** | ID khách hàng | Identifier |
| **degree_centrality** | Normalized degree | Mức độ active (mua nhiều products) |
| **betweenness_centrality** | Vai trò "cầu nối" | ⭐ Strongest indicator (+82%) |
| **closeness_centrality** | "Gần" với network center | Kết nối tốt với toàn network |
| **community_id** | Community assignment | Nhóm behavior pattern |
| **degree** | Số products đã mua | Activity level |
| **is_fraud** | Fraud label (0/1) | Ground truth |

---

## 🎨 Visualization Files

### **Full Network:**
- `data/network_for_gephi.gexf` — Format GEXF cho Gephi (khuyên dùng)

### **Fraud Ring Subgraphs:**
- `data/subgraphs/community_26.gexf` — Community có fraud rate cao nhất (11.5%)
- `data/subgraphs/community_1.gexf` — Community fraud rate 10.4%
- `data/subgraphs/community_3.gexf` — Community fraud rate 10.2%
- `data/subgraphs/community_7.gexf` — Community fraud rate 10.0%

**Tất cả files đều ở format GEXF** - mở trực tiếp trong Gephi (File → Open).

---

## 💡 Practical Implications

### **Ứng dụng thực tế:**
1. **Monitor real-time:** Track betweenness và degree của customers
2. **Flag anomalies:** Customers có degree > 10 hoặc betweenness cao bất thường
3. **Investigate communities:** Communities có fraud_rate > 10%
4. **Product patterns:** Phân tích products được mua bởi fraud rings

### **Advantages vs Traditional Methods:**
- ✅ Phát hiện organized fraud (fraud rings)
- ✅ Capture relational patterns (không chỉ per-transaction features)
- ✅ Identify hubs và anomalies
- ✅ Scalable cho large networks

### **Limitations:**
- ⚠️ Computational cost cao (betweenness = O(n³) cho dense graphs)
- ⚠️ Cần data quality tốt (customer/product IDs chính xác)
- ⚠️ Chưa có temporal/dynamic analysis
- ⚠️ Possible false positives (popular products có fraud count cao)

---

## 📚 Technical Details

### **Network Statistics:**
```
Nodes:          20,770 (20,652 customers + 118 products)
Edges:          101,196 unique customer-product pairs
Components:     19 (largest = 12,431 nodes)
Density:        0.000469 (sparse)
Avg degree:     9.74
Is bipartite:   True
Is connected:   False
Communities:    27 (Louvain, modularity = 0.1898)
```

### **Fraud Statistics:**
```
Total transactions:     180,519
Fraud transactions:     4,062 (2.25%)
Fraud customers:        1,429 (6.92% of customers)
Avg degree (fraud):     7.40
Avg degree (normal):    4.71
```

### **Python Dependencies:**
- pandas
- numpy
- networkx
- python-louvain (community)
- scipy (for statistical tests)

### **Visualization Tools:**
- Gephi (download từ https://gephi.org/)

---

## 📝 Research Questions Coverage

| Question | File | Status |
|----------|------|--------|
| **Q1.1:** Dataset structure? | `results/RESULTS_Q1_Q2_COMPLETE.txt` | ✅ |
| **Q1.2:** Phù hợp build network? | `results/RESULTS_Q1_Q2_COMPLETE.txt` | ✅ |
| **Q1.3:** File hiện có? | `results/RESULTS_Q1_Q2_COMPLETE.txt` | ✅ |
| **Q2.1:** Loại network phù hợp? | `results/RESULTS_Q1_Q2_COMPLETE.txt` | ✅ |
| **Q2.2:** Network đặc điểm? | `results/RESULTS_Q1_Q2_COMPLETE.txt` | ✅ |
| **Q2.3:** Degree distribution? | `results/RESULTS_Q1_Q2_COMPLETE.txt` | ✅ |
| **Q3.1:** Degree centrality? | `results/RESULTS_Q3_CENTRALITY.txt` | ✅ |
| **Q3.2:** Betweenness centrality? | `results/RESULTS_Q3_CENTRALITY.txt` | ✅ |
| **Q3.3:** Closeness centrality? | `results/RESULTS_Q3_CENTRALITY.txt` | ✅ |
| **Q3.4:** So sánh 3 measures? | `results/RESULTS_Q3_CENTRALITY.txt` | ✅ |
| **Q4.1:** Số communities? | `results/RESULTS_Q4_Q5_Q6_Q7_Q8.txt` | ✅ |
| **Q4.2:** Communities ý nghĩa? | `results/RESULTS_Q4_Q5_Q6_Q7_Q8.txt` | ✅ |
| **Q4.3:** Communities khác nhau? | `results/RESULTS_Q4_Q5_Q6_Q7_Q8.txt` | ✅ |
| **Q5.1:** Fraud patterns? | `results/RESULTS_Q4_Q5_Q6_Q7_Q8.txt` | ✅ |
| **Q5.2:** Fraud rings? | `results/RESULTS_Q4_Q5_Q6_Q7_Q8.txt` | ✅ |
| **Q5.3:** Network features giúp? | `results/RESULTS_Q4_Q5_Q6_Q7_Q8.txt` | ✅ |
| **Q6.1:** Network visualization? | `data/subgraphs/` + Gephi files | ✅ |
| **Q6.2:** Degree distribution? | `results/RESULTS_Q3_CENTRALITY.txt` | ✅ |
| **Q7.1:** Practical applications? | `results/RESULTS_Q4_Q5_Q6_Q7_Q8.txt` | ✅ |
| **Q7.2:** Áp dụng thực tế? | `results/RESULTS_Q4_Q5_Q6_Q7_Q8.txt` | ✅ |
| **Q8.1:** Limitations? | `results/RESULTS_Q4_Q5_Q6_Q7_Q8.txt` | ✅ |
| **Q8.2:** Chưa làm được? | `results/RESULTS_Q4_Q5_Q6_Q7_Q8.txt` | ✅ |

---
