# # Метод простого предшествования (с использованием функций предшествования, построенных итерационным методом Флойда)
import re

TERMS = ["!", "+", "*", "(", ")", "a", "b"]
N_TERMS = ["A", "B", "B`", "T", "T`", "M"]
RULES = {
    "A": ["!B!"],
    "B": ["B`"],
    "B`": ["T", "B`+T"],
    "T": ["T`"],
    "T`": ["M", "T`*M"],
    "M": ["a", "b", "(B)"]
}


# Построение множеств крайних правых и крайних левых символов
def build_L_R_set(L, R):
    for non_term in RULES:
        L[non_term] = []
        R[non_term] = []

    for non_term in L:
        for right_rule in RULES.get(non_term):
            # первый случай, когда в правой части стоит один символ
            if N_TERMS.count(right_rule) or TERMS.count(right_rule):
                L[non_term].append(right_rule)
                R[non_term].append(right_rule)
            # T`*M, B`+T
            if re.search("(`)[+*]", right_rule) is not None:
                if not L[non_term].count(right_rule[:len(right_rule) - 2]):
                    L[non_term].append(right_rule[:len(right_rule) - 2])
                if not R[non_term].count(right_rule[-1]):
                    R[non_term].append(right_rule[-1])
            # (B) (A) !T! !B!
            if re.search("(!|\()[A-Z]", right_rule) is not None:
                L[non_term].append(right_rule[:len(right_rule) - 2])
                R[non_term].append(right_rule[-1])

    for non_term in N_TERMS:
        for el in L[non_term]:
            if N_TERMS.count(el):
                for term in L[el]:
                    if not L[non_term].count(term):
                        L[non_term].append(term)

        for el in R[non_term]:
            if N_TERMS.count(el):
                for term in R[el]:
                    if not R[non_term].count(term):
                        R[non_term].append(term)
def build_matrix(L, R):
    s_i = []
    s_j = []
    for i in N_TERMS:
        s_i.append(i)
        s_j.append(i)

    for i in TERMS:
        s_i.append(i)
        s_j.append(i)

    s_i.remove('A')
    s_j.remove('A')

    matrix = [[' ' for c in range(len(s_i) + 1)] for r in range(len(s_j) + 1)]
    s_j.insert(0, ' ')
    matrix[0] = s_j
    for r in range(len(matrix)):
        for c in range(len(matrix)):
            if c == 0 and r > 0:
                matrix[r][c] = s_i[r - 1]

    # формируем правила, которые длиной больше 1
    vector_rules = []
    for rule in RULES:
        for right_rule in RULES.get(rule):
            if len(right_rule) > 1 and right_rule not in N_TERMS:
                vector_rules.append(right_rule)

    for rule in range(len(vector_rules)):
        vector_rules[rule] = list(vector_rules[rule])
        if '`' in vector_rules[rule]:
            idx = vector_rules[rule].index('`')
            vector_rules[rule][idx - 1] += vector_rules[rule][idx]
            vector_rules[rule].remove('`')

    # определяем отношение равенства =.
    for rule in vector_rules:
        for idx_el in range(len(rule) - 1):
            # print(f'{rule[idx_el]}{rule[idx_el + 1]}')
            idx_s_j = 0
            idx_s_i = 0
            for r in range(len(matrix[0])):
                if rule[idx_el] == matrix[0][r]:
                    idx_s_i = r
                if rule[idx_el + 1] == matrix[0][r]:
                    idx_s_j = r
            matrix[idx_s_i][idx_s_j] = '=.'

    # определяем отношение равенства <.
    # T <. N
    for rule in vector_rules:
        for idx_el in range(len(rule) - 1):
            if rule[idx_el] in TERMS and rule[idx_el + 1] in N_TERMS:
                # print(f'{rule[idx_el]}{rule[idx_el + 1]}')
                idx_s_i = 0

                for r in range(len(matrix[0])):
                    if rule[idx_el] == matrix[0][r]:
                        idx_s_i = r
                for term_from_L in L.get(rule[idx_el + 1]):
                    for k in range(len(matrix[0])):
                        if term_from_L == matrix[0][k]:
                            matrix[idx_s_i][k] = '<.'
    # определяем отношение равенства .>
    # N .> T
    for rule in vector_rules:
        for idx_el in range(len(rule) - 1):
            if rule[idx_el] in N_TERMS and rule[idx_el + 1] in TERMS:
                #print(f'{rule[idx_el]}{rule[idx_el + 1]}')
                idx_s_j = 0
                for r in range(len(matrix[0])):
                    if rule[idx_el + 1] == matrix[0][r]:
                        idx_s_j = r
                for term_from_R in R.get(rule[idx_el]):
                    for k in range(len(matrix[0])):
                        if term_from_R == matrix[0][k]:
                            matrix[k][idx_s_j] = '.>'

    # определяем отношение равенства .>
    # N .> N

    for row in matrix:
            print(row)
    pass

