import calendar


# 图表展示日期为"2020-07-01"形式
def getDateList(date: str, type: int):
    dateRaw = date.split('-')
    dateList = []
    # 按月查询
    if type == 1:
        year = int(dateRaw[0])
        month = int(dateRaw[1])
        daysOfMonth = calendar.monthrange(year, month)[1]
        for i in range(1, daysOfMonth + 1):
            if i <= 9:
                day = '0' + str(i)
            else:
                day = str(i)
            dateList.append(date + "-" + day)
        return dateList
    # 按年查询
    for i in range(1, 13):
        if i <= 9:
            month = '0' + str(i)
        else:
            month = str(i)
        dateList.append(date + "-" + month)
    return dateList


# 根据日期字符串获取数据库查询的起止时间整数
def getDateInterval(date: str, type: int):
    dateRaw = date.split('-')
    # 按月查询
    if type == 1:
        year = int(dateRaw[0])
        month = int(dateRaw[1])
        daysOfMonth = calendar.monthrange(year, month)[1]
        startTime = year * 10000 + month * 100 + 1
        endTime = year * 10000 + month * 100 + daysOfMonth
    # 按年查询， 从当年1月1日到12月31日
    else:
        year = int(dateRaw[0])
        startTime = year * 10000 + 101
        endTime = year * 10000 + 1231
    return startTime, endTime


def getNameListHW(dataType: int):
    if dataType == 1:
        nameList = ['点击量']
    elif dataType == 2:
        nameList = ['服务号会话PV', '服务号会话UV']
    elif dataType == 3:
        nameList = ['服务号主页PV', '服务号主页UV']
    else:
        nameList = ['服务号主页快应用PV', '服务号主页快应用UV']
    return nameList


def getNameListXM(dataType: int):
    if dataType == 1:
        nameList = ['菜单曝光量', '按钮曝光量']
    elif dataType == 2:
        nameList = ['菜单点击量', '菜单点击率']
    elif dataType == 3:
        nameList = ['按钮点击量', '按钮点击率']
    else:
        nameList = ['菜单-APP下载量', '按钮-APP下载量']
    return nameList


# 把两表查询数据根据查询类型（dataType）进行转换
# 1:点击量;
# 2:会话曝光;
# 3:主页曝光;
# 4:快应用曝光
def getDataListHW(dataType: int, resultsRef, results):
    dataList = []
    data1 = []
    data2 = []
    j = 0
    # TotalClick表查询结果作为参考列表，处理ServiceNumber表数据不存在的情况
    dataRef = [[result.TOTAL_CLICK for result in resultsRef]]
    if dataType == 1:
        dataList = dataRef

    elif dataType == 2:
        j = 0
        for i in range(len(resultsRef)):
            # 商家总点击数为0，在service_number表中不存在数据，补0
            if resultsRef[i].TOTAL_CLICK == 0:
                data1.append(0)
                data2.append(0)
            else:
                data1.append(results[j].CHAT_PV)
                data2.append(results[j].CHAT_UV)
                j += 1
        dataList.append(data1)
        dataList.append(data2)

    elif dataType == 3:
        for i in range(len(resultsRef)):
            if resultsRef[i].TOTAL_CLICK == 0:
                data1.append(0)
                data2.append(0)
            else:
                data1.append(results[j].PAGE_DAY_PV)
                data2.append(results[j].PAGE_DAY_UV)
                j += 1
        dataList.append(data1)
        dataList.append(data2)

    else:
        for i in range(len(resultsRef)):
            if resultsRef[i].TOTAL_CLICK == 0:
                data1.append(0)
                data2.append(0)
            else:
                data1.append(results[j].PAGE_QUICK_APP_PV)
                data2.append(results[j].PAGE_QUICK_APP_UV)
                j += 1
        dataList.append(data1)
        dataList.append(data2)
    return dataList


