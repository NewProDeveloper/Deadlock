import matplotlib.pyplot as plt
import matplotlib.patches as patches
import networkx as nx

processes = int(input("Enter the no of processes : "))
resources = int(input("Enter the no of resources : "))
print("                            ", end = "")
print(" ".join([f"R{i}" for i in range(resources)]))
available = [int(i) for i in input("Enter available resources : ").split()]
safe_sequence = []

print("\n-- Allocate Resources --")
print("     ", end = "")
print(" ".join([f"R{i}" for i in range(resources)]))
currently_allocated = [[int(i) for i in input(f"P{j} : ").split()] for j in range(processes)]

print("\n-- Request Resources --")
print("     ", end = "")
print(" ".join([f"R{i}" for i in range(resources)]))
request = [[int(i) for i in input(f"P{j} : ").split()] for j in range(processes)]

def BankersAlgo():
    message = ['', '', '']
    allocated = [0] * resources
    for i in range(processes):
        for j in range(resources):  
            allocated[j] += currently_allocated[i][j]

    running = [True] * processes
    count = processes
    while count != 0:
        safe = False
        for i in range(processes):
            if running[i]:
                executing = True
                for j in range(resources):
                    if request[i][j] > available[j]:
                        executing = False
                        break
                if executing:
                    safe_sequence.append(i)
                    running[i] = False
                    count -= 1
                    safe = True
                    for j in range(resources):
                        available[j] += currently_allocated[i][j]
                    break
        if not safe:
            st = "Unsafe State! Deadlock detected"
            message[0] = st
            return message

    if safe:
        st1 = "Safe State!! No deadlock detected"
        st2 = "-- Safe Sequence --"
        st3 = ""

        for i in safe_sequence[:-1]:
            st3 += f"P{i} -> "
        st3 += f"P{safe_sequence[-1]}"
        message[0] = st1
        message[1] = st2
        message[2] = st3
        return message

def ResourceAllocatorGraph(message):
    G = nx.DiGraph()

    process_nodes = [f"P{i}" for i in range(processes)]
    resource_nodes = [f"R{i}" for i in range(resources)]
    G.add_nodes_from(process_nodes, bipartite=0)
    G.add_nodes_from(resource_nodes, bipartite=1)

    for i in range(processes):
        for j in range(resources):
            if currently_allocated[i][j] > 0:
                G.add_edge(f"R{j}", f"P{i}", weight=currently_allocated[i][j])
    
    for i in range(processes):
        for j in range(resources):
            if request[i][j] > 0:
                G.add_edge(f"P{i}", f"R{j}", weight=request[i][j])
    
    top = resource_nodes
    pos = nx.bipartite_layout(G, top, align='horizontal')

    color_map = []
    for node in G:
        if node in top:
            color_map.append('skyblue')
        else: 
            color_map.append('lightgreen')

    # nx.draw_networkx_nodes(G, pos, nodelist=process_nodes, node_size=600, node_color='skyblue')
    for node in process_nodes:
        plt.gca().add_patch(patches.Circle((pos[node][0], pos[node][1]), 0.05, facecolor='skyblue'))
    for node in top:
        plt.gca().add_patch(patches.Rectangle((pos[node][0]-0.07, pos[node][1]-0.07), 0.14, 0.14, facecolor='lightgreen'))
    nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=20, connectionstyle='arc3,rad=0.05')
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

    plt.title("Resource Allocator Graph")
    plt.subplots_adjust(bottom=0.2)
    plt.figtext(0.5, 0.14, message[0], ha="center", fontsize=12, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
    if message[1]:
        plt.figtext(0.5, 0.09, message[1], ha="center", fontsize=12, bbox={"facecolor":"lightgreen", "alpha":0.5, "pad":5})
        plt.figtext(0.5, 0.04, message[2], ha="center", fontsize=12, bbox={"facecolor":"lightgreen", "alpha":0.5, "pad":5})

    plt.show()

message = BankersAlgo()
ResourceAllocatorGraph(message)