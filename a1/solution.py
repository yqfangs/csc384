#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os  # for time functions
from search import *  # for search engines
from sokoban import SokobanState, Direction, PROBLEMS  # for Sokoban specific classes and problems

previous_boxes = []
previous = 0

def sokoban_goal_state(state):
    '''
  @return: Whether all boxes are stored.
  '''
    for box in state.boxes:
        if box not in state.storage:
            return False
    return True


def heur_manhattan_distance(state):
    # IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # We want an admissible heuristic, which is an optimistic heuristic.
    # It must never overestimate the cost to get from the current state to the goal.
    # The sum of the Manhattan distances between each box that has yet to be stored and the storage point nearest to it is such a heuristic.
    # When calculating distances, assume there are no obstacles on the grid.
    # You should implement this heuristic function exactly, even if it is tempting to improve it.
    # Your function should return a numeric value; this is the estimate of the distance to the goal.

    rvalue = 0

    for box in state.boxes:
        distances = []
        if box in state.storage:
            continue

        for storage in state.storage:
            distance = abs(storage[0] - box[0]) + abs(storage[1] - box[1])
            distances.append(distance)
        if distances:
            rvalue += min(distances)

    return rvalue


# SOKOBAN HEURISTICS
def trivial_heuristic(state):
    '''trivial admissible sokoban heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''
    count = 0
    for box in state.boxes:
        if box not in state.storage:
            count += 1
    return count


def heur_alternate(state):
    # IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # heur_manhattan_distance has flaws.
    # Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    # Your function should return a numeric value for the estimate of the distance to the goal.

    r_value = 0;

    global previous_boxes
    global previous
    if state.boxes == previous_boxes:
        return previous
    else:
        previous_boxes = state.boxes

    unstored_boxes = set(state.boxes)
    unused_storages = set(state.storage)

    left_storage = 0
    right_storage = 0
    top_storage = 0
    bottom_storage = 0

    for storage in unused_storages:
        if storage[0] == 0:
            left_storage += 1
        elif storage[0] + 1 == state.width:
            right_storage += 1
        elif storage[1] == 0:
            bottom_storage += 1
        elif storage[1] + 1 == state.height:
            top_storage += 1

    # should not consider the storage that has been taken/box stored

    # consider when box cannot be moved(corner)
    for box in state.boxes:
        if box in state.storage:
            unstored_boxes.remove(box)
            unused_storages.remove(box)

    # left_wall = 0
    # right_wall = 0
    # top_wall = 0
    # bottom_wall = 0

    for box in unstored_boxes:
        # corners
        left_wall = box[0] == 0
        right_wall = box[0] + 1 == state.width
        top_wall = box[1] + 1 == state.height
        bottom_wall = box[1] == 0

        # if box[0] == 0:
        #     left_wall += 1
        # elif box[0] + 1 == state.width:
        #     right_wall += 1
        # elif box[1] == 0:
        #     bottom_wall += 1
        # elif box[1] + 1 == state.height:
        #     top_wall += 1

        left_obstacles = (box[0] - 1, box[1]) in state.obstacles
        right_obstacles = (box[0] + 1, box[1]) in state.obstacles
        top_obstacles = (box[0], box[1] + 1) in state.obstacles
        bottom_obstacles = (box[0], box[1] - 1) in state.obstacles

        left_box = (box[0] - 1, box[1]) in state.boxes
        right_box = (box[0] + 1, box[1]) in state.boxes
        top_box = (box[0], box[1] + 1) in state.boxes
        bottom_box = (box[0], box[1] - 1) in state.boxes

        left_blocked = left_wall or left_obstacles or left_box
        right_blocked = right_wall or right_obstacles or right_box
        top_blocked = top_wall or top_obstacles or top_box
        bottom_blocked = bottom_wall or bottom_obstacles or bottom_box

        if (top_blocked or bottom_blocked) and (right_blocked or left_blocked):
            previous = float('inf')
            return float('inf')
        # one side wall(can only move either horizontal/vertical but if without enough storage against the wall
        if left_wall:
            left_storage -= 1
            if left_storage < 0:
                previous = float('inf')
                return float('inf')
        elif right_wall:
            right_storage -= 1
            if right_storage < 0:
                previous = float('inf')
                return float('inf')
        elif bottom_wall:
            bottom_storage -= 1
            if bottom_storage < 0:
                previous = float('inf')
                return float('inf')
        elif top_wall:
            top_storage -= 1
            if top_storage < 0:
                previous = float('inf')
                return float('inf')

        robot_distances = []
        for robot in state.robots:
            distance = abs(robot[0] - box[0]) + abs(robot[1] - box[1])
            robot_distances.append(distance)
        if robot_distances:
            r_value += min(robot_distances)

        chosen_storage = None
        cur_min = -1
        for storage in unused_storages:
            distance = abs(storage[0] - box[0]) + abs(storage[1] - box[1])
            if distance > cur_min:
                cur_min = distance
                chosen_storage = storage
        unused_storages.remove(chosen_storage)
        r_value += cur_min

        previous = r_value

    return r_value


def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0


def fval_function(sN, weight):
    # IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """

    # Many searches will explore nodes (or states) that are ordered by their f-value.
    # For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    # You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    # The function must return a numeric f-value.
    # The value will determine your state's position on the Frontier list during a 'custom' search.
    # You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    return sN.gval + weight * sN.hval


def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound=10):
    # IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''

    engine = SearchEngine('custom', "full")
    wrapped_fval_function = (lambda sN: fval_function(sN, weight))
    engine.init_search(initial_state, sokoban_goal_state, heur_fn, wrapped_fval_function)

    r_state = False

    costbound = None
    start_time = os.times()[0]
    remaining = timebound
    while remaining > 0:
        goal = engine.search(remaining, costbound)
        if goal:
            r_state = goal
            current_time = os.times()[0]
            remaining = remaining - (current_time - start_time)
            costbound = (float('inf'), float('inf'), goal.gval)
        else:
            break

    return r_state


def anytime_gbfs(initial_state, heur_fn, timebound=10):
    # IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''

    engine = SearchEngine("best_first", "full")
    engine.init_search(initial_state, sokoban_goal_state, heur_fn)

    r_state = False

    costbound = None
    start_time = os.times()[0]
    remaining = timebound
    while remaining > 0:
        goal = engine.search(remaining, costbound)
        if goal:
            r_state = goal
            current_time = os.times()[0]
            remaining = remaining - (current_time - start_time)
            costbound = (goal.gval, float('inf'), float('inf'))
        else:
            break
    return r_state
