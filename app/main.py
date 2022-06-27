from flask import Flask, request
# import requests
import psycopg2

app = Flask(__name__)

# passwd = '3efe88864056f4a63eeebc8a511d12675ce0c78e998192c9e0ab04438867195d'
# db = psycopg2.connect(host='ec2-44-206-89-185.compute-1.amazonaws.com', dbname='d3bj01t0cv3v8b',user='qiulfncvkhhxhw',password= passwd,port=5432)
# cur=db.cursor()

# # NOS 서버 db
passwd = 'b55d94be7d8dbef24e28a72a0dcb228fb48d1595665100e8da2cd1aafbe8bbbc'
db = psycopg2.connect(host='ec2-54-204-56-171.compute-1.amazonaws.com', dbname='d2p5j2up8o05rg',user='dywzgxybcyjnzu',password= passwd,port=5432)
cur=db.cursor()

@app.route('/')
def hello_world():
    return 'welcome world7'

@app.route('/api/hello', methods=['POST'])
def hello():
    # body = request.get_json() # 사용자가 입력한 데이터

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "시작하셔도 됩니다."
                    }
                }
            ]
        }
    }

    return responseBody


# 유저가 입력 한 값 반환
@app.route('/api/test', methods=['POST'])
def test():
    body = request.get_json() # 사용자가 입력한 데이터

    # 입력값 줄바꿈 제거
    body2 = str(body['userRequest']['utterance']).strip() 
    userID = str(body['userRequest']['user']['id'])

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": body2 + "입력완료! \n" + userID
                    }
                }
            ]
        }
    }

    return responseBody




# # 채널 접속
@app.route('/api/enterchannel', methods=['POST'])
def enterchannel():
    body = request.get_json() # 사용자가 입력한 데이터

    
    id_data = '%s' %str(body['userRequest']['user']['id'])
    idid_data = "'%s'" %str(body['userRequest']['user']['id'])
    try :
        text = body['userRequest']['utterance'].split(" ")[0]
    except :
        text = "korea"
        
    channel_data = '%s' %text
    channelchannel_data = "'%s'" %text
    cur=db.cursor()

    cur.execute("SELECT * FROM blackwhite2 WHERE channel=%s;" % (channelchannel_data))
    rows = cur.fetchall()

    cur.execute("SELECT * FROM blackwhite2 WHERE channel=%s AND userid=%s;" % (channelchannel_data, idid_data))
    rows2 = cur.fetchall()

    cur.execute("SELECT * FROM blackwhite2 WHERE userid=%s;" % (idid_data))
    rows3 = cur.fetchall()

    if len(rows2) != 0:
        result = "해당 채널에 이미 접속중이십니다"
    elif len(rows3) != 0:
        result = "이미 다른 채널에 접속중이십니다"
    elif len(rows) < 2:
        cur.execute("INSERT INTO blackwhite2 (userid, channel, score, turn, numbers, usenum) VALUES (%s, %s, %s, %s, %s, %s);"
            , (id_data, channel_data, 0, 0, 200, 0) )
        db.commit()
        result = "채널에 참가하였습니다"
    else :
        result = "해당 채널에 이미 사람이 다 찼습니다."

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": result
                    }
                }
            ]
        }
    }

    return responseBody


