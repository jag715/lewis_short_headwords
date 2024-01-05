# lewis_short_headwords
Lewis and Short Latin Dictionary with computer-readable headword variations identified.

## Project Description

**A Latin Dictionary** (edited by Charlton T. Lewis and Charles Short) is human-readable but not very computer-readable. Many headwords have variations. This project contains two versions of said dictionary in which headword variations are identified and computer-readable. 

The Python script (main.py) looks for a copy of 'lewis-short.txt' which you can obtain from https://github.com/telemachus/plaintext-lewis-short. If found, it scans and attempts to identify each dictionary headword including all variations for every entry in the dictionary. It is a complicated process and the code is not pretty but is fairly successful.

For example, in the following four entries:

```
damnāticĭus (or -tius), a, um, adj. damno, condemned, sentenced;
disjunctĭo or dījunctio, ōnis, f. disjungo, a separation;
intĕremptĭo (-emt-), ōnis, f. id., destruction, slaughter;
octōgĭes or -iens..
```

it will identify both the headword as listed (damnāticĭus, disjunctĭo, intĕremptĭo and octōgĭes) and the alternate version (damnātitius, dījunctio, intĕremtĭo, octōgĭens).

INPUT:  lewis-short.txt

OUTPUT: lewis_short_by_headword.txt
        lewis_short_by_headword.json

The text output file is formatted in pairs of lines, as follows: The first line begins with # and then is a comma-separated list of headwords that link to a dictionary entry. The second line is the dictionary entry these headwords link to. Dictionary entries contain no newlines.

Line 1: #a,ab,abs
Line 2: a, ab, abs: preposition, 'from', etc..

The JSON file stores the same data in a Python dictionary.

main.py also contains example code for opening and using these files.

## Credits

The text for the Lewis and Short dictionary is provided under a CC BY-SA license by Perseus Digital Library, http://www.perseus.tufts.edu, with funding from The National Endowment for the Humanities. Data accessed from https://github.com/PerseusDL/lexica/ 11-15-2022.

The input text for this project (lewis-short.txt) is licensed under the CC BY-SA 3.0 license, and is available here: https://github.com/telemachus/plaintext-lewis-short.

## License

This project is distributed under the MIT License.
