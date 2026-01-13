from fastapi import FastAPI
from app.api import news

app = FastAPI(title="Daily News Dashboard API")

# 路由注册
app.include_router(news.router, prefix="/news", tags=["news"])
# app.include_router(ainews.router, prefix="/ai", tags=["ai"])
# app.include_router(mythoughts.router, prefix="/thoughts", tags=["thoughts"])

@app.get("/")
def root():
    return {"message": "FastAPI is running!"}
