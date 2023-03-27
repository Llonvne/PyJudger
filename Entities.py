from pydantic import BaseModel


class TestCase(BaseModel):
    input: str
    output: str


class CppRunnerRequest(BaseModel):
    submission_id: int
    testcases: list[TestCase]


class CppCompilerRequest(BaseModel):
    submission_id: int
    code: str
