import os
import sqlite3
from google.cloud import bigquery

# BigQuery setup
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'sdfsdfsd-7a9e10d2317f.json'
client = bigquery.Client()

BGquery = (
    '''
    SELECT name, url FROM `ghtorrent-bq.ght.projects`
    WHERE name='{}' AND deleted!=false AND forked_from IS NULL
    '''
)

# SQLite3 setup
pkgdb = "Debian-stable.db"
ghdb = "Debian-github.db"

ghconn = sqlite3.connect(ghdb)
ghc = ghconn.cursor()
ghc.execute(''' ATTACH DATABASE \'{}\' AS pkgdb '''.format(pkgdb))
ghc.execute(
    '''
    CREATE TABLE IF NOT EXISTS repos (
        name text,
        urltype text,
        apiurl text
    )
    '''
)
ghc.execute(''' DELETE FROM repos ''')

ghc.execute(''' SELECT DISTINCT name, homepage FROM pkgdb.packages''')
insert_query = ''' INSERT INTO repos(name, urltype, apiurl) VALUES(?, ?, ?) '''

index = 0
for package in ghc.fetchall():
    index += 1
    name, homepage = package

    # if the home page is github url
    if (homepage is not None and "github.com" in homepage):
        print("[{}] Name: {} Type: homepage Url: {}".format(index, name, homepage))
        ghc.execute(insert_query, (name, "homepage", homepage))
        ghconn.commit()
        continue
    
    try:
        query_job = client.query(
            BGquery.format(name),
            # Location must match that of the dataset(s) referenced in the query.
            location="US",
        )  # API request - starts the query

    except Exception:
        print("BigQuery failed querying ghtorrent for "+name)
        continue

    search_result = [name, None, None]
    if query_job.result().total_rows > 0:
        search_result[1] = "api"
        search_result[2] = list(query_job)[0].url

    print("[{}] Name: {} Type: {} Url: {}".format(index, search_result[0], search_result[1], search_result[2]))
    ghc.execute(insert_query, search_result)
    ghconn.commit()

ghc.close()

# for row in query_job:  # API request - fetches results
#     # Row values can be accessed by field name or index
#     assert row[0] == row.name == row["name"]
#     print(row)