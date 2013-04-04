#!/usr/bin/env python
"""Script to convert MediaWiki page links to a Gollum-friendly forum"""
import sys
import re
import os

DEBUG = True

def usage():
    print "Usage: [scriptname] [infilename]"

if len(sys.argv) != 2:
    usage()
    exit()

print os.getcwd()

filename_in = sys.argv[1]
filename_no_ext = os.path.basename(filename_in)
print "filename_no_ext: %s" % filename_no_ext

filename_out = filename_in + '.out'
file_in = open(filename_in, 'r')
file_out = open(filename_out, 'w')

# Note use of character class for brackets to narrow matches; otherwise
# [ ] [ ] is a single (moore general) re match.
external_link = re.compile(r"\[(http[\S]*)\ ([^]]*)\]")

internal_link = re.compile(r"\[\[#(.+)\|(.+)\]\]")


def process_external_links(line):
    """
    Gollum (https://github.com/gollum/gollum) requires that MediaLinks look like
    this:

    [[linkname|http://external_page_link]]

    rather than:

    [http://external_page linkname-pt1 linkname-pt2]
    """
    # Match multiple times in a line.
    line_rem = line  # Line left available for processing
    new_line = ""  # Line to be printed
    done = False
    found = False
    while not done:
        m = external_link.search(line_rem)
        if m:
            found = True
            assert(len(m.groups()) >= 2)
            link_addr = m.group(1)
            link_name = " ".join(m.groups()[1:])
            new_link = "[[%s|%s]]" % (link_name, link_addr)
            # shift by 1 to cover left bracket
            new_line += line_rem[:m.start(1) - 1] + new_link #+ line_rem[m.end(m.lastindex):]
            # shift by 1 to cover right bracket
            line_rem = line_rem[m.end(m.lastindex) + 1:]

            if (DEBUG):
                print "saw match at line %i:" % i
                print "\t groups: %s" % " ".join(m.groups())
                print "\t new link: %s" % new_link
                print "\t m.span: %i %i" % (m.start(1), m.end(m.lastindex))
                print "\t line_rem: %s" % line_rem,
                print "\t new line: %s" % new_line

        else:
            done = True
            new_line += line_rem
    if found:
        print
    return new_line


def process_internal_links(line, this_page_name):
    """
    Internal page links must look like this:

    [[thispagename#Anchor-Name-As-Caps-Hypen-List|linkname]]

    rather than:

    [[#Anchor Name As Spaced List | linkname]]
    """
    # Match multiple times in a line.
    line_rem = line  # Line left available for processing
    new_line = ""  # Line to be printed
    done = False
    found = False
    while not done:
        m = internal_link.search(line_rem)
        if m:
            found = True
            assert(len(m.groups()) >= 2)
            anchor_name = m.group(1).rstrip().lstrip().replace(' ', '-')
            link_text = "-".join(m.groups()[1:]).rstrip().lstrip()
            new_link = "[[%s#%s|%s]]" % (this_page_name, anchor_name, link_text)
            # shift by 3 to cover left brackets and #
            new_line += line_rem[:m.start(1) - 3] + new_link #+ line_rem[m.end(m.lastindex):]
            # shift by 2 to cover right brackets
            line_rem = line_rem[m.end(m.lastindex) + 2:]

            if (DEBUG):
                print "saw match at line %i:" % i
                print "\t groups: %s" % " ".join(m.groups())
                print "\t new link: %s" % new_link
                print "\t m.span: %i %i" % (m.start(1), m.end(m.lastindex))
                print "\t line_rem: %s" % line_rem,
                print "\t new line: %s" % new_line

        else:
            done = True
            new_line += line_rem
    if found:
        print
    return new_line


i = 0
for line in file_in.readlines():
    line = process_external_links(line)
    line = process_internal_links(line, filename_no_ext)
    file_out.write(line)
    i += 1
    
