import sqlite3, datetime

def gen_url(ip, key, redirect):
    time = datetime.datetime.now()
    con = sqlite3.connect('./db/database.db') # 데이터베이스 연결
    cur = con.cursor() 
    cur.execute('SELECT * FROM url WHERE route == ?;', (key,)) # URL 존재여부 확인
    result = cur.fetchone()
    if not result == None:
        return ('FAIL', '이미 존재하는 URL 입니다.') # 이미 존재하는 경우 FAIL 반환
    cur.execute("INSERT INTO url VALUES(?, ?, ?, ?)", (ip, time, key, redirect)) # 데이터 생성
    con.commit()
    con.close() # 데이터베이스 연결 해제
    return 'SUCCESS'

def get_url(key):
    con = sqlite3.connect('./db/database.db') # 데이터베이스 연결
    cur = con.cursor()
    cur.execute('SELECT * FROM url WHERE route == ?;', (key,))
    result = cur.fetchone()
    if result == None:
        return ('FAIL', '존재하지 않는 URL 입니다.')
    return ('SUCCESS', result[3])

