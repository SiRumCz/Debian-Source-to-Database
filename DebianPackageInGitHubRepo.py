from github import Github
import sqlite3

# persona; access token created from github
access_token = "8f1944fda791abd557b83dfc8c38349efed85670"

pkgdb = "Debian-stable.db"
ghdb = "Debian-github.db" 

# connect to SQLite db
ghconn = sqlite3.connect(ghdb)
ghc = ghconn.cursor()

ghc.execute(''' ATTACH DATABASE \'{}\' AS pkgdb '''.format(pkgdb))
ghc.execute(
    '''
    CREATE TABLE IF NOT EXISTS repos (
        name text,
        result text,
        url text,
        stars int
    )
    '''
)
ghc.execute(''' DELETE FROM repos ''')

#
ghc.execute(''' SELECT DISTINCT name, homepage FROM pkgdb.packages''')
insert_query = ''' INSERT INTO repos(name, result, url, stars) VALUES(?, ?, ?, ?) '''

gh = Github(access_token)

# https://pygithub.readthedocs.io/en/latest/examples/Repository.html
index = 0
for pkg in ghc.fetchall():
    index += 1
    name, homepage = pkg

    # if the home page is github url
    if (homepage is not None and "github.com" in homepage):
        user, reponame = homepage.strip().split('/')[-2:]

        try:
            repo = gh.get_repo("{}/{}".format(user, reponame))
        except Exception:
            print("cannot get_repo() from homepage of "+name)
            continue

        ghc.execute(insert_query, (name, None, homepage, repo.stargazers_count))
        ghconn.commit()
        continue

    try:
        repos = gh.search_repositories(query=name)
    except Exception:
        print("search_repositories() error")
        continue

    search_result = (name, None)
    maxStar = 0
    firstItem = True
    for repo in repos:
        if (repo.stargazers_count > maxStar or firstItem):
            maxStar = repo.stargazers_count
            search_result = (repo.name, repo.html_url)
            firstItem = False

    print("[{}] name: {} result: {} url: {} star: {}".format(index, name, search_result[0], search_result[1], maxStar))
    ghc.execute(insert_query, (name, search_result[0], search_result[1], maxStar))
    ghconn.commit()

ghc.close()