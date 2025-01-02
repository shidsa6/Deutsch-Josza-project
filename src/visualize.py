from typing import Dict, Optional
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram, circuit_drawer
import sys
import os
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.main import deutsch_jozsa_algorithm

def cleanup_previous_files(directory: str) -> None:
    path = Path(directory)
    if path.exists():
        for item in path.glob("*.png"):
            if "discussion" not in item.name:
                item.unlink()

def save_generic_circuit(
    n: int,
    save_path: str
) -> None:
    """Creates generic DJ circuit visualization."""
    qc = QuantumCircuit(n + 1, n)
    
    # Initial state preparation
    qc.x(n)
    qc.barrier()
    qc.h(range(n + 1))
    
    # Oracle (black box) representation
    qc.barrier()
    qc.append(QuantumCircuit(n + 1).to_instruction(label='Oracle'), range(n + 1))
    qc.barrier()
    
    # Final Hadamard gates
    qc.h(range(n))
    qc.barrier()
    
    # Measurement
    qc.measure(range(n), range(n))
    
    # Draw circuit
    plt.figure(figsize=(15, 8))
    style = {
        'backgroundcolor': '#FFFFFF',
        'fontsize': 14,
        'compress': True,
        'showindex': True,
        'margin': [2.0, 0.1, 0.1, 0.1],
        'plotbarrier': True
    }
    
    circuit_diagram = circuit_drawer(
        qc,
        output='mpl',
        style=style,
        plot_barriers=True
    )
    
    plt.title("Deutsch-Jozsa Algorithm Circuit\nGeneric Implementation", pad=20)
    plt.savefig(save_path, bbox_inches='tight', dpi=300, facecolor='white')
    plt.close()

def save_probability_distribution(
    counts: Dict[str, int],
    save_path: str,
    n_qubits: int,
    function_type: str
) -> None:
    """Creates probability distribution plot."""
    plt.figure(figsize=(12, 8))
    
    # Calculate probabilities
    total = sum(counts.values())
    states = sorted(counts.keys())
    probs = [counts[state]/total for state in states]
    
    # Create bar plot
    bars = plt.bar(range(len(states)), probs, color='skyblue')
    plt.xticks(range(len(states)), [f"|{state}⟩" for state in states], rotation=45)
    
    # Add labels
    title = "Measurement Results\n"
    if function_type == "constant":
        title += "Result: Constant Function (All measurements in |0...0⟩)"
    else:
        title += "Result: Balanced Function (No measurements in |0...0⟩)"
    
    plt.title(title, pad=20)
    plt.xlabel("Measured Quantum States")
    plt.ylabel("Probability")
    
    # Add probability values
    for idx, prob in enumerate(probs):
        plt.text(idx, prob, f'{prob:.3f}', ha='center', va='bottom')
    
    # Add quantum advantage note
    plt.figtext(0.02, 0.02, 
               "Quantum Advantage:\n"
               "- Classical: O(2^n) queries\n"
               "- Quantum: 1 query",
               fontsize=10)
    
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

def run_visualization(
    n: int = 3,
    save_dir: str = "docs"
) -> None:
    """Runs visualization pipeline."""
    try:
        save_path = Path(save_dir)
        save_path.mkdir(parents=True, exist_ok=True)
        cleanup_previous_files(save_dir)
        
        # Save generic circuit
        circuit_path = save_path / "dj_circuit_generic.png"
        save_generic_circuit(n, str(circuit_path))
        print(f"Saved generic circuit diagram to {circuit_path}")
        
        # Save probability distributions for both cases
        for function_type in ["constant", "balanced"]:
            _, counts = deutsch_jozsa_algorithm(n, function_type)
            prob_path = save_path / f"dj_probabilities_{function_type}.png"
            save_probability_distribution(counts, str(prob_path), n, function_type)
            print(f"Saved {function_type} function results to {prob_path}")
            
    except Exception as e:
        print(f"Visualization failed: {str(e)}")
        raise

if __name__ == "__main__":
    run_visualization(n=3, save_dir="docs")