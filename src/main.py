
from typing import Tuple, Dict
from qiskit import QuantumCircuit, execute
from qiskit_aer import AerSimulator
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.oracle import create_oracle, verify_oracle

def deutsch_jozsa_algorithm(
    n: int, 
    function_type: str = "balanced",
    shots: int = 1024,
    simulator = None
) -> Tuple[QuantumCircuit, Dict[str, int]]:
    """
    Implements Deutsch-Jozsa quantum algorithm.
    """
    if n <= 0 or shots <= 0:
        raise ValueError("Invalid input parameters")

    # Create circuit
    qc = QuantumCircuit(n + 1, n)
    
    # Initialize
    qc.x(n)
    qc.h(range(n + 1))
    
    # Apply oracle
    oracle = create_oracle(n, function_type)
    qc.compose(oracle, inplace=True)
    
    # Final Hadamard gates
    qc.h(range(n))
    
    # Measure
    qc.measure(range(n), range(n))
    
    # Execute with optimized simulator initialization
    if simulator is None:
        simulator = AerSimulator()
    job = execute(qc, simulator, shots=shots)
    counts = job.result().get_counts()
    
    return qc, counts

def analyze_results(counts: Dict[str, int], function_type: str, n: int) -> str:
    """
    Analyzes results of Deutsch-Jozsa algorithm.
    """
    zero_state = '0' * n
    total_shots = sum(counts.values())
    
    if function_type == "constant":
        if counts.get(zero_state, 0) > 0.9 * total_shots:
            return (
                "Function is CONSTANT-0:\n"
                f"- High probability in |{zero_state}⟩ state ({counts[zero_state]/total_shots:.2%})\n"
                "- Classical: requires 2^n queries\n"
                "- Quantum: solved in 1 query"
            )
        return (
            "Function is CONSTANT-1:\n"
            "- No measurements in |0...0⟩ state\n"
            "- Classical: requires 2^n queries\n"
            "- Quantum: solved in 1 query"
        )
    else:
        if zero_state not in counts:
            return (
                "Function is BALANCED:\n"
                "- No measurements in |0...0⟩ state\n"
                "- Equal 0s and 1s in output\n"
                f"- Classical: requires {2**(n-1)+1} queries minimum\n"
                "- Quantum: solved in 1 query"
            )
        return "Unexpected result for balanced function"

if __name__ == "__main__":
    n_qubits = 3
    function_types = ["constant", "balanced"]
    
    for f_type in function_types:
        try:
            print(f"\n{'='*50}")
            print(f"Deutsch-Jozsa Algorithm: {f_type.upper()} Function Test")
            print('='*50)
            
            # Run algorithm
            circuit, counts = deutsch_jozsa_algorithm(n_qubits, f_type)
            print(f"\nCircuit depth: {circuit.depth()}")
            print("Measurement distribution:")
            for state, count in counts.items():
                print(f"|{state}⟩: {count/1024:.2%}")
            
            # Show oracle behavior
            oracle = create_oracle(n_qubits, f_type)
            results = verify_oracle(oracle, n_qubits)
            
            print("\nOracle Function Pattern:")
            print("-" * 20)
            for input_state, output in sorted(results.items()):
                print(f"f(|{input_state}⟩) = |{int(output)}⟩")
            
            print("\nAlgorithm Analysis:")
            print("-" * 20)
            print(analyze_results(counts, f_type, n_qubits))
            
        except Exception as e:
            print(f"Error: {str(e)}")