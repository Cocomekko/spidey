#! /usr/bin/env python
import requests
import urllib3
import re, urllib.parse


class Crawl:
    def __init__(self, main_url, wordlist):
        self.directories = set()
        self.subdomains = set()
        self.url = main_url
        self.wordlist = wordlist
        if "http://" not in self.url and "https://" not in self.url:
            self.url = "http://" + self.url

    def find_directories(self):
        with open(self.wordlist, "r") as file:
            for line in file:
                self.directories.add(self.url + "/" + line.strip())
        self.get_directories()

    def get_directories(self):
        directories = sorted(list(self.directories))
        for url in directories:
            response = requests.get(url)
            if "[404]" not in str(response):
                if "[200]" in str(response):
                    print(url)
                else:
                    print(url + "-"*10 + str(response.status_code))

    def find_subdomains(self):
        with open(self.wordlist, "r") as file:
            for line in file:
                replace_part = "http://" + line.strip() + "."
                subdomain = self.url.replace("http://", replace_part)
                self.subdomains.add(subdomain)
        self.get_subdomains()

    def get_subdomains(self):
        subdomains = sorted(list(self.subdomains))
        for url in subdomains:
            try:
                response = requests.get(url)
                if "[404]" not in str(response):
                    print(url)
            except requests.exceptions.ConnectionError:
                pass
            except urllib3.exceptions.LocationParseError:
                print(url + " " + "-"*10 + " cannot be parsed")
            except UnicodeError:
                print(url, "-"*19 + "Invalid url")


class Spider:
    def __init__(self):
        self.site_links = set()

    @staticmethod
    def find_links(url):
        links = []
        if "http://" not in url and "https://" not in url:
            url = "https://" + url
        response = requests.get(url)
        try:
            captured = re.findall('(?:href=")(.*?)"', response.content.decode("utf-8"))
            for ele in captured:
                if "[" not in ele and "]" not in ele:
                    links.append(ele)
        except UnicodeDecodeError:
            pass
        return links

    def get_links(self, url):
        if "http://" in url:
            domain_name = url.split("http://")[1]
        elif "https://" in url:
            domain_name = url.split("https://")[1]
        else:
            domain_name = url

        links = self.find_links(url)
        links = set(links)
        links = sorted(list(links))
        for link in links:
            try:
                link = urllib.parse.urljoin(url, link)
            except ValueError:
                print("Value error", link)
            if domain_name in link and link != url:
                if link not in self.site_links:
                    print(link)
                self.site_links.add(link)
                self.get_links(link)
