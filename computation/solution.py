import dataclasses, networkx, itertools, heapq

@dataclasses.dataclass
class State:
    positions: dict
    clock: dict
    swaps: int = 0
    route: tuple = ()

def solve(program, hardware_graph) -> tuple[dict, tuple]:
    best = beam_search(program, hardware_graph)
    pos = best.positions
    for kind, *locs in reversed(best.route):
        pos = exchange(pos, *locs) if kind == 'SWAP' else pos
    return pos, best.route

def beam_search(program, graph) -> State:
    paths = dict(networkx.all_pairs_shortest_path(graph))
    distance = dict(networkx.all_pairs_shortest_path_length(graph))
    states = [State({}, dict.fromkeys(graph, 0))]
    for i, gate in enumerate(program):
        upcoming = program[i + 1:]
        candidates = proactive_swap(run_gate(states, gate, graph, paths), upcoming, graph)
        states = keep_best(candidates, upcoming, distance)
    return states[0]

def apply(state, kind, *locations):
    positions, clock, swaps = state.positions, state.clock, state.swaps
    a, b = locations
    layer = 1 + max(clock[a], clock[b])
    clock = clock | {a: layer, b: layer}
    if kind == 'SWAP':
        positions = exchange(positions, a, b)
        swaps += 1
    return State(positions, clock, swaps, state.route + ((kind, *locations),))

def exchange(positions, a, b):
    moves = {a: b, b: a}
    return {qubit: moves.get(location, location) for qubit, location in positions.items()}

def run_gate(states, gate, graph, paths):
    qubits = gate[1:]
    for state in states:
        for placed in placements(state, qubits, graph):
            yield run_two_qubit_gate(placed, *qubits, paths)

def placements(state, qubits, graph):
    new = [qubit for qubit in qubits if qubit not in state.positions]
    free = [location for location in graph if location not in state.positions.values()]
    choices = list(itertools.permutations(free, len(new)))
    if len(new) == 2:
        choices = [pair for pair in choices if graph.has_edge(*pair)] or choices
    for locations in choices:
        yield dataclasses.replace(state, positions=state.positions | dict(zip(new, locations)))

def run_two_qubit_gate(state, a, b, paths):
    path = paths[state.positions[a]][state.positions[b]]
    for left, right in itertools.pairwise(path[:-1]):
        state = apply(state, 'SWAP', left, right)
    return apply(state, '2Q', state.positions[a], state.positions[b])

def proactive_swap(states, upcoming, graph):
    needed = {qb for gate in upcoming for qb in gate[1:]}
    edges = list(graph.edges)
    for state in states:
        yield state
        busy = {loc for qb, loc in state.positions.items() if qb in needed}
        for a, b in edges:
            if a in busy or b in busy:
                yield apply(state, 'SWAP', a, b)

def keep_best(states, upcoming, distance, width=2048, lookahead=20 ):
    layout = lambda st: tuple(sorted(st.positions.items()))
    score = lambda st: st.swaps + max(st.clock.values()) / 2

    cheapest = {}
    for st in sorted(states, key=score):
        cheapest.setdefault(layout(st), st)
    pairs = [ga[1:] for ga in upcoming if ga[0] == '2Q'][:lookahead]

    def rank(state):
        where = state.positions
        future_swaps = sum(distance[where[a]][where[b]] - 1 for a, b in pairs if a in where and b in where)
        return score(state) + future_swaps * 0.5, layout(state)

    return heapq.nsmallest(width, cheapest.values(), key=rank)