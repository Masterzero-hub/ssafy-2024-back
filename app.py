# pip install fastapi uvicorn openai python-dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

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


@app.post("/chat")
async def chat_endpoint(req: MessageRequest):
    # Call the OpenAI ChatCompletion endpoint
    print('test')
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": req.message},
        ],
        # temperature=0.7,
    )
    # Extract assistant message
    assistant_reply = response.choices[0].message.content
    return {"reply": assistant_reply}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
