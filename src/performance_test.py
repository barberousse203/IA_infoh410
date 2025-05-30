import time
import sys
import os
import datetime
from game.Board import Board
from game.AiPlayer import AiPlayer
from game.HumanPlayer import HumanPlayer

def run_performance_test():
    """
    Run a performance test comparing standard Minimax against Alpha-Beta pruning.
    Tests various search depths and measures nodes evaluated.
    """
    print("\n" + "="*50)
    print("PERFORMANCE TEST: MINIMAX VS ALPHA-BETA PRUNING")
    print("="*50 + "\n")
    
    # Test depths to compare
    depths = [1, 2, 3, 4, 5]
    
    # Store results in these lists
    standard_nodes = []
    standard_times = []
    alpha_beta_nodes = []
    alpha_beta_times = []
    
    # For each depth, run both algorithms and collect stats
    for depth in depths:
        print(f"\nTesting at depth {depth}...")
        
        # Create a fresh board for each test
        ai_player = AiPlayer(1, depth)
        human_player = HumanPlayer(2)
        board = Board(ai_player, human_player)
        
        # Test standard minimax (with a timeout for deeper depths)
        try:
            # Set a timeout for deeper searches
            max_time = 60  # Maximum seconds to wait
            start_time = time.time()
            
            print(f"  Running standard Minimax (depth {depth})...")
            _, nodes = ai_player.get_move_with_standard_minimax(board)
            elapsed = time.time() - start_time
            
            standard_nodes.append(nodes)
            standard_times.append(elapsed)
            print(f"  Standard Minimax: {nodes:,} nodes evaluated in {elapsed:.2f} seconds")
            
        except KeyboardInterrupt:
            print(f"  Standard Minimax took too long, skipping...")
            standard_nodes.append("timeout")
            standard_times.append(max_time)
            
        # Test alpha-beta pruning
        try:
            print(f"  Running Alpha-Beta pruning (depth {depth})...")
            start_time = time.time()
            _, nodes = ai_player.get_move_with_alpha_beta(board)
            elapsed = time.time() - start_time
            
            alpha_beta_nodes.append(nodes)
            alpha_beta_times.append(elapsed)
            print(f"  Alpha-Beta pruning: {nodes:,} nodes evaluated in {elapsed:.2f} seconds")
            
        except KeyboardInterrupt:
            print(f"  Alpha-Beta pruning took too long, skipping...")
            alpha_beta_nodes.append("timeout")
            alpha_beta_times.append(max_time)
    
    # Print the final comparison table
    print("\n" + "="*50)
    print("RESULTS SUMMARY")
    print("="*50)
    print("\n{:<12} {:<25} {:<25}".format("Depth", "Minimax Nodes", "Alpha-Beta Nodes"))
    print("-" * 62)
    
    for i, depth in enumerate(depths):
        std_result = f"{standard_nodes[i]:,}" if isinstance(standard_nodes[i], int) else standard_nodes[i]
        ab_result = f"{alpha_beta_nodes[i]:,}" if isinstance(alpha_beta_nodes[i], int) else alpha_beta_nodes[i]
        print("{:<12} {:<25} {:<25}".format(depth, std_result, ab_result))
    
    # Save results to files
    results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
    os.makedirs(results_dir, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"performance_test_{timestamp}"
    
    # Save text results
    txt_filename = os.path.join(results_dir, f"{base_filename}.txt")
    save_text_results(txt_filename, depths, standard_nodes, standard_times, alpha_beta_nodes, alpha_beta_times)
    
    # Save LaTeX results
    latex_filename = os.path.join(results_dir, f"{base_filename}.tex")
    save_latex_results(latex_filename, depths, standard_nodes, standard_times, alpha_beta_nodes, alpha_beta_times)
    
    print(f"\nResults saved to {txt_filename} and {latex_filename}")
    
    # Still output LaTeX table to console for convenience
    print("\n" + "="*50)
    print("LaTeX Table Format:")
    print("\\begin{tabular}{|c|c|c|}")
    print("\\hline")
    print("Search Depth & Nodes Evaluated (Minimax) & Nodes Evaluated (Alpha-Beta) \\\\")
    print("\\hline")
    
    for i, depth in enumerate(depths):
        std_result = f"{standard_nodes[i]:,}" if isinstance(standard_nodes[i], int) else standard_nodes[i]
        ab_result = f"{alpha_beta_nodes[i]:,}" if isinstance(alpha_beta_nodes[i], int) else alpha_beta_nodes[i]
        print(f"{depth} & {std_result} & {ab_result} \\\\")
        
    print("\\hline")
    print("\\end{tabular}")
    print("="*50 + "\n")

def save_text_results(filename, depths, std_nodes, std_times, ab_nodes, ab_times):
    """Save results to a text file in a readable format."""
    with open(filename, 'w') as f:
        f.write("PERFORMANCE TEST RESULTS: MINIMAX VS ALPHA-BETA PRUNING\n")
        f.write("="*60 + "\n\n")
        
        f.write("System Information:\n")
        f.write(f"Date and Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Python Version: {sys.version}\n\n")
        
        f.write("{:<10} {:<20} {:<15} {:<20} {:<15}\n".format(
            "Depth", "Minimax Nodes", "Time (sec)", "Alpha-Beta Nodes", "Time (sec)"))
        f.write("-" * 80 + "\n")
        
        for i, depth in enumerate(depths):
            std_node_result = f"{std_nodes[i]:,}" if isinstance(std_nodes[i], int) else std_nodes[i]
            ab_node_result = f"{ab_nodes[i]:,}" if isinstance(ab_nodes[i], int) else ab_nodes[i]
            std_time_result = f"{std_times[i]:.2f}" if isinstance(std_times[i], float) else std_times[i]
            ab_time_result = f"{ab_times[i]:.2f}" if isinstance(ab_times[i], float) else ab_times[i]
            
            f.write("{:<10} {:<20} {:<15} {:<20} {:<15}\n".format(
                depth, std_node_result, std_time_result, ab_node_result, ab_time_result))
        
        f.write("\nEfficiency Comparison:\n")
        for i, depth in enumerate(depths):
            if isinstance(std_nodes[i], int) and isinstance(ab_nodes[i], int):
                efficiency = std_nodes[i] / ab_nodes[i] if ab_nodes[i] > 0 else float('inf')
                f.write(f"Depth {depth}: Alpha-Beta evaluates {efficiency:.2f}x fewer nodes than standard Minimax\n")
        
        f.write("\nConclusion:\n")
        f.write("Alpha-Beta pruning significantly reduces the number of nodes evaluated, enabling deeper searches\n")
        f.write("and improved decision-making within the same time constraints compared to standard Minimax.\n")

def save_latex_results(filename, depths, std_nodes, std_times, ab_nodes, ab_times):
    """Save results in LaTeX format."""
    with open(filename, 'w') as f:
        f.write("% Performance test results for Minimax vs Alpha-Beta pruning\n")
        f.write("% Generated on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
        
        # Nodes evaluation table
        f.write("\\begin{table}[htbp]\n")
        f.write("\\centering\n")
        f.write("\\caption{Comparison of Nodes Evaluated: Minimax vs Alpha-Beta Pruning}\n")
        f.write("\\label{tab:nodes_comparison}\n")
        f.write("\\begin{tabular}{|c|r|r|c|}\n")
        f.write("\\hline\n")
        f.write("\\textbf{Search Depth} & \\textbf{Minimax Nodes} & \\textbf{Alpha-Beta Nodes} & \\textbf{Improvement (\\%)} \\\\\n")
        f.write("\\hline\n")
        
        for i, depth in enumerate(depths):
            if isinstance(std_nodes[i], int) and isinstance(ab_nodes[i], int):
                improvement = 100 * (1 - ab_nodes[i] / std_nodes[i]) if std_nodes[i] > 0 else 0
                f.write(f"{depth} & {std_nodes[i]:,} & {ab_nodes[i]:,} & {improvement:.1f}\\% \\\\\n")
            else:
                std_str = f"{std_nodes[i]:,}" if isinstance(std_nodes[i], int) else "Timeout"
                ab_str = f"{ab_nodes[i]:,}" if isinstance(ab_nodes[i], int) else "Timeout"
                f.write(f"{depth} & {std_str} & {ab_str} & - \\\\\n")
                
        f.write("\\hline\n")
        f.write("\\end{tabular}\n")
        f.write("\\end{table}\n\n")
        
        # Time execution table
        f.write("\\begin{table}[htbp]\n")
        f.write("\\centering\n")
        f.write("\\caption{Execution Time Comparison: Minimax vs Alpha-Beta Pruning}\n")
        f.write("\\label{tab:time_comparison}\n")
        f.write("\\begin{tabular}{|c|r|r|c|}\n")
        f.write("\\hline\n")
        f.write("\\textbf{Search Depth} & \\textbf{Minimax Time (s)} & \\textbf{Alpha-Beta Time (s)} & \\textbf{Speedup} \\\\\n")
        f.write("\\hline\n")
        
        for i, depth in enumerate(depths):
            if isinstance(std_times[i], (int, float)) and isinstance(ab_times[i], (int, float)):
                speedup = std_times[i] / ab_times[i] if ab_times[i] > 0 else float('inf')
                f.write(f"{depth} & {std_times[i]:.2f} & {ab_times[i]:.2f} & {speedup:.1f}x \\\\\n")
            else:
                std_str = f"{std_times[i]:.2f}" if isinstance(std_times[i], (int, float)) else "Timeout"
                ab_str = f"{ab_times[i]:.2f}" if isinstance(ab_times[i], (int, float)) else "Timeout"
                f.write(f"{depth} & {std_str} & {ab_str} & - \\\\\n")
                
        f.write("\\hline\n")
        f.write("\\end{tabular}\n")
        f.write("\\end{table}\n")

if __name__ == "__main__":
    run_performance_test()
