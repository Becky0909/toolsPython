# 图表展示类的定义

class XAxis:
    def __init__(self,dateList):
        self.data = dateList


class Data:
    def __init__(self, dateList, nameList, dataList):
        self.xAxis = XAxis(dateList)
        res = []
        for i in range(len(nameList)):
            res2 = {}
            res2.update({"name": nameList[i]})
            res2.update({"data": dataList[i]})
            res.append(res2)
        self.series = res

