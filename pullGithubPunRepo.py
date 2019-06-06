from github import Github
from github import GithubException
import sqlite3

githubdb = "Github-Public-repo.db"

conn = sqlite3.connect(githubdb)
c = conn.cursor()

c.execute(
    '''
    CREATE TABLE IF NOT EXISTS pubrepos (
        name text,
        url text,
        stars int
    )
    '''
)
c.execute(''' DELETE FROM pubrepos ''')

insert_query = ''' INSERT INTO pubrepos(name, url, stars) VALUES(?, ?, ?) '''

# persona; access token created from github
access_token = "8f1944fda791abd557b83dfc8c38349efed85670"

gh = Github(access_token)
repos = gh.get_repos()

index = 0
for repo in repos:
    index += 1
    name = repo.name
    html_url = repo.html_url
    try:
        stars = repo.stargazers_count
    except GithubException as e:
        stars = 0
    print("[{}] name: {} url: {} star: {}".format(index, name, html_url, stars))
    c.execute(insert_query, (name, html_url, stars))
    conn.commit()

conn.close()