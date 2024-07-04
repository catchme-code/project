import DB_stock
import DB_data
from DB_adjust_table import ad_table
"""
# 코스피 10개 인기검색 순위 초기화, 재등록
DB_stock.ext()
DB_data.insert()
"""

stock_name = '기아'
"""
# 주식 종목 추가
create_table = ad_table.create_table(stock_name) # 1년전 데이터가 없으면 None 값 적재완료되면 'complete'
if create_table is None:
    print('해당하는 주식종목이 없습니다.')
elif create_table == 'not_data':
    print('1년전의 정보가 없습니다.')
elif create_table == 'equ':
    print('테이블 명 중복')
else:
    print('데이터 베이스 적재')

# 주식 종목 제거
delete_table = ad_table.delete_table(stock_name)
if delete_table is None:
    print('해당하는 주식종목이 없습니다.')
elif delete_table == 'not_data':
    print('존재하는 테이블이 없습니다.')
"""


