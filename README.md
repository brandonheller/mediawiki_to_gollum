mediawiki_to_gollum
===================

Utilities for converting mediawiki files to Gollum-friendly formats

These utilities were created to move the OpenFlow tutorial from a WordPress instance to a Gollum-backed wiki (local or on GitHub).  The internal and external link formats that Gollum uses before WikiCloth parses the MediaWiki require a few changes, so the first script, change_mediawiki_links.py, does this conversion automatically when given an input file.  The second script, split_by_headers.py, takes one big MediaWiki page and splits it by headers, plus generates a TOC automatically on the home page. 

As an example, here is the hosted Wordpress wiki:
http://www.openflow.org/wk/index.php/OpenFlow_Tutorial

Here is the converted one on Gollum:
https://github.com/onstutorial/onstutorial/wiki/onstutorial

... and the split version:
https://github.com/onstutorial/onstutorial/wiki 
