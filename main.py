from fastapi import FastAPI
from lib.connect_sheet import Sheet
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
data = Sheet()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get('/')
async def read_root():
    return data.get_question(161)

@app.get('/question/{question}')
async def get_question(question: int):
    return data.get_everything(question)

@app.put('/set_progress/{user}')
async def set_status(user: str):
    #this will be a number that is set from the frontend
    return True

@app.get('/get_progress/{user}')
async def get_progress(user: str):
    #This will be some number that is read from the DB
    return 23