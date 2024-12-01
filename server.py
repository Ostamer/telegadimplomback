from fastapi import FastAPI, Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from functions import first_func, second_func, third_func, first, second, third

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LemmatizationResponse(BaseModel):
    lemma: str


def lemmatize(mode: int, selected_option: str, input_value: str) -> str:
    if mode == 1:
        if selected_option == "-" or selected_option == "":
            res = first(input_value)
            return first_func(res)
        else:
            res = second(input_value, selected_option)
            return second_func(res)
    elif mode == 2:
        if selected_option == "Всё предложение" or selected_option == "":
            res = []
            for i in input_value:
                loc_res = third(i, input_value)
                res.append(third_func(loc_res))
            return " ".join(res)
        else:
            res = third(selected_option, input_value)
            return third_func(res)
    return "Некорректные данные"



# def lemmatize(mode: int, selected_option: str, input_value: str) -> str:
#     if mode == 1:
#         if selected_option == "-" or selected_option == "":
#             return "1 Вариант"
#         else:
#             return "2 Вариант"
#     elif mode == 2:
#         if selected_option == "Всё предложение" or selected_option == "":
#             return "3 Вариант"
#         else:
#             return "4 Вариант"
#     return "Некорректные данные"

@app.get("/lemmatize", response_model=LemmatizationResponse)
async def lemmatize_text(
    mode: int,
    selected_option: str = Query(...),
    input_value: str = Query(...)
):
    lemma = lemmatize(mode, selected_option, input_value)
    return LemmatizationResponse(lemma=lemma)