"""
Copyright (C) 2021  Konstantinos Stavratis
For the full notice of the program, see "main.py"
"""

from time import process_time
from typing import Any, List, Tuple
from numpy import inf, array, mean
from scipy.linalg import norm

from classes.PSOs.classicPSOswarm import ClassicSwarm
from classes.PSOs.clanPSOswarm import ClanSwarm
from classes.PSOs.Mixins.enhanced_information_sharing.enums.global_local_coefficient_types import GlobalLocalCoefficientTypes
from classes.PSOs.Mixins.enhanced_information_sharing.enums.control_factor_types import ControlFactorTypes
from classes.PSOs.wall_types import WallTypes

# This strict policy is enacted so as to catch rounding errors (overflows/underflows) as well.
import warnings
warnings.filterwarnings("error")

loop_stop_condition_limit = 5e-15


def experiment(objective_function: Any, spawn_boundaries: List[List[float]],
               objective_function_goal_point: array,
               maximum_iterations: int,
               swarm_size: int = 40, is_clan: bool = False, number_of_clans: int = 4, c1: float = 2.0, c2: float = 2.0,
               is_adaptive: bool = False,
               eis: Tuple[Tuple[GlobalLocalCoefficientTypes, float or None], Tuple[ControlFactorTypes, float or None]] =
               ((GlobalLocalCoefficientTypes.NONE, None), (ControlFactorTypes.NONE, None)),
               search_and_velocity_boundaries: List[List[float]] = None, wt: WallTypes = WallTypes.NONE):
    """
    :param objective_function:
    :param spawn_boundaries:
    :param maximum_iterations:
    :param swarm_size:
    :param is_clan:
    :param number_of_clans:
    :param c1:
    :param c2:
    :param is_adaptive:
    :param eis:
    :param search_and_velocity_boundaries:
    :param wt:

    :return:
    """

    # global experiment_swarm

    if not is_clan:
        experiment_swarm = ClassicSwarm(swarm_or_fitness_function=objective_function,
                                        spawn_boundaries=spawn_boundaries,
                                        swarm_size=swarm_size,
                                        maximum_iterations=maximum_iterations,
                                        is_adaptive=is_adaptive, eis=eis, current_iteration=0,
                                        search_and_velocity_boundaries=search_and_velocity_boundaries, wt=wt)

    if is_clan:
        experiment_swarm = ClanSwarm(fitness_function=objective_function,
                                     spawn_boundaries=spawn_boundaries,
                                     swarm_size=swarm_size // number_of_clans, number_of_clans=number_of_clans,
                                     maximum_iterations=maximum_iterations,
                                     c1=c1, c2=c2,
                                     is_adaptive=is_adaptive, eis=eis, current_iteration=0,
                                     search_and_velocity_boundaries=search_and_velocity_boundaries, wt=wt)

    loop_times = []

    # START EXPERIMENT
    experiment_start = process_time()

    iteration = 0
    loop_stop_condition_value = inf
    

    while not (loop_stop_condition_value < loop_stop_condition_limit) and iteration < maximum_iterations:
        loop_start = process_time()

        try:
            experiment_swarm.update_swarm()
        # Stopping process when rounding errors (overflow or underflow) appear.
        except FloatingPointError:
            iteration += 1
            loop_end = process_time()
            loop_times.append(loop_end - loop_start)
            break
        except RuntimeWarning:
            iteration += 1
            loop_end = process_time()
            loop_times.append(loop_end - loop_start)
            break

            
        loop_stop_condition_value = experiment_swarm.calculate_swarm_distance_from_swarm_centroid()
        iteration += 1

        loop_end = process_time()
        loop_times.append(loop_end - loop_start)

    experiment_end = process_time()
    # END EXPERIMENT

    precision = None
    if not is_clan:
        precision = norm(experiment_swarm.global_best_position - objective_function_goal_point)
    if is_clan:
        precision = norm(experiment_swarm.find_population_global_best_position() - objective_function_goal_point)

    iterations = iteration
    experiment_average_iteration_cpu_time = mean(loop_times)
    experiment_total_cpu_time = experiment_end - experiment_start

    return precision, iterations, experiment_average_iteration_cpu_time, experiment_total_cpu_time