from __future__ import annotations

from collections import deque

def simulate(
    word: deque[str], accept_states: set[int], states: dict[int, dict[str, set[int]]]
) -> str:
    result = ""
    current_states: set[int] = {0}
    while len(word) != 0:
        symbol: str = word.popleft()
        next_states: set = set()
        for q in current_states:
            if symbol in states[q]:
                next_states.update(states[q][symbol])
        current_states = next_states

        in_accept: str = "N"
        for q in next_states:
            if q in accept_states:
                in_accept = "Y"
                break
        result += in_accept

    return result


word: str = input()
n, a, t = [int(x) for x in input().split(" ") if x != ""]
accept_states: set[int] = set([int(x) for x in input().split(" ") if x != ""])
states: dict[int, dict[str, set[int]]] = {}
for i in range(n):
    states[i] = {}
    line: list[str] = [x for x in input().split(" ") if x != ""]
    for j in range(1, int(line[0]) + 1):
        symbol: str = line[2 * j - 1]
        next: int = int(line[2 * j])
        if symbol in states[i]:
            states[i][symbol].update({next})
        else:
            states[i][symbol] = {next}


result: str = simulate(deque(word), accept_states, states)
print(result)