# # 숫자 제출하기
@app.route('/api/submitnumber', methods=['POST'])
def submitnumber():
    body = request.get_json() # 사용자가 입력한 데이터

    id_data = '%s' %str(body['userRequest']['user']['id'])
    idid_data = "'%s'" %str(body['userRequest']['user']['id'])
    round_winner = '%s' %("승리")
    round_loser = '%s' %("패배")
    round_draw = '%s' %("무승부")


    target_data = body['userRequest']['utterance']

    if (target_data != '발화 내용'):
        text = '0'
    else:
        text = target_data.split(" ")[0]
    
    

    cur.execute("SELECT * FROM blackwhite2 WHERE userid=%s AND turn='0';" % (idid_data))
    find_channel = cur.fetchall()

    userchannel = find_channel[0][1]
    channel_data = '%s' %(userchannel)
    channelchannel_data = "'%s'" %(userchannel)

    cur.execute("SELECT * FROM blackwhite2 WHERE userid=%s AND channel=%s;" % (idid_data, channelchannel_data))
    user_rows = cur.fetchall()

    cur.execute("SELECT * FROM blackwhite2 WHERE userid!=%s AND channel=%s;" % (idid_data, channelchannel_data))
    enemy_rows = cur.fetchall()

    # input_user_turn = '%s' %(len(user_rows))
    where_user_turn = "'%s'" %(len(user_rows)-1)
    where_enemy_turn = "'%s'" %(len(enemy_rows)-1)

    cur.execute("SELECT * FROM blackwhite2 WHERE userid=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_user_turn))
    user_last_rows = cur.fetchone()

    cur.execute("SELECT * FROM blackwhite2 WHERE userid!=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_enemy_turn))
    enemy_last_rows = cur.fetchone()
    
    if (len(enemy_rows) == 0):
            result = "상대방이 없습니다."
    # # 보유 포인트보다 더 많이 제출하려고 할 때
    elif (user_last_rows[4]-int(text) < 0) or (int(text) < 0) :
        result = "현재 남은 포인트는 %d개입니다.\n다시 제출하세요."
    else:
        result = "리스트: %d\n포인트: %d\n text: %d" %(len(user_last_rows), user_last_rows[4], int(text))
        # # 숫자 정상적으로 제출
        # if(len(user_rows) == len(enemy_rows)) :
        #     # # 길이가 같을 때 입력한 사람이 제출
        #     cur.execute("INSERT INTO blackwhite2 (userid, channel, score, turn, numbers, usenum) VALUES (%s, %s, %s, %s, %s, %s);"
        #         , (id_data, channel_data, user_last_rows[2], user_last_rows[3] + 1, 200 - int(text), int(text)) )
        #     db.commit()
        #     result = "%s라운드 제출 완료!" %(user_last_rows[3] + 1)
        # elif(len(user_rows) > len(enemy_rows)):
        #     result = "상대방이 제출 할 차례입니다."
        # elif(len(user_rows) < len(enemy_rows)):

        #     # # 양쪽 다 제출했으니 숫자를 비교 할 예정
        #     enemy_num = enemy_last_rows[5]
        #     user_num = int(text)

        #     # # 제출 한 사람이 승리 할 경우
        #     if (user_num > enemy_num):
        #         # # 유저 승리로 입력
        #         cur.execute("INSERT INTO blackwhite2 (userid, channel, score, turn, numbers, usenum, result) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        #             , (id_data, channel_data, user_last_rows[2] + 1, user_last_rows[3] + 1, 200 - int(text), int(text)), round_winner )
        #         # # 상대 패배로 입력
        #         cur.execute("UPDATE blackwhite2 SET result=%s WHERE userid!=%s AND channel=%s AND turn=%s;" % (round_loser, idid_data, channelchannel_data, where_enemy_turn))
        #         db.commit()
        #         result = "당신이 승리하였습니다!"
        #     # # 상대방이 승리 할 경우
        #     elif (user_num < enemy_num):
        #         # # 유저 패배로 입력
        #         cur.execute("INSERT INTO blackwhite2 (userid, channel, score, turn, numbers, usenum, result) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        #             , (id_data, channel_data, user_last_rows[2], user_last_rows[3] + 1, 200 - int(text), int(text)), round_loser )
        #         # # 상대 승리로 입력
        #         cur.execute("UPDATE blackwhite2 SET score=%s , result=%s WHERE userid!=%s AND channel=%s AND turn=%s;" % ( enemy_last_rows[2]+1, round_winner, idid_data, channelchannel_data, where_enemy_turn))
        #         db.commit()
        #         result = "상대방이 승리하였습니다!"
        #     # # 무승부인 상황
        #     elif (user_num == enemy_num):
        #         cur.execute("INSERT INTO blackwhite2 (userid, channel, score, turn, numbers, usenum, result) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        #             , (id_data, channel_data, user_last_rows[2], user_last_rows[3] + 1, 200 - int(text), int(text)), round_draw)
        #         # # 상대 승리로 입력
        #         cur.execute("UPDATE blackwhite2 SET score=%s , result=%s WHERE userid!=%s AND channel=%s AND turn=%s;" % ( enemy_last_rows[2], round_draw, idid_data, channelchannel_data, where_enemy_turn))
        #         db.commit()
        #         result = "무승부입니다!\n선 플레이어부터 다시 시작해주세요."

    

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": result
                    }
                }
            ]
        }
    }

    return responseBody




