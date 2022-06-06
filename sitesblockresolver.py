import dns.resolver
from bs4 import BeautifulSoup
import requests

def scrape_blocked_domains():
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"}
    html_data = requests.get("https://sitesbloqueados.pt/",headers=headers)
    soup = BeautifulSoup(html_data.text, 'html.parser')
    data = [a.text.strip() for a in soup.select("div[class='row list-content'] > p")]
    return data

# Usar alternativa em baixo para ler de um ficheiro
#domains = open("urls.txt").read().splitlines()
domains = scrape_blocked_domains()

def resolve_domain(domain):
    resolver = dns.resolver.Resolver()
    resolver.timeout = 5
    resolver.lifetime = 5
    try:
        answers = resolver.resolve(domain,'NS')
        for server in answers:
            if "cloudflare" in str(server.target) or "cloudfront" in str(server.target):
                return True
        return False
    except:
        return "dead"

cloud_tag = 0
offline_tag = 0
for index, i in enumerate(domains):
    resolve_data = resolve_domain(i)
    if resolve_data == True:
        cloud_tag+=1
        print(str(index+1) + " - " + str(i) + " - is using CLOUDFLARE: " + str(cloud_tag))
    elif resolve_data == "dead":
        offline_tag+=1
        print(str(index+1) + " - " + str(i) + " - DEAD: ")
    else:
        print(str(index+1) + " - " + str(i) + " - FALSE: ")
print("CLOUDFLARE NUMBER: " + str(cloud_tag))
print("DEAD NUMBER: " + str(offline_tag))
