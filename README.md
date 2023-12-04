# PyJudger

## Introduction

PyJudger is a sandbox code execution module for an online judge system based on FastApi and Docker.

## Status ![Static Badge](https://img.shields.io/badge/status-Finished-8A2BE2)

PyJudger has already completed the implementation of the sandbox code execution module for **C++, Java, and
Python**.Relying on Docker technology, we can easily provide almost all versions of Java and Python.

## Usage

When starting the program with Python, it will automatically listen on the localhost:8000 port and respond to the
following URIs.

![Static Badge](https://img.shields.io/badge/C++-Compile-blue) /api/cpp_compiler : Pass in the CompilerRequest to
execute the C++ compilation task.

![Static Badge](https://img.shields.io/badge/C++-Run-blue) /api/cpp_runner : Pass in the RunnerRequest to
execute the C++ runner task.

![Static Badge](https://img.shields.io/badge/Python3-Compile-blue) /api/python3_runner : Pass in the CompilerRequest to
execute the Python3 compilation task (in fact,server just save the code in code file).

![Static Badge](https://img.shields.io/badge/Python3-Run-blue) /api/python3_runner/{python_version} : Pass in the RunnerRequest to
execute the Python3 runner task.

![Static Badge](https://img.shields.io/badge/Java-Compile-blue) /api/jdk_compiler : Pass in the CompilerRequest to
execute the Java compilation task (in fact,server just save the code in code file).

![Static Badge](https://img.shields.io/badge/Java-Run-blue) /api/jdk_runner/{java_version} : Pass in the RunnerRequest to
execute the Java runner task.

