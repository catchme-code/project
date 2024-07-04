import sys
import os
from PyQt5.QtWidgets import QMainWindow,QListWidgetItem,QMessageBox,QWidget,QApplication
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap # 이미지
import oracledb as db # 오라클 데이터베이스

from DB_adjust_table import ad_table
from test_sub import graf


class MainWindow(QMainWindow):  
    def __init__(self):
        super(MainWindow, self).__init__()
        # .ui 파일의 경로를 지정
        main_file_path = os.path.join(os.path.dirname(__file__), 'main_page.ui')
        loadUi(main_file_path, self)
        
        try:
            con = db.connect(dsn="127.0.0.1:1521/xe", user="C##STOCK", password="1234")
            cursor = con.cursor() # DB상호작용 메소드
            
            cursor.execute("SELECT ID FROM STOCK")
            data_stock = cursor.fetchall()
            
            for i in data_stock:
                self.list_stock.addItem(QListWidgetItem(i[0])) # 변수를 listWidget에 적재
       
        except db.DatabaseError as e:
            print(e)
        con.commit()
        cursor.close()
        con.close()
         
        self.list_stock.itemClicked.connect(self.ch_label) # listWidget의 항목을 클릭하였을때
        self.butt_select.clicked.connect(self.select_stock) # butt_select를 클릭 했을 때
        self.butt_insert.clicked.connect(self.insert_stock) # butt_insert를 클릭 했을 때
        self.butt_delete.clicked.connect(self.delete_stock) # butt_delete를 클릭 했을 때
        
    def ch_label(self, item): #리스트를 클릭했을때
        selected_text = item.text() #클릭한 item의 text를 selected_text에 저장
        self.label.setText(f"{selected_text}") # label을 f"Selected item: {selected_text}"로 변환
        
    def select_stock(self): # 2번째 창으로 이동.
        stock_name=self.label.text()
        alert = self.alert_wait()
        alert.show()
        graf.drow_graf(stock_name)
        
        
        
        
        alert.close()
        self.second = insert_page() # self.second라는 이름에 insert_page() 클라스 호출 등록
        self.second.show()
        
    def alert_wait(self):
        alert = QMessageBox(self)
        alert.setWindowTitle("wait")
    
        return alert
        

    def insert_stock(self): # insert
        self.hide()
        alert = self.alert_wait()
        alert.show()
        stock_name = self.input_stock.text() #input_stock에 입력한 데이터 가져옴 type=str

        # 주식 종목 추가
        self.create_table = ad_table.create_table(stock_name) # 1년전 데이터가 없으면 None 값 적재완료되면 'complete' 
        if self.create_table is None:
            QMessageBox.about(self, "Error", "해당하는 주식 종목이 없습니다.") # alert창 [메세지 title], [내용]
            alert.close()
            self.show()
        elif self.create_table == 'not_data':
            QMessageBox.about(self, "Error", "주식 정보가 많지않아 예측하기 어렵습니다.")
            alert.close()
            self.show()
        elif self.create_table == 'equ':
            QMessageBox.about(self, "Error", "중복된 주식 종목이 존재합니다.")
            alert.close()
            self.show()
        else:
            self.list_stock.clear()
            try:
                con = db.connect(dsn="127.0.0.1:1521/xe", user="C##STOCK", password="1234")
                cursor = con.cursor() # DB상호작용 메소드
                
                cursor.execute("SELECT ID FROM STOCK")
                data_stock = cursor.fetchall()
                
                for i in data_stock:
                    self.list_stock.addItem(QListWidgetItem(i[0])) # 변수를 listWidget에 적재
            except db.DatabaseError as e:
                print(e)
            alert.close()
            self.show()
            QMessageBox.about(self, "Success", "종목이 추가되었습니다.")
            con.commit()
            cursor.close()
            con.close()

    def delete_stock(self):
        self.hide()
        alert = self.alert_wait()
        alert.show()
        stock_name = self.input_stock.text() #input_stock에 입력한 데이터 가져옴 type=str
        
        # 주식 종목 제거
        delete_table = ad_table.delete_table(stock_name) 
        if delete_table is None:
            QMessageBox.about(self, "Error", "해당하는 주식 종목이 없습니다.") # alert창 [메세지 title], [내용]
            alert.close()
            self.show()
        elif delete_table == 'not_data':
            QMessageBox.about(self, "Error", "존재하는 테이블이 없습니다.")
            alert.close()
            self.show()
        else:
            self.list_stock.clear()
            try:
                con = db.connect(dsn="127.0.0.1:1521/xe", user="C##STOCK", password="1234")
                cursor = con.cursor() # DB상호작용 메소드
                
                cursor.execute("SELECT ID FROM STOCK")
                data_stock = cursor.fetchall()
                
                for i in data_stock:
                    self.list_stock.addItem(QListWidgetItem(i[0])) # 변수를 listWidget에 적재
            except db.DatabaseError as e:
                print(e)
            alert.close()
            self.show()
            QMessageBox.about(self, "Success", "삭제 되었습니다.")
            con.commit()
            cursor.close()
            con.close()
         
class insert_page(QWidget): 
    def __init__(self):
        super(insert_page, self).__init__()
        insert_file_path = os.path.join(os.path.dirname(__file__), 'insert_page.ui')
        loadUi(insert_file_path, self)

class login_page(QMainWindow):
    def __init__(self):
        super(login_page, self).__init__()
        login_file_path = os.path.join(os.path.dirname(__file__), 'login.ui')
        loadUi(login_file_path, self)
        
        pixmap = QPixmap('./img/login.png')
        self.label.setPixmap(pixmap)



def window():
    # 현재 파일의 경로로 작업 디렉토리를 변경
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show() # GUI를 보여준다.
    #login_window = login_page()
    #login_window.show()
    
    
    sys.exit(app.exec_())