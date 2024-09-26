def predict_parent(supplier, top_n=5):
    # Get all parent companies
    parent_companies = [node for node, data in G.nodes(data=True) if data['type'] == 'parent']
    
    # Calculate similarity scores between the supplier and all parent companies
    similarity_scores = {parent: similarity_dict[supplier][parent] for parent in parent_companies}
    
    # Sort parent companies by similarity score
    sorted_parents = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_parents[:top_n]

# Predict parent companies for suppliers without assigned parents
for supplier in suppliers_without_parents:
    top_predictions = predict_parent(supplier)
    print(f"Top 5 predicted parent companies for {supplier}:")
    for parent, score in top_predictions:
        print(f"  {parent}: {score:.4f}")
    print()

# Function to add the most likely parent company to the graph
def add_most_likely_parent(supplier, threshold=0.5):
    predictions = predict_parent(supplier, top_n=1)
    if predictions and predictions[0][1] > threshold:
        parent, score = predictions[0]
        G.add_edge(supplier, parent)
        print(f"Added edge: {supplier} -> {parent} (score: {score:.4f})")
    else:
        print(f"No suitable parent found for {supplier}")

# Add most likely parents to the graph
for supplier in suppliers_without_parents:
    add_most_likely_parent(supplier)

# Print updated graph information
print(f"\nUpdated number of edges: {G.number_of_edges()}")