import pymysql
import math
import models


# 获取游标
def connDB():
    conn = pymysql.connect(host="localhost", user="root", passwd="19990909", db="test",port=3306,charset='utf8')
    cur = conn.cursor()
    return (conn, cur)


# 把元组形式的数据列表通过执行SQL语句插入表
def exeHWTotalClick(data, dateSet, db):
    (conn, cur) = connDB()
    conn.ping(reconnect=True)
    # 每次插入2000条数据
    n = math.ceil(len(data) / 2000)
    try:
        # SQL alchemy查询数据库内的在日期段的数据并删除，执行SQL语句插入新数据
        dbInfo = db.query(models.HuaweiTotalClick).filter(models.HuaweiTotalClick.DATA_TIME.in_(dateSet)).all()
        for each in dbInfo:
            db.delete(each)
        db.commit()
        cur.execute('ALTER TABLE HUAWEI_TOTAL_CLICK AUTO_INCREMENT = 1')
        for n1 in range(0, n):
            cur.executemany("""INSERT INTO HUAWEI_TOTAL_CLICK 
            (INDUSTRY,MERCHANT_NAME,LOCATED_FIELD,TOTAL_CLICK, DATA_TIME)
             VALUES (%s,%s,%s,%s,%s)""", data[2000*n1:2000*(n1+1)])
        conn.commit()
    # 获取报错信息
    except Exception as e:
        conn.rollback()
        raise Exception


def exeHWServiceNumber(data, dateSet, db):
    (conn, cur) = connDB()
    conn.ping(reconnect=True)
    n = math.ceil(len(data) / 2000)
    try:
        dbInfo = db.query(models.HuaweiServiceNumber).filter(models.HuaweiServiceNumber.DATA_TIME.in_(dateSet)).all()
        for each in dbInfo:
            db.delete(each)
        db.commit()
        cur.execute('alter table HUAWEI_SERVICE_NUMBER auto_increment = 1')
        for n1 in range(0, n):
            cur.executemany("""insert into HUAWEI_SERVICE_NUMBER (SERVICE_NAME, INDUSTRY, MERCHANT_NAME,
                          LOCATED_FIELD, OPEN_SERVICE_NUM, OPEN_MENU_NUM,
                          OPEN_PAGE_NUM, PAGE_DAY_PV, PAGE_DAY_UV, PAGE_QUICK_APP_PV,
                          PAGE_QUICK_APP_UV, CHAT_PV, CHAT_UV, DATA_TIME) 
                          VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", data[2000*n1:2000*(n1+1)])
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception


def exeXM(data1,data2, dateSet, db):
    (conn, cur) = connDB()
    conn.ping(reconnect=True)
    n = math.ceil(len(data1) / 2000)
    try:
        dbInfo1 = db.query(models.XiaomiServiceBtn).filter(models.XiaomiServiceBtn.DATA_TIME.in_(dateSet)).all()
        for each1 in dbInfo1:
            db.delete(each1)
        dbInfo2 = db.query(models.XiaomiServiceMenu).filter(models.XiaomiServiceMenu.DATA_TIME.in_(dateSet)).all()
        for each2 in dbInfo2:
            db.delete(each2)
        db.commit()
        cur.execute('ALTER TABLE XIAOMI_SERVICE_BTN AUTO_INCREMENT = 1')
        cur.execute('ALTER TABLE XIAOMI_SERVICE_MENU AUTO_INCREMENT = 1')
        for n1 in range(0, n):
            cur.executemany("""INSERT INTO XIAOMI_SERVICE_BTN 
            (SERVICE_NAME,BTN_EXPO, BTN_CLICK, BTN_DOWNLOAD, BTN_CLICK_RATE, DATA_TIME)
             VALUES (%s,%s,%s,%s,%s,%s)""", data1[2000*n1:2000*(n1+1)])
            cur.executemany("""INSERT INTO XIAOMI_SERVICE_MENU 
            (SERVICE_NAME,MENU_EXPO, MENU_CLICK, MENU_DOWNLOAD, MENU_CLICK_RATE, DATA_TIME)
             VALUES (%s,%s,%s,%s,%s,%s)""",data2[2000*n1:2000*(n1+1)])
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception
