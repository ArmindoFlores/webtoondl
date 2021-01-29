try:
    import cv2
    import imageio
    import numpy as np
except Exception:
    cv2 = None
import os

import requests
import tqdm
from bs4 import BeautifulSoup

COOKIES = {"pagGDPR": "true"}


def get_name_from_url(url):
    if url.endswith("/"):
        return url[:-1].split("/")[-1]
    else:
        return url.split("/")[-1]
    
def get_id_from_url(url):
    if url.endswith("/"):
        url = url[:-1].split("/")[-1]
    else:
        url = url.split("/")[-1]
    return url.split("=")[-1]

def get_url_from_id(eid):
    if eid.startswith("o"):
        full_url = f"https://www.webtoons.com/episodeList?titleNo={eid[1:]}"
    else:
        full_url = f"https://www.webtoons.com/challenge/episodeList?titleNo={eid[1:]}"
    req = requests.get(full_url, cookies=COOKIES)
    url = "/".join(req.url.split("/")[:-1]) + "/"
    return url

def get_img_urls(url, episode, eid):
    full_url = f"{url}a/viewer?title_no={eid}&episode_no={episode}"
    req = requests.get(full_url, cookies=COOKIES)
    soup = BeautifulSoup(req.content, features="lxml")
    content = soup.find("div", {"id": "content"})
    imagelist = content.find("div", {"id": "_imageList"})
    images = []
    if imagelist is not None:
        for img in imagelist.findAll("img", {"class": "_images"}):
            images.append(img["data-url"])
    return images, full_url

def get_filetype(url):
    if url.endswith("/"):
        return url[:-1].split("/")[-1].split("?")[0].split(".")[-1]
    else:
        return url.split("/")[-1].split("?")[0].split(".")[-1]

def download_imgs(urls, referer, name):
    names = []
    c = 1
    for url in tqdm.tqdm(urls):
        ext = get_filetype(url)
        req = requests.get(url, headers={"Referer": referer})
        assert req.status_code == 200
        with open(f"{name}-{c}.{ext}", "wb") as file:
            file.write(req.content)
        names.append(f"{name}-{c}.{ext}")
        c += 1
    return names

def download_imgs_of(urls, referer, name):
    c = 1
    for url in tqdm.tqdm(urls):
        ext = get_filetype(url)
        req = requests.get(url, headers={"Referer": referer})
        assert req.status_code == 200
        if ext != "gif":
            arr = np.asarray(bytearray(req.content), dtype=np.uint8)
            img = cv2.imdecode(arr, 1)
        else:
            with open("temp.gif", "wb") as f:
                f.write(req.content)
            img = np.array(imageio.imread("temp.gif"))[:,:,:-1]
            os.remove("temp.gif")
        if c == 1:
            curr = img
        else:
            if img.shape[1] > curr.shape[1]:
                img = img[:,:curr.shape[1]-img.shape[1],:]
            elif img.shape[1] < curr.shape[1]:
                curr = curr[:,:img.shape[1]-curr.shape[1],:]
            curr = cv2.vconcat([curr, img])
        c += 1
    cv2.imwrite(name+".png", curr)
    return name

def search(query):
    original_results, canvas_results = [], []
    full_url = f"https://www.webtoons.com/en/search?keyword={query}"
    req = requests.get(full_url, cookies=COOKIES)
    soup = BeautifulSoup(req.content, features="lxml")
    
    originals = soup.find("ul", {"class": "card_lst"})
    if originals is not None:
        for item in originals.findAll("li"):
            eid = int(item.a["href"].split("?")[-1].split("=")[-1])
            name = str(item.find("p", {"class": "subj"}).getText())
            author = str(item.find("p", {"class": "author"}).getText())
            likes = str(item.find("em", {"class": "grade_num"}).getText())
            genre = str(item.find("span", {"class": "genre"}).getText())
            original_results.append({"eid": eid, "name": name, "author": author, "likes": likes, "genre": genre, "type": "o"})
            
    canvas = soup.find("div", {"class": "challenge_lst"})
    if canvas is not None and canvas.ul is not None:
        canvas = canvas.ul
        for item in canvas.findAll("li"):
            eid = int(item.a["href"].split("?")[-1].split("=")[-1])
            name = str(item.find("p", {"class": "subj"}).getText())
            author = str(item.find("p", {"class": "author"}).getText())
            genre = str(item.find("p", {"class": "genre"}).getText())
            canvas_results.append({"eid": eid, "name": name, "author": author, "genre": genre, "type": "c"})
            
    return original_results, canvas_results
    