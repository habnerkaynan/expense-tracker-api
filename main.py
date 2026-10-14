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


@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, data: ExpenseCreate):
    for index, expense in enumerate(expenses):
        if expense.id == expense_id:
            updated = Expense(id=expense_id, **data.model_dump())
            expenses[index] = updated
            return updated
    raise HTTPException(status_code=404, detail="Expense not found")


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    for index, expense in enumerate(expenses):
        if expense.id == expense_id:
            expenses.pop(index)
            return {"message": "Expense deleted"}
    raise HTTPException(status_code=404, detail="Expense not found")
