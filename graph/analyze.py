# Identify suppliers without parent companies
suppliers_without_parents = [node for node, data in G.nodes(data=True) 
                             if data['type'] == 'supplier' and G.out_degree(node) == 0]

print(f"Number of suppliers without parents: {len(suppliers_without_parents)}")

# Identify parent companies with the most suppliers
parent_supplier_count = {node: G.in_degree(node) for node, data in G.nodes(data=True) 
                         if data['type'] == 'parent'}
top_parents = sorted(parent_supplier_count.items(), key=lambda x: x[1], reverse=True)[:5]

print("Top 5 parent companies by number of suppliers:")
for parent, count in top_parents:
    print(f"{parent}: {count} suppliers")

# Calculate the average number of suppliers per parent company
avg_suppliers_per_parent = sum(parent_supplier_count.values()) / len(parent_supplier_count)
print(f"Average number of suppliers per parent company: {avg_suppliers_per_parent:.2f}")