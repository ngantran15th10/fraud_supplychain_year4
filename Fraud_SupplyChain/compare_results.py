## Compare results from 3 fraud detection models

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_results():
    """Load evaluation metrics from all 3 models"""
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    results = {}
    
    # Model 1: Transaction-based
    trans_file = os.path.join(current_dir, 'transaction_model', 'results', 'evaluation_metrics.txt')
    if os.path.exists(trans_file):
        results['Transaction'] = parse_metrics_file(trans_file)
    
    # Model 2: Network-based
    net_file = os.path.join(current_dir, 'network_model', 'results', 'evaluation_metrics.txt')
    if os.path.exists(net_file):
        results['Network'] = parse_metrics_file(net_file)
    
    # Model 3: Combined
    comb_file = os.path.join(current_dir, 'combined_model', 'results', 'evaluation_metrics.txt')
    if os.path.exists(comb_file):
        results['Combined'] = parse_metrics_file(comb_file)
    
    return results

def parse_metrics_file(filepath):
    """Parse evaluation metrics from text file"""
    metrics = {}
    
    with open(filepath, 'r') as f:
        content = f.read()
        
        # Extract metrics
        for line in content.split('\n'):
            if 'Accuracy:' in line:
                metrics['Accuracy'] = float(line.split(':')[1].strip())
            elif 'Precision:' in line:
                metrics['Precision'] = float(line.split(':')[1].strip())
            elif 'Recall:' in line:
                metrics['Recall'] = float(line.split(':')[1].strip())
            elif 'F1-Score:' in line:
                metrics['F1-Score'] = float(line.split(':')[1].strip())
            elif 'ROC-AUC:' in line:
                metrics['ROC-AUC'] = float(line.split(':')[1].strip())
    
    return metrics

def create_comparison_table(results):
    """Create comparison table"""
    df = pd.DataFrame(results).T
    return df

