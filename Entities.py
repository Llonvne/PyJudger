from pydantic import BaseModel


class TestCase(BaseModel):
    input: str
    output: str


class RunnerRequest(BaseModel):
    submission_id: int
    testcases: list[TestCase]


class CompilerRequest(BaseModel):
    submission_id: int
    code: str
