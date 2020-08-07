from fastapi import Depends, UploadFile, File
from sqlalchemy.orm import Session
from import_app.impfile import analyseDataHW, analyseDataXM
import crud, schemas, os, numpy
from import_app import importToDB, exam_file
from chart_app import query_operate, result_models
from starlette.responses import FileResponse
from database import SessionLocal
from decimal import Decimal


# Dependency 依赖项
def get_db():
    try:
        db = SessionLocal()  # 本地会话
        yield db
    finally:
        db.close()


def pageHW(query: schemas.queryBase1, db: Session = Depends(get_db)):
    dbInfoTotalClick = crud.queryHWTotalClick(db, query.startTime, query.endTime, query.name)
    dbInfoServiceNum = crud.queryHWServiceNum(db, query.startTime, query.endTime, query.name)
    # 当前总共条数
    num: int = len(dbInfoTotalClick)
    # 当前页实际显示
    numberOfElements = crud.getNumberOfElements(query.page, query.size, num)
    # 分页信息，第一页从1开始
    pageResponse = schemas.PageInfo(query.page, query.size, num, numberOfElements)
    # 分页数据，取全部再列表切片
    responsePageHW = crud.getResponseHW(dbInfoTotalClick, dbInfoServiceNum)
    repon = schemas.ResponseStandard("success", 0,
                                     responsePageHW[(query.page-1)*query.size:(query.page-1)*query.size+numberOfElements],
                                     pageResponse, True)
    return repon


def pageXM(query: schemas.queryBase1, db: Session = Depends(get_db)):
    dbInfoBtn = crud.queryXMServiceBtn(db, query.startTime, query.endTime, query.name)
    dbInfoMenu = crud.queryXMServiceMenu(db, query.startTime, query.endTime, query.name)
    num: int = len(dbInfoBtn)
    numberOfElements = crud.getNumberOfElements(query.page, query.size, num)
    pageResponse = schemas.PageInfo(query.page, query.size, num, numberOfElements)
    responsePageXM = crud.getResponseXM(dbInfoBtn, dbInfoMenu)
    repon = schemas.ResponseStandard("success", 0,
                                     responsePageXM[(query.page-1)*query.size:(query.page-1)*query.size+numberOfElements],
                                     pageResponse, True)
    return repon


def importHW(queryType, subPage, subSize, file: UploadFile = File(...), db: Session = Depends(get_db)):
    name = file.filename
    # 文件格式校验
    if len(name) < 6 or name[-4:] != 'xlsx':
        return schemas.ResponseStandard("文件格式错误", 412, None, None, True)

    try:
        # excel内容写入test文件以便解析
        res = file.file.read()
        with open("./test.xlsx", "wb") as f:
            f.write(res)
            f.close()
        # 文件列数校验
        if not exam_file.rowExam(3):
            return schemas.ResponseStandard("文件模板错误，少列", 412, None, None, True)
    except Exception as e:
        repon = schemas.ResponseStandard(str(e), 500, None, None, True)
        return repon

    # 文件数据校验，flag为0则数据格式有误
    flag, dataErr = exam_file.formExam(queryType)
    if flag == 0:
        # 错误信息条数，不超过30条
        num: int = len(dataErr)
        numberOfElements = crud.getNumberOfElements(subPage, subSize, num)
        pageResponse = schemas.PageInfo(subPage, subSize, num, numberOfElements)
        return schemas.ResponseStandard("数据校验异常", 402,
                                        {'data': dataErr[(subPage-1)*subSize:(subPage-1)*subSize+numberOfElements],
                                         'pageInfo': pageResponse}, None, True)

    # 无错误，开始导入
    data, dateSet = analyseDataHW(queryType)
    try:
        if queryType == 1:
            # TotalClick表
            importToDB.exeHWTotalClick(data, dateSet, db)
        else:
            # ServiceNumber表
            importToDB.exeHWServiceNumber(data, dateSet, db)
        repon = schemas.ResponseStandard("success", 0, None, None, True)
    except Exception as e:
        repon = schemas.ResponseStandard(str(e), 500, None, None, True)
    finally:
        return repon


def importXM(subPage, subSize, file=File(...), db: Session = Depends(get_db)):
    name = file.filename
    if len(name) < 6 or name[-4:] != 'xlsx':
        return schemas.ResponseStandard("文件格式错误", 412, None, None, True)

    try:
        res = file.file.read()
        with open("./test.xlsx", "wb") as f:
            f.write(res)
            f.close()
        if not exam_file.rowExam(3):
            return schemas.ResponseStandard("文件模板错误，少列", 412, None, None, True)
    except Exception as e:
        repon = schemas.ResponseStandard(str(e), 500, None, None, True)
        return repon

    flag, dataErr = exam_file.formExam(3)
    if flag == 0:
        num: int = len(dataErr)
        numberOfElements = crud.getNumberOfElements(subPage, subSize, num)
        pageResponse = schemas.PageInfo(subPage, subSize, num, numberOfElements)
        return schemas.ResponseStandard("数据校验异常", 402,
                                        {'data': dataErr[(subPage-1)*subSize:(subPage-1)*subSize+numberOfElements],
                                         'pageInfo': pageResponse}, None, True)

    data1, data2, dateSet = analyseDataXM()
    try:
        importToDB.exeXM(data1, data2, dateSet, db)
        repon = schemas.ResponseStandard("success", 0, None, None, True)
    except Exception as e:
        repon = schemas.ResponseStandard(str(e), 500, None, None, True)
    finally:
        return repon


