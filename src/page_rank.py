from typing import List
from collections import namedtuple

Row = namedtuple("Row", ["src", "degree", "destinations"])


def l1_norm(vector):
    return sum(abs(x) for x in vector)


def naive_pagerank(M: List[Row], beta=0.80, epsilon=0.00001):
    """
    For now, let us assume that we are passed M as described in
    the README section "Computing PageRank on Big Graphs" -
    When r^{new} fits into memory.

    Returns a vector r of PageRanks, where r[i] is the importance of
    the page at the i-th index of M.
    """
    N = len(M)
    r = [1/N] * N
    has_converged = False

    while not has_converged:
        r_old = r.copy()
        for r_idx in range(len(r)):
            current_page = M[r_idx].src
            # Sum the votes of all nodes pointing to r[idx]
            importances = []
            in_degree = 0
            for matrix_idx, node in enumerate(M):
                if current_page in node.destinations:
                    # Get importance of page pointing to current page
                    r_i = r_old[matrix_idx]
                    d_i = node.degree
                    importances.append(r_i / d_i)
                    in_degree += 1

            if in_degree > 0:
                r[r_idx] = beta * sum(importances)
            else:
                r[r_idx] = 0

        # Evenly redistribute the lost PageRank
        to_distribute = (1 - sum(r)) / N
        for i in range(len(r)):
            r[i] += to_distribute

        distance_vector = [x - y for x, y in zip(r, r_old)]
        if l1_norm(distance_vector) < epsilon:
            has_converged = True

    return r


if __name__ == "__main__":
    from math import isclose
    row_1 = Row("y", 2, set(["y", "a"]))
    row_2 = Row("a", 2, set(["y", "m"]))
    row_3 = Row("m", 0, set())
    example_M_1 = [row_1, row_2, row_3]

    print(naive_pagerank(example_M_1))

    row_4 = Row("y", 2, set(["y", "a"]))
    row_5 = Row("a", 2, set(["y", "m"]))
    row_6 = Row("m", 1, set(["m"]))
    example_M_2 = [row_4, row_5, row_6]

    ranks = naive_pagerank(example_M_2)
    y_rank, a_rank, m_rank = ranks
    print(ranks)
    assert isclose(y_rank, 7/33, rel_tol=0.01)
    assert isclose(a_rank, 5/33, rel_tol=0.01)
    assert isclose(m_rank, 21/33, rel_tol=0.01)
