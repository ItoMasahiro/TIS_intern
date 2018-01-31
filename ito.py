import collections
import json
from _operator import itemgetter

import requests
from bottle import get, run
from bs4 import BeautifulSoup

if __name__ == "__main__":
    todos = collections.defaultdict(str)


    @get("/dict1/<code>")
    def _dict1(code):  # 指定された企業の情報を返す
        print(f"code is {code}")
        # webpageのテキストを取得
        r = requests.get("https://jp.kabumap.com/servlets/kabumap/Action?SRC=marketList/base")
        # webpageをパースし必要なテキストを収集
        bs = BeautifulSoup(r.text, "html.parser")

        stockList = []
        tempMap = {}
        for i, text in enumerate(bs.find_all('a', onmouseout='javascript:hideChart(0);')):  # 銘柄コード、企業名が含まれる要素を取得
            #  対応箇所を抜き取る
            if i % 2 == 0:
                tempMap['code'] = text.string
            else:
                tempMap['name'] = text.string
                stockList.append(tempMap.copy())

        for i, text in enumerate(bs.find_all('td', class_='KM_NUMERIC')):
            if i % 10 == 0:
                stockList[int(i / 10)]['price'] = text.string
            if i % 10 == 2:
                stockList[int(i / 10)]['change'] = text.string

        for i in stockList:
            if i['code'] == code or i['name'] == code:
                res = {"code": i["code"], "name": i["name"], "price": i["price"]}
                return json.dumps(res)

        return json.dumps({"name": "銘柄が見つかりませんでした", "price": "ごめんなさい"})


    @get("/dict2")
    def _dict2():  # 上昇率ランキングを返す
        # webpageのテキストを取得
        r = requests.get("https://jp.kabumap.com/servlets/kabumap/Action?SRC=marketList/base")
        # webpageをパースし必要なテキストを収集
        bs = BeautifulSoup(r.text, "html.parser")

        stockList = []
        tempMap = {}
        for i, text in enumerate(bs.find_all('a', onmouseout='javascript:hideChart(0);')):  # 銘柄コード、企業名が含まれる要素を取得
            #  対応箇所を抜き取る
            if i % 2 == 0:
                tempMap['code'] = text.string
            else:
                tempMap['name'] = text.string
                stockList.append(tempMap.copy())

        for i, text in enumerate(bs.find_all('td', class_='KM_NUMERIC')):
            if i % 10 == 0:
                stockList[int(i / 10)]['price'] = text.string
            if i % 10 == 2:
                stockList[int(i / 10)]['change'] = text.string

        changeList = []  # stockListを上昇率でソートするためのリスト
        for i, stock in enumerate(stockList):
            changeList.append([i, float(stock['change'])])
        print(stockList)
        changeList.sort(key=itemgetter(1))  # 上昇率でソート
        changeList.reverse()

        print(changeList)

        res = {}
        for i in range(0, 3):
            key = "rank" + str(i + 1)
            res[key] = {"code": stockList[changeList[i][0]]["code"],
                        "name": stockList[changeList[i][0]]["name"],
                        "price": stockList[changeList[i][0]]["price"],
                        "change": stockList[changeList[i][0]]["change"]}

        return json.dumps(res)


    @get("/dict3")
    def _dict3():  # 低下率ランキングを返す
        # webpageのテキストを取得
        r = requests.get("https://jp.kabumap.com/servlets/kabumap/Action?SRC=marketList/base")
        # webpageをパースし必要なテキストを収集
        bs = BeautifulSoup(r.text, "html.parser")

        stockList = []
        tempMap = {}
        for i, text in enumerate(bs.find_all('a', onmouseout='javascript:hideChart(0);')):  # 銘柄コード、企業名が含まれる要素を取得
            #  対応箇所を抜き取る
            if i % 2 == 0:
                tempMap['code'] = text.string
            else:
                tempMap['name'] = text.string
                stockList.append(tempMap.copy())

        for i, text in enumerate(bs.find_all('td', class_='KM_NUMERIC')):
            if i % 10 == 0:
                stockList[int(i / 10)]['price'] = text.string
            if i % 10 == 2:
                stockList[int(i / 10)]['change'] = text.string

        changeList = []  # stockListを上昇率でソートするためのリスト
        for i, stock in enumerate(stockList):
            changeList.append([i, float(stock['change'])])
        changeList.sort(key=itemgetter(1))  # 上昇率でソート

        res = {}
        for i in range(0, 3):
            key = "rank" + str(i + 1)
            res[key] = {"code": stockList[changeList[i][0]]["code"],
                        "name": stockList[changeList[i][0]]["name"],
                        "price": stockList[changeList[i][0]]["price"],
                        "change": stockList[changeList[i][0]]["change"]}

        return json.dumps(res)

    run(host="0.0.0.0", port=8080)
