#!/usr/bin/python2

# Author: Joseph Wiseman <joswiseman@cock.li>
# URL: https://github.com/dryes/nzbinfo/

import os
import re
import sys
from datetime import date
from pynzb import nzb_parser


def main(nzbfile):
    try:
        nzb = open(nzbfile, 'r').read()
    except:
        print('Error reading nzb.')
        return False

    try:
        nzbparse = nzb_parser.parse(nzb)
    except:
        print('Error parsing nzb.')
        return False

    posters = []
    dates = []
    subjects = []
    parfiles = []
    groups = []
    segments = []

    filecount = 0
    filesize = 0
    parsize = 0
    parredundancy = 0

    for f in nzbparse:
        posters.append(f.poster)
        dates.append(f.date)
        subjects.append(f.subject)

        if re.search(r'\.par2\"', f.subject, re.IGNORECASE) is not None:
            parfiles.append(f)

        for g in f.groups:
            groups.append(g)

        for s in f.segments:
            segments.append(s)

    print('Complete name\t\t\t : %s' % nzbfile)

    sys.stdout.write('Poster(s)\t\t\t : ')
    sys.stdout.flush()
    print(', '.join(str(s) for s in set(posters)))

    print('Age\t\t\t\t : %s' % (date.today() - sorted(dates)[-1]))

    sys.stdout.write('Group(s)\t\t\t : ')
    sys.stdout.flush()
    print(', '.join(str(s) for s in set(groups)))

    print('File count\t\t\t : %s (+%s)' %
          ((len(subjects) - len(parfiles)), len(parfiles)))

    for s in set(segments):
        filesize += s.bytes

    for p in parfiles:
        for ps in p.segments:
            parsize += ps.bytes

    print('File size\t\t\t : %s MB' % ((filesize - parsize) / float(1 << 20)))

    if parsize:
        parredundancy = (filesize / parsize)

    print('Par redundancy\t\t\t : %s' % parredundancy + '%')

    print('\n')

if __name__ == '__main__':
    err = 0
    for f in sys.argv[1:]:
        if os.path.isfile(f) and main(f) == False:
            err = (err + 1)
    if err > 0:
        sys.exit(1)
