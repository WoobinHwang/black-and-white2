import psycopg2

passwd = 'b55d94be7d8dbef24e28a72a0dcb228fb48d1595665100e8da2cd1aafbe8bbbc'
db = psycopg2.connect(host='ec2-54-204-56-171.compute-1.amazonaws.com', dbname='d2p5j2up8o05rg',user='dywzgxybcyjnzu',password= passwd,port=5432)
cur=db.cursor()



id_data = '%s' %("woobin")
idid_data = "'%s'" %("woobin")
channel_data = '%s' %("korea")
channelchannel_data = "'%s'" %("korea")
where_user_turn = 4
text = '2'

cur.execute("SELECT * FROM blackwhite3 WHERE userid=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_user_turn))
user_last_rows = cur.fetchone()
# print(user_last_rows)


cur.execute("INSERT INTO blackwhite3 (userid, channel, score, turn, numbers, usenum, result) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    , (id_data, channel_data, user_last_rows[2], user_last_rows[3] + 1, user_last_rows[4] - int(text), int(text), user_last_rows[6]))


db.commit()
# # 상대 무승부 입력
# cur.execute("UPDATE blackwhite3 SET result=%s WHERE userid!=%s AND channel=%s AND turn=%s;" % (where_round_draw, idid_data, channelchannel_data, where_enemy_turn))

print("good!")