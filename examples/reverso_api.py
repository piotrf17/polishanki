import json
import re
import urllib.request

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
BASE_URL = "https://context.reverso.net/bst-query-service"
REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "pl-PL,pl;q=0.9",
    "Content-Type": "application/json",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "Linux",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": USER_AGENT,
}


def _cleanup_html_tags(text):
    """Remove html tags like <b>...</b> or <em>...</em> from text
    I'm well aware that generally it's a felony, but in this case tags cannot even overlap
    """
    return re.sub(r"<.*?>", "", text)


def request_translations(word, page_num=1):
    data = {
        "source_lang": "pl",
        "target_lang": "en",
        "source_text": word,
        "target_text": "",
        "npage": page_num,
        "mode": 0,
    }
    json_data = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(BASE_URL, data=json_data)
    for header, val in REQUEST_HEADERS.items():
        req.add_header(header, val)
    with urllib.request.urlopen(req) as response:
        response_data = response.read().decode("utf-8")
        response_json = json.loads(response_data)
    results = []
    for example_json in response_json["list"]:
        polish = _cleanup_html_tags(example_json["s_text"])
        english = _cleanup_html_tags(example_json["t_text"])
        source = example_json["cname"]
        results.append(
            {
                "polish": polish,
                "english": english,
                "source": source,
            }
        )
    return results


if __name__ == "__main__":
    r = request_translations("stary")
    print(r)
