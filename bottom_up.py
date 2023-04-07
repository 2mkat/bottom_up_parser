import enum

TERMS = ["!", "+", "*", "(", ")", "a", "b"]
N_TERMS = ["A", "B", "T", "M"]
RULES = [
    ["A", "!B!"],
    ["B", "T"],
    ["B", "T+B"],
    ["T", "M"],
    ["T", "M*T"],
    ["M", "a"],
    ["M", "b"],
    ["M", "(B)"]
]


class State(enum.Enum):
    q = 1
    b = 2
    t = 3


def bottom_up(word):
    l1 = []
    l2 = []
    state = State.q
    idx = 0

    while True:
        # print(f"s = {state} | L1 = {' '.join(l1)} | L2 = {' '.join(str(x) for x in l2)} | idx = {idx}")
        if state == State.q:
            while check_item(l1) is not None:
                reduce(l1, l2, check_item(l1))
            if idx < len(word):
                state, idx = shift(idx, l1, l2, word)
            elif len(l1) == 1 and l1[len(l1) - 1] == 'A':
                state = State.t
            else :
                state = State.b
        elif state == State.b:
            state, idx = reverse(l1, l2, idx, word)
        else:
            return output(l2)


# операция переноса символа в стек L1
def shift(idx, l1, l2, word):
    l1.append(word[idx])
    l2.append(-1)  # -1 - символ переноса s
    idx += 1

    return State.q, idx


# проверяем есть ли правило
def check_item(l1):
    l1_str = "".join(l1)
    idx = 0
    flag = False
    for i in range(len(RULES)):
        if l1_str.endswith(RULES[i][1]) and i >= idx:
            idx = i
            flag = True

    if flag:
        return idx
    return None


# операция свертки
def reduce(l1, l2, rule_idx):
    left = RULES[rule_idx][0]
    right = RULES[rule_idx][1]

    for i in range(len(right)):
        l1.pop()
    l1.append(left)
    l2.append(rule_idx)

    return State.q


def reverse(l1, l2, idx, word):
    if len(l1) == 0 or len(l2) == 0:
        return State.t, idx
    l1.pop()
    top_l2 = l2.pop()
    # 5г
    if top_l2 == -1 and idx != 0:
        idx -= 1
        return State.b, idx
    if idx == 0:
        # не принадлежит грамматике
        return State.t, idx

    if top_l2 != -1:
        for c in RULES[top_l2][1]:
            l1.append(c)

        # 5a проверяем возможны ли новые свертки
        new_rule = check_item(l1)
        if new_rule is None:
            new_rule = -1

        if new_rule > top_l2:
            right = RULES[new_rule][1]
            left = RULES[new_rule][0]
            for i in range(len(right)):
                l1.pop()
            l1.append(left)
            l2.append(new_rule)
            return State.q, idx
        else:
            # 5б
            if idx == len(word):
                return State.b, idx
            # 5в
            if idx != len(word):
                l1.append(word[idx])
                idx += 1
                l2.append(-1)
                return State.q, idx
def output(l2):
    if len(l2) == 0:
        return None

    idx = 0
    while idx < len(l2):
        if l2[idx] == -1:
            l2.pop(idx)
        else:
            l2[idx] += 1
            idx += 1

    return "".join(str(x) for x in l2)


if __name__ == "__main__":
    assert bottom_up("!a+b!") == "6474231", "Should be 6474231"
    assert bottom_up("!a*b!") == "674521", "Should be 674521"
    assert bottom_up("!(a+b)*(b+a)!") == "647423874642384521", "Should be 647423874642384521"
    assert bottom_up("!b*a+a*b!") == "76456745231", "Should be 76456745231"
    assert bottom_up("!(a+b)*a+b*a!") == "64742386457645231", "Should be 64742386457645231"
    assert bottom_up("!(a+b*a)*(b*b+a*(a+b+a))!") == "647645238774566474642338452384521", "Should be 647645238774566474642338452384521"
    assert bottom_up("!a+*b!") is None, "Should be None"
    assert bottom_up("a+b*a+b") is None, "Should be None"
    assert bottom_up("a!b") is None, "Should be None"
    assert bottom_up("!a(b+a()!") is None, "Should be None"
    assert bottom_up("!a*(b+a)*b!") == "67464238745521", "Should be 67464238745521"
    print("Everything passed")

    #term = str(input())
    #print("Номеров продукций левого вывода: {}", bottom_up(term))