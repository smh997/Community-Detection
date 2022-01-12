from threading import Thread, Lock

Graph = {}
Origin = []
Comm = {}
Visited = []
add = 0
rand_it = 0  # used for iteration over rands
rands = []


def propagator(chunk_of_alphas, semaphore):
    """
    Implemented to assign it to a thread in order to propagate labels in parallel.
    Inputs:
        chunked_of_alphas: a list of alphas or current origins of information (labels)
        semaphore: a lock for controlling parallel use of resources
    Output:
        No output
    """
    global Origin, Graph, rands, add, Comm, rand_it, Visited
    for u in chunk_of_alphas:
        if u in Graph:  # N(u) ≠ ∅
            count_of_unlabeled = 0  # used for checking "Comm[x] ≠ 0 ∀x ∈ N(u)"
            Nu, W = Graph[u][0], Graph[u][1]
            for v, Wuv in zip(Nu, W):  # for all v ∈ N(u) do
                if Comm[v] == 0:  # Comm[v] == 0, i.e. v is not visited
                    count_of_unlabeled += 1
                    random_probability = float(rands[(rand_it % len(rands))])
                    # P(u,v) = Wuv^(1/4) / δ∗^(1/4)
                    Puv = (Wuv/sum(W))**(1/4)
                    if Puv >= random_probability:  # if P(u,v) is greater than random_probability we can propagate
                        semaphore.acquire()
                        if Comm[v] == 0:  # maybe another u in another thread propagated v while we were facing lock!
                            # Comm[v] ← u: propagating label over v
                            Comm[v] = Comm[u]
                            # Append(Origin, v): activating v for continuing propagation
                            Origin.append(v)
                            add = 0
                        count_of_unlabeled -= 1
                        semaphore.release()
                rand_it += 1
            if count_of_unlabeled == 0:  # Comm[x] ≠ 0 ∀x ∈ N(u)
                # Delete(Origin, u)
                Origin.remove(u)
                # Append(Visited, u)
                Visited.append(u)
        else:
            # Delete(Origin, u)
            Origin.remove(u)
            # Append(Visited, u)
            Visited.append(u)


def label_propagator(G, X, lamda, rand_list, origin_size_threshold=200, default_number_of_chunks=100, default_size_of_chunks=2):
    """
    Implementation of label propagation algorithm as a function
    Inputs:
        G: Graph
        X(Origin): set of alphas
        λ(lamda): max iterations with no data flow
    other_params:
        rand_list: list of random generated numbers for implementing probability
        origin_size_threshold: threshold for origin size in chunkification
        default_number_of_chunks: number of chunks if origin size is greater than threshold
        default_size_of_chunks: size of each chunk if origin size is less than threshold
                                (number_of_chunks = origin_size / default_size_of_chunks)
    Output :hash table Comm of cluster assignments
    """
    global Graph, Origin, Comm, add, rand_it, rands, Visited
    # Initialize: List Origin ← X, List Visited ← ∅, Hash Table Comm ← (v, 0) ∀v ∈ V
    Origin = X
    Visited = []
    Comm = {}
    for u, H in G.items():
        Comm[u] = 0
        for v in H[0]:
            Comm[v] = 0
    rands = rand_list
    Graph = G
    add = 0
    rand_it = 0
    semaphore = Lock()
    origin_size = len(Origin)
    for u in Origin:  # for all u ∈ Origin do
        # Comm[u] ← u
        Comm[u] = u
    while add <= lamda:  # while add ≤ λ do
        # add ← add + 1
        add += 1
        # for all u ∈ Origin in parallel do
        threads = []
        if origin_size <= origin_size_threshold:
            number_of_chunks = int(origin_size / default_size_of_chunks)
            chunks = [Origin[i::number_of_chunks] for i in range(number_of_chunks)]
            for chunk in chunks:
                threads.append(Thread(target=propagator, args=(chunk, semaphore)))
        else:
            number_of_chunks = default_number_of_chunks
            chunks = [Origin[i::number_of_chunks] for i in range(number_of_chunks)]
            for chunk in chunks:
                threads.append(Thread(target=propagator, args=(chunk, semaphore)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
    return Comm
