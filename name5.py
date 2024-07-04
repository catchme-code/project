import bcrypt
import oracledb as db # 오라클 데이터베이스
"""
# 사용자가 입력한 비밀번호 문자열
password_str = '1234'

# 비밀번호를 바이트로 변환
password_bytes = password_str.encode('utf-8')
# 무작위 솔트 생성
salt = bcrypt.gensalt()
#str_salt = salt.decode()
# 비밀번호 해싱
hashed_password_bytes = bcrypt.hashpw(password_bytes, salt)
"""
try:
    con = db.connect(dsn="127.0.0.1:1521/xe", user="C##STOCK", password="1234")
    cursor = con.cursor() # DB상호작용 메소드
    
    #cursor.execute("insert into test values(:pw, :salt)", pw=hashed_password_bytes, salt=salt)
    
    cursor.execute("select * from test")
    pw_data = cursor.fetchall()

    str_login_pw = '1234'
    bytes_login_pw = str_login_pw.encode('utf-8')

    for i in pw_data:
        DB_salt = i[1].read()

        hashed_pw = bcrypt.hashpw(bytes_login_pw, DB_salt) # 현재 로그인 한 해싱
        bytes_DB_hash = i[0].read()

        if bytes_DB_hash == hashed_pw:
            print('이건 돼')


    
except db.DatabaseError as e:
    print(e)
con.commit()
cursor.close()
con.close()
