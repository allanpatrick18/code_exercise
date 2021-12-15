Application Overview

Run internal nodes tests

    python -m unittest discover internal_nodes/

Run the init
    
    python create_tables.py

Run the application

    uvicorn app:app --reload

