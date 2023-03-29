FROM python:3.10
RUN pip install fastapi docker uvicorn
COPY . .
CMD ["uvicorn","api:app","--host","0.0.0.0"]