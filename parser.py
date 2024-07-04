# -*- coding: utf-8 -*-

import argparse
import requests
from bs4 import BeautifulSoup
import re

parser = argparse.ArgumentParser()
parser.add_argument("--url", default="inforrunning.ru", help="Link to parse")

args = parser.parse_args()
if not re.search("^https?://", args.url): args.url = "https://" + args.url

try:
	print("Connection to", args.url, "....")
	response = requests.get(args.url)
	if response.status_code != 200: 
		error_text = f"Status_code for {response.url} response: {response.status_code} and is not 200 !!!"
		raise Exception(error_text)
except:
	raise

try:
	host = re.search("https?://(.+\\.)*(.+\\..+?)(/|\\?|$)", args.url).group(2).strip()
except Exception as e:
	print(f"Host is not found in url {args.url} !!!")
	raise

def func_starts_with():
	def wrapper(href):
		return href and (href.startswith("https://") or href.startswith("http://")) and host not in href 
	return wrapper

soup = BeautifulSoup(response.content, "html.parser")
soup_hrefs = soup.find_all("a", href=func_starts_with())

print(f"External links on url {response.url}:\n")
counter = 0
for link in soup_hrefs:
	counter += 1
	print(f"-{counter}- {link.text.strip()} {link['href']}")
