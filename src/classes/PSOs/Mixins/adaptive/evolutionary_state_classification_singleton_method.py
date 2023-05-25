"""
Copyright (C) 2021  Konstantinos Stavratis
For the full notice of the program, see "main.py"
"""

from numpy import inf

from classes.PSOs.Mixins.adaptive.enums.evolutionary_states import EvolutionaryStates

"""
For details see "Adaptive Particle Swarm Optimization (Zhan et al.)" -> III ESE for PSO -> B. ESE -> Step 3
The singleton defuzzification classification technique is used to determine the state the swarm is in.

The ruletable according to which conflicts are solved is

Confusion \ Current State   S1  S2  S3  S4
------------------------------------------
    S1 - S2|                S1  S2  S2  S1
    S1 - S4|                S1  S1  S4  S4
    S2 - S3|                S2  S2  S3  S3
"""


# Defining transition matrix as a tuple, so as to make it unchangeable.
transition_matrix = (
    (EvolutionaryStates.EXPLORATION, EvolutionaryStates.EXPLOITATION, EvolutionaryStates.EXPLOITATION, EvolutionaryStates.EXPLORATION),
    (EvolutionaryStates.EXPLORATION, EvolutionaryStates.EXPLORATION, EvolutionaryStates.JUMP_OUT, EvolutionaryStates.JUMP_OUT),
    (EvolutionaryStates.EXPLOITATION, EvolutionaryStates.EXPLOITATION, EvolutionaryStates.CONVERGENCE, EvolutionaryStates.CONVERGENCE)
)

current_state = EvolutionaryStates.EXPLORATION



def classify_evolutionary_state(evolutionary_factor: float):
    """
    The ruletable according to which conflicts are solved is

    Confusion \ Current State   S1  S2  S3  S4
    ------------------------------------------
        S1 - S2|                S1  S2  S2  S1
        S1 - S4|                S1  S1  S4  S4
        S2 - S3|                S2  S2  S3  S3
    """
    
    membership_function_dict = {
        EvolutionaryStates.EXPLORATION: __exploration_membership_function,
        EvolutionaryStates.EXPLOITATION: __exploitation_membership_function,
        EvolutionaryStates.CONVERGENCE: __convergence_membership_function,
        EvolutionaryStates.JUMP_OUT: __jumping_out_membership_function
    }


    # Initialization of array
    f = [-inf for i in range(len(EvolutionaryStates))]

    greater_than_zero_membership_values = 0


    # Calculate membership function values.
    f[EvolutionaryStates.EXPLORATION.value] = \
        membership_function_dict[EvolutionaryStates.EXPLORATION](evolutionary_factor)
    if f[EvolutionaryStates.EXPLORATION.value] > 0:
        greater_than_zero_membership_values += 1

    f[EvolutionaryStates.EXPLOITATION.value] = \
        membership_function_dict[EvolutionaryStates.EXPLOITATION](evolutionary_factor)
    if f[EvolutionaryStates.EXPLOITATION.value] > 0:
        greater_than_zero_membership_values += 1

    f[EvolutionaryStates.CONVERGENCE.value] = \
        membership_function_dict[EvolutionaryStates.CONVERGENCE](evolutionary_factor)
    if f[EvolutionaryStates.CONVERGENCE.value] > 0:
        greater_than_zero_membership_values += 1

    f[EvolutionaryStates.JUMP_OUT.value] = \
        membership_function_dict[EvolutionaryStates.JUMP_OUT](evolutionary_factor)
    if f[EvolutionaryStates.JUMP_OUT.value] > 0:
        greater_than_zero_membership_values += 1


    global current_state

    if greater_than_zero_membership_values <= 0:
        raise ValueError("f_evol must be classified to at least one evolutionary state.")
    elif greater_than_zero_membership_values == 1:
        next_evolutionary_state = EvolutionaryStates(f.index(max(f)))
        current_state = next_evolutionary_state
        return next_evolutionary_state  # singleton defuzzification classification technique
    else:
        if f[EvolutionaryStates.EXPLORATION.value] > 0 and f[EvolutionaryStates.EXPLOITATION.value] > 0:
            current_state = transition_matrix[0][current_state.value]
            return current_state
        elif f[EvolutionaryStates.EXPLORATION.value] > 0 and f[EvolutionaryStates.JUMP_OUT.value] > 0:
            current_state = transition_matrix[1][current_state.value]
            return current_state
        elif f[EvolutionaryStates.EXPLOITATION.value] > 0 and f[EvolutionaryStates.CONVERGENCE.value] > 0:
            current_state = transition_matrix[2][current_state.value]
            return current_state

def __membership_value_error_message(f):
    return f"The evolutionary factor is bounded in the values [0,1].\n\ Its value is {f} instead."

def __exploration_membership_function(f: float) -> float:
        if 0 <= f <= 0.4 or 0.8 < f <= 1.0:
            return 0
        elif 0.4 < f <= 0.6:
            return 5 * f - 2
        elif 0.6 < f <= 0.7:
            return 1
        elif 0.7 < f <= 0.8:
            return -10 * f + 8
        else:
            raise ValueError(__membership_value_error_message(f))

def __exploitation_membership_function(f: float) -> float:
        if 0 <= f <= 0.2 or 0.6 < f <= 1:
            return 0
        elif 0.2 < f <= 0.3:
            return 10 * f - 2
        elif 0.3 < f <= 0.4:
            return 1
        elif 0.4 < f <= 0.6:
            return -5 * f + 3
        else:
            raise ValueError(__membership_value_error_message(f))

def __convergence_membership_function(f: float) -> float:
        if 0 <= f <= 0.1:
            return 1
        elif 0.1 < f <= 0.3:
            return -5 * f + 1.5
        elif 0.3 < f <= 1:
            return 0
        else:
            raise ValueError(__membership_value_error_message(f))

def __jumping_out_membership_function(f: float) -> float:
        if 0 <= f <= 0.7:
            return 0
        elif 0.7 < f <= 0.9:
            return 5 * f - 3.5
        elif 0.9 < f <= 1:
            return 1
        else:
            raise ValueError(__membership_value_error_message(f))