import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges from the dataframe
for _, row in df.iterrows():
    supplier = row['Supplier']
    parent = row['Parent Company']
    G.add_node(supplier, type='supplier')
    if parent:
        G.add_node(parent, type='parent')
        G.add_edge(supplier, parent)

# Print some basic information about the graph
print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}")