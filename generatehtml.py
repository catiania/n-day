#!/usr/bin/env python3

"""
 * This file is a customised version of an RCES script: https://github.com/dithpri/RCES and licensed under
 * the MIT license. See https://github.com/dithpri/RCES/blob/master/LICENSE.md for more details.
"""
import re
import configparser

html_start = """
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
	padding: 1em;
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
 <div class="sticky">
  <p>W to open nation and focus next, A/D to open prod, S to open incoming, Q to focus prev nation, E to focus next nation</p>
</div> 
<body onkeypress="select()">
<table class = "center">
"""

html_end = """
</table>
<script>

const body = document.querySelector('body');

var count = 0;
document.querySelectorAll('a')[count].style.color = "red";
function select(e){
    document.querySelectorAll('a')[count].style.color = "black";
	if (window.event) keycode = window.event.keyCode; 	// IE
	else if (e) keycode = e.which;
	if (keycode == 87) { 
		document.querySelectorAll('a')[count].click()
		count+=4;
	}
	else if(keycode==65||keycode==68){
		document.querySelectorAll('a')[count+1].click()
		count+=4;
	}
	else if(keycode==83){
		document.querySelectorAll('a')[count+2].click()
		count+=4;
	}
	else if (keycode == 81){
		count-=4;
	}
	else if (keycode == 69){
		count+=4;
	}
	if(count<0){
		count = 0;
	}else if(count>=document.querySelectorAll('a').length){
		count = document.querySelectorAll('a').length-3;	
	}
	document.querySelectorAll('a')[count].style.color = "red";
	if(count>1)
	document.querySelectorAll('a')[count-1].scrollIntoView();
	
}
body.onkeydown=select;
</script>

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
links = open('puppet_links.html', 'w')

links.write(html_start)

for nation in puppets:
	canonical = nation.lower().replace(" ", "_")
	escaped_canonical = re.escape(canonical)
	container_protolink = container_prefix.format(*([canonical for _ in range(container_prefix.count("{}"))]))
	containerise_rules_container.write("@^.*\\.nationstates\\.net/(.*/)?container={}(/.*)?$ , {}\n".format(escaped_canonical, nation))
	containerise_rules_nation.write("@^.*\\.nationstates\\.net/(.*/)?nation={}(/.*)?$ , {}\n".format(escaped_canonical, nation))
	links.write("<tr>\n")
	links.write(f'\t<td><p><a target="_blank" href="https://www.nationstates.net/{container_protolink}/nation={canonical}">{nation}</a></p></td>\n')
	try:
		for key, value in config['links'].items():
			links.write(f'\t<td><p><a target="_blank" href="https://www.nationstates.net/{container_protolink}/{value}">{key}</a></p></td>\n')
	except KeyError:
		pass
	# links.write("""<td><p><a target="_blank" href="https://www.nationstates.net/container={}/nation={}/page=zombie_control">Zombie Control</a></p></td>""".format(canonical))
	links.write("</tr>\n")

links.write(html_end)
