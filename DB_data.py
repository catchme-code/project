import FinanceDataReader as fdr # pip install finance-datareader 주식정보 라이브러리
import oracledb as db # 오라클 데이터베이스
import datetime
class insert:
    krx_list = fdr.StockListing('KRX') # 한국거래소(KRX)의 상장 종목 전체 목록 가져오기

    try:
        con = db.connect(dsn="127.0.0.1:1521/xe", user="C##STOCK", password="1234")
        cursor = con.cursor() # DB상호작용 메소드
        
        # table 삭제
        cursor.execute("select table_name from user_tables where table_name like 'STOCK_DATA_%'")
        del_table = cursor.fetchall()
        li_del =[]
        for row in del_table:
            li_del.append(row[0])
        
        if li_del:
            try:
                for i in range(len(li_del)):
                    sql = f"DROP TABLE {li_del[i]}"
                    cursor.execute(sql)
            except db.DatabaseError as e:
                print(e)
        
        # table 생성
        cursor.execute("SELECT * FROM stock")
        select_table = cursor.fetchall()

        li_id =[]; li_code =[]
        for row in select_table:
            li_id.append(row[0])
            li_code.append(row[1])
        
        try:
            for i in range(len(li_id)):
                sql = f"CREATE TABLE STOCK_DATA_{li_id[i]} (date_ VARCHAR(15), open VARCHAR(10), high VARCHAR(10), low VARCHAR(10), close VARCHAR(10), volume VARCHAR(12))"
                cursor.execute(sql)
        except db.DatabaseError as e:
            print(e)
        
        # insert stock_data
        cursor.execute("Select code from stock")
        select_table = cursor.fetchall()
        try:
            cnt=0
            for row in select_table:
                now=datetime.now()
                
                sto_data = fdr.DataReader(row[0],'2024-01-02',now.strftime('%Y-%m-%d'))
                sql = f"TRUNCATE TABLE STOCK_DATA_{li_id[cnt]}"
                cursor.execute(sql)
                
                for i in range(len(sto_data.index)):
                    a=sto_data['Open'][i]; b=sto_data['High'][i];c=sto_data['Low'][i];d=sto_data['Close'][i];e=sto_data['Volume'][i]
                    date = str(sto_data.index[i])[:10]
                    sql = f"INSERT INTO STOCK_DATA_{li_id[cnt]} VALUES({date}, {a}, {b}, {c}, {d}, {e})"
                    cursor.execute(sql)
                cnt+=1            
                
        except db.DatabaseError as e:
            print(e)
    except db.DatabaseError as e:
        print(e)

    con.commit()
    cursor.close()
    con.close()