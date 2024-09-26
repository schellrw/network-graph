import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data from Excel file
df = pd.read_excel('supplier_parent_data.xlsx')

# Assume columns are 'Supplier' and 'Parent Company'
# Fill NaN values with an empty string
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