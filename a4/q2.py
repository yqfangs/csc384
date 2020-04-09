from bnetbase import *

A = Variable("A", [True, False])
B = Variable("B", [True, False])
C = Variable("C", [True, False])
D = Variable("D", [True, False])
E = Variable("E", [True, False])
F = Variable("F", [True, False])
G = Variable("G", [True, False])
H = Variable("H", [True, False])
I = Variable("I", [True, False])

F1 = Factor("f(A)", [A])
F1.add_values([[True, 0.9], [False, 0.1]])

F2 = Factor("f(B,A,H)", [B, A, H])
F2.add_values([[True, True, True, 1.0], [False, True, True, 0.0],
             [True, True, False, 0.0], [False, True, False, 1.0],
             [True, False, True, 0.5], [False, False, True, 0.5],
             [True, False, False, 0.6], [False, False, False, 0.4]])

F3 = Factor("f(C,B,G)", [C, B, G])
F3.add_values([[True, True, True, 0.9], [False, True, True, 0.1],
             [True, True, False, 0.9], [False, True, False, 0.1],
             [True, False, True, 0.1], [False, False, True, 0.9],
             [True, False, False, 1.0], [False, False, False, 0.0]])

F4 = Factor("f(D,C,F)", [D, C, F])
F4.add_values([[True, True, True, 0.0], [False, True, True, 1.0],
             [True, True, False, 1.0], [False, True, False, 0.0],
             [True, False, True, 0.7], [False, False, True, 0.3],
             [True, False, False, 0.2], [False, False, False, 0.8]])

F5 = Factor("f(E,C)", [E, C])
F5.add_values([[True, True, 0.2], [False, True, 0.8],
             [True, False, 0.4], [False, False, 0.6]])

F6 = Factor("f(F)", [F])
F6.add_values([[True, 0.1], [False, 0.9]])

F7 = Factor("f(G)", [G])
F7.add_values([[True, 1.0], [False, 0.0]])

F8 = Factor("f(H)", [H])
F8.add_values([[True, 0.5], [False, 0.5]])

F9 = Factor("f(I, B)", [I, B])
F9.add_values([[True, True, 0.3], [False, True, 0.7],
             [True, False, 0.9], [False, False, 0.1]])

bn = BN("q2", [A, B, C, D, E, F, G, H, I], [F1, F2, F3, F4, F5, F6, F7, F8, F9] )

if __name__ == '__main__':
    print("P(B|A)\n")
    A.set_evidence(True)
    r1 = VE(bn, B, [A])
    print(r1)

    print("P(C|A)\n")
    A.set_evidence(True)
    r2 = VE(bn, C, [A])
    print(r2)

    print("P(C|A,E)\n")
    A.set_evidence(True)
    E.set_evidence(False)
    r3 = VE(bn, C, [A, E])
    print(r3)

    print("P(C|A,F)\n")
    A.set_evidence(True)
    F.set_evidence(False)
    r4 = VE(bn, C, [A, F])
    print(r4)
    print("\n")

