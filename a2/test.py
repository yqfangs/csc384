from cspbase import *
from futoshiki_csp import *
from propagators import *

def print_sol(var_array):
    for i in range(len(var_array)):
        sol = []
        for j in range(len(var_array)):
            sol.append(var_array[i][j].get_assigned_value())
        print(sol)

puzzle1 =     [[0,'>',0,'.',2,'.',0,'.',9,'.',0,'.',0,'.',6,'.',0],
     [0,'.',4,'.',0,'.',0,'.',0,'.',1,'.',0,'.',0,'.',8],
     [0,'.',7,'.',0,'<',0,'.',2,'.',0,'.',0,'.',0,'.',3],
     [5,'.',0,'.',0,'.',0,'.',0,'.',0,'.',3,'.',0,'.',0],
     [0,'.',0,'.',1,'.',0,'.',6,'.',0,'.',5,'.',0,'.',0],
     [0,'.',0,'<',3,'.',0,'.',0,'.',0,'.',0,'.',0,'.',6],
     [1,'.',0,'.',0,'.',0,'.',5,'.',7,'.',0,'.',4,'.',0],
     [0,'>',0,'.',0,'.',9,'.',0,'<',0,'.',0,'.',2,'.',0],
     [0,'.',2,'.',0,'.',0,'.',8,'.',0,'<',1,'.',0,'.',0]]

if __name__=="__main__":
    # csp, var_array = futoshiki_csp_model_1(puzzle1)
    # csp.print_all()
    # solver = BT(csp)
    # solver.bt_search(prop_FC)
    # print_sol(var_array)

    # csp, var_array = futoshiki_csp_model_2(puzzle1)
    # csp.print_all()
    # print('finish building')
    # solver = BT(csp)
    # solver.bt_search(prop_GAC,ord_mrv)
    # # sol = []
    # print_sol(var_array)