# # # 오늘의 만족도
# @app.route('/api/todayscore', methods=['POST'])
# def todayscore():

#     # date_data = "'%s'" %(datetime.today().strftime('%Y-%m-%d'))
#     cur.execute("SELECT * FROM score;")
#     rows = cur.fetchall()

#     today_score = 0
#     for i in range(len(rows)):
#         today_score = today_score + int(rows[i][2])
#     today_score = round(today_score / len(rows), 2)

#     responseBody = {
#         "version": "2.0",
#         "template": {
#             "outputs": [
#                 {
#                     "simpleText": {
#                         "text": "평균 만족도는 %s점이며\n총 %s명이 만족도 점수를 눌러주셨습니다." % (today_score, len(rows))
#                     }
#                 }
#             ]
#         }
#     }

#     return responseBody

# # # 모의주식 구매
# @app.route('/api/buyitem', methods=['POST'])
# def buyitem():

#     body = request.get_json() # 사용자가 입력한 데이터
#     target_item = body['userRequest']['utterance']
#     ssstttrrr = target_item.split()

#     # user=유저, money=잔액, item=주식, many=매수한 주식 수
#     if len(ssstttrrr) >= 3 :
#         item = "'%s'" % ssstttrrr[1]
#         many = int(ssstttrrr[2])

#     else :
#         item = "'%s'" % ("갤럭시")
#         many = 1
        
#     user = "'%s'" %str(body['userRequest']['user']['id'])
#     target_item = item

#     headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
#     data = requests.get('https://kr.investing.com/search/?q=' + target_item, headers=headers)
#     soup = BeautifulSoup(data.text, 'html.parser')

#     try:
#         item_code = soup.select_one('#fullColumn > div > div.js-section-wrapper.searchSection.allSection > div:nth-child(2) > div.js-inner-all-results-quotes-wrapper.newResultsContainer.quatesTable > a:nth-child(1) > span.second').text
#         item_name = soup.select_one('#fullColumn > div > div.js-section-wrapper.searchSection.allSection > div:nth-child(2) > div.js-inner-all-results-quotes-wrapper.newResultsContainer.quatesTable > a:nth-child(1) > span.third').text
 
#         try:
#             # # 국내 주식
#             # # naver finance에서 추출
#             target_data = web.DataReader(item_code, 'naver')
#             last = (target_data.shape[0])
#             target_data = target_data.iloc[last - 1].loc["Close"]

#             # # 가격 추출 성공!
#             item = "'%s'" % item_name
#             cur.execute("SELECT * FROM game WHERE userid = %s;"% (user))
#             rows = cur.fetchall()

#             # # id가 없을 시 투자자금 1,000,000원 지급
#             if len(rows) == 0 :
#                 cur.execute("INSERT INTO game (userid, money) VALUES (%s, %d);"% (user, 1000000) )

#             # # 돈만 있는 쿼리
#             cur.execute("SELECT * FROM game WHERE userid = %s AND money IS NOT null;"% (user))
#             rows2 = cur.fetchall()

#             # # 종목명과 id로 검색한 쿼리
#             cur.execute("SELECT * FROM game WHERE userid=%s AND item = %s;"% (user, item))
#             rows3 = cur.fetchall()

#             # 잔액이 0이상이면 실행
#             money = int(rows2[0][1]) - int(target_data) * many
#             if money >= 0 : 

#                 # # 가지고 있는 주식 종목을 추가로 구매 
#                 if len(rows3) != 0 :
#                     shares = rows3[0][3] + many
#                     cur.execute("UPDATE game SET shares=%d WHERE userid=%s AND item = %s;"% (shares, user, item) )
#                     cur.execute("UPDATE game SET money=%d WHERE userid=%s AND money IS NOT null;"% (money, user) )
#                     result =  str(many) + "주를 구매했습니다."
                    
#                 elif many <= 0:
#                     result = "수량을 확인해주세요."

#                 # # 가지고 있지 않은 주식을 구매
#                 else :
#                     cur.execute("INSERT INTO game (userid, item, shares) VALUES (%s, %s, %d);"% (user, item, many) )
#                     cur.execute("UPDATE game SET money=%d WHERE userid=%s AND money IS NOT null;"% (money, user) )
#                     result =  item_name + " " + str(many) + "주를 구매했습니다."
#             else :
#                 result = "잔액이 부족합니다"

#             db.commit()

