from collections import deque

from NFA import NFA

# Converts RegEx string written infix into postfix
def infix_to_postfix(regex: str) -> str:
    # insert concatenation operator "?"
    infix: deque[str] = deque(insert_concat_symbol(regex))
    # precedence priorities for operations
    priors: dict[str, int] = {"*": 1, "?": 2, "|": 3}
    # stack for Shunting-Yard algorithm
    stack: deque[str] = deque()
    # postfix representation of regex
    postfix: str = ""

    while len(infix) != 0:
        symbol = infix.popleft()

        if symbol in priors:
            while (
                len(stack) != 0
                and stack[0] != "("
                and priors[stack[0]] <= priors[symbol]
            ):
                postfix += stack.popleft()
            stack.appendleft(symbol)

        elif symbol == "(":
            if infix[0] == ")":
                infix.popleft()
                postfix += "$"  # for an empty string
            else:
                stack.appendleft(symbol)

        elif symbol == ")":
            while stack[0] != "(":
                postfix += stack.popleft()
            stack.popleft()

        else:
            postfix += symbol

    while len(stack) != 0:
        postfix += stack.popleft()

    return postfix


# Let the concatenate symbol be ? for the sake of simplicity
def insert_concat_symbol(regex: str) -> str:
    result: str = ""

    not_conc_left: str = "|("
    not_conc_right: str = "|*)"

    for i in range(len(regex)):
        result += regex[i]

        if i + 1 == len(regex):
            break

        if regex[i] not in not_conc_left and regex[i + 1] not in not_conc_right:
            result += "?"

    return result


# Constructs an NFA from regex
def regex_to_nfa(regex: str) -> NFA:
    symbols: deque[str] = deque(regex)

    stack: deque[NFA] = deque()

    while len(symbols) != 0:
        symbol = symbols.popleft()
        if symbol == "*":
            nfa: NFA = stack.popleft()
            result: NFA = NFA.star(nfa)
            stack.appendleft(result)
        elif symbol == "?":
            nfa2: NFA = stack.popleft()
            nfa1: NFA = stack.popleft()
            result = NFA.concatenate(nfa1, nfa2)
            stack.appendleft(result)
        elif symbol == "|":
            nfa2 = stack.popleft()
            nfa1 = stack.popleft()
            result = NFA.union(nfa1, nfa2)
            stack.appendleft(result)
        else:
            nfa = NFA.unit_nfa(symbol)
            stack.appendleft(nfa)
    return stack.popleft()


regex: str = infix_to_postfix(input())
nfa: NFA = regex_to_nfa(regex)
nfa.print()
