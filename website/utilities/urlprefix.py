from flask import request


def geturl(prefix: str , echo: str):
    url = "/".join(request.base_url.split("/")[3:])
    print(url,"\n")
    print(request.base_url)
    if url:return echo if prefix == url else "" 
    return echo
