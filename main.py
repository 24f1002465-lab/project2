from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Home route so Render doesn't show "Not Found"
@app.get("/")
async def home():
    return {"message": "Sentiment API is running"}

class CommentRequest(BaseModel):
    comment: str

class SentimentResponse(BaseModel):
    sentiment: str
    rating: int

positive_words = ["good", "great", "amazing", "love", "excellent", "best", "fantastic", "awesome"]
negative_words = ["bad", "worst", "hate", "terrible", "awful", "poor", "disappointing"]

def analyze(text):
    text = text.lower()
    score = 0

    for word in positive_words:
        if word in text:
            score += 1

    for word in negative_words:
        if word in text:
            score -= 1

    if score > 0:
        return "positive", min(5, 3 + score)
    elif score < 0:
        return "negative", max(1, 3 + score)
    else:
        return "neutral", 3

@app.post("/comment", response_model=SentimentResponse)
async def analyze_comment(data: CommentRequest):
    sentiment, rating = analyze(data.comment)
    return {
        "sentiment": sentiment,
        "rating": rating
    }