from requests import Session


def bypass_recaptcha3(get_url: str, post_url: str, proxy: str = {}):
    from urllib.parse import urlparse
    from urllib.parse import parse_qs
    url_variables = parse_qs(urlparse(get_url).query)
    with Session() as s:
        s.proxies.update(proxy)

        r = s.get(get_url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"})
        token_1 = r.text.split("type=\"hidden\" id=\"recaptcha-token\" value=\"")[1].split("\"")[0]

        data = f"v={url_variables['v'][0]}&reason=q&c={token_1}&k={url_variables['k'][0]}&co={url_variables['co'][0]}&hl=en&size=invisible"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "referer": r.url,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        r = s.post(post_url, headers=headers, data=data)
        return r.text.split("[\"rresp\",\"")[1].split("\"")[0]