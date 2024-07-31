import crawler
import argparse


def commandline():
    argument = argparse.ArgumentParser()
    argument.add_argument("-w", "--wordlist", dest="wordlist", help="mention the wordlist to use for guessing")
    argument.add_argument("-u", "--url", dest="url", help="mention the url to scan", required=True)
    argument.add_argument("-f", "--find", dest="find", help="find directories, domains", required=True)
    return argument.parse_args()


values = commandline()

if values.wordlist is None:
    values.wordlist = "common.txt"

obj = crawler.Crawl(values.url, values.wordlist)
if values.find.lower() == "directories":
    obj.find_directories()
elif values.find.lower() == "domains":
    obj.find_subdomains()
elif values.find.lower() == "links":
    spidey = crawler.Spider()
    spidey.get_links(values.url)
