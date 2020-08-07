from pydantic import BaseModel
from decimal import Decimal
import models

# 分页查询请求参数类
class queryBase1(BaseModel):
    startTime: int = 20200101
    endTime: int = 21000101
    name: str = ""
    size: int = 10
    page: int = 1


# 图表展示请求参数类
class queryBase2(BaseModel):
    name:str
    type:int
    date:str
    dataType:int


# 模板下载请求参数类
class fileBase(BaseModel):
    queryType: int = 3


class TableBase(BaseModel):
    id:int = 0
    dataTime:int = 0
    createTime: str = ""


# 数据校验pydanic兼容类
class HuaweiTotalClick(TableBase):
    INDUSTRY:str = ""
    MERCHANT_NAME:str = ""
    LOCATED_FIELD:str = ""
    TOTAL_CLICK:int=0

    class Config:
        orm_mode = True # 用于为Pydantic提供配置


class HuaweiServiceNumber(TableBase):
    SERVICE_NAME: str = ""
    INDUSTRY: str = ""
    MERCHANT_NAME: str = ""
    LOCATED_FIELD: str = ""
    OPEN_SERVICE_NUM: int = 0
    OPEN_MENU_NUM: int = 0
    OPEN_PAGE_NUM: int = 0
    PAGE_DAY_PV: int = 0
    PAGE_DAY_UV: int = 0
    PAGE_QUICK_APP_PV: int = 0
    PAGE_QUICK_APP_UV: int = 0
    CHAT_PV: int = 0
    CHAT_UV: int = 0

    class Config:
        orm_mode = True # 用于为Pydantic提供配置


class XiaomiServiceMenu(TableBase):
    SERVICE_NAME: str = ""
    MENU_EXPO: int = 0
    MENU_CLICK: int = 0
    MENU_DOWNLOAD: int = 0
    MENU_CLICK_RATE: Decimal = 0

    class Config:
        orm_mode = True # 用于为Pydantic提供配置


class XiaomiServiceBtn(TableBase):
    SERVICE_NAME: str = ""
    BTN_EXPO: int = 0
    BTN_CLICK: int = 0
    BTN_DOWNLOAD: int = 0
    BTN_CLICK_RATE: Decimal = 0

    class Config:
        orm_mode = True # 用于为Pydantic提供配置


# 分页信息类
class PageInfo():
    def __init__(self, page, size,  num, numberOfElements):
        self.page = page
        self.size = size
        self.total = num  # 当前总共条数
        self.numberOfElements = numberOfElements  # 当前页实际显示


# 响应参数类
class ResponseStandard():
    def __init__(self, message, subCode, data, pageInfo, cache):
        self.message = message
        self.subCode = subCode
        self.data = data
        self.pageInfo = pageInfo
        self.cache = cache


class ResponsePageHW():
    # id:int
    # industry:str
    # merchantName:str
    # serviceName:str
    # locatedField:str
    # pageDayPV:int
    # pageDayUV:int
    # pageQuickAppPV:int
    # pageQuickAppUV:int
    # chatPV:int
    # chatUV:int
    # date:int
    # totalClick:int
    # createTime:str
    # row:int
    def __init__(self,infoTotalClick:models.HuaweiTotalClick,
                 infoServiceNum:models.HuaweiServiceNumber=HuaweiServiceNumber(), row=1):
        self.id = infoTotalClick.ID
        self.industry = infoTotalClick.INDUSTRY
        self.merchantName = infoTotalClick.MERCHANT_NAME
        self.locatedField = infoTotalClick.LOCATED_FIELD
        self.pageDayPV = infoServiceNum.PAGE_DAY_PV
        self.pageDayUV = infoServiceNum.PAGE_DAY_UV
        self.pageQuickAppPV = infoServiceNum.PAGE_QUICK_APP_PV
        self.pageQuickAppUV = infoServiceNum.PAGE_QUICK_APP_UV
        self.chatPV = infoServiceNum.CHAT_PV
        self.chatUV = infoServiceNum.CHAT_UV
        self.date = infoTotalClick.DATA_TIME
        self.totalClick = infoTotalClick.TOTAL_CLICK
        self.createTime = infoTotalClick.CREATE_TIME
        self.row = row


class ResponsePageXM():
    def __init__(self,infoServiceBtn:models.XiaomiServiceBtn,
                 infoServiceMenu:models.XiaomiServiceMenu, row=1):
        self.id = infoServiceBtn.ID
        if infoServiceBtn.SERVICE_NAME == "":
            self.serviceName = infoServiceMenu.SERVICE_NAME
        else:
            self.serviceName = infoServiceBtn.SERVICE_NAME
        self.menuExpo = infoServiceMenu.MENU_EXPO
        self.menuClick = infoServiceMenu.MENU_CLICK
        self.menuDownload = infoServiceMenu.MENU_DOWNLOAD
        self.menuClickRate = infoServiceMenu.MENU_CLICK_RATE
        self.btnExpo = infoServiceBtn.BTN_EXPO
        self.btnClick = infoServiceBtn.BTN_CLICK
        self.btnDownload = infoServiceBtn.BTN_DOWNLOAD
        self.btnClickRate = infoServiceBtn.BTN_CLICK_RATE
        self.date = infoServiceBtn.DATA_TIME
        self.createTime = infoServiceBtn.CREATE_TIME
        self.row = row
