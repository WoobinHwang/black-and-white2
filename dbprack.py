import psycopg2

passwd = 'b55d94be7d8dbef24e28a72a0dcb228fb48d1595665100e8da2cd1aafbe8bbbc'
db = psycopg2.connect(host='ec2-54-204-56-171.compute-1.amazonaws.com', dbname='d2p5j2up8o05rg',user='dywzgxybcyjnzu',password= passwd,port=5432)
cur=db.cursor()

input_score = '%s' %(2)
input_result = "'%s'" %('win')
where_id = "'%s'" %('woobin')
where_channel = "'%s'" %('korea')
where_turn = '%s' %(3)


# # # 상대 승리로 입력
# cur.execute("UPDATE blackwhite3 SET score=%s , result=%s WHERE userid!=%s AND channel=%s AND turn=%s;" % ( input_score, input_result, where_id, where_channel, where_turn))
cur.execute("DELETE FROM blackwhite3 WHERE userid=%s;" %(where_id))
db.commit()
result = "삭제완료!"
print(result)