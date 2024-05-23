import re
from urllib.request import urlopen


def get_external_ip():
    # add wearetriple
    EXTERNAL_IP_URLS = [
        "https://ifconfig.wearetriple.com",
        "https://api.ipify.org",
        "https://ident.me",
        "https://icanhazip.com",
        "https://myexternalip.com/raw",
        "https://ipecho.net/plain",
        "https://checkip.amazonaws.com",
        "https://ipinfo.io/ip"
    ]
    for url in EXTERNAL_IP_URLS:
        try:
            response = urlopen(url)
            data = response.read().decode("utf-8").strip()

            # check if valid ip
            if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", data):
                return data
        except Exception as e:
            print(e)
            continue
    
    print("None of the external IP services are available.")
    print("Most likely there is no network connection.")
