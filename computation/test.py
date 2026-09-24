import time, sys, solution, starter_kit
GRAPH = starter_kit.build_hardware_graph()

benches = sys.argv[1:] if len(sys.argv) > 1 else starter_kit.BENCHMARKS.keys()
total = 0.0

for name in benches:
    before = time.time()
    my_placement, my_routed = solution.solve(starter_kit.BENCHMARKS[name], GRAPH)
    elapsed = time.time() - before
    result = starter_kit.score_summary(starter_kit.BENCHMARKS[name], GRAPH, my_placement, my_routed)
    if result['valid']:
        total += result['score']
        print(f'[{name}] {result['score']:.1f} score {result['depth']} '
              f'depth {result['swap_count']} swaps {elapsed:.1f} seconds')
    else:
        print(f"[{name}] [invalid] {result['error']}")

if total > 0 and len(benches) > 1:
    print(f"[total] {total}")