#华为图表展示
def preHW(query: schemas.queryBase2, db: Session = Depends(get_db)):
    dateList = query_operate.getDateList(query.date, query.type)
    nameList = query_operate.getNameListHW(query.dataType)
    # 要查询的数量
    queryNumber = len(nameList)
    # 按月查询
    if query.type == 1:
        startTime, endTime = query_operate.getDateInterval(query.date, query.type)
        resultsRef = crud.queryHWTotalClickUnique(db, startTime, endTime, query.name)
        # 根据query得到实例组成的list
        results = crud.queryHWServiceNumUnique(db, startTime, endTime, query.name)
        # 组成需要的格式
        dataList = query_operate.getDataListHW(query.dataType, resultsRef, results)
        # 用0补齐长度
        dataListFinal = query_operate.operateList(dataList, dateList, resultsRef)
    else:  # 按年查询
        year = int(query.date) * 10000
        dataListFinal = [[] for j in range(queryNumber)]
        # 按月查询后求每个月的总和
        for i in range(1, 13):
            startTime = year + i * 100
            endTime = year + (i + 1) * 100
            resultsRef = crud.queryHWTotalClickUnique(db, startTime, endTime, query.name)
            results = crud.queryHWServiceNumUnique(db, startTime, endTime, query.name)
            dataList = query_operate.getDataListHW(query.dataType, resultsRef, results)
            dataListMid = query_operate.operateList(dataList, dateList, resultsRef)
            for h in range(queryNumber):
                dataListFinal[h].append(sum(dataListMid[h]))

    data = result_models.Data(dateList, nameList, dataListFinal)
    repon = schemas.ResponseStandard("success", 0, data, None, True)
    return repon


def preXM(query: schemas.queryBase2, db: Session = Depends(get_db)):
    dateList = query_operate.getDateList(query.date, query.type)
    nameList = query_operate.getNameListXM(query.dataType)
    # 按月查询
    if query.type == 1:
        startTime, endTime = query_operate.getDateInterval(query.date, query.type)
        resultsMenu = crud.queryXMServiceMenuUnique(db, startTime, endTime, query.name)
        resultsBtn = crud.queryXMServiceBtnUnique(db, startTime, endTime, query.name)
        dataList, dateInt = query_operate.getDataListXM(query.dataType, resultsMenu, resultsBtn)
        dataListFinal = query_operate.operateListXM(dataList, dateList, dateInt)
    # 按年查询
    else:
        year = int(query.date) * 10000
        dataListFinal = [[], []]
        for i in range(1, 13):
            startTime = year + i * 100
            endTime = year + (i + 1) * 100
            resultsMenu = crud.queryXMServiceMenuUnique(db, startTime, endTime, query.name)
            resultsBtn = crud.queryXMServiceBtnUnique(db, startTime, endTime, query.name)
            dataList, dateInt = query_operate.getDataListXM(query.dataType, resultsMenu, resultsBtn)
            dataListMid = query_operate.operateListXM(dataList, dateList, dateInt)
            dataListFinal[0].append(sum(dataListMid[0]))
            # 每月按钮（type=2）/菜单点击率（type=3）取平均数，保留四位小数，其余取总和
            if query.type == 2:
                tmp = sum(dataListMid[1]) / max(len(resultsMenu), 1)
                t = Decimal(str(tmp)).quantize(Decimal('0.0000'))
            elif query.type == 3:
                tmp = sum(dataListMid[1]) / max(len(resultsBtn), 1)
                t = Decimal(str(tmp)).quantize(Decimal('0.0000'))
            else:
                t = sum(dataListMid[1])
            dataListFinal[1].append(t)

    data = result_models.Data(dateList, nameList, dataListFinal)
    repon = schemas.ResponseStandard(
        "success", 0, data, None, True)
    return repon


def exModel(query: schemas.fileBase, db: Session = Depends(get_db)):
    filedic = {1: 'TotalClickHuaweiModel.xlsx', 2: 'ServiceNumberHuaweiModel.xlsx', 3: 'TableXiaomiModel.xlsx'}
    short = '\\' + 'export_model' + '\\'
    filePath = os.path.abspath(os.path.join(os.path.dirname("__file__"),
                                            os.path.pardir)) + short + filedic[query.queryType]
    response = FileResponse(filePath)
    return response


def preNameList(queryType, db):
    nameList = crud.exNameList(queryType, db)
    res = []
    for name in nameList:
        res.append({'key': name, 'value': name})
    repon = schemas.ResponseStandard(
        "success", 0, res, None, True)
    return repon
