def alpha_detector(G, k: float):
    """
    Implementation of alpha detection algorithm as a function
    Inputs:
        G: Graph
        k: Percentage of vertices to consider for alphas
    Output:
        X: Set of alpha vertices
    """

    numrank = []
    degrank = []

    for u, H in G.items():
        # fetching N(u) as neighbors of u and W(u) as weights of edges between u and its neighbors from H(u)
        Nu, Wu = H[0], H[1]
        # building NumRank and DegRank
        numrank.append((len(Nu), u))  # δ(u) = |N(u)| = len(Nu)
        degrank.append((sum(Wu), u))  # δ*(u) = sum of W(u) = sum(Wu)

    # Sort(NumRank) by δ(u) descending order
    numrank = sorted(numrank, reverse=True)
    # Sort(DeдRank) by δ∗(u) descending order
    degrank = sorted(degrank, reverse=True)

    # Truncate(NumRank) to retain top k% elements
    numrank = [v for s, v in numrank[:int(len(numrank) * k)+1]]
    # Truncate(DeдRank) to retain top k% elements
    degrank = [v for s, v in degrank[:int(len(degrank) * k)+1]]

    # X = NumRank ∩ DeдRank
    # Sort NumRank and DegRank to build X optimally in O(N logN) instead of O(N^2)
    numrank.sort()
    degrank.sort()
    numrank_index, degrank_index, len_ranks = 0, 0, len(numrank)
    X = []
    while numrank_index < len_ranks and degrank_index < len_ranks:
        if numrank[numrank_index] == degrank[degrank_index]:
            X.append(numrank[numrank_index])
            numrank_index += 1
            degrank_index += 1
        elif numrank[numrank_index] < degrank[degrank_index]:
            numrank_index += 1
        else:
            degrank_index += 1
    return X

