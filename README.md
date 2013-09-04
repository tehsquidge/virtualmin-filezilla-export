virtualmin-filezilla-export
===========================

a script to export all sites in virtualmin to a filezilla xml file which is ready to import.

Usage
=====

You will need to run it as root.

```
./virtualmin-filezilla-export.py > output.xml
```

using a different port default:

```
./virtualmin-filezilla-export.py -p 25252 > output.xml
```

the protocol to use: ftp - 0 (default), sftp - 1:

```
./virtualmin-filezilla-export.py -t 1 > output.xml
```
