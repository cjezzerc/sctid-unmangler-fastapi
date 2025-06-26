import sys
import sqlite3

import pymongo

output_folder = sys.argv[1]
date_string = sys.argv[2]


with sqlite3.connect(f"{output_folder}/descriptions_{date_string}.db") as conn:
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS descriptions (
            description_id TEXT PRIMARY KEY UNIQUE, 
            term TEXT, 
            concept_id TEXT 
        );"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS concepts (
            concept_id TEXT PRIMARY KEY UNIQUE, 
            pt TEXT 
        );"""
    )
    conn.commit()

    client = pymongo.MongoClient()

    # add concepts

    collection = client["concepts_service"][f"concepts_{date_string}"]
    print("Doing concepts")
    n = 0
    for document in collection.find():
        n += 1
        if n % 10000 == 0:
            print(n)

        cid = document["code"]
        pt = document["display"]
        pt = pt.replace('"', '""')
        try:
            conn.execute(
                f"""
                INSERT INTO concepts (concept_id, pt)
                VALUES("{cid}", "{pt}");
                """
            )
        except Exception as e:
            print(e)
            print(f"pt={pt}")
    conn.commit()

    # add descriptions

    collection = client["descriptions_service"][
        f"sct2_Description_MONOSnapshot-en_GB_{date_string}"
    ]

    print("Doing descriptions")
    n = 0
    for document in collection.find():
        n += 1
        if n % 10000 == 0:
            print(n)

        did = document["desc_id"]
        term = document["term"]
        cid = document["concept_id"]
        term = term.replace('"', '""')

        conn.execute(
            f"""
            INSERT INTO descriptions (description_id, term, concept_id)
            VALUES("{did}", "{term}", "{cid}");
            """
        )
    conn.commit()
