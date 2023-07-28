from __future__ import annotations

from copy import deepcopy

# Unit NFAs of this class have following properties:
#   (1) The simplest NFA has either a single state or 2 states
#   (2) If it accepts empty string only, then:
#           states = {0}, accept_states = {0}, no arrows
#   (3) If NFA accepts a single symbol then:
#           states = {0, 1}, accept_states = {1}, 0 -> 1 by the symbol
#
# Every NFA is built from one of the unit NFAs described above
# thus through the constructions below:
#   (1) Arrows never go in the start state
#   (2) No NFA contains an Epsilon transition
#   (3) Number of states in NFA is always at most length(RegEx)+1,


class NFA:
    def __init__(
        self, accept_states: set[int], states: dict[int, dict[str, set[int]]]
    ) -> None:
        # list of accept states
        self.accept_states: set[int] = accept_states
        # mapping for transitions
        self.states: dict[int, dict[str, set[int]]] = states

    @classmethod
    def union(cls, nfa1: NFA, nfa2: NFA) -> NFA:
        nfa2_start: int = len(nfa1.states) - 1
        nfa2 = NFA.shift_numbering(nfa2, nfa2_start)

        new_accept_states: set[int] = deepcopy(nfa2.accept_states)
        if nfa2_start in nfa2.accept_states:
            new_accept_states.remove(nfa2_start)
            new_accept_states.update({0})
        new_accept_states.update(deepcopy(nfa1.accept_states))

        new_states: dict[int, dict[str, set[int]]] = deepcopy(nfa2.states)
        new_states.update(nfa1.states)

        for symbol in nfa2.states[nfa2_start]:
            if symbol in nfa1.states[0]:
                new_states[0][symbol].update(deepcopy(nfa2.states[nfa2_start][symbol]))
            else:
                new_states[0][symbol] = deepcopy(nfa2.states[nfa2_start][symbol])

        return cls(new_accept_states, new_states)

    @classmethod
    def concatenate(cls, nfa1: NFA, nfa2: NFA) -> NFA:
        nfa2_start: int = len(nfa1.states) - 1
        nfa2 = NFA.shift_numbering(nfa2, nfa2_start)

        new_accept_states: set[int] = deepcopy(nfa2.accept_states)
        if nfa2_start in new_accept_states:
            new_accept_states.remove(nfa2_start)
            new_accept_states.update(deepcopy(nfa1.accept_states))

        new_states: dict[int, dict[str, set[int]]] = deepcopy(nfa2.states)
        new_states.update(nfa1.states)

        for state in nfa1.accept_states:
            for symbol in nfa2.states[nfa2_start]:
                if symbol in nfa1.states[state]:
                    new_states[state][symbol].update(
                        deepcopy(nfa2.states[nfa2_start][symbol])
                    )
                else:
                    new_states[state][symbol] = deepcopy(
                        nfa2.states[nfa2_start][symbol]
                    )
        return cls(new_accept_states, new_states)

    @classmethod
    def star(cls, nfa: NFA) -> NFA:
        new_accept_states: set[int] = deepcopy(nfa.accept_states)
        new_accept_states.update({0})

        new_states: dict[int, dict[str, set[int]]] = deepcopy(nfa.states)
        new_states.update({0: {}})
        for state in new_accept_states:
            for symbol in nfa.states[0]:
                if symbol in new_states[state]:
                    new_states[state][symbol].update(deepcopy(nfa.states[0][symbol]))
                else:
                    new_states[state][symbol] = deepcopy(nfa.states[0][symbol])

        return cls(new_accept_states, new_states)

    @classmethod
    def shift_numbering(cls, nfa: NFA, n: int) -> NFA:
        new_accept_states: set[int] = {q + n for q in nfa.accept_states}

        new_states: dict[int, dict[str, set[int]]] = {}
        for state in nfa.states:
            new_transitions: dict[str, set[int]] = {}
            for symbol in nfa.states[state]:
                new_transitions[symbol] = {q + n for q in nfa.states[state][symbol]}
            new_states[state + n] = new_transitions

        return cls(new_accept_states, new_states)

    @classmethod
    def unit_nfa(cls, symbol: str) -> NFA:
        accept_states: set[int] = set()
        states: dict[int, dict[str, set[int]]] = {}
        if symbol == "$":
            accept_states = {0}
            states = {0: {}}
        else:
            accept_states = {1}
            states = {0: {symbol: {1}}, 1: {}}
        return cls(accept_states, states)

    def count_transitions(self) -> int:
        count: int = 0
        for state in self.states:
            for symbol in self.states[state]:
                count += len(self.states[state][symbol])
        return count

    def print(self) -> None:
        print(
            str(len(self.states))
            + " "
            + str(len(self.accept_states))
            + " "
            + str(self.count_transitions())
        )

        acc_states: str = ""
        for q in self.accept_states:
            acc_states += str(q) + " "
        print(acc_states[:-1])

        for q in range(len(self.states)):
            pairs: str = ""
            count: int = 0
            for symbol in self.states[q]:
                count += len(self.states[q][symbol])
                for next in self.states[q][symbol]:
                    pairs += symbol + " " + str(next) + " "
            print(str(count) + " " + pairs)
