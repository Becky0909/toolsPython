from sqlalchemy.orm import Session
import models, schemas

# 名称模糊查询
def queryHWTotalClick(db: Session, startTime, endTime, name:str = ""):
    return db.query(models.HuaweiTotalClick).filter(
        models.HuaweiTotalClick.DATA_TIME.between(startTime, endTime),
        models.HuaweiTotalClick.MERCHANT_NAME.like("%"+name+"%")).order_by(
        models.HuaweiTotalClick.DATA_TIME, models.HuaweiTotalClick.ID).all()

# 名称非模糊查询（用于图表展示接口）
def queryHWTotalClickUnique(db: Session, startTime, endTime, name):
    return db.query(models.HuaweiTotalClick).filter(
        models.HuaweiTotalClick.DATA_TIME.between(startTime, endTime),
        models.HuaweiTotalClick.MERCHANT_NAME == name).order_by(
        models.HuaweiTotalClick.DATA_TIME, models.HuaweiTotalClick.ID).all()


# return实例组成的列表
def queryHWServiceNum(db: Session, startTime, endTime, name:str = ""):
    return db.query(models.HuaweiServiceNumber).filter(
        models.HuaweiServiceNumber.DATA_TIME.between(startTime, endTime),
        models.HuaweiServiceNumber.MERCHANT_NAME.like("%"+name+"%")).order_by(
        models.HuaweiServiceNumber.DATA_TIME, models.HuaweiServiceNumber.ID).all()


def queryHWServiceNumUnique(db: Session, startTime, endTime, name):
    return db.query(models.HuaweiServiceNumber).filter(
        models.HuaweiServiceNumber.DATA_TIME.between(startTime, endTime),
        models.HuaweiServiceNumber.MERCHANT_NAME == name).order_by(
        models.HuaweiServiceNumber.DATA_TIME, models.HuaweiServiceNumber.ID).all()


def queryXMServiceMenu(db: Session, startTime, endTime, name:str = ""):
    return db.query(models.XiaomiServiceMenu).filter(
        models.XiaomiServiceMenu.DATA_TIME.between(startTime, endTime),
        models.XiaomiServiceMenu.SERVICE_NAME.like("%"+name+"%")).order_by(
        models.XiaomiServiceMenu.DATA_TIME, models.XiaomiServiceMenu.ID).all()


def queryXMServiceMenuUnique(db: Session, startTime, endTime, name):
    return db.query(models.XiaomiServiceMenu).filter(
        models.XiaomiServiceMenu.DATA_TIME.between(startTime, endTime),
        models.XiaomiServiceMenu.SERVICE_NAME == name).order_by(
        models.XiaomiServiceMenu.DATA_TIME, models.XiaomiServiceMenu.ID).all()


def queryXMServiceBtn(db: Session, startTime, endTime, name:str = ""):
    return db.query(models.XiaomiServiceBtn).filter(
        models.XiaomiServiceBtn.DATA_TIME.between(startTime, endTime),
        models.XiaomiServiceBtn.SERVICE_NAME.like("%"+name+"%")).order_by(
        models.XiaomiServiceBtn.DATA_TIME, models.XiaomiServiceBtn.ID).all()


def queryXMServiceBtnUnique(db: Session, startTime, endTime, name:str = ""):
    return db.query(models.XiaomiServiceBtn).filter(
        models.XiaomiServiceBtn.DATA_TIME.between(startTime, endTime),
        models.XiaomiServiceBtn.SERVICE_NAME == name).order_by(
        models.XiaomiServiceBtn.DATA_TIME, models.XiaomiServiceBtn.ID).all()


# 华为service_number表查询结果HW2可能为空或少于total_click查询结果HW1
def getResponseHW(HW1, HW2=None):
    if HW2 is None:
        res = [schemas.ResponsePageHW(HW1[i], schemas.HuaweiServiceNumber(), i) for i in range(len(HW1))]
    else:
        # 查询结果
        res = []
        # HW2每一天表里有的商家名称字典
        name2 = {}
        for h in range(len(HW2)):
            day = HW2[h].DATA_TIME
            if day in name2.keys():
                name2[day].append(HW2[h].MERCHANT_NAME)
            else:
                name2[day] = [HW2[h].MERCHANT_NAME]
        for i in range(len(HW1)):
            if HW1[i].MERCHANT_NAME not in name2[HW1[i].DATA_TIME]:
                res.append(schemas.ResponsePageHW(HW1[i], schemas.HuaweiServiceNumber(), i))
            else:
                j = name2[HW1[i].DATA_TIME].index(HW1[i].MERCHANT_NAME)
                res.append(schemas.ResponsePageHW(HW1[i], HW2[j], i))
    return res


def getResponseXM(XM1, XM2):
    res = []
    length1 = len(XM1)
    length2 = len(XM2)
    i = 0
    j = 0
    count = 0
    while i < length1 or j < length2:
        if i >= length1:
            res.append(schemas.ResponsePageXM(schemas.XiaomiServiceBtn(), XM2[j], count))
            j += 1
            count += 1
        elif j >= length2:
            res.append(schemas.ResponsePageXM(XM1[i], schemas.XiaomiServiceMenu(), count))
            i += 1
            count += 1
        elif XM1[i].DATA_TIME == XM2[j].DATA_TIME:
            res.append(schemas.ResponsePageXM(XM1[i], XM2[j], count))
            i += 1
            j += 1
            count += 1
        elif XM1[i].DATA_TIME < XM2[j].DATA_TIME:
            res.append(schemas.ResponsePageXM(XM1[i], schemas.XiaomiServiceMenu(), count))
            i += 1
            count += 1
        else:
            res.append(schemas.ResponsePageXM(schemas.XiaomiServiceBtn(), XM2[j], count))
            j += 1
            count += 1
    return res


# 当前页数显示条数
def getNumberOfElements(page, size, num):
    if page*size <= num:
        return size
    return num-size*(page-1)


# 商家名称列表， type=1：华为商家列表，2：小米服务号列表
def exNameList(type, db):
    nameList = set()
    if type == 1:
        dbInfo1 = db.query(models.HuaweiTotalClick).order_by(models.HuaweiTotalClick.ID).all()
        for each1 in dbInfo1:
            nameList.add(each1.MERCHANT_NAME)
        dbInfo2 = db.query(models.HuaweiServiceNumber).order_by(models.HuaweiServiceNumber.ID).all()
        for each2 in dbInfo2:
            nameList.add(each2.MERCHANT_NAME)
    else:
        dbInfo1 = db.query(models.XiaomiServiceMenu).order_by(models.XiaomiServiceMenu.ID).all()
        for each in dbInfo1:
            nameList.add(each.SERVICE_NAME)
        dbInfo2 = db.query(models.XiaomiServiceBtn).order_by(models.XiaomiServiceBtn.ID).all()
        for each in dbInfo2:
            nameList.add(each.SERVICE_NAME)
    return nameList
