#!/usr/bin/env python
"""Script to split a large mediawiki file into multiple files, by header."""
import sys
import re
import os

ADD_TOC = True  # Add TOC everywhere?

def usage():
    print "Usage: [scriptname] [infilename]"

if len(sys.argv) != 2:
    usage()
    exit()

filename_in = sys.argv[1]
if '.' in filename_in:
    filename_no_exts = filename_in[:filename_in.find('.')]
else:
    filename_no_exts = filename_in

# Match top-level headers only.
header = re.compile(r"^=([^=]+)=")

current_filename = '' # Set once we see a header, hyphenated
current_filename_orig = ''  # Original.
current_text = ''  # Build up the next file to write.

file_in = open(filename_in, 'r')

header_names = []  # list of (hyphenated, orig) file name pairs

TOC_FILE = 'Home.mediawiki'  # location of intro text before headers + TOC.

def cap_firsts(s):
    s_caps = ''
    words = s.split(' ')
    for j, word in enumerate(words):
        words[j] = word[0].upper() + word[1:]
    return " ".join(words)

first = True
i = 0
for line in file_in.readlines():
    m = header.match(line)
    if m: 
        assert len(m.groups()) == 1
        # dump string to file.
        if first:
            filename = TOC_FILE
            first = False
        else:
            filename = current_filename + '.mediawiki'
        f = open(filename, 'w')
        if ADD_TOC and not filename == TOC_FILE:
            f.write("__TOC__\n\n")
        f.write(current_text)
        f.close()
        current_text = ''
        # Who knows how Gollum/Mediawiki handle spaces.  Convert to hyphens.
        current_filename_orig = cap_firsts(m.groups()[0].strip())
        current_filename = current_filename_orig.replace(' ', '-')
        header_names.append((current_filename, current_filename_orig))
    else:
        current_text += line

    i += 1

# Finish last file
filename = current_filename + '.mediawiki'
f = open(filename, 'w')
f.write(current_text)
f.close()

print "processed %i lines" % i

home_file = open('Home.mediawiki', 'a')

# Dump out the header names to a Home.ext to form a TOC.
for k, (hyphenated, orig) in enumerate(header_names):
    # Link | Page Title
    home_file.write("%i: [[%s|%s]]\n\n" % (k + 1, hyphenated, orig))
