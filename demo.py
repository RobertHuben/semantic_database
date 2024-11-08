from vector_database import create_database_from_directory, semantic_query


if __name__=="__main__":
    df=create_database_from_directory()
    queries=["Canadian Politics", "Greyhounds", "Ireland", "Freshwater Polyp"]
    for query in queries:
        semantic_query(query, df, k=5)
        print("")


