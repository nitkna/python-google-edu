#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""
#find lines with puzzle in it
def read_puzzle(filename):
	puzzles = []
	with open(filename, 'r') as f:
		for line in f:
			if 'puzzle' in line:
				puzzles.append(line)
	return puzzles

#get all image urls with server name
def get_urls(puzzles, filename):
	server_name = get_server_name(filename)
	urls =[]
	url_pattern = re.compile(r'(GET\s*[a-z\/.-]*)')
	for puzzle in puzzles:
		unformated_url = re.findall(url_pattern, puzzle)
		url = unformated_url[0].split(" ")[1]
		if url.endswith(".jpg"):
			urls.append("http://"+server_name + url)

	return urls

def get_server_name(logfile):
	return logfile.split("_")[1]

#remove duplicates from the url list
def remove_duplicates(urls):
	img_urls = []
	for url in urls:
		if url not in img_urls:
			img_urls.append(url)

	return img_urls

def pp(k):
	for i in k:
		print i


def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  # +++your code here+++
  return remove_duplicates(sorted(get_urls(read_puzzle(filename), filename)))
  
def get_image_and_move(img_urls, dest_dir):
	image_no = 0
	os.makedirs(dest_dir)
	for url in img_urls:
		image_path = urllib.urlretrieve(url)[0]
		to_dir = dest_dir+"/img"+str(image_no)+".jpg"
		print "retrieved image to: ", image_path
		print "moving: ", image_path, ">>", to_dir
		os.system("mv {} {}".format(image_path, to_dir))
		image_no += 1

	return image_no

def create_index_file(images_count, dest_dir):
	with open("index.html", 'w') as f:
		f.write("<html>\n<body>")
		for i in xrange(0, images_count ):
			img_location = "img{}".format(i) +".jpg"
			f.write("<img src ={}>".format(img_location))
		f.write("</body>\n</html>")

	os.system("mv index.html {}".format(dest_dir+"/"+"index.html"))
	


  

def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  # +++your code here+++
  image_count = get_image_and_move(img_urls, dest_dir)
  create_index_file(image_count, dest_dir)

def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])
  pp(img_urls)

  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
