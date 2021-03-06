# Debian-Source-to-Database

convert text information in http://ftp.ca.debian.org/debian/dists/stable/main/source/ to SQLite 3 database

Note: According to [Debian Policy Manual](https://www.debian.org/doc/debian-policy/ch-archive.html#archive-areas), only *main* area is considered to be part of Debian distribution.

Note 2: Since this file is used by Debian package management tool for the installation process, the only dependency relationship are Build relationships. For each individual project, their debian/control file should contain different list of dependency such as Depends and Suggests, etc. 

This is a replacement to my Debian-Packages-Scrapy

# How to use it
Download and uncompresee the Source.gz file from debian ftp server(for example: http://ftp.ca.debian.org/debian/dists/stable/main/source/ to have the latest stable version) for any Debian version


# Research papers
[A Model to Understand the Building and Running Inter-Dependencies of Software](http://turingmachine.org/~dmg/papers/dmg2007_wcre_depend.pdf) --Daniel M German

[Macro-level software evolution: a case study
of a large software compilation](https://link.springer.com/content/pdf/10.1007%2Fs10664-008-9100-x.pdf) --Jesus M. Gonzalez-Barahona

# Some findings
Top 10 frequently used packages as dependecies:<br>
('debhelper ', 18568), <br>
('perl', 3244), <br>
('dh-autoreconf', 2558), <br>
('dh-python', 2360), <br>
('pkg-config', 2060), <br>
('autotools-dev', 1894), <br>
('python-setuptools', 1567), <br>
('cdbs', 1248), <br>
('dh-buildinfo', 1226), <br>
('python3-setuptools', 1215)<br>

