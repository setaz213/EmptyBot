import pymysql
import pymysql.cursors

def conn():
    # con = pymysql.connect('localhost', 'root', '', 'minecraft',cursorclass=pymysql.cursors.DictCursor)
    con = pymysql.connect('node84046-empty.mircloud.ru', 'root', 'VSNrrr74711', 'Empty',cursorclass=pymysql.cursors.DictCursor)
    return con