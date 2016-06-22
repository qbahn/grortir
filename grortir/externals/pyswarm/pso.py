# pylint: skip-file
from functools import partial

import numpy as np

from grortir.main.model.core.abstract_stage import AbstractStage
from grortir.main.model.core.optimization_status import OptimizationStatus


def _obj_wrapper(func, args, kwargs, x):
    return func(x, *args, **kwargs)


def _is_feasible_wrapper(func, x):
    return np.all(func(x) >= 0)


def _cons_none_wrapper(x):
    return np.array([0])


def _cons_ieqcons_wrapper(ieqcons, args, kwargs, x):
    return np.array([y(x, *args, **kwargs) for y in ieqcons])


def _cons_f_ieqcons_wrapper(f_ieqcons, args, kwargs, x):
    return np.array(f_ieqcons(x, *args, **kwargs))


def _results(stage, *args):
    stage.control_params = args[0].tolist()
    if stage.is_enough_quality(args[1]):
        stage.optimization_status = OptimizationStatus.success
    else:
        stage.optimization_status = OptimizationStatus.failed
    return args


def pso(stage=AbstractStage(), ieqcons=[], f_ieqcons=None, args=(), kwargs={},
        swarmsize=100, omega=0.5, phip=0.5, phig=0.5, maxiter=100, minstep=1e-8,
        minfunc=1e-8, debug=False, processes=1, particle_output=False):
    """
    Perform a particle swarm optimization (PSO)

    Parameters
    ==========
    Optional
    ========
    stage : AbstractStage
        Stage which should be optimized.
    ieqcons : list
        A list of functions of length n such that ieqcons[j](x_positions_of_swarm,*args) >= 0.0 in
        a successfully optimized problem (Default: [])
    f_ieqcons : function
        Returns a 1-D array in which each element must be greater or equal
        to 0.0 in a successfully optimized problem. If f_ieqcons is specified,
        ieqcons is ignored (Default: None)
    args : tuple
        Additional arguments passed to objective and constraint functions
        (Default: empty tuple)
    kwargs : dict
        Additional keyword arguments passed to objective and constraint
        functions (Default: empty dict)
    swarmsize : int
        The number of particles in the swarm (Default: 100)
    omega : scalar
        Particle velocity scaling factor (Default: 0.5)
    phip : scalar
        Scaling factor to search away from the particle's best known position
        (Default: 0.5)
    phig : scalar
        Scaling factor to search away from the swarm's best known position
        (Default: 0.5)
    maxiter : int
        The maximum number of iterations for the swarm to search (Default: 100)
    minstep : scalar
        The minimum stepsize of swarm's best position before the search
        terminates (Default: 1e-8)
    minfunc : scalar
        The minimum change of swarm's best objective value before the search
        terminates (Default: 1e-8)
    debug : boolean
        If True, progress statements will be displayed every iteration
        (Default: False)
    processes : int
        The number of processes to use to evaluate objective function and
        constraints (default: 1)
    particle_output : boolean
        Whether to include the best per-particle position and the objective
        values at those.
    Returns
    =======
    g : array
        The swarm's best known position (optimal design)
    f : scalar
        The objective value at ``g``
    it : int
        Number of iterations
    p : array
        The best known position per particle
    pf: arrray
        The objective values at each position in p

    """
    func_to_opt = stage.get_quality
    stage.optimization_status = OptimizationStatus.in_progress
    lb = stage.lower_bounds
    ub = stage.upper_bounds
    assert len(lb) == len(ub), 'Lower- and upper-bounds must be the same length'
    assert hasattr(func_to_opt, '__call__'), 'Invalid function handle'
    lb = np.array(lb)
    ub = np.array(ub)
    assert np.all(
        ub > lb), 'All upper-bound values must be greater than lower-bound values'

    vhigh = np.abs(ub - lb)
    vlow = -vhigh

    # Initialize objective function
    obj = partial(_obj_wrapper, func_to_opt, args, kwargs)

    # Check for constraint function(s) #########################################
    if f_ieqcons is None:
        if not len(ieqcons):
            if debug:
                print('No constraints given.')
            cons = _cons_none_wrapper
        else:
            if debug:
                print('Converting ieqcons to a single constraint function')
            cons = partial(_cons_ieqcons_wrapper, ieqcons, args, kwargs)
    else:
        if debug:
            print('Single constraint function given in f_ieqcons')
        cons = partial(_cons_f_ieqcons_wrapper, f_ieqcons, args, kwargs)
    is_feasible = partial(_is_feasible_wrapper, cons)

    # Initialize the multiprocessing module if necessary
    if processes > 1:
        import multiprocessing
        mp_pool = multiprocessing.Pool(processes)

    # Initialize the particle swarm ############################################
    Swarm_size = swarmsize
    Dimensions = len(lb)  # the number of dimensions each particle has
    x_positions_of_swarm = np.random.rand(Swarm_size, Dimensions)  # particle positions
    velocity_of_particles = np.zeros_like(x_positions_of_swarm)  # particle velocities
    best_positions = np.zeros_like(x_positions_of_swarm)  # best particle positions
    current_func_values = np.zeros(Swarm_size)  # current particle function values
    feasibility = np.zeros(Swarm_size, dtype=bool)  # feasibility of each particle
    best_values = np.ones(Swarm_size) * np.inf  # best particle function values
    initial_best_position = np.inf  # best swarm position starting value

    # Initialize the particle's position
    x_positions_of_swarm = lb + x_positions_of_swarm * (ub - lb)

    # Calculate objective and constraints for each particle
    if processes > 1:
        current_func_values = np.array(mp_pool.map(obj, x_positions_of_swarm))
        feasibility = np.array(mp_pool.map(is_feasible, x_positions_of_swarm))
    else:
        for i in range(Swarm_size):
            current_func_values[i] = obj(x_positions_of_swarm[i, :])
            feasibility[i] = is_feasible(x_positions_of_swarm[i, :])

    # Store particle's best position (if constraints are satisfied)
    i_update = np.logical_and((current_func_values < best_values), feasibility)
    best_positions[i_update, :] = x_positions_of_swarm[i_update, :].copy()
    best_values[i_update] = current_func_values[i_update]

    # Update swarm's best position
    i_min = np.argmin(best_values)
    if best_values[i_min] < initial_best_position:
        initial_best_position = best_values[i_min]
        best_position = best_positions[i_min, :].copy()
    else:
        # At the start, there may not be any feasible starting point, so just
        # give it a temporary "best" point since it's likely to change
        best_position = x_positions_of_swarm[0, :].copy()

    # Initialize the particle's velocity
    velocity_of_particles = vlow + np.random.rand(Swarm_size, Dimensions) * (vhigh - vlow)

    # Iterate until termination criterion met ##################################
    it = 1
    while it <= maxiter and stage.could_be_optimized():
        rp = np.random.uniform(size=(Swarm_size, Dimensions))
        rg = np.random.uniform(size=(Swarm_size, Dimensions))

        # Update the particles velocities
        velocity_of_particles = omega * velocity_of_particles + phip * rp * (best_positions - x_positions_of_swarm) + phig * rg * (
            best_position - x_positions_of_swarm)
        # Update the particles' positions
        x_positions_of_swarm = x_positions_of_swarm + velocity_of_particles
        # Correct for bound violations
        maskl = x_positions_of_swarm < lb
        masku = x_positions_of_swarm > ub
        x_positions_of_swarm = x_positions_of_swarm * (~np.logical_or(maskl, masku)) + lb * maskl + ub * masku

        # Update objectives and constraints
        if processes > 1:
            current_func_values = np.array(mp_pool.map(obj, x_positions_of_swarm))
            feasibility = np.array(mp_pool.map(is_feasible, x_positions_of_swarm))
        else:
            for i in range(Swarm_size):
                current_func_values[i] = obj(x_positions_of_swarm[i, :])
                feasibility[i] = is_feasible(x_positions_of_swarm[i, :])

        # Store particle's best position (if constraints are satisfied)
        i_update = np.logical_and((current_func_values < best_values),
                                  feasibility)
        best_positions[i_update, :] = x_positions_of_swarm[i_update, :].copy()
        best_values[i_update] = current_func_values[i_update]

        # Compare swarm's best position with global best position
        i_min = np.argmin(best_values)
        if best_values[i_min] < initial_best_position:
            if debug:
                print('New best for swarm at iteration {:}: {:} {:}' \
                      .format(it, best_positions[i_min, :], best_values[i_min]))

            p_min = best_positions[i_min, :].copy()
            stepsize = np.sqrt(np.sum((best_position - p_min) ** 2))

            if np.abs(initial_best_position - best_values[i_min]) <= minfunc:
                print(
                    'Stopping search: Swarm best objective change less than {:}' \
                        .format(minfunc))
                return formated_values(particle_output, stage, best_position,
                                       initial_best_position, it,
                                       best_positions, best_values)
            elif stepsize <= minstep:
                print(
                    'Stopping search: Swarm best position change less than {:}' \
                        .format(minstep))
                return formated_values(particle_output, stage, best_position,
                                       initial_best_position, it,
                                       best_positions,
                                       best_values)
            else:
                best_position = p_min.copy()
                initial_best_position = best_values[i_min]

            if stage.is_enough_quality(best_values[i_min]):
                print('Stopping search: Enough quality reached.')
                return formated_values(particle_output, stage, best_position,
                                       initial_best_position, it,
                                       best_positions, best_values)

        if debug:
            print('Best after iteration {:}: {:} {:}'.format(it, best_position,
                                                             initial_best_position))
        it += 1
    if maxiter == it:
        print('Stopping search: maximum iterations reached --> {:}'.format(
            maxiter))
    else:
        print("Stopping search: stage couldn't be optimized")

    if not is_feasible(best_position):
        print(
            "However, the optimization couldn't find a feasible design. Sorry")
    return formated_values(particle_output, stage, best_position,
                           initial_best_position, it, best_positions,
                           best_values)


def formated_values(particle_output, stage, best_position,
                    initial_best_position,
                    it, best_positions, best_values):
    if particle_output:
        return _results(stage, best_position, initial_best_position, it,
                        best_positions, best_values)
    else:
        return _results(stage, best_position, initial_best_position, it)
