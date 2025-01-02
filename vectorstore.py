import os
import pprint
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_upstage import ChatUpstage
from pinecone import Pinecone, ServerlessSpec
from langchain_upstage import UpstageEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

load_dotenv()

def identify_manufacturer(query):
    manufacturer_keywords = {
        "SAMSUNG": ["SAMSUNG", "samsung", "삼성", "샘숭", "갤럭시", "갤럭시북"],
        "LG": ["엘지", "lg", "그램", "gram"],
        "LENOVO": ["레노버", "레노바", "LENOVO", "씽크패드", "ThinkPad", "아이디어패드", "IdeaPad", "요가", "Yoga"],
        "HP": ["에이치피", "hp", "엘리트북"]
    }
    
    query_lower = query.lower()
    for manufacturer, keywords in manufacturer_keywords.items():
        if any(keyword.lower() in query_lower for keyword in keywords):
            return manufacturer
    return None

# Pinecone 설정
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)
index_name = "laptop-manuals"

# llm 설정
llm = ChatUpstage(model='solar-pro')

# query embedding model 설정
embedding_model = UpstageEmbeddings(model="embedding-query")

# index 생성
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=4096,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
)

# 벡터스토어 및 리트리버 정의
vectorstore = PineconeVectorStore(
    index=pc.Index(index_name), 
    embedding=embedding_model
)

# 메타데이터 필터링이 포함된 리트리버 
def get_filtered_retriever(manufacturer):
    return vectorstore.as_retriever(
                search_type='mmr',
                search_kwargs={
                    'k': 3,
                    'filter': {"manufacturer": manufacturer}
                }
    )

# 프롬프트 정의
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        당신은 노트북 제품과 관련된 문제 해결을 돕는 전문 AI 어시스턴트입니다.
        사용자 질문과 문맥(RAG로 검색된 정보)을 바탕으로, **구체적이고 실용적인 해결 방법**만 제안하세요.

        --- 문맥 ---
        {retrieved_content}

        --- 지침 ---
        1. 문맥에 있는 정보만 사용하여 문제를 해결하세요.
        2. 필요한 경우 추가 정보가 필요하다고 요청하세요.
        3. 간결하고 명확한 언어로 답변하세요.
        4. 가장 먼저 제조사 정보를 명시해주세요. 예시) " 삼성전자의 제품이군요 "
            - 만약 등록되지 않은 제조사라면 그점을 명시하고 답변을 중지하세요.
        
    """,
    ),
    ("human", "{input}"),
])

# 사용자 입력 쿼리에 따른 반환하는 함수
def process_query(query):
    """
    주어진 쿼리에 대해 제조사 식별, 리트리버 필터링, LLM 체인 처리까지 수행하는 함수.

    Parameters:
        query (str): 사용자가 입력한 쿼리.

    Returns:
        str: LLM 처리 결과.
    """
    # 제조사 식별
    manufacturer = identify_manufacturer(query)

    if manufacturer:
        # 해당 제조사의 문서만 검색하는 리트리버 생성
        filtered_retriever = get_filtered_retriever(manufacturer)
        result_docs = filtered_retriever.invoke(query)
    else:
        # 제조사를 식별할 수 없는 경우 기본 검색
        retriever = vectorstore.as_retriever(
            search_type='mmr',
            search_kwargs={'k': 3}
        )
        result_docs = retriever.invoke(query)

    # LLM 체인 생성 및 실행
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"retrieved_content": result_docs, "input": query})

    return response




# # 사용자 입력 쿼리는 따로 받을거긴 해
# query = "맥북 관련된 것도 답변할 수 있어???"

# # 제조사 식별부터 함.
# #   - 메타데이터 구분해야 해서.
# manufacturer = identify_manufacturer(query)

# if manufacturer:
#     # 해당 제조사의 문서만 검색하는 리트리버 생성
#     filtered_retriever = get_filtered_retriever(manufacturer)
#     result_docs = filtered_retriever.invoke(query)
# else:
#     # 제조사를 식별할 수 없는 경우 기본 검색
#     retriever = vectorstore.as_retriever(
#         search_type='mmr',
#         search_kwargs={'k': 3}
#     )
#     result_docs = retriever.invoke(query)

# chain = prompt | llm | StrOutputParser()
# response = chain.invoke({"retrieved_content": result_docs, "input": query})

# print(response)