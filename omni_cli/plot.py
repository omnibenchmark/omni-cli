# plotting functions for provenance graph

def plot_graph(graph):
    import networkx as nx
    import matplotlib.pyplot as plt
    nx.draw_networkx(G)
    plt.show()

def plot_connected_component(graph, target_node):
    import networkx as nx
    import matplotlib.pyplot as plt
    # Get the connected component containing the target node
    connected_component = nx.weakly_connected_components(graph)
    subgraph = graph
    for component in connected_component:
        if target_node in component:
            subgraph = graph.subgraph(component)
            break
    
    # Plot the subgraph
    pos = nx.spring_layout(subgraph)
    nx.draw_networkx(subgraph, pos, with_labels=True, node_color='lightblue', node_size=500, edge_color='gray')
    plt.title(f"Connected Component for Node: {target_node}")
    plt.show()
