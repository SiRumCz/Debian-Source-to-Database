import MySQLdb, sqlite3

ghtdb = MySQLdb.connect(host="localhost", user="zkchen", passwd="ghtorrentpassword", db="ghtorrent_restore")
ghtc = ghtdb.cursor()
ghtquery = ''' 
SELECT url FROM projects
WHERE name = '{}' AND deleted IS NOT TRUE AND forked_from IS NULL
LIMIT 1
'''

DPdb = "Debian-stable.db"
pkgconn = sqlite3.connect(DPdb)
pkgc = pkgconn.cursor()

pkgc.execute(''' SELECT DISTINCT name, homepage FROM packages ''')
update_query = ''' UPDATE packages SET githubapi = ? WHERE name = ? '''

index = 0
for package in pkgc.fetchall():
    index += 1
    name, homepage = package

    if (homepage is not None and "github.com" in homepage):
        print("[{}] Name: {} homepage: {}".format(index, name, homepage))
        continue

    ghtc.execute(ghtquery.format(name))
    ghtresult = ghtc.fetchone()
    
    ghapi = ghtresult[0] if ghtresult is not None else None

    pkgc.execute(update_query, (ghapi, name))
    pkgconn.commit()
    print("[{}] Name: {} githubapi: {}".format(index, name, ghapi))

pkgc.close()
ghtc.close()
    