This repo contains code for a vector search database, and querying it.

Contents:

- `Database/` is a folder of files scraped from random Wikipedia pages by selecting all contents and copying into a .txt file.
- `vector_database.py` is the core code for initializing and querying the semantic database.
- `demo.py` shows a few examples of semantic queries.
- `interactive_demo.py` allows the user to input their own query.

Usage:
- Install packages by running `pip install -r requirements.txt`
- Run the demonstration via `python demo.py`, which will show a or the interactive version with `python interactive_demo.py`
