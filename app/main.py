from collections import UserList
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

    cur.execute("SELECT * FROM blackwhite3 WHERE channel=%s;" % (channelchannel_data))
    rows = cur.fetchall()

    cur.execute("SELECT * FROM blackwhite3 WHERE channel=%s AND userid=%s;" % (channelchannel_data, idid_data))
    rows2 = cur.fetchall()

    cur.execute("SELECT * FROM blackwhite3 WHERE userid=%s;" % (idid_data))
    rows3 = cur.fetchall()

    if len(rows2) != 0:
        result = "해당 채널에 이미 접속중이십니다"
    elif len(rows3) != 0:
        result = "이미 다른 채널에 접속중이십니다"
    elif len(rows) < 2:
        cur.execute("INSERT INTO blackwhite3 (userid, channel, score, turn, numbers, usenum) VALUES (%s, %s, %s, %s, %s, %s);"
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
    round_winner = '%s' %("win")
    round_loser = '%s' %("lose")
    round_draw = '%s' %("draw")
    where_round_winner = "'%s'" %("win")
    where_round_loser = "'%s'" %("lose")
    where_round_draw = "'%s'" %("draw")


    target_data = body['userRequest']['utterance']

    if (target_data == '발화 내용'):
        text = '0'
    else:
        text = target_data.split(" ")[0]
    
    

    cur.execute("SELECT * FROM blackwhite3 WHERE userid=%s AND turn='0';" % (idid_data))
    find_channel = cur.fetchall()

    userchannel = find_channel[0][1]
    channel_data = '%s' %(userchannel)
    channelchannel_data = "'%s'" %(userchannel)

    cur.execute("SELECT * FROM blackwhite3 WHERE userid=%s AND channel=%s;" % (idid_data, channelchannel_data))
    user_rows = cur.fetchall()

    cur.execute("SELECT * FROM blackwhite3 WHERE userid!=%s AND channel=%s;" % (idid_data, channelchannel_data))
    enemy_rows = cur.fetchall()

    input_user_turn = '%s' %(len(user_rows))
    input_enemy_turn = '%s' %(len(enemy_rows))
    where_user_turn = "'%s'" %(len(user_rows)-1)
    where_enemy_turn = "'%s'" %(len(enemy_rows)-1)

    cur.execute("SELECT * FROM blackwhite3 WHERE userid=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_user_turn))
    user_last_rows = cur.fetchone()

    cur.execute("SELECT * FROM blackwhite3 WHERE userid!=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_enemy_turn))
    enemy_last_rows = cur.fetchone()
    
    # # 상대가 없을 때
    if (len(enemy_rows) == 0):
            result = "상대방이 들어오지 않았습니다."
    # # 보유 포인트보다 더 많이 제출하려고 할 때
    elif (user_last_rows[4]-int(text) < 0) or (int(text) < 0) :
        result = "현재 남은 포인트는 %d개입니다.\n다시 제출하세요." %(user_last_rows[4])

    else:
        
        # # 숫자 정상적으로 제출
        # # 길이가 같을 때 입력한 사람이 제출
        if(len(user_rows) == len(enemy_rows)) :
            cur.execute("INSERT INTO blackwhite3 (userid, channel, score, turn, numbers, usenum) VALUES (%s, %s, %s, %s, %s, %s);"
                , (id_data, channel_data, user_last_rows[2], user_last_rows[3] + 1, user_last_rows[4] - int(text), int(text)) )
            db.commit()
            result = "%s라운드 제출 완료!" %(user_last_rows[3] + 1)
        elif(len(user_rows) > len(enemy_rows)):
            result = "상대방이 제출 할 차례입니다."
        elif(len(user_rows) < len(enemy_rows)):
            
            
            # # 양쪽 다 제출했으니 숫자를 비교 할 예정
            enemy_num = enemy_last_rows[5]
            user_num = int(text)

            # # 제출 한 사람이 승리 할 경우
            if (user_num > enemy_num):
                # # 유저 승리로 입력
                cur.execute("INSERT INTO blackwhite3 (userid, channel, score, turn, numbers, usenum, result) VALUES (%s, %s, %s, %s, %s, %s, %s);"
                    , (id_data, channel_data, user_last_rows[2] + 1, user_last_rows[3] + 1, user_last_rows[4] - int(text), int(text), round_winner ))
                # # 상대 패배로 입력
                cur.execute("UPDATE blackwhite3 SET result=%s WHERE userid!=%s AND channel=%s AND turn=%s;" % (where_round_loser, idid_data, channelchannel_data, where_enemy_turn))
                db.commit()
                
                result = "%s라운드 제출 완료!\n당신이 승리하였습니다!!!"%(user_last_rows[3] + 1)

            # # 상대방이 승리 할 경우
            elif (user_num < enemy_num):
                # # 유저 패배로 입력
                cur.execute("INSERT INTO blackwhite3 (userid, channel, score, turn, numbers, usenum, result) VALUES (%s, %s, %s, %s, %s, %s, %s);"
                    , (id_data, channel_data, user_last_rows[2], user_last_rows[3] + 1, user_last_rows[4] - int(text), int(text), round_loser ))
                # # # 상대 승리로 입력
                cur.execute("UPDATE blackwhite3 SET score=%s , result=%s WHERE userid!=%s AND channel=%s AND turn=%s;" % ( enemy_last_rows[2]+1, where_round_winner, idid_data, channelchannel_data, input_enemy_turn))
                db.commit()
                result = "%s라운드 제출 완료!\n상대방이 승리하였습니다..." %(user_last_rows[3] + 1)

            # # 무승부인 상황
            elif (user_num == enemy_num):
                cur.execute("INSERT INTO blackwhite3 (userid, channel, score, turn, numbers, usenum, result) VALUES (%s, %s, %s, %s, %s, %s, %s);"
                    , (id_data, channel_data, user_last_rows[2], user_last_rows[3] + 1, user_last_rows[4] - int(text), int(text), round_draw))
                # # 상대 무승부 입력
                cur.execute("UPDATE blackwhite3 SET result=%s WHERE userid!=%s AND channel=%s AND turn=%s;" % (where_round_draw, idid_data, channelchannel_data, where_enemy_turn))
                db.commit()
                result = "무승부입니다!\n선 플레이어부터 다시 시작해주세요."

    

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