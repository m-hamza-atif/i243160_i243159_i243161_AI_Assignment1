# search.py
# ---------


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import csv
import os

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


class CSVTraceLogger:
    """
    Traces execution actions and logs them into CSV.
    """
    def __init__(self, algorithm_name, problem):
        self.algorithm_name = algorithm_name
        self.problem_name = problem.__class__.__name__
        self.rows = []
        self.iteration = 0
        self.headers = [
            "iteration",
            "expanded_state",
            "parent",
            "action",
            "generated_successors",
            "frontier_before",
            "frontier_after",
            "explored",
            "g",
            "h",
            "f"
        ]

    def _extract_frontier_states(self, frontier):
        """Helper to inspect elements in Stack, Queue, or PriorityQueue."""
        states = []
        if hasattr(frontier, 'list'):
            # Stack or Queue
            for item in frontier.list:
                states.append(str(item[0]))
        elif hasattr(frontier, 'heap'):
            # PriorityQueue: items stored as (priority, count, item)
            for entry in frontier.heap:
                item = entry[2]
                states.append(str(item[0]))
        return states

    def log_step(self, expanded_state, parent, action, successors,
                 frontier_before_obj, frontier_after_obj, explored_set,
                 g=0, h=0, f=0):
        self.iteration += 1
        
        # Format successors as [(next_state, action, cost), ...]
        succ_formatted = [
            (str(s[0]), str(s[1]), s[2]) if len(s) >= 3 else (str(s[0]), str(s[1]))
            for s in successors
        ]

        frontier_before = self._extract_frontier_states(frontier_before_obj)
        frontier_after = self._extract_frontier_states(frontier_after_obj)
        explored_snapshot = [str(st) for st in explored_set]

        self.rows.append({
            "iteration": self.iteration,
            "expanded_state": str(expanded_state),
            "parent": str(parent) if parent is not None else "START",
            "action": str(action) if action is not None else "None",
            "generated_successors": str(succ_formatted),
            "frontier_before": str(frontier_before),
            "frontier_after": str(frontier_after),
            "explored": str(explored_snapshot),
            "g": g,
            "h": h,
            "f": f
        })

    def write_to_csv(self):
        """Flushes buffered traces into the evidence/ directory."""
        evidence_dir = "evidence"
        os.makedirs(evidence_dir, exist_ok=True)
        filename = f"{evidence_dir}/{self.algorithm_name}_{self.problem_name}_trace.csv"

        try:
            with open(filename, mode="w", newline="") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=self.headers)
                writer.writeheader()
                writer.writerows(self.rows)
        except IOError as e:
            print(f"Warning: Failed to write trace to {filename}: {e}")


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """

    logger = CSVTraceLogger("dfs", problem)
    frontier = util.Stack()
    explored = set()
  
    start_state = problem.getStartState()
    frontier.push((start_state, [], None, None))   # Elements in frontier: (current_state, actions_path, parent_state, incoming_action)

    while not frontier.isEmpty():
        frontier_before_copy = list(frontier.list)
        state, actions, parent, incoming_action = frontier.pop()

        if problem.isGoalState(state):
            logger.log_step(
                expanded_state=state,
                parent=parent,
                action=incoming_action,
                successors=[],
                frontier_before_obj=type('obj', (object,), {'list': frontier_before_copy}),
                frontier_after_obj=frontier,
                explored_set=explored,
                g=len(actions), h=0, f=len(actions)
            )
            logger.write_to_csv()
            return actions

        if state not in explored:
            explored.add(state)
            successors = problem.getSuccessors(state)

            for succ_state, succ_action, _ in successors:
                if succ_state not in explored:
                    frontier.push((succ_state, actions + [succ_action], state, succ_action))

            logger.log_step(
                expanded_state=state,
                parent=parent,
                action=incoming_action,
                successors=successors,
                frontier_before_obj=type('obj', (object,), {'list': frontier_before_copy}),
                frontier_after_obj=frontier,
                explored_set=explored,
                g=len(actions), h=0, f=len(actions)
            )

    logger.write_to_csv()
    return []


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    logger = CSVTraceLogger("bfs", problem)
    frontier = util.Queue()
    explored = set()
    frontier_states = set()

    start_state = problem.getStartState()
    frontier.push((start_state, [], None, None))
    frontier_states.add(start_state)

    while not frontier.isEmpty():
        frontier_before_copy = list(frontier.list)
        state, actions, parent, incoming_action = frontier.pop()
        frontier_states.discard(state)
        explored.add(state)

        if problem.isGoalState(state):
            logger.log_step(
                expanded_state=state,
                parent=parent,
                action=incoming_action,
                successors=[],
                frontier_before_obj=type('obj', (object,), {'list': frontier_before_copy}),
                frontier_after_obj=frontier,
                explored_set=explored,
                g=len(actions), h=0, f=len(actions)
            )
            logger.write_to_csv()
            return actions

        successors = problem.getSuccessors(state)
        for succ_state, succ_action, _ in successors:
            if succ_state not in explored and succ_state not in frontier_states:
                frontier_states.add(succ_state)
                frontier.push((succ_state, actions + [succ_action], state, succ_action))

        logger.log_step(
            expanded_state=state,
            parent=parent,
            action=incoming_action,
            successors=successors,
            frontier_before_obj=type('obj', (object,), {'list': frontier_before_copy}),
            frontier_after_obj=frontier,
            explored_set=explored,
            g=len(actions), h=0, f=len(actions)
        )

    logger.write_to_csv()
    return []


def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    logger = CSVTraceLogger("ucs", problem)
    frontier = util.PriorityQueue()
    explored = set()
    frontier_costs = {}

    start_state = problem.getStartState()
    frontier.push((start_state, [], 0, None, None), 0) # Stored item: (state, actions, current_cost, parent, incoming_action)
    frontier_costs[start_state] = 0

    while not frontier.isEmpty():
        frontier_before_copy = list(frontier.heap)
        state, actions, cost, parent, incoming_action = frontier.pop()

        if problem.isGoalState(state):
            logger.log_step(
                expanded_state=state,
                parent=parent,
                action=incoming_action,
                successors=[],
                frontier_before_obj=type('obj', (object,), {'heap': frontier_before_copy}),
                frontier_after_obj=frontier,
                explored_set=explored,
                g=cost, h=0, f=cost
            )
            logger.write_to_csv()
            return actions

        if state not in explored:
            explored.add(state)
            successors = problem.getSuccessors(state)

            for succ_state, succ_action, step_cost in successors:
                new_cost = cost + step_cost
                if succ_state not in explored:
                    # Update fringe if state is unvisited or if cheaper path found
                    if succ_state not in frontier_costs or new_cost < frontier_costs[succ_state]:
                        frontier_costs[succ_state] = new_cost
                        frontier.push(
                            (succ_state, actions + [succ_action], new_cost, state, succ_action),
                            new_cost
                        )

            logger.log_step(
                expanded_state=state,
                parent=parent,
                action=incoming_action,
                successors=successors,
                frontier_before_obj=type('obj', (object,), {'heap': frontier_before_copy}),
                frontier_after_obj=frontier,
                explored_set=explored,
                g=cost, h=0, f=cost
            )

    logger.write_to_csv()
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
