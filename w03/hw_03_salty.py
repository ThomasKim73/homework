# 라이브러리 imports
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient             # pymongo를 임포트 하기(패키지 설치 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)    # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                        # 'dbsparta'라는 이름의 db를 사용합니다. 'dbsparta' db가 없다면 새로 만듭니다.


# 타겟 URL을 읽어서 HTML 받아옴
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200801',headers=headers)

# HTML을 BeautifulSoup 라이브러리 활용 > 검색 용이한 상태
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.
soup = BeautifulSoup(data.text, 'html.parser')
hitsongs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

#############################
# 코딩
#############################
for tr in hitsongs:
    rank = tr.select_one('td.number').text[0:2].strip()
    title = tr.select_one('td.info > a.title.ellipsis').text.strip()
    artist = tr.select_one('td.info > a.artist.ellipsis').text
    print(rank, title, artist)

    doc = {
        'rank' :rank,
        'title' : title,
        'artist' : artist
    }
    db.genie.insert_one(doc)


#############################
# 사이트 분석 - copy selector
#############################
# web site address - 8월 1일 genie 뮤직 음원순위
# https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200801
# rank
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.number
# title
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis
# artist
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis

#############################
# Github Upload
#############################