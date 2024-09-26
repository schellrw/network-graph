import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

# Load data from Excel file
df = pd.read_excel('supplier_parent_data.xlsx')

# Assume columns are 'Supplier' and 'Parent Company'
# Keep track of originally null values
df['Original_Parent_Null'] = df['Parent Company'].isnull()
df['Parent Company'] = df['Parent Company'].fillna('')

# Create a set of all unique companies (both suppliers and parents)
all_companies = set(df['Supplier']) | set(df['Parent Company'])

# Create TF-IDF vectors for all company names
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(list(all_companies))

# Compute cosine similarity between all pairs of companies
similarity_matrix = cosine_similarity(tfidf_matrix)

# Create a dictionary to store similarity scores
similarity_dict = {company: dict(zip(all_companies, similarities)) 
                   for company, similarities in zip(all_companies, similarity_matrix)}

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

def predict_parent(supplier, top_n=5):
    # Get all parent companies
    parent_companies = [node for node, data in G.nodes(data=True) if data['type'] == 'parent']
    
    # Calculate similarity scores between the supplier and all parent companies
    similarity_scores = {parent: similarity_dict[supplier][parent] for parent in parent_companies}
    
    # Sort parent companies by similarity score
    sorted_parents = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_parents[:top_n]

# Function to get top 5 predictions and their scores
def get_top_5_predictions(supplier):
    predictions = predict_parent(supplier, top_n=5)
    return [pred[0] for pred in predictions], [pred[1] for pred in predictions]

# Add columns for predicted parents and scores
df['Predicted_Parent'] = ''
df['Prediction_Score'] = np.nan
for i in range(1, 6):
    df[f'Potential_Parent_{i}'] = ''
    df[f'Potential_Parent_{i}_Score'] = np.nan

# Fill in predictions for originally null values
for idx, row in df[df['Original_Parent_Null']].iterrows():
    supplier = row['Supplier']
    predictions, scores = get_top_5_predictions(supplier)
    
    df.at[idx, 'Predicted_Parent'] = predictions[0]
    df.at[idx, 'Prediction_Score'] = scores[0]
    
    for i in range(5):
        if i < len(predictions):
            df.at[idx, f'Potential_Parent_{i+1}'] = predictions[i]
            df.at[idx, f'Potential_Parent_{i+1}_Score'] = scores[i]

# Update 'Parent Company' column with predictions where it was originally null
df.loc[df['Original_Parent_Null'], 'Parent Company'] = df.loc[df['Original_Parent_Null'], 'Predicted_Parent']

# Reorder columns
column_order = ['Supplier', 'Parent Company', 'Original_Parent_Null', 'Predicted_Parent', 'Prediction_Score']
for i in range(1, 6):
    column_order.extend([f'Potential_Parent_{i}', f'Potential_Parent_{i}_Score'])

df = df[column_order]

# Save the enriched dataframe to a new Excel file
output_file = 'enriched_supplier_parent_data.xlsx'
df.to_excel(output_file, index=False)

print(f"Enriched data saved to {output_file}")

# Display a sample of the enriched dataframe
print(df[df['Original_Parent_Null']].head())