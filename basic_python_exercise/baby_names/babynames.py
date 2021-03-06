#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
"""
def read_file(filename):
	lines = []
	with open(filename, 'r') as f:
		for line in f:
			lines.append(line)
	return lines

def find_year(lines):
	pattern = re.compile(r"(^<h3[\sa-z=\">]*Popularity)")
	pattern_year = re.compile(r"[0-9]{4}")
	for line in lines:
		if re.search(pattern, line) != None:
			return re.findall(pattern_year, line)

#<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
def find_rank_and_name(lines):
	name_and_rank = []
	pattern = re.compile(r"(^<tr\salign=\"right\")")
	pattern_rank = re.compile(r"([0-9]{1,4})")
	pattern_name = re.compile(r"(?![tr])(?![right])(?![ailgn])(?!td)([a-zA-Z]+)(?<!td)")
	for line in lines:
		if re.search(pattern, line) != None:
			rank = re.findall(pattern_rank, line)
			name = re.findall(pattern_name, line)
			name_and_rank.append(name[0] + " " + rank[0])
			name_and_rank.append(name[1] + " " + rank[0])

	return name_and_rank


#extarcts each years baby names
def extract_each_names_to_stdout(arguments):
	for each in arguments:
		print extract_names(each)
		print "\n"


#write summary files
def generate_summary_files(filename, name_and_rank_list):
	with open("summary/"+filename+".summary",'w') as f:
		for name_and_rank in name_and_rank_list:
			f.write(name_and_rank + os.linesep)

#iterates over each files and creates summary on each files
def extract_each_names_with_summary(arguments):
	for each in arguments:
		generate_summary_files(each, extract_names(each))



def extract_names(filename):
  """
  Given a file name for baby.html, returns a list starting with the year string
  followed by the name-rank strings in alphabetical order.
  ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
  """
  # +++your code here+++
  lines = read_file(filename)
  
  result = sorted(find_rank_and_name(lines))
  result.insert(0,find_year(lines)[0])
  return result



def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]

  if not args:
    print 'usage: [--summaryfile] file [file ...]'
    sys.exit(1)


  # Notice the summary flag and remove it from args if it is present.
  summary = False
  if args[0] == '--summaryfile':
  	print "writing summary files"
  	os.makedirs("summary") #create summary directory
  	summary = True
  	del args[0]

  # +++your code here+++
  # For each filename, get the names, then either print the text output
  # or write it to a summary file

  #iterating over each file in passed as command line argument
  if summary:
  	extract_each_names_with_summary(args)
  else:
  	extract_each_names_to_stdout(args)
  
if __name__ == '__main__':
  main()