def plot_comparison(df, output_dir):
    """Plot comparison charts"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Bar chart comparison
    fig, ax = plt.subplots(figsize=(12, 6))
    df.plot(kind='bar', ax=ax, width=0.8)
    plt.title('Model Performance Comparison', fontsize=16, fontweight='bold')
    plt.xlabel('Model', fontsize=12)
    plt.ylabel('Score', fontsize=12)
    plt.legend(title='Metrics', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=0)
    plt.ylim(0, 1.05)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'comparison_bar_chart.png'), dpi=300, bbox_inches='tight')
    print(f"Bar chart saved to: {os.path.join(output_dir, 'comparison_bar_chart.png')}")
    plt.close()
    
    # 2. Grouped bar chart
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    metrics = df.columns
    
    for idx, metric in enumerate(metrics):
        row = idx // 3
        col = idx % 3
        ax = axes[row, col]
        
        df[metric].plot(kind='bar', ax=ax, color=['#3498db', '#2ecc71', '#e74c3c'])
        ax.set_title(metric, fontsize=14, fontweight='bold')
        ax.set_ylabel('Score', fontsize=11)
        ax.set_ylim(0, 1.05)
        ax.grid(axis='y', alpha=0.3)
        ax.set_xticklabels(df.index, rotation=0)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'comparison_individual_metrics.png'), dpi=300, bbox_inches='tight')
    print(f"Individual metrics chart saved to: {os.path.join(output_dir, 'comparison_individual_metrics.png')}")
    plt.close()
    
    # 3. Radar chart (if all 3 models exist)
    if len(df) == 3:
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        categories = list(df.columns)
        N = len(categories)
        
        angles = [n / float(N) * 2 * 3.14159 for n in range(N)]
        angles += angles[:1]
        
        ax.set_theta_offset(3.14159 / 2)
        ax.set_theta_direction(-1)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, size=12)
        
        colors = ['#3498db', '#2ecc71', '#e74c3c']
        
        for idx, (model_name, row) in enumerate(df.iterrows()):
            values = row.values.flatten().tolist()
            values += values[:1]
            ax.plot(angles, values, 'o-', linewidth=2, label=model_name, color=colors[idx])
            ax.fill(angles, values, alpha=0.15, color=colors[idx])
        
        ax.set_ylim(0, 1)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        plt.title('Model Performance Radar Chart', size=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'comparison_radar_chart.png'), dpi=300, bbox_inches='tight')
        print(f"Radar chart saved to: {os.path.join(output_dir, 'comparison_radar_chart.png')}")
        plt.close()

def save_comparison_report(df, output_dir):
    """Save comparison report to text file"""
    
    os.makedirs(output_dir, exist_ok=True)
    report_file = os.path.join(output_dir, 'comparison_report.txt')
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("FRAUD DETECTION MODELS COMPARISON REPORT\n")
        f.write("="*70 + "\n\n")
        
        f.write("Models Compared:\n")
        f.write("  1. Transaction-based Model (57 transaction features)\n")
        f.write("  2. Network-based Model (4 network centrality features)\n")
        f.write("  3. Combined Model (57 transaction + 4 network features)\n\n")
        
        f.write("-"*70 + "\n")
        f.write("Performance Metrics:\n")
        f.write("-"*70 + "\n\n")
        f.write(df.to_string() + "\n\n")
        
        f.write("-"*70 + "\n")
        f.write("Analysis:\n")
        f.write("-"*70 + "\n\n")
        
        # Find best model for each metric
        for metric in df.columns:
            best_model = df[metric].idxmax()
            best_score = df[metric].max()
            f.write(f"{metric}:\n")
            f.write(f"  Best: {best_model} ({best_score:.4f})\n")
            f.write(f"  Rankings: {df[metric].sort_values(ascending=False).to_dict()}\n\n")
        
        f.write("-"*70 + "\n")
        f.write("Research Questions Answers:\n")
        f.write("-"*70 + "\n\n")
        
        f.write("RQ2: Network centrality measures vs traditional features?\n")
        if 'Network' in df.index and 'Transaction' in df.index:
            net_avg = df.loc['Network'].mean()
            trans_avg = df.loc['Transaction'].mean()
            if net_avg > trans_avg:
                f.write(f"  → Network-based model OUTPERFORMS transaction-based\n")
                f.write(f"     (Average: {net_avg:.4f} vs {trans_avg:.4f})\n\n")
            else:
                f.write(f"  → Transaction-based model OUTPERFORMS network-based\n")
                f.write(f"     (Average: {trans_avg:.4f} vs {net_avg:.4f})\n\n")
        
        f.write("RQ3: Does combining features improve accuracy?\n")
        if 'Combined' in df.index:
            comb_avg = df.loc['Combined'].mean()
            f.write(f"  → Combined model average performance: {comb_avg:.4f}\n")
            
            if 'Transaction' in df.index and 'Network' in df.index:
                if comb_avg > max(trans_avg, net_avg):
                    f.write(f"  → YES! Combined model IMPROVES performance\n")
                else:
                    f.write(f"  → NO. Individual models perform better\n")
    
    print(f"\nComparison report saved to: {report_file}")

def main():
    print("="*70)
    print("COMPARING FRAUD DETECTION MODELS")
    print("="*70)
    
    # Load results
    results = load_results()
    
    if not results:
        print("\nNo results found! Please train the models first.")
        return
    
    print(f"\nFound results for {len(results)} model(s):")
    for model_name in results.keys():
        print(f"  - {model_name}")
    
    # Create comparison table
    df = create_comparison_table(results)
    
    print("\n" + "-"*70)
    print("Performance Comparison:")
    print("-"*70)
    print(df.to_string())
    print()
    
    # Output directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, 'comparison_results')
    
    # Plot comparison
    plot_comparison(df, output_dir)
    
    # Save comparison report
    save_comparison_report(df, output_dir)
    
    print("\n" + "="*70)
    print("COMPARISON COMPLETED!")
    print("="*70)
    print(f"Results saved to: {output_dir}")

if __name__ == "__main__":
    main()
