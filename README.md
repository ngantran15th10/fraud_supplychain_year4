# 🔍 Supply Chain Fraud Detection using Social Network Analysis

**Dự án phân tích:** Ứng dụng Social Network Analysis (SNA) để phát hiện gian lận trong supply chain

**Dataset:** DataCo Supply Chain Dataset (Kaggle)  
**Status:** ✅ Hoàn thành (All Q1-Q8 answered)

---

## � Hướng dẫn sử dụng

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

**Full network:**
- Mở Gephi → File → Open → `data/network_for_gephi.gexf`
- Apply layout: ForceAtlas2 (Prevent Overlap ON)
- Color: Customer (blue), Product (red), Fraud (yellow/orange)

**Fraud rings (4 communities):**
- `data/subgraphs/community_26.gexf` (fraud_rate=11.5%)
- `data/subgraphs/community_1.gexf` (fraud_rate=10.4%)
- `data/subgraphs/community_3.gexf` (fraud_rate=10.2%)
- `data/subgraphs/community_7.gexf` (fraud_rate=10.0%)

### **3. Chạy lại phân tích**
```powershell
python analyze_dataset.py
python create_edgelist.py
python build_network.py
python calculate_network_features.py
```

---

## �🔄 Quy trình làm việc (Workflow)

```
┌─────────────────┐
│  1. RAW DATA    │  DataCoSupplyChainDataset.csv (180k transactions)
└────────┬────────┘
         │ analyze_dataset.py
         ↓
┌─────────────────┐
│  2. EDGE LIST   │  edgelist.csv (customer-product pairs + fraud labels)
└────────┬────────┘
         │ create_edgelist.py
         ↓
┌─────────────────┐
│  3. NETWORK     │  bipartite_graph.gpickle (20,770 nodes, 101,196 edges)
└────────┬────────┘
         │ build_network.py
         ↓
┌─────────────────┐
│  4. FEATURES    │  network_features.csv (degree, betweenness, closeness)
└────────┬────────┘
         │ calculate_network_features.py
         ↓
┌─────────────────┐
│  5. ANALYSIS    │  • Communities detected (27 communities via Louvain)
│                 │  • Fraud rings identified (4 communities với fraud_rate>10%)
│                 │  • Gephi exports created
└────────┬────────┘
         ↓
┌─────────────────┐
│  6. RESULTS     │  RESULTS_Q1_Q2_COMPLETE.txt (Dataset & Network)
│                 │  RESULTS_Q3_CENTRALITY.txt (Centrality Measures)
│                 │  RESULTS_Q4_Q5_Q6_Q7_Q8.txt (Communities & Patterns)
└─────────────────┘
```

**Community IDs:** Louvain phát hiện 27 communities (ID 0-26). Top 4 fraud rings: Communities 26, 1, 3, 7 (fraud_rate 10-11.5%)

---

## 📂 Cấu trúc thư mục

```
fraud_supplychain/
│
├── data/                          # Dữ liệu và network files
│   ├── DataCoSupplyChainDataset.csv         # Dataset gốc từ Kaggle (95.9 MB)
│   ├── DescriptionDataCoSupplyChain.csv     # Mô tả các cột trong dataset
│   ├── edgelist.csv                         # Edge list cho network (7 cột chính)
│   ├── bipartite_graph.gpickle              # Network object (20,770 nodes, 101,196 edges)
│   ├── graph_info.pkl                       # Metadata tóm tắt về network
│   ├── network_features.csv                 # Network features cho mỗi customer
│   ├── community_stats_nopandas.csv         # Thống kê các communities
│   ├── community_top_products_nopandas.json # Top products mỗi community
│   ├── network_for_gephi.gexf               # Network export cho Gephi (full)
│   └── subgraphs/                           # Subgraphs của candidate fraud rings
│       ├── community_26.gexf                # Community 26 (fraud_rate=11.5%)
│       ├── community_1.gexf                 # Community 1 (fraud_rate=10.4%)
│       ├── community_3.gexf                 # Community 3 (fraud_rate=10.2%)
│       └── community_7.gexf                 # Community 7 (fraud_rate=10.0%)
│
├── results/                       # Kết quả phân tích (Q1-Q8)
│   ├── RESULTS_Q1_Q2_COMPLETE.txt           # Dataset & Network Construction
│   ├── RESULTS_Q3_CENTRALITY.txt            # Centrality Measures Analysis
│   └── RESULTS_Q4_Q5_Q6_Q7_Q8.txt           # Communities, Patterns, Viz, Implications
│
├── analyze_dataset.py             # Script: phân tích dataset, tạo fraud labels
├── create_edgelist.py             # Script: tạo edge list từ dataset
├── build_network.py               # Script: xây dựng bipartite network
├── calculate_network_features.py  # Script: tính network features
├── .gitignore                     # Git ignore file
│
└── README.md                      # File hướng dẫn này
```

---

## 🎯 Tóm tắt dự án

### **Mục tiêu nghiên cứu:**
Trả lời 3 câu hỏi chính (Research Questions):
1. **RQ1:** Có thể adapt SNA code cho supply chain fraud detection không?
2. **RQ2:** Network centrality measures so với traditional features như thế nào?
3. **RQ3:** Kết hợp features có cải thiện accuracy không?

### **Dataset:**
- **Nguồn:** DataCo Supply Chain (Kaggle)
- **Kích thước:** 180,519 transactions, 20,652 customers, 118 products
- **Fraud definition:** Order Status = "SUSPECTED_FRAUD" (2.25% fraud rate)

### **Network type:**
- **Bipartite network:** Customer nodes (20,652) ↔ Product nodes (118)
- **Total nodes:** 20,770
- **Total edges:** 101,196 (unique customer-product pairs)
- **Structure:** 19 connected components, largest = 12,431 nodes
- **Density:** 0.000469 (sparse network - TỐT cho fraud detection)

---

## 📊 Kết quả chính (Key Findings)

### **Q1-Q2: Dataset & Network Construction**
✅ Dataset phù hợp để build bipartite network  
✅ Network có power-law distribution (scale-free)  
✅ Fraud customers có degree cao hơn (+57%)  
📄 **Chi tiết:** `results/RESULTS_Q1_Q2_COMPLETE.txt`

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

##  Network Features

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

**Full Network:** `data/network_for_gephi.gexf`  
**Fraud Rings:** `data/subgraphs/community_{26,1,3,7}.gexf`

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

**🎓 Academic Project - Year 4 | Social Network Analysis for Fraud Detection**