def main():
    L = {}
    R = {}
    build_L_R_set(L, R)
    build_matrix(L, R)


if __name__ == "__main__":
    main()

# alt = {
#     "A1": "!B!",
#     "B1": "B`",
#     "B`1": "T",
#     "B`2": "B`+T",
#     "T1": "T`",
#     "T`1": "M",
#     "T`2": "T`*M",
#     "M1": "a",
#     "M2": "b",
#     "M3": "(B)",
# }
# L = {}
# R = {}
# for x in alt.keys():
#     st = x[: len(x) - 1]
#     L[st] = []
#     R[st] = []
# for x in L.keys():
#     tmp = x + "1"
#     while alt.get(tmp) != None:
#         val = alt.get(tmp)
#         l_tmp = L.get(x)
#         if len(val) > 1:
#             if val[1] == "`":
#                 if (val[0] + val[1]) in l_tmp:
#                     pass
#                 else:
#                     l_tmp.append(val[0] + val[1])
#             else:
#                 if (val[0]) in l_tmp:
#                     pass
#                 else:
#                     l_tmp.append(val[0])
#         else:
#             if (val[0]) in l_tmp:
#                 pass
#             else:
#                 l_tmp.append(val[0])
#         L[x] = l_tmp
#         r_tmp = R.get(x)
#         if val[len(val) - 1] == "`":
#             if (val[len(val) - 2] + val[len(val) - 1]) in r_tmp:
#                 pass
#             else:
#                 r_tmp.append(val[len(val) - 2] + val[len(val) - 1])
#         else:
#             if (val[len(val) - 1]) in r_tmp:
#                 pass
#             else:
#                 r_tmp.append(val[len(val) - 1])
#         R[x] = r_tmp
#         tmp = tmp[: len(tmp) - 1] + chr(ord(tmp[len(tmp) - 1]) + 1)
# l_keys = list(L.keys())
# for i in range(1, len(l_keys) - 1):
#     append_l = L.get(l_keys[i])
#     for j in range(i + 1, len(l_keys)):
#         tmp_l = L.get(l_keys[j])
#         for x in tmp_l:
#             if x in append_l:
#                 pass
#             else:
#                 append_l.append(x)
#     L[l_keys[i]] = append_l
# r_keys = list(R.keys())
# for i in range(1, len(r_keys) - 1):
#     append_r = R.get(r_keys[i])
#     for j in range(i + 1, len(r_keys)):
#         tmp_r = R.get(r_keys[j])
#         for x in tmp_r:
#             if x in append_r:
#                 pass
#             else:
#                 append_r.append(x)
#     R[r_keys[i]] = append_r
#
# mp_idx = []
# for x in alt.keys():
#     tmp = alt.get(x)
#     tmp_list = []
#     for y in tmp:
#         if y != "`":
#             tmp_list.append(str(y))
#         else:
#             tmp_list[len(tmp_list) - 1] = tmp_list[len(tmp_list) - 1] + "`"
#     for y in tmp_list:
#         if y in mp_idx:
#             pass
#         else:
#             mp_idx.append(y)
#
# print(mp_idx)
# mp = []
# for i in mp_idx:
#     mp_str = []
#     for j in mp_idx:
#         mp_str.append("")
#     mp.append(mp_str)
# for x in alt.keys():
#     tmp = alt.get(x)
#     tmp_list = []
#     for y in tmp:
#         if y != "`":
#             tmp_list.append(str(y))
#         else:
#             tmp_list[len(tmp_list) - 1] = tmp_list[len(tmp_list) - 1] + "`"
#     if len(tmp_list) > 1:
#         for i in range(0, len(tmp_list) - 1):
#             v = mp_idx.index(tmp_list[i])
#             g = mp_idx.index(tmp_list[i + 1])
#             mp[v][g] = "=."
# print(mp)
# T = ["!", "(", "*", "+", ")"]
# NT = ["B", "B`", "T", "T`", "M"]
# for x in alt.keys():
#     tmp = alt.get(x)
#     tmp_list = []
#     for y in tmp:
#         if y != "`":
#             tmp_list.append(str(y))
#         else:
#             tmp_list[len(tmp_list) - 1] = tmp_list[len(tmp_list) - 1] + "`"
#     if len(tmp_list) > 1:
#         for i in range(0, len(tmp_list) - 1):
#             if (tmp_list[i] in T) and (tmp_list[i + 1] in NT):
#                 v = mp_idx.index(tmp_list[i])
#                 tmp_l = L.get(tmp_list[i + 1])
#                 for j in tmp_l:
#                     g = mp_idx.index(j)
#                     mp[v][g] = "<."
# for x in alt.keys():
#     tmp = alt.get(x)
#     tmp_list = []
#     for y in tmp:
#         if y != "`":
#             tmp_list.append(str(y))
#         else:
#             tmp_list[len(tmp_list) - 1] = tmp_list[len(tmp_list) - 1] + "`"
#     if len(tmp_list) > 1:
#         for i in range(0, len(tmp_list) - 1):
#             if (tmp_list[i] in NT) and (tmp_list[i + 1] in T):
#                 g = mp_idx.index(tmp_list[i + 1])
#                 tmp_r = R.get(tmp_list[i])
#                 for j in tmp_r:
#                     v = mp_idx.index(j)
#                     mp[v][g] = ".>"
#
#
# in_str = str(input("Enter string ="))
# print("L=")
# for x in L:
#     print(x, "\t", L.get(x))
# print("\nR=")
# for x in R:
#     print(x, "\t", R.get(x))
# res = ""
# for x in mp_idx:
#     res += "\t" + x
# print(res)
# for x in range(len(mp_idx)):
#     res = ""
#     for y in mp[x]:
#         res += y + "\t"
#     print(mp_idx[x], "\t", res)
# idx_alt = {
#     "A1": "1",
#     "B1": "2",
#     "B`1": "3",
#     "B`2": "4",
#     "T1": "5",
#     "T`1": "6",
#     "T`2": "7",
#     "M1": "8",
#     "M2": "9",
#     "M3": "10",
# }
# res = ""
# stack1 = []
# stack1.append(in_str[0])
# in_str = in_str[1:]
# while stack1[0] != "A":
#     if len(in_str) == 0:
#         svertka = []
#         svertka = [stack1.pop()] + svertka
#         while (
#             len(stack1) > 0
#             and mp[mp_idx.index(stack1[len(stack1) - 1])][mp_idx.index(svertka[0])]
#             != "<."
#         ):
#             svertka = [stack1.pop()] + svertka
#         st_svertka = ""
#         for x in svertka:
#             st_svertka += x
#         flag = True
#         for x in alt.keys():
#             if alt.get(x) == st_svertka:
#                 res += idx_alt.get(x) + " "
#                 flag = False
#                 stack1.append(x[: len(x) - 1])
#                 break
#         if flag:
#             res = "Can't represent this string"
#             break
#         continue
#
#     if (mp[mp_idx.index(stack1[len(stack1) - 1])][mp_idx.index(in_str[0])] == "<.") or (
#         mp[mp_idx.index(stack1[len(stack1) - 1])][mp_idx.index(in_str[0])] == "=."
#     ):
#         stack1.append(in_str[0])
#         in_str = in_str[1:]
#         continue
#     if mp[mp_idx.index(stack1[len(stack1) - 1])][mp_idx.index(in_str[0])] == ".>":
#         svertka = []
#         svertka = [stack1.pop()] + svertka
#         while (
#             len(stack1) > 0
#             and mp[mp_idx.index(stack1[len(stack1) - 1])][mp_idx.index(svertka[0])]
#             != "<."
#         ):
#             svertka = [stack1.pop()] + svertka
#         st_svertka = ""
#         for x in svertka:
#             st_svertka += x
#         flag = True
#         for x in alt.keys():
#             if alt.get(x) == st_svertka:
#                 res += idx_alt.get(x) + " "
#                 flag = False
#                 stack1.append(x[: len(x) - 1])
#                 break
#         if flag:
#             res = "Can't represent this string"
#             break
#         continue
#     res = "Can't represent this string"
#     break
# print(res)
