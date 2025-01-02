import os
from dotenv import load_dotenv #환경변수
from fastapi import FastAPI #FastAPI tldud
from fastapi.middleware.cors import CORSMiddleware
from langchain.chains import RetrievalQA
from langchain_pinecone import PineconeVectorStore
from langchain_upstage import ChatUpstage, UpstageEmbeddings
from pinecone import Pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_upstage import UpstageDocumentParseLoader
from pydantic import BaseModel #JSON 구조 스키마마

load_dotenv()

# upstage 모델 초기화
chat_upstage = ChatUpstage()
embedding_upstage = UpstageEmbeddings(model="embedding-query")

# Pinecone 초기화
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
pinecone_env = os.environ.get("PINECONE_ENV", "us-east-1")
index_name = "chatbot-index"

# Pinecone 연결
pinecone = Pinecone(api_key=pinecone_api_key, environment=pinecone_env)

# Pinecone 인덱스 생성 (인덱스가 없으면 자동으로 생성)
if index_name not in pinecone.list_indexes().names():
    pinecone.create_index(name=index_name, dimension=4096, metric="cosine")

# PDF 파일 자동 분석 및 임베딩 (서버 시작 시 자동으로 실행)
def analyze_pdf_and_store():
    pdf_path = "Galaxy_A_35.pdf"  # PDF 파일 경로

    # PDF 파일 파싱 및 로딩
    document_parse_loader = UpstageDocumentParseLoader(
        pdf_path,
        output_format='html',  # 결과물 형태 : HTML
        coordinates=False  # 이미지 OCR 좌표계 가지고 오지 않기
    )
    docs = document_parse_loader.load()

    # 텍스트를 청크로 나누기
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    splits = text_splitter.split_documents(docs)

    # Pinecone에 문서 임베딩하여 저장
    PineconeVectorStore.from_documents(splits, embedding_upstage, index_name=index_name)
    print(f"{pdf_path} 파일 분석 및 저장 완료")

# 서버 시작 시 자동으로 PDF 파일 분석 및 임베딩
analyze_pdf_and_store()

# Pinecone에서 데이터를 검색하는 기능을 위한 벡터 스토어 설정
pinecone_vectorstore = PineconeVectorStore(index=pinecone.Index(index_name), embedding=embedding_upstage)

# 질문에 대한 답을 제공하는 검색기 설정
pinecone_retriever = pinecone_vectorstore.as_retriever(
    search_type='similarity',  # 유사도 검색
    search_kwargs={"k": 3}  # 쿼리와 관련된 chunk를 3개 검색
)

# FastAPI 애플리케이션 설정
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 프론트엔드와 연동을 위함, CORS 미들웨어
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 챗봇 응답 모델 설정
class MessageRequest(BaseModel):
    message: str 

@app.post("/chat")
async def chat_endpoint(req: MessageRequest):
    # 검색기 및 LLM을 활용한 QA 처리
    qa = RetrievalQA.from_chain_type(
        llm=chat_upstage,
        chain_type="stuff",
        retriever=pinecone_retriever,
        return_source_documents=True
    )
    
    result = qa(req.message)
    return {"reply": result['result']}

@app.get("/health")
@app.get("/")
async def health_check():
    return {"status": "ok"}

# 서버 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
