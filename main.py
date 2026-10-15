from datetime import date

from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select


class ExpenseCreate(SQLModel):
    description: str
    amount: float
    category: str
    spent_on: date


class Expense(ExpenseCreate, table=True):
    id: int | None = Field(default=None, primary_key=True)


engine = create_engine("sqlite:///expenses.db")
SQLModel.metadata.create_all(engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Expense Tracker API"}


@app.post("/expenses")
def create_expense(data: ExpenseCreate):
    expense = Expense.model_validate(data)
    with Session(engine) as session:
        session.add(expense)
        session.commit()
        session.refresh(expense)
        return expense


@app.get("/expenses")
def list_expenses(
    category: str | None = None,
    start: date | None = None,
    end: date | None = None,
):
    with Session(engine) as session:
        query = select(Expense)
        if category:
            query = query.where(Expense.category == category)
        if start:
            query = query.where(Expense.spent_on >= start)
        if end:
            query = query.where(Expense.spent_on <= end)
        return session.exec(query).all()


@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int):
    with Session(engine) as session:
        expense = session.get(Expense, expense_id)
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        return expense


@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, data: ExpenseCreate):
    with Session(engine) as session:
        expense = session.get(Expense, expense_id)
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        expense.sqlmodel_update(data.model_dump())
        session.add(expense)
        session.commit()
        session.refresh(expense)
        return expense


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    with Session(engine) as session:
        expense = session.get(Expense, expense_id)
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        session.delete(expense)
        session.commit()
        return {"message": "Expense deleted"}
