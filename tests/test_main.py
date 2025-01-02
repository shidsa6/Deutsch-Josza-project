from typing import Dict
import unittest
import sys
import os
from qiskit_aer import AerSimulator
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.main import deutsch_jozsa_algorithm

class TestDeutschJozsa(unittest.TestCase):
    def setUp(self):
        """Initialize test environment with optimized simulator"""
        self.simulator = AerSimulator(method='automatic')
        self.shots = 8192
        self.tolerance = 0.4

    def verify_distribution(self, counts: Dict[str, int], expected_zero: bool = True) -> None:
        """Helper to verify measurement distribution"""
        total_counts = sum(counts.values())
        for state, count in counts.items():
            prob = count/total_counts
            if expected_zero and state == '0' * len(state):
                self.assertGreater(prob, 0.9, 
                    f"Expected high probability for |{state}⟩ state")
            elif not expected_zero:
                self.assertGreater(prob, 0.1,
                    f"Expected non-zero probability for |{state}⟩ state")

    def test_invalid_inputs(self):
        """Test invalid input handling"""
        with self.assertRaises(ValueError):
            deutsch_jozsa_algorithm(0)
        with self.assertRaises(ValueError):
            deutsch_jozsa_algorithm(2, shots=-1)
        with self.assertRaises(ValueError):
            deutsch_jozsa_algorithm(3, "invalid_type")

    def test_constant_function(self):
        """Test constant function behavior"""
        for n in [2, 3]:
            circuit, counts = deutsch_jozsa_algorithm(
                n=n,
                function_type="constant",
                shots=self.shots,
                simulator=self.simulator
            )
            
            # Verify circuit structure
            self.assertEqual(circuit.num_qubits, n + 1)
            self.assertEqual(circuit.num_clbits, n)
            
            # Verify measurement results
            self.verify_distribution(counts, expected_zero=True)

    def test_balanced_function(self):
        """Test balanced function behavior"""
        for n in [2, 3]:
            circuit, counts = deutsch_jozsa_algorithm(
                n=n,
                function_type="balanced",
                shots=self.shots,
                simulator=self.simulator
            )
            
            # Verify circuit structure
            self.assertEqual(circuit.num_qubits, n + 1)
            self.assertEqual(circuit.num_clbits, n)
            
            # Verify no zero state
            zero_state = '0' * n
            self.assertNotIn(zero_state, counts,
                "Balanced function should not measure |0...0⟩ state")
            
            # Verify uniform distribution
            total_counts = sum(counts.values())
            num_states = len(counts)
            expected_prob = 1.0 / num_states
            
            for state, count in counts.items():
                prob = count/total_counts
                self.assertLess(abs(prob - expected_prob), self.tolerance,
                    f"State |{state}⟩ probability ({prob:.3f}) deviates from expected ({expected_prob:.3f})")

if __name__ == '__main__':
    unittest.main(verbosity=2)