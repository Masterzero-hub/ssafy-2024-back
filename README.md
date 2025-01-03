# ssafy-2024-back
# 노트북 정보 제공 챗봇

## 1. 문제 제기

### 1) 최신 노트북에 대한 정보 제공
- 이전에 기록된 정보만 제공되어 최신 노트북에 대한 정보가 제공되지 않았습니다.

### 2) 할루시네이션 발생
- GPT에서 제공하는 웹 검색 기능을 사용하더라도, 원하는 정보와 동일한 명칭에 대한 정보가 포함되어 할루시네이션이 발생할 수 있습니다.

## 2. 최신 노트북 사용 설명 챗봇 소개
- **RAG(Retrieval-Augmented Generation)** 기반 챗봇 서비스 구현

## 3. Task 유형 정의 / 주요 기능

### 1) 대화형 인터페이스 설계 및 구현
- 사용자 요청을 자연스럽게 처리하는 직관적인 챗봇 UI 개발
- 사용자 경험(UX) 최적화를 위한 인터페이스 개선

### 2) DB 생성
- 최신 노트북 정보가 담긴 데이터베이스 구축

### 3) 대규모 언어 모델(LLM) 활용
- LLM을 통해 자연스러운 대화와 문맥 기반 응답 생성

### 4) RAG 기법 적용
- DB 검색 결과를 바탕으로 LLM이 최적의 답변을 생성하도록 설계

## 4. 사용 툴

### 프론트엔드: Node.js
<img src="https://camo.githubusercontent.com/3358fe92e876704b4bf9965ef89ec7f7d842398c9db8bf64806b4d2211cd9a27/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4e6f64652e6a732d3333393933393f7374796c653d666f722d7468652d6261646765266c6f676f3d4e6f64652e6a73266c6f676f436f6c6f723d7768697465">
<img src="https://camo.githubusercontent.com/bb609305bebe02f66a56aedbc7bb565f7a2b91e55c11dbdec7834af157ad5aa2/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4a6176615363726970742d4637444631453f7374796c653d666f722d7468652d6261646765266c6f676f3d5265616374266c6f676f436f6c6f723d7768697465">

### 백엔드: FastAPI
<img src="https://camo.githubusercontent.com/9d770366baad027e7316fcbffeb7ae265dc9a464ad86c2bb386a30d1e8d70f7b/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f707974686f6e2d3337373641423f7374796c653d666f722d7468652d6261646765266c6f676f3d707974686f6e266c6f676f436f6c6f723d7768697465">

![FastAPI 로고](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)

### 데이터베이스: Pinecone
![Pinecone 로고](https://pinecone.io/images/pinecone-logo.svg)

### 모델
- **임베딩**: [모델명 추가]
- **리트리버**: [모델명 추가]

### 모델 테스트: RAGAS
![RAGAS 로고](https://raw.githubusercontent.com/explodinggradients/ragas/main/docs/images/ragas-logo-light.png)

### 배포: AWS, Fly.io
<img src="https://camo.githubusercontent.com/a8c9424c4c80c2c77f6c62ba94547494c0286073d63c138001e089dc907955c8/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f636b65722d3234393645443f7374796c653d666f722d7468652d6261646765266c6f676f3d446f636b6572266c6f676f436f6c6f723d7768697465">

![AWS 로고](https://a0.awsstatic.com/libra-css/images/logos/aws_logo_smile_1200x630.png)
![Fly.io 로고](https://fly.io/static/images/brand/logo-text-dark.svg)

### GitHub에서 사용되는 도구들
- **Git**: ![Git 로고](https://git-scm.com/images/logos/downloads/Git-Logo-2Color.png)
- **Docker**: ![Docker 로고](https://www.docker.com/wp-content/uploads/2022/03/Moby-logo.png)
- **Kubernetes**: ![Kubernetes 로고](https://kubernetes.io/images/header.png)


<img src="https://img.shields.io/badge/Mattermost-0058CC?style=for-the-badge&logo=Mattermost&logoColor=white" style="height : auto; margin-left : 10px; margin-right : 10px;"/>
<img src="https://camo.githubusercontent.com/0c43d19336fe5adc9b7a892ecb0152393d36a9512cb7da6d6529ae140aeb8334/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4749542d4630353033323f7374796c653d666f722d7468652d6261646765266c6f676f3d474954266c6f676f436f6c6f723d7768697465">

# 기능

- 사용자가 노트북에 대한 사용 방법을 묻는 경우, 질문 내용에서 노트북 제조사를 식별하는 기능을 추가했습니다.
- 식별된 노트북 제조사를 기반으로, 사전 학습된 사용 설명서를 참조하여 정확한 답변을 제공합니다.

## 주요 기능

### 1. 할루시네이션 답변 방지

- **notbot의 답변**
    ![image.png](images/notbot_1.png)

- **OpenAI ChatGPT의 답변**:
  - "Yoga"는 레노바의 노트북 모델명이지만, 그래픽 디지털 디자인 소프트웨어와 혼동될 수 있습니다.
  - "Pen Pro"는 스타일러스(디지털 펜)로 혼동될 수 있습니다.
  
  ![image.png](images/gpt_1.png)

### 2. 부정확한 답변 방지

- **notbot의 답변**
    ![image.png](images/notbot_2.png)

- **OpenAI ChatGPT의 답변** → 웹 검색을 통한 답변
  
  삼성 S펜에 대한 답변도 포함하여 제공되고 있습니다.

    ![image.png](images/gpt_2.png)
