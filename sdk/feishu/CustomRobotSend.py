import json

import requests

"""
[[{'tag': 'text', 'text': 'KONO实时营销数据'}], [{'tag': 'text', 'text': '>>日期：2024-10-11'}], [{'tag': 'text', 'text': '>>获取时间：2024-10-11 11:08:31'}], [{'tag': 'text', 'text': '【经典数据】'}], [{'tag': 'text', 'text': '>>经典消耗：0.00'}], [{'tag': 'text', 'text': '>>经典总成交：0.00'}], [{'tag': 'text', 'text': '>>经典ROI：除数为0，无法计算'}], [{'tag': 'text', 'text': '【沙龙数据】'}], [{'tag': 'text', 'text': '>>沙龙消耗：0.00'}], [{'tag': 'text', 'text': '>>沙龙成交：0.00'}], [{'tag': 'text', 'text': '>>沙龙ROI：除数为0，无法计算'}], [{'tag': 'text', 'text': '【新香氛数据】'}], [{'tag': 'text', 'text': '>>新香氛消耗：0.00'}], [{'tag': 'text', 'text': '>>新香氛成交：0.00'}], [{'tag': 'text', 'text': '>>新香氛ROI：0.00'}], [{'tag': 'text', 'text': '【淘客数据】'}], [{'tag': 'text', 'text': '>>淘客佣服：340.42'}], [{'tag': 'text', 'text': '>>淘客销售额：1702.01'}], [{'tag': 'text', 'text': '>>淘客ROI：5.00'}], [{'tag': 'text', 'text': '【达播数据】'}], [{'tag': 'text', 'text': '>>达播佣服：170.22'}], [{'tag': 'text', 'text': '>>达播销售额：851.09'}], [{'tag': 'text', 'text': '【关键词数据】'}], [{'tag': 'text', 'text': '>>关键词消耗：2707.79'}], [{'tag': 'text', 'text': '>>关键词直接成交：4642.69'}], [{'tag': 'text', 'text': '>>关键词总成交：7725.04'}], [{'tag': 'text', 'text': '【精准人群推广数据】'}], [{'tag': 'text', 'text': '>>精准人群消耗：300.45'}], [{'tag': 'text', 'text': '>>精准人群直接成交：651.59'}], [{'tag': 'text', 'text': '>>精准人群总成交：867.59'}], [{'tag': 'text', 'text': '【万相台数据】'}], [{'tag': 'text', 'text': '>>万相台消耗：349.80'}], [{'tag': 'text', 'text': '>>万相台总成交：1376.86'}], [{'tag': 'text', 'text': '【超级直播数据】'}], [{'tag': 'text', 'text': '>>超级直播消耗：0.00'}], [{'tag': 'text', 'text': '>>超级直播成交：0.00'}], [{'tag': 'text', 'text': '【全域智投数据】'}], [{'tag': 'text', 'text': '>>全域智投消耗：0.00'}], [{'tag': 'text', 'text': '>>全域智投成交：0.00'}], [{'tag': 'text', 'text': '【全站推广数据】'}], [{'tag': 'text', 'text': '>>全站推广消耗：3392.53'}], [{'tag': 'text', 'text': '>>全站推广直接成交：6762.89'}], [{'tag': 'text', 'text': '>>全站推广总成交：8201.63'}], [{'tag': 'text', 'text': '【广告总数据】'}], [{'tag': 'text', 'text': '>>广告总成交：19022.21'}], [{'tag': 'text', 'text': '>>广告总消耗：7090.99'}], [{'tag': 'text', 'text': '>>广告总ROI：2.68'}], [{'tag': 'text', 'text': '【广告直接成交数据】'}], [{'tag': 'text', 'text': '>>广告直接成交：12057.17'}], [{'tag': 'text', 'text': '>>广告总消耗：7090.99'}], [{'tag': 'text', 'text': '>>广告直接ROI：1.70'}], [{'tag': 'text', 'text': '【站外时段效果】'}], [{'tag': 'text', 'text': '>>站外时段消耗：0.00'}], [{'tag': 'text', 'text': '>>站外时段成交：0.00'}], [{'tag': 'text', 'text': '>>站外时段ROI：除数为0，无法计算'}], [{'tag': 'text', 'text': '【站内时段效果】'}], [{'tag': 'text', 'text': '>>站内时段消耗：1314.70'}], [{'tag': 'text', 'text': '>>站内时段成交：3799.30'}], [{'tag': 'text', 'text': '>>站内时段ROI：2.89'}], [{'tag': 'text', 'text': '【全店销售额】'}], [{'tag': 'text', 'text': '>>全店销售额：32336.17'}], [{'tag': 'text', 'text': '>>站外占比：0.00'}], [{'tag': 'text', 'text': '>>站内占比：0.21'}], [{'tag': 'text', 'text': '>>全店占比：0.22'}]]

"""


def send_text(texts: list):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    content = []
    for text in texts:
        for t in text:
            content.append(t['text'])
    msg = {
        "msg_type": "text",
        "content": {
            "text": "\n".join(content)
        }

    }
    rep = requests.request(
        method="post", headers=headers,
        url="https://open.feishu.cn/open-apis/bot/v2/hook/73d899f5-5f87-45e6-b322-821d8ffc49f8", data=json.dumps(msg)
        # url="", data=json.dumps(msg)
    )
    return rep.json()


def read_wps_data(texts: list):
    hook_url = "https://www.kdocs.cn/api/v3/ide/file/crHqb8IjxQyC/script/V2-1WA5RMroDJiySbRHr0HQOU/sync_task"
    token = "2XeqmzoIHDaCqs8AWPbUZK"
    headers = {
        'Content-Type': "application/json",
        'AirScript-Token': token
    }
    data_value = []
    for text in texts:
        for t in text:
            if t["text"] == "KONO昨日同时段营销数据":
                return
            if ">>" in t["text"]:
                data_value.append(
                    t["text"].split("：")[1]
                )
    key_value = [
        "currentDate",
        "getCurrentDate",
        "clssicConsumption",
        "clssicDeal",
        "clssicROI",
        "shalogConsumption",
        "shalogDeal",
        "shalogROI",
        "xiangfenConsumption",
        "xiangfenDeal",
        "xiangfenROI",
        "taokeHire",
        "taokeSale",
        "taokeROI",
        "daboHire",
        "daboSale",
        "keyConsumption",
        "keyDeal",
        "keyAllDeal",
        "preciseConsumption",
        "preciseDeal",
        "preciseAllDeal",
        "wangxiangtaiConsumption",
        "wangxiangtaiDeal",
        "superliveConsumption",
        "superliveDeal",
        "universeConsumption",
        "universeDeal",
        "universepromotionConsumption",
        "universepromotionDeal",
        "universepromotionAllDeal",
        "adsDeal",
        "adsConsumption",
        "adsROI",
        "adsdataDeal",
        "adsdataConsumption",
        "adsdataROI",
        "outsidestationConsumption",
        "outsidestationDeal",
        "outsidestationROI",
        "insidestationConsumption",
        "insidestationDeal",
        "insidestationROI",
        "shopSale",
        "shopOutsidestationPer",
        "shopInsidestationPer",
        "shopPer"
    ]
    argv = dict(zip(key_value, data_value))

    data = {
        "Context": {
            "argv": argv
        }
    }
    print(data)

    rep = requests.request(
        method="post",
        url=hook_url,
        headers=headers,
        data=json.dumps(data, ensure_ascii=False).encode(encoding='utf-8')
    )
    print(rep.text)
