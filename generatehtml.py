#!/usr/bin/env python3

"""
 * This file is a customised version of an RCES script: https://github.com/dithpri/RCES and licensed under
 * the MIT license. See https://github.com/dithpri/RCES/blob/master/LICENSE.md for more details.
"""
import re
import configparser

html_start = """
<!doctype html>
<html>
<head>
<style>
td.createcol p {
	padding-left: 10em;
}

p{
	font-family: 'Segoe UI';
}
a {
	text-decoration: none;
    font-family: 'Segoe UI';
	color: black;
}

a:visited {
	color: grey;
}

table {
	border-collapse: collapse;
	max-width: 1000%;
	border: 1px solid grey;
}
table.center {
    margin-left:auto; 
    margin-right:auto;
}
tr, td {
	border-bottom: 2px solid green;
}
tr.end, td.end {
	border-bottom: 5px solid rgb(216, 216, 32);
}
td p {
	padding: 0.7em;
}

body {
	text-align:center;
	padding-top: 50px;
	margin:0;
}

tr:hover {
	background-color: lightgrey;
}

.sticky {
  position: fixed;
  top: 0;
  width: 100%;
  background-color: #CCCD;
  border-radius: 0px 0px 5px 5px;
}

</style>
</head>

<table class = "center">
"""

html_end = """
</table>

</body>
</html>
"""

config = configparser.ConfigParser()
config.read("config.txt")

try:
	container_prefix = config['config']['containerPrefix']
except KeyError:
	container_prefix = "container={}/nation={}"
	containerise_rules = {
		
	}

with open('puppets_list.txt') as f:
	puppets = f.read().split('\n')

puppets = list(filter(None, puppets))

containerise_rules_container = open('containerise (container).txt', 'w')
containerise_rules_nation = open('containerise (nation).txt', 'w')
links = open('nday_links.html', 'w')

user = input("Enter Your Main Nation: ").strip().replace(" ","_")

links.write(html_start)

for nation in puppets:
	canonical = nation.lower().strip().replace(" ", "_")
	escaped_canonical = re.escape(canonical)
	container_protolink = container_prefix.format(*([canonical for _ in range(container_prefix.count("{}"))]))
	containerise_rules_container.write("@^.*\\.nationstates\\.net/(.*/)?container={}(/.*)?$ , {}\n".format(escaped_canonical, nation))
	containerise_rules_nation.write("@^.*\\.nationstates\\.net/(.*/)?nation={}(/.*)?$ , {}\n".format(escaped_canonical, nation))
	links.write("<tr>\n")
	links.write(f'\t<td><p><a target="_blank" href="https://www.nationstates.net/{container_protolink}/nation={canonical}?generated_by=cat_nuke_thing_by_catiania_used_by_{user}">{nation}</a></p></td>\n')
	try:
		for key, value in config['links'].items():
			links.write(f'\t<td><p><a target="_blank" href="https://www.nationstates.net/{container_protolink}/{value}?generated_by=cat_nuke_thing_by_catiania_used_by_{user}">{key}</a></p></td>\n')
	except KeyError:
		pass
	# links.write("""<td><p><a target="_blank" href="https://www.nationstates.net/container={}/nation={}/page=zombie_control">Zombie Control</a></p></td>""".format(canonical))
	links.write("</tr>\n")

links.write(html_end)
