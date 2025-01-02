from typing import Dict
from qiskit import QuantumCircuit, execute, Aer
from qiskit_aer import AerSimulator
import numpy as np

def create_oracle(n: int, function_type: str = "balanced") -> QuantumCircuit:
    """
    Creates quantum oracle for Deutsch-Jozsa algorithm.
    
    Args:
        n (int): Number of input qubits
        function_type (str): "constant" or "balanced"
        
    Returns:
        QuantumCircuit: Oracle circuit implementation
    """
    if n <= 0:
        raise ValueError("Number of qubits must be positive")
    if function_type not in ["constant", "balanced"]:
        raise ValueError("Function type must be 'constant' or 'balanced'")

    oracle = QuantumCircuit(n + 1)
    
    if function_type == "constant":
        # Implement constant function (f(x) = 0 for all x)
        # For f(x) = 1, uncomment next line
        # oracle.x(n)
        pass
    else:
        # Implement balanced function (f(x) = 1 for half inputs)
        for i in range(n):
            oracle.cx(i, n)
    
    return oracle

def verify_oracle(oracle: QuantumCircuit, n: int) -> Dict[str, bool]:
    """
    Verifies oracle behavior on all possible inputs.
    
    Args:
        oracle (QuantumCircuit): Oracle to verify
        n (int): Number of input qubits
        
    Returns:
        dict: Mapping of input states to oracle outputs
    """
    simulator = Aer.get_backend('statevector_simulator')
    results = {}
    
    for i in range(2**n):
        qc = QuantumCircuit(n + 1, 1)
        binary = format(i, f'0{n}b')
        
        # Prepare input state
        for j, bit in enumerate(binary):
            if bit == '1':
                qc.x(j)
                
        # Apply oracle
        qc.compose(oracle, inplace=True)
        
        # Measure output
        qc.measure(n, 0)
        
        # Get result
        counts = execute(qc, simulator, shots=1024).result().get_counts()
        results[binary] = '1' in counts
    
    # Verify balanced/constant property
    ones = sum(results.values())
    if ones not in [0, 2**n, 2**(n-1)]:
        raise ValueError("Invalid oracle: neither constant nor balanced")
    
    return results

if __name__ == "__main__":
    # Test oracle implementation
    n_qubits = 3
    for ftype in ["constant", "balanced"]:
        oracle = create_oracle(n_qubits, ftype)
        results = verify_oracle(oracle, n_qubits)
        print(f"\n{ftype.capitalize()} function mapping:")
        for input_state, output in sorted(results.items()):
            print(f"|{input_state}⟩ → |{int(output)}⟩")