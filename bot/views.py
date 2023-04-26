from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, ImageSendMessage
from bs4 import BeautifulSoup
import requests
#from tools import get_chrome, find_element

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parse = WebhookParser(settings.LINE_CHANNEL_SECRET)


def get_biglottery():
    try:
        url = 'https://www.taiwanlottery.com.tw/lotto/Lotto649/history.aspx'
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'lxml')
        trs = soup.find('table', class_="table_org td_hm").find_all('tr')
        data1 = [td.text.strip() for td in trs[0].find_all('td')]
        data2 = [td.text.strip() for td in trs[1].find_all('td')]
        numbers = [td.text.strip() for td in trs[4].find_all('td')][1:]
        data = ''
        for i in range(len(data1)):
            data += f'{data1[i]}:{data2[i]}\n'
        data += ','.join(numbers[:-1])+'特別號:'+numbers[-1]
        print(data)

        return data
    except Exception as e:
        print(e)
        return '取得大樂透號碼，請稍後在試...'


def get_movie():
    try:
        url = 'https://movies.yahoo.com.tw/chart.html'
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'lxml')
        trs = soup.find('div', class_="rank_list table rankstyle1").find_all(
            'div', class_='tr')

        data = ''
        for i, tr in enumerate(trs[1:]):
            tds = tr.find_all('div', class_='td')
            rank = tds[0].text.strip()
            title = tds[3].find('h2').text.strip(
            ) if i == 0 else tds[3].text.strip()
            link = tds[3].find('a').get('href')
            data += f'\n本周排名:{rank} 電影名稱:{title}\n 連結:{link}\n'+'='*52
            print(f'本周排名:{rank} 電影名稱:{title}\n連結:{link}\n')
        return data
    except Exception as e:
        print(e)


def Jincai_539():
    try:

        url = 'https://www.taiwanlottery.com.tw/lotto/DailyCash/history.aspx'

        resp = requests.get(url)

        soup = BeautifulSoup(resp.text, 'lxml')

        trs = soup.find('table', class_="table_org td_hm").find_all('tr')

        prd = [td.text.strip().split()[0] for td in trs[2].find_all('td')[:1]]

        prd_date = [td.text.strip().split()[1]
                    for td in trs[2].find_all('td')[:1]]

        data1 = [td.text.strip() for td in trs[0].find_all('td')[:-1]] + \
            [td.text.strip() for td in trs[3].find_all('td')[:2]]+prd

        dates = [td.text.strip() for td in trs[1].find_all('td')[1:2]]
        date3 = []
        for date in dates:
            print(date.replace('開獎\n', ''))
            date3.append(date.replace('開獎\n', ''))

        data2 = [td.text.strip() for td in trs[1].find_all('td')[:1]]+date3 + \
            [td.text.strip() for td in trs[4].find_all('td')[:2]]+prd_date

        numbers = [td.text.strip() for td in trs[2].find_all('td')[2:]]

        data = ''
        for i in range(len(data1)):
            print(f'{data1[i]}:{data2[i]}')
            data += f'{data1[i]}:{data2[i]}\n'

        data += ','.join(numbers)
        return data
    except Exception as e:
        print(e)


def ktv_rank():
    try:
        url = 'https://www.holiday.com.tw/SongInfo/SongList.aspx?st=top&lt=tc'
        chrome = get_chrome(url, hide=True)
        soup = BeautifulSoup(chrome.page_source, 'lxml')
        sings = soup.find(id="divSongList").find_all(
            'div', class_="songs-list")
        data = ''
        for sing in sings:
            rank = sing.find('div', class_="songs-number").text.strip()
            last_rank = sing.find('div', class_="songs-l-number").text.strip()
            title = sing.find('div', class_="name").text.strip()
            name = sing.find('a').text.strip()
            #print(f'本週排名:{rank} 上週排名:{last_rank} 歌名:{title} 歌手:{name}',end='\n')
            data += f'\n本週排名:{rank} 上週排名:{last_rank} 歌名:{title} 歌手:{name}\n'+'='*52
            # print('==============================================')
        # print(data)
        return data
    except Exception as e:
        print(e)


def get_weather():
    try:
        url = 'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=rdec-key-123-45678-011121314&format=JSON'
        data = requests.get(url)   # 取得 JSON 檔案的內容為文字
        data_json = data.json()    # 轉換成 JSON 格式
        location = data_json['cwbopendata']['dataset']['location']
        datas = ''
        for i in location:
            city = i['locationName']    # 縣市名稱
            # 天氣現象
            wx8 = i['weatherElement'][0]['time'][0]['parameter']['parameterName']
            # 最高溫
            maxt8 = i['weatherElement'][1]['time'][0]['parameter']['parameterName']
            # 最低溫
            mint8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']
            # 舒適度
            ci8 = i['weatherElement'][3]['time'][0]['parameter']['parameterName']
            # 降雨機率
            pop8 = i['weatherElement'][4]['time'][0]['parameter']['parameterName']
            datas += f'{city}未來 8 小時{wx8}，最高溫 {maxt8} 度，最低溫 {mint8} 度，降雨機率 {pop8} %\n'+'='
        return datas
    except Exception as e:
        print(e)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parse.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:
            if isinstance(event, MessageEvent):
                message = None
                text = event.message.text
                print(text)
                if text == '1':
                    message = '早安'
                elif text == '2':
                    message = '午安'
                elif text == '3':
                    message = '晚安'
                elif '早安' in text:
                    message = '早安你好!'
                elif '捷運' in text:
                    mrts = {
                        '台北': 'https://web.metro.taipei/pages/assets/images/routemap2023n.png',
                        '台中': 'https://assets.piliapp.com/s3pxy/mrt_taiwan/taichung/20201112_zh.png?v=2',
                        '高雄': 'https://upload.wikimedia.org/wikipedia/commons/5/56/%E9%AB%98%E9%9B%84%E6%8D%B7%E9%81%8B%E8%B7%AF%E7%B6%B2%E5%9C%96_%282020%29.png'
                    }
                    image_url = 'https://web.metro.taipei/pages/assets/images/routemap2023n.png'
                    for mrt in mrts:
                        if mrt in text:
                            image_url = mrts[mrt]
                            print(image_url)
                            break
                elif '樂透' in text:
                    message = get_biglottery()
                elif '今彩539' in text:
                    message = Jincai_539()
                elif '電影' in text:
                    message = get_movie()
                # elif 'ktv'.lower() in text:
                    #message = ktv_rank()
                elif '星座' in text:
                    message = 'https://www.youtube.com/watch?v=KusSOMoeI_8&ab_channel=%E5%A5%B3%E4%BA%BA%E6%88%91%E6%9C%80%E5%A4%A7'
                elif '天氣' in text:
                    message = get_weather()
                else:
                    message = '抱歉，我不知道你說甚麼?'

                if message is None:
                    message_obj = ImageSendMessage(image_url, image_url)
                else:
                    message_obj = TextSendMessage(text=message)
                line_bot_api.reply_message(event.reply_token, message_obj)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


def index(request):
    return HttpResponse("<h1>你好，我是AI機器人</h1>")
