from fastapi import Depends, FastAPI, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import api_def as api
import models, schemas
from starlette.requests import Request

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# 华为终端报表分页
@app.post("/OperateService/operateManage/queryPageHuaWei")
def queryPageHuaWei(query: schemas.queryBase1, db: Session = Depends(api.get_db)):
    return api.pageHW(query, db)


# 小米终端报表分页
@app.post("/OperateService/operateManage/queryPageXiaoMi")
def queryPageXiaoMi(query: schemas.queryBase1, db: Session = Depends(api.get_db)):
    return api.pageXM(query, db)


# 华为终端点击报表导入/华为终端统计数据表导入
@app.post("/OperateService/operateManage/importHuaWei")
def importHuaWei(request:Request,queryType : int = Form(...),
                subPage: int = Form(...), subSize: int = Form(...) ,
                file: UploadFile = File(...), db: Session = Depends(api.get_db)):
    return api.importHW(queryType, subPage, subSize, file, db)


# 小米终端报表导入
@app.post("/OperateService/operateManage/importXiaoMi")
def importXiaoMi(request: Request, subPage: int = Form(...), subSize: int = Form(...),
                 file: UploadFile = File(...), db: Session = Depends(api.get_db)):
    return api.importXM(subPage, subSize, file, db)


@app.post("/OperateService/operateData/getHuaWeiChart")
def getHuaWeiChart(query: schemas.queryBase2, db: Session = Depends(api.get_db)):
    return api.preHW(query, db)


@app.post("/OperateService/operateData/getXiaoMiChart")
def getXiaoMiChart(query: schemas.queryBase2, db: Session = Depends(api.get_db)):
    return api.preXM(query, db)


# 华为终端点击报表模板下载/华为终端数据报表模板下载/小米终端报表模板下载
@app.post("/OperateService/operateManage/downloadTemplate")
def downloadTemplate(query: schemas.fileBase, db: Session = Depends(api.get_db)):
    return api.exModel(query, db)


@app.post("/OperateService/operate/getNameList")
def getNameList(query: schemas.fileBase, db: Session = Depends(api.get_db)):
    return api.preNameList(query.queryType, db)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="218.17.39.34", port=8000)
