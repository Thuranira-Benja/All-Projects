from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

# --- DUMMY ML MODEL LOGIC ---
# In a real app, you would load a pre-trained model file here.
# e.g., import joblib; model = joblib.load('path/to/model.pkl')
def dummy_classify(text: str) -> dict:
    text = text.lower()
    if "water" in text:
        return {"category": "WATER", "confidence": 0.95}
    if "road" in text or "pothole" in text:
        return {"category": "ROADS", "confidence": 0.92}
    if "hospital" in text:
        return {"category": "HEALTH", "confidence": 0.88}
    return {"category": "OTHER", "confidence": 0.50}
# --- END DUMMY LOGIC ---

app = FastAPI(title="Meru ML Service")
router = APIRouter()

class ComplaintRequest(BaseModel):
    text: str

class ComplaintResponse(BaseModel):
    category: str
    confidence: float

@router.post("/classify", response_model=ComplaintResponse)
def classify_complaint(request: ComplaintRequest):
    """Classifies a complaint text using a dummy model."""
    return dummy_classify(request.text)

app.include_router(router, prefix="/complaints")

@app.get("/")
def health_check():
    return {"status": "ok"}