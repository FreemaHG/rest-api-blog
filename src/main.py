from fastapi import FastAPI


app = FastAPI(title='Blog API', debug=True)

@app.get("/")
async def root():
    return {"message": "Hello World"}