# 1:会话曝光
# 2:菜单点击;
# 3:按钮点击;
# 4:APP下载;
def getDataListXM(dataType: int, XM2, XM1):
    dataList = [[], []]
    # Btn按钮结果长度
    length1 = len(XM1)
    # Menu菜单结果长度
    length2 = len(XM2)
    i = 0
    j = 0
    # 两个查询结果存在长短不同情况， 数据开始日期为两个中最早的一项数据的日期
    if length2 != 0 and length1 != 0:
        dateInt = min(XM1[0].DATA_TIME, XM2[0].DATA_TIME)
    elif length1 == 0 and length2 != 0:
        dateInt = XM2[0].DATA_TIME
    elif length2 == 0 and length1 != 0:
        dateInt = XM1[0].DATA_TIME
    else:
        dateInt = 0
    # 合并两表查询结果
    if dataType == 1:
        while i < length1 or j < length2:
            if i >= length1:
                dataList[1].extend([result.MENU_EXPO for result in XM2[j:]])
                dataList[0].extend([0 for c in range(length2 - j)])
                break
            elif j >= length2:
                dataList[0].extend([result.BTN_EXPO for result in XM1[i:]])
                dataList[1].extend([0 for c in range(length1 - i)])
                break
            elif XM1[i].data_time == XM2[j].data_time:
                dataList[1].append(XM2[j].MENU_EXPO)
                dataList[0].append(XM1[i].BTN_EXPO)
                i += 1
                j += 1
            elif XM1[i].data_time < XM2[j].DATA_TIME:
                dataList[0].append(XM1[i].BTN_EXPO)
                dataList[1].append(0)
                i += 1
            else:
                dataList[1].append(XM2[j].MENU_EXPO)
                dataList[0].append(0)
                j += 1

    elif dataType == 2:
        dataList[0].extend([result.MENU_CLICK for result in XM2])
        dataList[1].extend([result.MENU_CLICK_RATE for result in XM2])

    elif dataType == 3:
        dataList[0].extend([result.btn_click for result in XM1])
        dataList[1].extend([result.btn_click_rate for result in XM1])

    else:
        while i < length1 or j < length2:
            if i >= length1:
                dataList[1].extend([result.MENU_DOWNLOAD for result in XM2[j:]])
                dataList[0].extend([0 for c in range(length2 - j)])
                break
            elif j >= length2:
                dataList[0].extend([result.BTN_DOWNLOAD for result in XM1[i:]])
                dataList[1].extend([0 for c in range(length1 - i)])
                break
            elif XM1[i].data_time == XM2[j].DATA_TIME:
                dataList[1].append(XM2[j].MENU_DOWNLOAD)
                dataList[0].append(XM1[i].BTN_DOWNLOAD)
                i += 1
                j += 1
            elif XM1[i].DATA_TIME < XM2[j].DATA_TIME:
                dataList[0].append(XM1[i].BTN_DOWNLOAD)
                dataList[1].append(0)
                i += 1
            else:
                dataList[1].append(XM2[j].MENU_DOWNLOAD)
                dataList[0].append(0)
                j += 1
    return dataList, dateInt


# 根据dateList补齐dataList长度， resultsRef的第一项含当月起始时间信息
def operateList(dataList: list, dateList: list, resultsRef):
    ll = len(resultsRef)
    l = len(dataList)
    if ll == 0:
        for i in range(l):
            interval = [0 for j in range(len(dateList))]
            dataList[i] = interval
    else:
        # 获取数据从当月第几天开始
        tmp = resultsRef[0].DATA_TIME % 100 - 1
        for i in range(l):
            interval = [0 for h in range(tmp)]
            interval.extend(dataList[i])
            interval.extend([0 for j in range(len(dateList) - len(interval))])
            dataList[i] = interval
    return dataList


# 根据dateList补齐dataList长度， dateInt为当月起始时间
def operateListXM(dataList: list, dateList: list, dateInt):
    l = len(dataList)
    tmp = dateInt % 100 - 1
    for i in range(l):
        interval = [0 for h in range(tmp)]
        interval.extend(dataList[i])
        interval.extend([0 for j in range(len(dateList) - len(interval))])
        dataList[i] = interval
    return dataList
