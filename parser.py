# -*- coding: utf-8 -*-

import argparse
import requests
from bs4 import BeautifulSoup
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--url", default="inforrunning.ru", help="Link to parse")
args = parser.parse_args()


def get_response(url, timeout):
	print("\n-Next step-")
	print("Connection to", url, "....", "   with timeout for:", timeout, "seconds", end=" ")
	try:
		response = requests.get(url, timeout=timeout)
		if 300 > response.status_code >= 200:
			print(" - OK got response")
			return response
		print(f"\n--- Status_code for {response.url} response: {response.status_code} and is not 200 !!!")
	except requests.exceptions.Timeout:
		print("\n--- Connection was closed after timeout of:", timeout_sec, "sec")
	except Exception as e:
		print("\n--- Failed to connect", url)
		print(e)


def func_starts_with(host):
	def wrapper(href):
		return href and (href.startswith("https://") or href.startswith("http://")) and host not in href
	return wrapper


def host_from_url(url):
	try:
		return re.search("https?://(.+\\.)*(.+\\..+?)(/|\\?|$)", url).group(2).strip()
	except:
		print(f"Host is not found in url {url} !!!")


def find_hrefs(html, host):
	print("hrefs analizing in html ... ", end=" ")
	soup = BeautifulSoup(html.content, "html.parser")
	hrefs = soup.find_all("a", href=func_starts_with(host))
	print(" - It's finished")

	return hrefs


def print_to_console(links, level):
	counter = 0
	for url in links:
		print(f"\n*** Level-{level} external links on url {url}:")
		for soup_link in links[url]:
			counter += 1
			print(f"{level}.{counter}. {soup_link.text.strip()} {soup_link['href']}")


def print_to_file(links, level, file_path):
	with open(file_path, "a") as f:
		orig_stdout = sys.stdout
		sys.stdout = f
		print_to_console(links, level)
		sys.stdout = orig_stdout


def print_links(links, level, file_path):
	if file_path: print("file_path: True")
	print_to_file(links, level, file_path) if file_path else print_to_console(links, level)


def parse_url(url, timeout):
	if not re.search("^https?://", url):
		url = "https://" + url
	host = host_from_url(url)
	response = get_response(url, timeout)
	if host and response:
		return find_hrefs(response, host)


def run(url):
	links = {url: [{'href': url}]}
	for level in range(nesting_level + 1):
		links_next = {}
		for url in links:
			soup_links = {soup_link['href']: soup_links for soup_link in links[url] if
						  (soup_links := parse_url(soup_link['href'], timeout_sec))}
			print_links(
				soup_links,
				level + 1,
				file_path)
			links_next |= soup_links
		links = links_next


nesting_level = input(f"What external links parsing nesting level of {args.url} to use (empty or 0 - default level of parsing {args.url} only): ")
nesting_level = int(nesting_level) if nesting_level.isdigit() else 0
output_way = input("Where external links to print to (1 - file, empty or other - console (default)): ")
to_file = output_way.isdigit() and int(output_way) == 1
if to_file:
	while True:
		file_path = input("Input file name with path (empty - default file links.txt in current folder): ").strip()
		if file_path == "": file_path = "links.txt"
		try:
			f = open(file_path, "w")
		except:
			print("Path from your input is unavailable")
			continue
		f.close()
		break
else:
	file_path = None
timeout_sec = input("What timeout set to connect to url (seconds, empty -  5 sec by default): ")
timeout_sec = timeout_sec if timeout_sec.isdigit() else 5

run(args.url)