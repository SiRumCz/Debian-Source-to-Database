# Debian-Source-to-Database

convert text information in http://ftp.ca.debian.org/debian/dists/stable/main/source/ to SQLite 3 database

Note: According to [Debian Policy Manual](https://www.debian.org/doc/debian-policy/ch-archive.html#archive-areas), only *main* area is considered to be part of Debian distribution.

This is a replacement to my Debian-Packages-Scrapy

# Research papers
[A Model to Understand the Building and Running Inter-Dependencies of Software](http://turingmachine.org/~dmg/papers/dmg2007_wcre_depend.pdf) --Daniel M German

[Macro-level software evolution: a case study
of a large software compilation](https://link.springer.com/content/pdf/10.1007%2Fs10664-008-9100-x.pdf) --Jesus M. Gonzalez-Barahona

# Some findings
Top 10 frequently used packages as dependecies
[('python3-setuptools', 1215), ('dh-buildinfo', 1226), ('cdbs', 1248), ('python-setuptools', 1567), ('autotools-dev', 1894), ('pkg-config', 2060), ('dh-python', 2360), ('dh-autoreconf', 2558), ('perl', 3244), ('debhelper ', 18568)]
