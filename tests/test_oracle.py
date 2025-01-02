import unittest
import sys
import os
from qiskit import QuantumCircuit, execute
from qiskit_aer import AerSimulator
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.oracle import create_oracle, verify_oracle

class TestOracle(unittest.TestCase):
    def setUp(self):
        """Initialize test environment with proper simulator"""
        self.simulator = AerSimulator()
        self.shots = 8192
        self.tolerance = 0.4
        self.test_sizes = [2, 3]

    def verify_oracle_distribution(self, results: dict, expected_constant: bool = True) -> None:
        """Helper to verify oracle output distribution"""
        ones = sum(results.values())
        total = len(results)
        
        if expected_constant:
            self.assertIn(ones, [0, total], 
                "Constant oracle should return all 0s or all 1s")
        else:
            self.assertEqual(ones, total // 2,
                "Balanced oracle should return 1s for exactly half inputs")

    def test_invalid_inputs(self):
        """Test invalid input handling"""
        with self.assertRaises(ValueError):
            create_oracle(0)
        with self.assertRaises(ValueError):
            create_oracle(2, "invalid")

    def test_constant_oracle(self):
        """Test constant oracle behavior"""
        for n in self.test_sizes:
            oracle = create_oracle(n, "constant")
            self.assertIsInstance(oracle, QuantumCircuit)
            
            # Verify circuit structure
            self.assertEqual(oracle.num_qubits, n + 1)
            
            # Verify oracle behavior
            results = verify_oracle(oracle, n)
            self.verify_oracle_distribution(results, expected_constant=True)

    def test_balanced_oracle(self):
        """Test balanced oracle behavior"""
        for n in self.test_sizes:
            oracle = create_oracle(n, "balanced")
            self.assertIsInstance(oracle, QuantumCircuit)
            
            # Verify circuit structure
            self.assertEqual(oracle.num_qubits, n + 1)
            
            # Verify oracle behavior
            results = verify_oracle(oracle, n)
            self.verify_oracle_distribution(results, expected_constant=False)

if __name__ == '__main__':
    unittest.main(verbosity=2)