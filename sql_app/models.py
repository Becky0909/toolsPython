from sqlalchemy import Column, DECIMAL, Integer, String, BigInteger, TIMESTAMP, UniqueConstraint, text
from database import Base # 已声明的数据库
"""row：行    column：列"""


#数据库映射SQL alchemy ORM
class HuaweiTotalClick(Base):
    __tablename__ = 'HUAWEI_TOTAL_CLICK'
    __table_args__ = (UniqueConstraint('MERCHANT_NAME', 'DATA_TIME', name='UK_MERCHANT_DATE'),)#联合唯一
    ID = Column(BigInteger, primary_key=True, autoincrement=True,nullable=False, comment="ID")
    INDUSTRY = Column(String(128),nullable=False, server_default='', comment="行业")
    MERCHANT_NAME = Column(String(128), nullable=False, server_default='', comment="商家昵称")
    LOCATED_FIELD = Column(String(128), nullable=False, server_default='', comment="所在域")
    TOTAL_CLICK = Column(BigInteger, nullable=False, server_default=text('0'), comment="总点击数")
    DATA_TIME = Column(Integer, nullable=False, server_default=text('19700101'), comment="日期")
    CREATE_TIME = Column(TIMESTAMP, nullable=False, default='1970-01-01 00:00:00', comment="创建时间")


class HuaweiServiceNumber(Base):
    __tablename__ = 'HUAWEI_SERVICE_NUMBER'
    __table_args__ = (UniqueConstraint('MERCHANT_NAME', 'DATA_TIME', name='UK_MERCHANT_DATE'),)  # 联合唯一
    ID = Column(BigInteger, primary_key=True, autoincrement=True,nullable=False, comment="ID")
    SERVICE_NAME = Column(String(128), nullable=False, server_default='', comment="服务号名称")
    INDUSTRY = Column(String(128),nullable=False, server_default='', comment="行业")
    MERCHANT_NAME = Column(String(128), nullable=False, server_default='', comment="商家昵称")
    LOCATED_FIELD = Column(String(128), nullable=False, server_default='', comment="所属域")
    OPEN_SERVICE_NUM = Column(BigInteger, nullable=False,server_default=text('0'), comment="总开通服务号数")
    OPEN_MENU_NUM = Column(BigInteger, nullable=False, server_default=text('0'), comment="总开通了菜单的服务号数")
    OPEN_PAGE_NUM = Column(BigInteger, nullable=False, server_default=text('0'), comment="总开通了主页的服务号数")
    PAGE_DAY_PV = Column(BigInteger, nullable=False, server_default=text('0'), comment="服务号主页日PV")
    PAGE_DAY_UV = Column(BigInteger, nullable=False, server_default=text('0'), comment="服务号主页日UV")
    PAGE_QUICK_APP_PV = Column(BigInteger, nullable=False, server_default=text('0'), comment="服务号主页快应用PV")
    PAGE_QUICK_APP_UV = Column(BigInteger, nullable=False, server_default=text('0'), comment="服务号主页快应用UV")
    CHAT_PV = Column(BigInteger, nullable=False, server_default=text('0'), comment="服务号会话PV")
    CHAT_UV = Column(BigInteger, nullable=False, server_default=text('0'), comment="服务号会话UV")
    DATA_TIME = Column(Integer, nullable=False, server_default=text('19700101'), comment="日期")
    CREATE_TIME = Column(TIMESTAMP, nullable=False, default='1970-01-01 00:00:00', comment="创建时间")


class XiaomiServiceMenu(Base):
    __tablename__ = 'XIAOMI_SERVICE_MENU'
    __table_args__ = (UniqueConstraint('SERVICE_NAME', 'DATA_TIME', name='UK_SERVICE_DATE'),)  # 联合唯一
    ID = Column(BigInteger, primary_key=True, autoincrement=True,nullable=False, comment="ID")
    SERVICE_NAME = Column(String(128), nullable=False, server_default='', comment="服务号名称")
    MENU_EXPO = Column(BigInteger, nullable=False, server_default=text('0'), comment="菜单曝光数")
    MENU_CLICK = Column(BigInteger, nullable=False, server_default=text('0'), comment="菜单点击数")
    MENU_DOWNLOAD = Column(BigInteger, nullable=False, server_default=text('0'), comment="菜单-APP下载量")
    MENU_CLICK_RATE = Column(DECIMAL(9,4),nullable=False, server_default=text('0'), comment="菜单点击率百分比")
    DATA_TIME = Column(Integer, nullable=False, server_default=text('19700101'), comment="日期")
    CREATE_TIME = Column(TIMESTAMP, nullable=False, default='1970-01-01 00:00:00', comment="创建时间")


class XiaomiServiceBtn(Base):
    __tablename__ = 'XIAOMI_SERVICE_BTN'
    __table_args__ = (UniqueConstraint('SERVICE_NAME', 'DATA_TIME', name='UK_SERVICE_DATE'),)  # 联合唯一
    ID = Column(BigInteger, primary_key=True, autoincrement=True,nullable=False, comment="ID")
    SERVICE_NAME = Column(String(128), nullable=False, server_default='', comment="服务号名称")
    BTN_EXPO = Column(BigInteger, nullable=False, server_default=text('0'), comment="按钮曝光数")
    BTN_CLICK = Column(BigInteger, nullable=False, server_default=text('0'), comment="按钮点击数")
    BTN_DOWNLOAD = Column(BigInteger, nullable=False, server_default=text('0'), comment="按钮-APP下载量")
    BTN_CLICK_RATE = Column(DECIMAL(9,4),nullable=False, server_default=text('0'), comment="按钮点击率百分比")
    DATA_TIME = Column(Integer, nullable=False, server_default=text('19700101'), comment="日期")
    CREATE_TIME = Column(TIMESTAMP, nullable=False, default='1970-01-01 00:00:00', comment="创建时间")