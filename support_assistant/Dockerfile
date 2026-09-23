FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    pydantic \
    langgraph \
    chromadb \
    sentence-transformers

EXPOSE 7860

CMD ["uvicorn", "main:api", "--host", "0.0.0.0", "--port", "7860"]