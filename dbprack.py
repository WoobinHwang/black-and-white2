import psycopg2

passwd = 'b55d94be7d8dbef24e28a72a0dcb228fb48d1595665100e8da2cd1aafbe8bbbc'
db = psycopg2.connect(host='ec2-54-204-56-171.compute-1.amazonaws.com', dbname='d2p5j2up8o05rg',user='dywzgxybcyjnzu',password= passwd,port=5432)
cur=db.cursor()

id_num = 'woob1'
id_data = '%s' %id_num
idid_data = "'%s'" %id_num

# turn_data = "'%s'" %'0'

# cur.execute("SELECT * FROM practice WHERE userid=%s AND turn=%s;" % (idid_data, turn_data))
# rows = cur.fetchone

# print(rows[0][1])
# print(len(rows))


# cur.execute("DROP TABLE blackwhite2")


    # 테이블명 : blackwhite2
    # 컬럼 : userid, channel, score, turn, numbers, usenum, result
cur.execute("CREATE TABLE IF NOT EXISTS practice (userid varchar, numbers int, score varchar);")

# cur.execute("INSERT INTO blackwhite2 (userid, channel, score, turn, numbers, usenum) VALUES (%s, %s, %s, %s, %s, %s);"
#             , ("woob", "korea", 0, 1, 200, 0) )

# db.commit()

print("끝!!")