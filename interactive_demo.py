from vector_database import create_database_from_directory, semantic_query

if __name__=="__main__":
    df=create_database_from_directory()
    print("Provide query to search for in the database: ")
    query=input()
    semantic_query(query, df, k=5)


