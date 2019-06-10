import sqlite3
import collections # orderedDict

debianpkgdb = "Debian-stable.db" 
conn = sqlite3.connect(debianpkgdb)
c = conn.cursor()

c.execute(''' SELECT name, version, dependency, section FROM packages ''')

pkgDependsFreq = {}

for package in c.fetchall():
    # version and section are queried but not used
    # might be able to tell in the future if current version suitable for other package as dependency
    # section was to see which section in debian packages has the most frequently used package
    (name, version, dependency, section) = package

    if name not in pkgDependsFreq:
        pkgDependsFreq[name] = 0

    # get all alternative packages
    for altpkgname in dependency.split("|"):
        # remove white space
        altpkgname = altpkgname.strip()
        # remove required version or architecure
        altpkgname = altpkgname.split("[")[0].split("(")[0]

        pkgDependsFreq[altpkgname] = pkgDependsFreq.get(altpkgname, 0)+1


for pkgname, pkgfreq in pkgDependsFreq.items():
    print("name: ", pkgname, " used: ", pkgfreq)

conn.close()
