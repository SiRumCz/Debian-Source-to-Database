# NOT WORKING
import pandas as pd
import sqlite3

ghtorrent_project = "F:/mysql-2019-06-01/projects.csv"
pkgdb = "Debian-stable.db"
debianGhDB = "debian_gh.db"

ghconn = sqlite3.connect(debianGhDB)
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

chunksize = 10 ** 8

index = 0
for datachunk in pd.read_csv(ghtorrent_project, chunksize=chunksize, engine="python"):
    if index > 2:
        break
    
    index += 1
    print(datachunk.shape)