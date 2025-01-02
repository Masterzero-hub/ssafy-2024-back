# pip install fastapi uvicorn openai python-dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from langchain.schema.output_parser import StrOutputParser
from vectorstore import identify_manufacturer, get_filtered_retriever, vectorstore, prompt, llm


load_dotenv()  # Load .env file if present

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MessageRequest(BaseModel):
    message: str

def process_query(query):
    """
    주어진 쿼리에 대해 제조사 식별, 리트리버 필터링, LLM 체인 처리까지 수행하는 함수.

    Parameters:
        query (str): 사용자가 입력한 쿼리.

    Returns:
        str: LLM 처리 결과.
    """
    manufacturer = identify_manufacturer(query)

    if manufacturer:
        filtered_retriever = get_filtered_retriever(manufacturer)
        result_docs = filtered_retriever.invoke(query)
    else:
        retriever = vectorstore.as_retriever(
            search_type='mmr',
            search_kwargs={'k': 3}
        )
        result_docs = retriever.invoke(query)

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"retrieved_content": result_docs, "input": query})

    return response

@app.post("/chat")
async def chat_endpoint(req: MessageRequest):
    """
    Chat 엔드포인트: 사용자의 메시지를 받아 process_query를 호출하고 LLM 응답을 반환.

    Parameters:
        req (MessageRequest): 사용자의 메시지를 포함한 요청 객체.

    Returns:
        dict: 처리된 응답 메시지를 포함한 JSON 객체.
    """
    # Process the query through process_query function
    response = process_query(req.message)

    # Return the response as a JSON object
    return {"reply": response}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
