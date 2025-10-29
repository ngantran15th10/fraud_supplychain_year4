"""
TÍNH NETWORK FEATURES
Extract các centrality measures và community detection
"""
import pickle
import networkx as nx
import pandas as pd
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')


def calculate_network_features():
    """Tính toán network features cho mỗi customer"""
    
    print("="*80)
    print("TÍNH NETWORK FEATURES")
    print("="*80)
    
    # Load network
    print("\n[1] Load bipartite network...")
    with open('data/bipartite_graph.gpickle', 'rb') as f:
        G = pickle.load(f)
    
    print(f"✓ Đã load network:")
    print(f"  - Nodes: {G.number_of_nodes():,}")
    print(f"  - Edges: {G.number_of_edges():,}")
    
    # Lọc customer nodes
    customer_nodes = [n for n in G.nodes() if n.startswith('C_')]
    print(f"  - Customer nodes: {len(customer_nodes):,}")
    
    # 1. DEGREE CENTRALITY
    print("\n[2] Tính Degree Centrality...")
    print("  (Đo lường số lượng connections của node)")
    
    degree_centrality = nx.degree_centrality(G)
    
    # Chỉ lấy customers
    degree_dict = {node: degree_centrality[node] for node in customer_nodes}
    
    print(f"  ✓ Đã tính degree centrality cho {len(degree_dict):,} customers")
    print(f"  - Min: {min(degree_dict.values()):.6f}")
    print(f"  - Max: {max(degree_dict.values()):.6f}")
    print(f"  - Mean: {sum(degree_dict.values())/len(degree_dict):.6f}")
    
    # 2. BETWEENNESS CENTRALITY
    print("\n[3] Tính Betweenness Centrality...")
    print("  (Đo lường vai trò làm cầu nối giữa các nodes)")
    print("  ⏳ Đây có thể mất vài phút...")
    
    # Sử dụng sampling để tăng tốc
    k = min(5000, G.number_of_nodes())
    betweenness_centrality = nx.betweenness_centrality(G, k=k)
    
    # Chỉ lấy customers
    betweenness_dict = {node: betweenness_centrality[node] for node in customer_nodes}
    
    print(f"  ✓ Đã tính betweenness centrality cho {len(betweenness_dict):,} customers")
    print(f"  - Min: {min(betweenness_dict.values()):.6f}")
    print(f"  - Max: {max(betweenness_dict.values()):.6f}")
    print(f"  - Mean: {sum(betweenness_dict.values())/len(betweenness_dict):.6f}")
    
    # 3. CLOSENESS CENTRALITY
    print("\n[4] Tính Closeness Centrality...")
    print("  (Đo lường khoảng cách trung bình đến các nodes khác)")
    
    # Network không connected, nên tính cho từng component
    # Hoặc dùng closeness cho disconnected graph
    closeness_dict = {}
    
    print("  ⏳ Tính closeness cho từng customer...")
    for node in tqdm(customer_nodes, desc="  Progress"):
        try:
            # Chỉ tính closeness trong component của node
            closeness_dict[node] = nx.closeness_centrality(G, node)
        except:
            closeness_dict[node] = 0.0
    
    print(f"  ✓ Đã tính closeness centrality cho {len(closeness_dict):,} customers")
    print(f"  - Min: {min(closeness_dict.values()):.6f}")
    print(f"  - Max: {max(closeness_dict.values()):.6f}")
    print(f"  - Mean: {sum(closeness_dict.values())/len(closeness_dict):.6f}")
    
    # 4. COMMUNITY DETECTION
    print("\n[5] Detect Communities...")
    print("  (Phát hiện nhóm nodes có kết nối chặt chẽ)")
    
    try:
        import community as community_louvain
        
        # Louvain algorithm cần undirected graph (đã có rồi)
        print("  ⏳ Chạy Louvain algorithm...")
        communities = community_louvain.best_partition(G)
        
        # Chỉ lấy customers
        community_dict = {node: communities[node] for node in customer_nodes}
        
        num_communities = len(set(community_dict.values()))
        modularity = community_louvain.modularity(communities, G)
        
        print(f"  ✓ Đã phát hiện {num_communities} communities")
        print(f"  - Modularity score: {modularity:.4f}")
        
        # Phân bố communities
        from collections import Counter
        comm_counts = Counter(community_dict.values())
        print(f"  - Largest community: {max(comm_counts.values()):,} members")
        print(f"  - Smallest community: {min(comm_counts.values()):,} members")
        
    except ImportError:
        print("  ⚠️ python-louvain not installed")
        print("  Tạo community IDs dựa trên connected components thay thế...")
        
        community_dict = {}
        for i, component in enumerate(nx.connected_components(G)):
            for node in component:
                if node in customer_nodes:
                    community_dict[node] = i
        
        num_communities = len(set(community_dict.values()))
        print(f"  ✓ Đã tạo {num_communities} communities từ connected components")
    
    # Tổng hợp kết quả
    print("\n[6] Tạo DataFrame tổng hợp...")
    
    # Tạo DataFrame
    results = []
    for node in customer_nodes:
        customer_id = node.replace('C_', '')
        
        results.append({
            'customer_id': customer_id,
            'degree_centrality': degree_dict.get(node, 0),
            'betweenness_centrality': betweenness_dict.get(node, 0),
            'closeness_centrality': closeness_dict.get(node, 0),
            'community_id': community_dict.get(node, 0),
            'degree': G.degree(node),  # Actual degree (number of products)
            'is_fraud': G.nodes[node].get('is_fraud', 0)
        })
    
    df_features = pd.DataFrame(results)
    
    print(f"  ✓ Đã tạo DataFrame với {len(df_features):,} rows và {len(df_features.columns)} columns")
    
    # Thống kê
    print("\n[7] Thống kê network features:")
    print(df_features.describe())
    
    # So sánh fraud vs normal
    print("\n[8] So sánh Fraud vs Normal customers:")
    
    fraud_df = df_features[df_features['is_fraud'] == 1]
    normal_df = df_features[df_features['is_fraud'] == 0]
    
    print(f"\n  Fraud customers ({len(fraud_df):,}):")
    print(f"    - Avg degree: {fraud_df['degree'].mean():.2f}")
    print(f"    - Avg degree centrality: {fraud_df['degree_centrality'].mean():.6f}")
    print(f"    - Avg betweenness: {fraud_df['betweenness_centrality'].mean():.6f}")
    print(f"    - Avg closeness: {fraud_df['closeness_centrality'].mean():.6f}")
    
    print(f"\n  Normal customers ({len(normal_df):,}):")
    print(f"    - Avg degree: {normal_df['degree'].mean():.2f}")
    print(f"    - Avg degree centrality: {normal_df['degree_centrality'].mean():.6f}")
    print(f"    - Avg betweenness: {normal_df['betweenness_centrality'].mean():.6f}")
    print(f"    - Avg closeness: {normal_df['closeness_centrality'].mean():.6f}")
    
    # Lưu dictionaries
    print("\n[9] Lưu dictionaries...")
    
    features_dict = {
        'degree_centrality': degree_dict,
        'betweenness_centrality': betweenness_dict,
        'closeness_centrality': closeness_dict,
        'community_id': community_dict
    }
    
    with open('data/network_features_dict.pkl', 'wb') as f:
        pickle.dump(features_dict, f)
    print(f"  ✓ Đã lưu dictionaries vào: data/network_features_dict.pkl")
    
    # Lưu DataFrame
    df_features.to_csv('data/network_features.csv', index=False)
    print(f"  ✓ Đã lưu DataFrame vào: data/network_features.csv")
    
    # Tóm tắt
    print("\n" + "="*80)
    print("TÓM TẮT NETWORK FEATURES")
    print("="*80)
    print(f"✓ Đã tính 4 loại features:")
    print(f"  1. Degree Centrality - Số lượng connections")
    print(f"  2. Betweenness Centrality - Vai trò cầu nối")
    print(f"  3. Closeness Centrality - Khoảng cách đến nodes khác")
    print(f"  4. Community ID - Nhóm cộng đồng")
    print(f"\n✓ Kết quả:")
    print(f"  - {len(df_features):,} customers có features")
    print(f"  - {num_communities} communities được phát hiện")
    print(f"  - Files đã tạo:")
    print(f"    • network_features_dict.pkl (4 dictionaries)")
    print(f"    • network_features.csv (DataFrame)")
    print(f"\n✓ Sẵn sàng để so sánh với traditional features!")
    print("="*80)
    
    return df_features, features_dict


if __name__ == "__main__":
    df_features, features_dict = calculate_network_features()
