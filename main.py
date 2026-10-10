from datetime import date

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Expense(BaseModel):
    description: str
    amount: float
    category: str
    spent_on: date


expenses = []  # Provisory DataBase


@app.get("/")
def home():
    return {"message": "Expense Tracker API"}


@app.post("/expenses")
def create_expense(expense: Expense):
    expenses.append(expense)
    return expense


@app.get("/expenses")
def list_expenses():
    return expenses
