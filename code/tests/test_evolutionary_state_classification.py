import unittest
from scripts.evolutionary_state_classification import classify_evolutionary_state
from classes.evolutionary_states import EvolutionaryStates


class TestEvolutionaryStateClassification(unittest.TestCase):

    def test_convergence_state_outside_of_left_boundary(self):
        with self.assertRaises(ValueError):
            classify_evolutionary_state(evolutionary_factor=-10)

    def test_convergence_state_just_outside_of_left_boundary(self):
        with self.assertRaises(ValueError):
            classify_evolutionary_state(evolutionary_factor=-10 ** (-9))

    def test_convergence_state_on_left_boundary(self):
        evolutionary_state = classify_evolutionary_state(evolutionary_factor=0)
        self.assertEqual(evolutionary_state, EvolutionaryStates.CONVERGENCE)

    def test_convergence_state_near_left_boundary(self):
        evolutionary_state = classify_evolutionary_state(evolutionary_factor = 10**(-9))
        self.assertEqual(evolutionary_state, EvolutionaryStates.CONVERGENCE)

    def test_convergence_state_normal_case(self):
        evolutionary_state = classify_evolutionary_state(evolutionary_factor=0.1)
        self.assertEqual(evolutionary_state, EvolutionaryStates.CONVERGENCE)




    # CONVERGENCE and EXPLOITATION membership functions are both active in the interval [0.2, 0.3]

    def test_convergence_and_exploitation_common_area_convergence_wins(self):
        evolutionary_state = classify_evolutionary_state(evolutionary_factor=0.21)
        self.assertEqual(evolutionary_state, EvolutionaryStates.CONVERGENCE)

    def test_convergence_and_exploitation_intersection(self):
        # y = y <=> -5f + 1.5 = 10f - 2 <=> 15f = 3.5 <=> f = 3.5/15 = 0.7/3
        evolutionary_state = classify_evolutionary_state(evolutionary_factor=0.7/3)
        self.assertEqual(evolutionary_state, EvolutionaryStates.CONVERGENCE)

    def test_convergence_and_exploitation_common_area_exploitation_wins(self):
        evolutionary_state = classify_evolutionary_state(evolutionary_factor=0.29)
        self.assertEqual(evolutionary_state, EvolutionaryStates.EXPLOITATION)

    def test_exploitation_normal_case(self):
        evolutionary_state = classify_evolutionary_state(evolutionary_factor=0.35)
        self.assertEqual(evolutionary_state, EvolutionaryStates.EXPLOITATION)




    # EXPLOITATION and EXPLORATION membership functions are both active in the interval [0.4, 0.6]

    def test_exploitation_and_exploration_common_area_exploitation_wins(self):
        evolutionary_state = classify_evolutionary_state(evolutionary_factor=0.45)
        self.assertEqual(evolutionary_state, EvolutionaryStates.EXPLOITATION)

    def test_exploitation_and_exploration_intersection(self):
        # y = y <=> -5f - 2 = -5f + 3 <=> 10f = 5 <=> f = 1/2 = 0.5
        evolutionary_state = classify_evolutionary_state(evolutionary_factor=0.5)
        self.assertTrue(evolutionary_state == EvolutionaryStates.EXPLOITATION or
                        evolutionary_state == EvolutionaryStates.EXPLORATION)

    def test_exploitation_and_exploration_common_area_exploration_wins(self):
        evolutionary_state = classify_evolutionary_state(evolutionary_factor=0.55)
        self.assertEqual(evolutionary_state, EvolutionaryStates.EXPLORATION)

    def test_exploration_normal_case(self):
        evolutionary_state = classify_evolutionary_state(evolutionary_factor=0.65)
        self.assertEqual(evolutionary_state, EvolutionaryStates.EXPLORATION)



    # EXPLORATION and JUMP_OUT membership functions are both active in the interval [0.7, 0.8]

    def test_exploration_and_jumpout_common_area_exploration_wins(self):
        evolutionary_state = classify_evolutionary_state(evolutionary_factor=0.72)
        self.assertEqual(evolutionary_state, EvolutionaryStates.EXPLORATION)

    def test_exploration_and_jumpout_intersection(self):
        # y = y <=> 5f - 3.5 = -10f + 8 <=> 15f = 11.5 <=> f = 11.5/15 = 2.3/3
        evolutionary_state = classify_evolutionary_state(evolutionary_factor=2.3/3)
        self.assertEqual(evolutionary_state, EvolutionaryStates.EXPLORATION)

    def test_exploration_and_jumpout_common_area_jumpout_wins(self):
        evolutionary_state = classify_evolutionary_state(evolutionary_factor=0.78)
        self.assertEqual(evolutionary_state, EvolutionaryStates.JUMP_OUT)

    def test_jumpout_normal_case(self):
        evolutionary_state = classify_evolutionary_state(evolutionary_factor=0.9)
        self.assertEqual(evolutionary_state, EvolutionaryStates.JUMP_OUT)


    def test_jumpout_state_near_left_boundary(self):
        evolutionary_state = classify_evolutionary_state(evolutionary_factor=1 - 10**(-9))
        self.assertEqual(evolutionary_state, EvolutionaryStates.JUMP_OUT)

    def test_jumpout_state_on_right_boundary(self):
        evolutionary_state = classify_evolutionary_state(evolutionary_factor=1)
        self.assertEqual(evolutionary_state, EvolutionaryStates.JUMP_OUT)

    def test_jumpout_state_just_outside_of_right_boundary(self):
        with self.assertRaises(ValueError):
            classify_evolutionary_state(evolutionary_factor=1 + 10**(-9))

    def test_jumpout_state_outside_of_right_boundary(self):
        with self.assertRaises(ValueError):
            classify_evolutionary_state(evolutionary_factor=1.5)
