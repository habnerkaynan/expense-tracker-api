from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class ExpenseCreate(BaseModel):
    description: str
    amount: float
    category: str
    spent_on: date


class Expense(ExpenseCreate):
    id: int


expenses = []  # Provisory DataBase
next_id = 1


@app.get("/")
def home():
    return {"message": "Expense Tracker API"}


@app.post("/expenses")
def create_expense(data: ExpenseCreate):
    global next_id
    expense = Expense(id=next_id, **data.model_dump())
    expenses.append(expense)
    next_id += 1
    return expense


@app.get("/expenses")
def list_expenses():
    return expenses


@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int):
    for expense in expenses:
        if expense.id == expense_id:
            return expense
    raise HTTPException(status_code=404, detail="Expense not found")
