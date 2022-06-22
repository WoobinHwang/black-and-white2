import psycopg2

passwd = '3efe88864056f4a63eeebc8a511d12675ce0c78e998192c9e0ab04438867195d'
db = psycopg2.connect(host='ec2-44-206-89-185.compute-1.amazonaws.com', dbname='d3bj01t0cv3v8b',user='qiulfncvkhhxhw',password= passwd,port=5432)
cur=db.cursor()


# cur.execute("DROP TABLE blackwhite")


    # 테이블명 : blackwhite
    # 컬럼 : userid, channel, score, turn, numbers, usenum
# cur.execute("CREATE TABLE IF NOT EXISTS blackwhite (userid varchar, channel varchar, score varchar, turn varchar, numbers varchar, usenum varchar);")

# cur.execute("INSERT INTO blackwhite (userid, channel, score, turn, numbers, usenum) VALUES (%s, %s, %s, %s, %s, %s);"
#             , ("woob", "korea", 0, 1, 200, 0) )

db.commit()

print("끝!!")