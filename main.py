
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,Field
from typing import List, Literal
import math

app = FastAPI()

Operation = Literal["add", "subtract", "multiply", "divide", "power", "sqrt"]

class CalcRequest(BaseModel):
    operation: Operation
    operands: list[float] = Field(..., min_length=3, max_length=3)

class CalcResponse(BaseModel):
    operation: Operation
    operands: List[float]
    result: float


@app.post("/calculate", response_model=CalcResponse)
async def calculate(req: CalcRequest):
    op = req.operation
    nums = req.operands

    try:
        if op == "add":
            result = sum(nums)
        elif op == "subtract":
            # subtract all subsequent numbers from the first
            result = nums[0]
            for n in nums[1:]:
                result -= n
        elif op == "multiply":
            result = 1.0
            for n in nums:
                result *= n
        elif op == "divide":
            result = nums[0]
            for n in nums[1:]:
                if n == 0:
                    raise HTTPException(status_code=400, detail="Division by zero")
                result /= n
        elif op == "power":
            # power: first operand raised to each subsequent operand in sequence
            result = nums[0]
            for n in nums[1:]:
                result = math.pow(result, n)
        elif op == "sqrt":
            # sqrt only uses the first operand
            if nums[0] < 0:
                raise HTTPException(status_code=400, detail="Cannot take sqrt of negative number")
            result = math.sqrt(nums[0])
        else:
            raise HTTPException(status_code=400, detail="Unsupported operation")
    except OverflowError:
        raise HTTPException(status_code=400, detail="Numeric overflow")

    return CalcResponse(operation=op, operands=nums, result=result)

# Convenience path endpoints
@app.get("/add")
async def add(a: float, b: float):
    return {"result": a + b}

@app.get("/subtract")
async def subtract(a: float, b: float):
    return {"result": a - b}

@app.get("/multiply")
async def multiply(a: float, b: float):
    return {"result": a * b}

@app.get("/divide")
async def divide(a: float, b: float):
    if b == 0:
        raise HTTPException(status_code=400, detail="Division by zero")
    return {"result": a / b}