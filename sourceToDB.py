import sqlite3

conn = sqlite3.connect('Debian-stable.db')
c = conn.cursor()

# create table
c.execute(
    '''
        CREATE TABLE IF NOT EXISTS packages (
            name text,
            version text,
            dependency text,
            vcsbrowser text,
            vcsname text,
            vcslink text,
            homepage text,
            section text
        )
    '''
)

c.execute(''' CREATE INDEX IF NOT EXISTS pname_index ON packages(name) ''')

# clean table before insertion
c.execute(''' DELETE FROM packages ''')

insert_query = ''' INSERT INTO packages(name, version,
                 dependency, vcsbrowser, vcsname, vcslink, 
                 homepage, section) VALUES(?, ?, ?, 
                 ?, ?, ?, ?, ?) '''

# Source file path
fname = "Sources"

# =============================
# retrive an array of vcs names
# =============================
vcs_arr = []

with open(fname, encoding='utf-8') as dpfile:  
    for fline in dpfile:
        if (": " in fline):
            attr_name, attr_value = fline.strip("\n").split(": ", 1)

            if ("Vcs-" in attr_name and attr_name not in vcs_arr):
                vcs_arr.append(attr_name)

vcs_arr.pop(vcs_arr.index("Vcs-Browser"))
# =============================

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

attr_dict = {
    "Package": "name",
    "Version": "version",
    "Build-Depends": "dependency",
    "Build-Depends-Indep": "dependency",
    "Vcs-Browser": "vcsbrowser",
    "Homepage": "homepage",
    "Section": "section"
}

for vcs in vcs_arr:
    attr_dict[vcs] = "vcslink"

# dictionary key
attr_str = list(attr_dict.keys())

# package info in dictionary
package = {
    "name": None,
    "version": None,
    "dependency": None,
    "vcsbrowser": None,
    "vcsname": None,
    "vcslink": None,
    "homepage": None,
    "section": None
}
pkg_depends = []
index = 0

def do_db_insert():
    for depend in pkg_depends:
        package["dependency"] = depend
        
        print(index,": ",list(package.values()))
        c.execute(insert_query, list(package.values()))

    return conn.commit()

with open(fname, encoding='utf-8') as dpfile:
    for fline in dpfile:
        if (": " in fline):
            attr_name, attr_value = fline.strip("\n").split(": ", 1)

            if (attr_name in attr_str):
                # clean package info
                if (attr_name == "Package"):
                    index += 1
                    if (package["name"] is not None):
                        do_db_insert()

                    pkg_depends.clear()
                    package["vcsname"] = None
                    for dbattr in list(attr_dict.values()):
                        package[dbattr] = None

                if (attr_name in vcs_arr):
                    package["vcsname"] = attr_name
                
                if (attr_name == "Build-Depends" or attr_name == "Build-Depends-Indep"):
                    pkg_depends = [x.strip() for x in attr_value.split(", ")]
                else:
                    package[attr_dict[attr_name]] = attr_value

do_db_insert()

conn.close()
dpfile.close()

# Counts in Notepad++
# Package: 2486
# Vcs-: 40853
# Vcs-browser: 20338
# Vcs-Git: 18014
# Vcs-Svn: 2282
# Vcs-Mtn: 25
# Vcs-Bzr: 124
# Vcs-Hg: 42
# Vcs-Darcs: 14
# Vcs-Cvs: 7
# Vcs-Arch: 7