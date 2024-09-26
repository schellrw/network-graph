import matplotlib.pyplot as plt

def visualize_graph(G, title):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=100, node_color='lightblue')
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
    
    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# Visualize a subgraph (e.g., top 50 nodes by degree) to avoid cluttering
top_nodes = sorted(G.degree, key=lambda x: x[1], reverse=True)[:50]
subgraph = G.subgraph([node for node, degree in top_nodes])

visualize_graph(subgraph, "Top 50 Nodes in Supplier-Parent Company Graph")