#         except:
#             result = "해외 주식은 아직 구현을 못했습니다."

#     except AttributeError:
#         result = "'" + target_item.strip() + "' 으로 검색결과가 없습니다.\n" + "찾는 주식이 있다면 주식명과 주가를 입력해주세요."

#     responseBody = {
#             "version": "2.0",
#             "template": {
#                 "outputs": [
#                     {
#                         "simpleText": {
#                             "text": result
#                         }
#                     }
#                 ]
#             }
#         }

#     return responseBody

# # # 모의주식 판매
# @app.route('/api/sellitem', methods=['POST'])
# def sellitem():

#     body = request.get_json() # 사용자가 입력한 데이터
#     target_item = body['userRequest']['utterance']
#     ssstttrrr = target_item.split()

#     # user=유저, money=잔액, item=주식, many=매수한 주식 수
#     if len(ssstttrrr) >= 3 :
#         item = "'%s'" % ssstttrrr[1]
#         many = int(ssstttrrr[2])

#     else :
#         item = "'%s'" % ("갤럭시")
#         many = 1
        
#     user = "'%s'" %str(body['userRequest']['user']['id'])
#     target_item = item

#     headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
#     data = requests.get('https://kr.investing.com/search/?q=' + target_item, headers=headers)
#     soup = BeautifulSoup(data.text, 'html.parser')

#     try:
#         item_code = soup.select_one('#fullColumn > div > div.js-section-wrapper.searchSection.allSection > div:nth-child(2) > div.js-inner-all-results-quotes-wrapper.newResultsContainer.quatesTable > a:nth-child(1) > span.second').text
#         item_name = soup.select_one('#fullColumn > div > div.js-section-wrapper.searchSection.allSection > div:nth-child(2) > div.js-inner-all-results-quotes-wrapper.newResultsContainer.quatesTable > a:nth-child(1) > span.third').text

#         try:
#             # # 국내 주식
#             # # naver finance에서 추출
#             target_data = web.DataReader(item_code, 'naver')
#             last = (target_data.shape[0])
#             target_data = target_data.iloc[last - 1].loc["Close"]

#             # # 가격 추출 성공!
#             item = "'%s'" % item_name

#             # # id와 종목명
#             cur.execute("SELECT * FROM game WHERE userid=%s AND item = %s;"% (user, item))
#             rows = cur.fetchall()

#             if len(rows) != 0 :
#                 limit = int(rows[0][3]) - int(many)

#                 # # 돈만 있는 쿼리
#                 cur.execute("SELECT * FROM game WHERE userid = %s AND money IS NOT null;"% (user))
#                 rows = cur.fetchall()
#                 harmoney = int(rows[0][1]) + int(target_data) * int(many)

#                 if limit < 0 :
#                     result = "보유 주식보다 더 많이 팔 수 없습니다."

#                 elif limit == 0 :
#                     # # money 컬럼 update
#                     cur.execute("UPDATE game SET money = %d WHERE userid = %s AND money IS NOT null;" % (harmoney, user))
                    
#                     # # 해당 주식 행 삭제
#                     cur.execute("DELETE FROM game WHERE userid = %s AND item = %s" % (user, item) )

#                     result = item_name + " " + str(many) + "주를 모두 팔았습니다."
#                 elif limit > 0 :
#                     # # money 컬럼 update
#                     cur.execute("UPDATE game SET money = %d WHERE userid = %s AND money IS NOT null;" % (harmoney, user))

#                     # # 해당 주식 수 update
#                     cur.execute("UPDATE game SET shares = %d WHERE userid = %s AND item = %s" % (limit, user, item)  )

#                     result = item_name + " " + str(many) + "주를 팔았습니다."
#                 else :
#                     result = "알 수 없는 에러가 발생했습니다."
#             else :
#                 result = "보유하지 않은 주식은 판매 할 수 없습니다."

#             db.commit()

#         except:
#             result = "해외 주식은 아직 구현을 못했습니다."

#     except AttributeError:
#         result = "'" + target_item.strip() + "' 으로 검색결과가 없습니다.\n" + "찾는 주식이 있다면 주식명만을 입력해주세요."

#     responseBody = {
#             "version": "2.0",
#             "template": {
#                 "outputs": [
#                     {
#                         "simpleText": {
#                             "text": result
#                         }
#                     }
#                 ]
#             }
#         }

#     return responseBody