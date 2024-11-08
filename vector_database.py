import os
import pandas as pd
import numpy as np
import torch
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def read_all_files_in_directory(data_directory="Database"):
    '''
    converts all documents in data_directory into strings. Also removes redundant lines.
    '''
    file_names=os.listdir(data_directory)
    documents=[]
    for file in file_names:
        with open(f"{data_directory}/{file}") as f:
            documents.append(f.read())
    reassembled_documents, shared_lines= trim_files(documents)
    return reassembled_documents, shared_lines, file_names

def trim_files(documents):
    '''
    for each line in the first file, checks if that line is shared in the other files, and trims them out
    additionally removes lines repeating inside a file.
    returns a list of files trimmed of common lines, and the list of common lines
    '''
    documents_split_into_lines=[document.split("\n") for document in documents]
    shared_lines=[]
    lines_to_iterate_over=documents_split_into_lines[0].copy()
    for line in lines_to_iterate_over:
        if all(line in document_by_line for document_by_line in documents_split_into_lines):
            shared_lines.append(line)
            for document_by_line in documents_split_into_lines:
                document_by_line.remove(line)
    reassembled_documents=["\n".join(list(set(document_by_line))) for document_by_line in documents_split_into_lines]
    return reassembled_documents, shared_lines

def add_article_to_df(article_text:str, df:pd.DataFrame, article_name:str):
    '''
    adds the data from article_text to the dataframe. returns the new, extended dataframe
    '''
    article_as_lines=article_text.split("\n")
    embedded_text=model.encode(article_as_lines)
    new_df=pd.DataFrame(data={
        "text":article_as_lines,
        "line_number":range(len(article_as_lines)),
        "article_name":[article_name for _ in article_as_lines],
        "embedded_text":[x for x in embedded_text]
    })
    return pd.concat([df, new_df], ignore_index=True)

def create_database_from_directory(data_directory="Database"):
    '''
    creates a semantic database from all the files in data_directory
    '''
    documents, discarded_lines, file_names=read_all_files_in_directory(data_directory)
    df=pd.DataFrame()
    for document, file_name in zip(documents, file_names):
        df=add_article_to_df(document, df, file_name)
    return df

def semantic_query(query_text, df, k=5):
    '''
    searches the semantic database based on a plain-text phrase.
    '''
    embedded_query=model.encode(query_text)
    queryables=np.stack(df['embedded_text'])
    similarities = model.similarity(embedded_query, queryables)[0]
    top_indices=torch.topk(similarities, k=k).indices
    print(f"Results for query `{query_text}`:")
    for n in range(k):
        best_match_contents=df.iloc[int(top_indices[n])]
        print(f"(Similarity: {float(similarities[int(top_indices[n])]):.2f}, Article {best_match_contents['article_name']}, Line {best_match_contents['line_number']})\n\t{best_match_contents['text']}")
