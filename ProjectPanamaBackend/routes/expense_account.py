from fastapi import APIRouter, Depends
from controller.expense_account import get_expenseAccount

expenseAccount_router = APIRouter()

@expenseAccount_router.get("/expense-accounts/", tags=["Expense Account"])
async def get_expenseAccounts():
  return await get_expenseAccount()