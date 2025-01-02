import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_upstage import UpstageDocumentParseLoader
from langchain_upstage import UpstageEmbeddings
from pinecone import Pinecone

load_dotenv()

# 환경 변수 로드
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
pinecone_env = os.environ.get("PINECONE_ENV", "us-east-1")
index_name = "chatbot-index"

# Pinecone 초기화
pinecone = Pinecone(api_key=pinecone_api_key, environment=pinecone_env)

# Pinecone 인덱스가 없으면 생성
if index_name not in pinecone.list_indexes().names():
    pinecone.create_index(name=index_name, dimension=4096, metric="cosine")

# Upstage 임베딩 모델 초기화
embedding_upstage = UpstageEmbeddings(model="embedding-query")

# PDF 파일 경로 설정
pdf_path = "Galaxy_A_35.pdf"

# PDF 파일 로딩 및 분석
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

# Pinecone에 임베딩된 문서를 저장
PineconeVectorStore.from_documents(splits, embedding_upstage, index_name=index_name)
print(f"{pdf_path} 파일 분석 및 Pinecone에 저장 완료")
