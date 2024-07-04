# -*- coding: utf-8 -*-

import argparse
import requests
from bs4 import BeautifulSoup
import re

parser = argparse.ArgumentParser()
parser.add_argument("--url", default="inforrunning.ru", help="Link to parse")

args = parser.parse_args()

def parse_url(url: str):

	if not re.search("^https?://", url): url = "https://" + url

	try:
		print("Connection to", url, "....")
		response = requests.get(url)
		if response.status_code != 200: 
			error_text = f"Status_code for {response.url} response: {response.status_code} and is not 200 !!!"
			raise Exception(error_text)
	except:
		raise

	try:
		host = re.search("https?://(.+\\.)*(.+\\..+?)(/|\\?|$)", url).group(2).strip()
	except Exception as e:
		print(f"Host is not found in url {url} !!!")
		raise

	def func_starts_with():
		def wrapper(href):
			return href and (href.startswith("https://") or href.startswith("http://")) and host not in href 
		return wrapper

	soup = BeautifulSoup(response.content, "html.parser")
	soup_hrefs = soup.find_all("a", href=func_starts_with())

	counter = 0
	output_way = input("Where external links to print to (empty - console (default), 1 - file): ")
	if int(output_way) == 1:			 
		while True:
			file_path = input("Input file name with path (empty - default file links.txt in current folder): ").strip()
			if file_path == "": file_path = "links.txt"
			try:
				f = open(file_path, "w")
			except:
				print("Path from your input is unavailable")
				continue
			break

			with f:
				f.write(f"External links on url {response.url}:\n")
				for link in soup_hrefs:
					counter += 1
					f.write(f"-{counter}- {link.text.strip()} {link['href']}") 

	print(f"External links on url {response.url}:\n")
	for link in soup_hrefs:
		counter += 1
		print(f"-{counter}- {link.text.strip()} {link['href']}")



parse_url(args.url)