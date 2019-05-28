# The goal of this script is to select 20 random packages
# and see how many are still active
#
# Steps: fetch 20 pkgs and see if the vcslink and home page are still alive 

import sqlite3
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

dbname = "Debian-stable.db"

conn = sqlite3.connect(dbname)
c = conn.cursor()

pkgcount = 20
c.execute(
    ''' 
    SELECT DISTINCT name, vcsbrowser, vcsname, vcslink, homepage 
    FROM packages WHERE vcsbrowser IS NOT NULL AND homepage IS NOT 
    NULL ORDER BY RANDOM() LIMIT {}
    '''.format(pkgcount)
)

# vcs_arr = [
#     'Vcs-Svn', 
#     'Vcs-Git', 
#     'Vcs-Bzr', 
#     'Vcs-Mtn', 
#     'Vcs-Hg', 
#     'Vcs-Darcs', 
#     'Vcs-Cvs', 
#     'Vcs-Arch'
# ]

vcs_error_count = 0
hp_error_count = 0
print('Getting '+str(pkgcount)+' random packages ...')
index = 0

for package in c.fetchall():
    print()

    index += 1
    name, vcsbrowser, vcsname, vcslink, homepage = package
    print('Package '+str(index)+': '+name)

    vcsreq = Request(vcsbrowser.strip())
    hpreq = Request(homepage.strip())

    error = False

    try:
        print('Vcs-browser: '+vcsbrowser)        
        vcsresponse = urlopen(vcsreq)
        print('Redirected: '+vcsresponse.geturl())
    except HTTPError as e:
        print('VCS Error code: ', e.code)
        error = True
    except URLError as e:
        print('VCS Reason: ', e.reason)
        error = True
        
    if (error):
        vcs_error_count += 1
        error = False

    try:
        print('Homepage link: '+homepage)
        hpresponse = urlopen(hpreq)
        print('Redirected: '+hpresponse.geturl())
    except HTTPError as e:
        print('Homepage Error code: ', e.code)
        error = True
    except URLError as e:
        print('Homepage Reason: ', e.reason)
        error = True

    if (error):
        hp_error_count += 1

conn.close()    
print('VCS error count: ', vcs_error_count)
print('Homepage error count: ', hp_error_count)