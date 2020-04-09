#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = futoshiki_csp_model_1(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the Futoshiki puzzle.

1. futoshiki_csp_model_1 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only
      binary not-equal constraints for both the row and column constraints.

2. futoshiki_csp_model_2 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only n-ary
      all-different constraints for both the row and column constraints.

'''
from cspbase import *
import itertools


def futoshiki_csp_model_1(futo_grid):
    ##IMPLEMENT
    num_row = len(futo_grid)
    num_col = len(futo_grid[0])
    dom = []
    for i in range(num_row):
        dom.append(i + 1)

    vars = []
    for i in range(num_row):
        vars.append([])

    cons = []
    all_vars = []

    for i in range(num_row):
        for j in range(0, num_col, 2):
            if futo_grid[i][j] == 0:
                vars[i].append(Variable('V{}{}'.format(i + 1, j // 2 + 1), dom))
            else:
                vars[i].append(Variable('V{}{}'.format(i + 1, j // 2 + 1), [futo_grid[i][j]]))

            all_vars.append(vars[i][j // 2])
            ineq = futo_grid[i][j - 1]

            if (j != 0) and (ineq != '.'):
                var1 = vars[i][j // 2 - 1]
                var2 = vars[i][j // 2]
                ineq = futo_grid[i][j - 1]
                con = Constraint("C(V{}{} {} V{}{})".format(i + 1, j // 2, ineq, i + 1, j // 2 + 1), [var1, var2])
                sat_tuples = []
                for t in itertools.product(var1.domain(), var2.domain()):
                    if inequality(ineq, t[0], t[1]):
                        sat_tuples.append(t)
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

    for i in range(num_row):
        for j in range(num_row):
            for k in range(j + 1, num_row):
                var1 = vars[i][j]
                var2 = vars[i][k]
                con = Constraint("C(V{}{}, V{}{})".format(i + 1, j + 1, i + 1, k + 1), [var1, var2])
                sat_tuples = []
                for t in itertools.product(var1.domain(), var2.domain()):
                    if binary_diff(t[0], t[1]):
                        sat_tuples.append(t)
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

    for i in range(num_row):
        for j in range(num_row):
            for k in range(j + 1, num_row):
                var1 = vars[j][i]
                var2 = vars[k][i]
                con = Constraint("C(V{}{}, V{}{})".format(j + 1, i + 1, k + 1, i + 1), [var1, var2])
                sat_tuples = []
                for t in itertools.product(var1.domain(), var2.domain()):
                    if binary_diff(t[0], t[1]):
                        sat_tuples.append(t)
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

    csp = CSP("futoshiki_csp_model_1", all_vars)
    for con in cons:
        csp.add_constraint(con)

    return csp, vars


def futoshiki_csp_model_2(futo_grid):
    ##IMPLEMENT
    num_row = len(futo_grid)
    num_col = len(futo_grid[0])
    dom = []
    for i in range(num_row):
        dom.append(i + 1)

    vars = []
    for i in range(num_row):
        vars.append([])

    cons = []
    all_vars = []

    for i in range(num_row):
        for j in range(0, num_col, 2):
            if futo_grid[i][j] == 0:
                vars[i].append(Variable('V{}{}'.format(i + 1, j // 2 + 1), dom))
            else:
                vars[i].append(Variable('V{}{}'.format(i + 1, j // 2 + 1), [futo_grid[i][j]]))

            all_vars.append(vars[i][j // 2])
            ineq = futo_grid[i][j - 1]

            if (j != 0) and (ineq != '.'):
                var1 = vars[i][j // 2 - 1]
                var2 = vars[i][j // 2]
                con = Constraint("C(V{}{} {} V{}{})".format(i + 1, j // 2, ineq, i + 1, j // 2 + 1), [var1, var2])
                sat_tuples = []
                for t in itertools.product(var1.domain(), var2.domain()):
                    if inequality(ineq, t[0], t[1]):
                        sat_tuples.append(t)
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

    for i in range(num_row):
        con = Constraint("C_Row{}".format(i+1), vars[i])
        sat_tuples = []
        doms = []
        for var in vars[i]:
            doms.append(var.domain())
        for t in itertools.product(*doms):
            if all_diff(t):
                sat_tuples.append(t)
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)

    for i in range(num_row):
        col = []
        for j in range(num_row):
            col.append(vars[j][i])
        con = Constraint("C_Col{}".format(i+1), col)
        sat_tuples = []
        doms = []
        for var in col:
            doms.append(var.domain())
        for t in itertools.product(*doms):
            if all_diff(t):
                sat_tuples.append(t)
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)

    csp = CSP("futoshiki_csp_model_2", all_vars)
    for con in cons:
        csp.add_constraint(con)

    return csp, vars


def inequality(symbol, t1, t2):
    if symbol == "<":
        return t1 < t2
    elif symbol == ">":
        return t1 > t2

def binary_diff(t1, t2):
    return t1 != t2

def all_diff(t):
    return len(set(t)) == len(t)

