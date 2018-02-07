#For Qianjun
from urllib import request
from lxml import etree
import json
import time
import requests

iterms = ["注册商", "联系邮箱", "注册城市", "创建时间"]
def get_title(website):
    url = "http://whois.chinaz.com/getTitleInfo.ashx"
    payload="host=" +website + "&isupdate="
    headers ={
        'Host': 'whois.chinaz.com',
        'Connection': 'keep-alive',
        'Content-Length': '28',
        'Origin': 'http://whois.chinaz.com',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    ret = requests.post(url,payload, headers = headers);
    return ret.text

def get_rank(website):
    url = "http://alexa.chinaz.com/" + website
    page = request.urlopen(url)
    html = page.read().decode("utf-8")
    # print(html)
    tree = etree.HTML(html)

    ranks = tree.xpath("//*[@class=\"row_title bor-t1s pt20 clearfix\"]/h4/em[2]")
    # print(ranks)
    if len(ranks) > 0:
        return ranks[0].text
    else:
        return ""


def get_info(website):
    items
    result = {"注册商": "", "联系邮箱": "", "注册城市": "", "创建时间": "", "rank": "", "title":"", "keywords":[], "description":""}
    url = "http://whois.chinaz.com/" + website
    page = request.urlopen(url)
    html = page.read().decode("utf-8")

    # print(html)
    tree = etree.HTML(html)
    result["rank"] = get_rank(website)
    for i in range(1, 10):
        path1 = "//*[@id=\"sh_info\"]/li[" + str(i) + "]/div[1]"
        path2 = "//*[@id=\"sh_info\"]/li[" + str(i) + "]/div[2]/span"
        path3 = "//*[@id=\"sh_info\"]/li[" + str(i) + "]/div[2]/div/span"

        left = tree.xpath(path1)
        right = tree.xpath(path2)
        if len(left) > 0:
            title = left[0].text
            if len(right) > 0:
                val = right[0].text
            else:
                right = tree.xpath(path3)
                if len(right) > 0:
                    val = right[0].text
                else:
                    continue
            if title in iterms:
                result[title] = val

    tree = etree.HTML(get_title(website))
    title = tree.xpath("//p[1]")
    if len(title)>0:
        result["title"] = title[0].text
    keywords = tree.xpath("//p[2]/a")
    for keyword in keywords:
        result["keywords"].append(keyword.text)
    description = tree.xpath("//p[3]")
    if len(description)>0 :
        result["description"] = description[0].text
    return result


if __name__ == "__main__":
    f = open("websites.txt")
    out_f = open('websites_info.txt', 'w')
    line = f.readline()
    count = 0
    while line:
        result = get_info(line)
        json_out = json.dumps(result)
        out_f.write(json_out)
        out_f.write("\n")
        # json_to_python = json.loads(json_out)
        # print(json_to_python)
        line = f.readline()
        count += 1
        print("finish " + str(count) + " websites.")
        # break
        time.sleep(1)
    f.close()
    out_f.close()
