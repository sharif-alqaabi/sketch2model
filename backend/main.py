from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import anthropic
import os
from dotenv import load_dotenv
import base64
from io import BytesIO
from PIL import Image
from datetime import datetime
from typing import Optional
import httpx
import json

# import agents
from agents.root_agent import RootAgent

# firebase imports - commented out for now, uncomment when ready to use
# import firebase_admin
# from firebase_admin import credentials, firestore

load_dotenv()
app = FastAPI(title="Drawing to 3D House Design API - Multi-Agent System")

# cors middleware for react frontend
# Get allowed origins from environment variable or use defaults
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if os.getenv("ENVIRONMENT") == "production" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialize anthropic client
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# initialize root agent for multi-agent workflow
root_agent = RootAgent()

# firebase initialization - commented out for now
# uncomment this section when you're ready to use firebase
db = None  # set to none by default (firebase disabled)

# try:
#     if not firebase_admin._apps:
#         firebase_cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
#         if firebase_cred_path and os.path.exists(firebase_cred_path):
#             cred = credentials.Certificate(firebase_cred_path)
#             firebase_admin.initialize_app(cred)
#             db = firestore.client()
#             print("✅ Firebase initialized successfully")
#         else:
#             print("ℹ️  Firebase not configured - running without database")
# except Exception as e:
#     print(f"⚠️  Firebase initialization error: {e}")
#     db = None


@app.get("/")
async def root():
    return {"message": "Drawing to 3D House Design API", "status": "running"}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "anthropic_configured": bool(os.getenv("ANTHROPIC_API_KEY")),
        "firebase_configured": db is not None
    }


@app.post("/api/generate-3d-design")
async def generate_3d_design(file: UploadFile = File(...)):
    """
    accepts a drawing image and executes multi-agent workflow:
    1. generator agent: creates 3d design from drawing
    2. estimator agent: estimates construction costs and materials
    """
    try:
        # read and validate the uploaded image
        contents = await file.read()
        
        # validate image format
        try:
            image = Image.open(BytesIO(contents))
            # convert to rgb if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # resize if too large (max 1024x1024 for api efficiency)
            max_size = 1024
            if image.width > max_size or image.height > max_size:
                image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # convert back to bytes
            img_byte_arr = BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image format: {str(e)}")
        
        # encode image to base64
        image_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
        
        # execute only generator agent for design generation
        workflow_input = {
            'image_base64': image_base64,
            'image_width': image.width,
            'image_height': image.height
        }
        
        generator_result = await root_agent.generator_agent.execute(workflow_input)
        
        if not generator_result.get('success'):
            raise HTTPException(status_code=500, detail=f"Design generation failed")
        
        # prepare response data with only design (no cost estimation yet)
        result = {
            "success": True,
            "design_description": generator_result.get('design_description'),
            "generated_image_url": generator_result.get('generated_image_url'),
            "timestamp": datetime.utcnow().isoformat(),
            "model_used": "claude-sonnet-4-20250514"
        }
        
        # save to firebase if available (currently disabled)
        # uncomment this section when firebase is configured
        # if db:
        #     try:
        #         doc_ref = db.collection('designs').add({
        #             'design_description': ai_response,
        #             'timestamp': firestore.SERVER_TIMESTAMP,
        #             'model_used': 'claude-sonnet-4-20250514',
        #             'image_size': f"{image.width}x{image.height}"
        #         })
        #         result['firebase_id'] = doc_ref[1].id
        #         print(f"✅ Design saved to Firebase with ID: {doc_ref[1].id}")
        #     except Exception as e:
        #         print(f"⚠️  Firebase save error: {e}")
        #         # continue even if firebase save fails
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.post("/api/estimate-cost")
async def estimate_cost(file: UploadFile = File(...)):
    """
    estimates construction cost and materials for a house drawing
    uses estimator agent to provide detailed material list and cost breakdown
    """
    try:
        # read and validate the uploaded image
        contents = await file.read()
        
        # validate image format
        try:
            image = Image.open(BytesIO(contents))
            # convert to rgb if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # resize if too large (max 1024x1024 for api efficiency)
            max_size = 1024
            if image.width > max_size or image.height > max_size:
                image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # convert back to bytes
            img_byte_arr = BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image format: {str(e)}")
        
        # encode image to base64
        image_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
        
        # execute estimator agent
        estimator_input = {
            'image_base64': image_base64,
            'design_description': ''  # can be empty, estimator will analyze image directly
        }
        
        estimator_result = await root_agent.estimator_agent.execute(estimator_input)
        
        if not estimator_result.get('success'):
            raise HTTPException(status_code=500, detail=f"Cost estimation failed")
        
        # prepare response
        result = {
            "success": True,
            "cost_estimation": estimator_result.get('cost_estimation'),
            "cost_estimation_json": estimator_result.get('cost_estimation_json'),
            "timestamp": datetime.utcnow().isoformat(),
            "agent": "EstimatorAgent"
        }
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.post("/api/voice-to-design")
async def voice_to_design(file: UploadFile = File(...)):
    """
    accepts audio input, converts to text using Fish Audio API,
    then generates 3D house design - VoiceAgent handles everything independently
    """
    try:
        # read the uploaded audio file
        audio_contents = await file.read()
        
        # determine audio format from filename
        audio_format = file.filename.split('.')[-1] if '.' in file.filename else 'webm'
        
        print(f"🎤 Received audio file: {file.filename} (format: {audio_format})")
        
        # step 1: convert audio to text using voice agent
        voice_input = {
            'audio_data': audio_contents,
            'audio_format': audio_format
        }
        
        voice_result = await root_agent.voice_agent.execute(voice_input)
        
        if not voice_result.get('success'):
            raise HTTPException(status_code=500, detail="Voice transcription failed")
        
        transcribed_text = voice_result.get('transcribed_text', '')
        print(f"📝 Transcribed: {transcribed_text}")
        
        # step 2: VoiceAgent generates complete design (independent like GeneratorAgent)
        design_result = await root_agent.voice_agent.generate_design_from_text(transcribed_text)
        
        if not design_result.get('success'):
            raise HTTPException(status_code=500, detail="Design generation failed")
        
        print(f"✅ Design generated successfully by VoiceAgent")
        
        # prepare response in same format as generate-3d-design endpoint
        result = {
            "success": True,
            "transcribed_text": transcribed_text,
            "design_description": design_result.get('design_description'),
            "generated_image_url": design_result.get('generated_image_url'),
            "timestamp": datetime.utcnow().isoformat(),
            "model_used": "fish-audio + claude-sonnet-4-20250514"
        }
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error in voice-to-design: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/api/designs")
async def get_designs(limit: int = 10):
    """
    retrieve recent designs from firebase
    """
    if not db:
        raise HTTPException(status_code=503, detail="Firebase not configured")
    
    try:
        designs_ref = db.collection('designs').order_by(
            'timestamp', direction=firestore.Query.DESCENDING
        ).limit(limit)
        
        designs = []
        for doc in designs_ref.stream():
            design_data = doc.to_dict()
            design_data['id'] = doc.id
            designs.append(design_data)
        
        return {"designs": designs}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving designs: {str(e)}")


@app.get("/api/design/{design_id}")
async def get_design(design_id: str):
    """
    Retrieve a specific design by ID.
    """
    if not db:
        raise HTTPException(status_code=503, detail="Firebase not configured")
    
    try:
        doc_ref = db.collection('designs').document(design_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Design not found")
        
        design_data = doc.to_dict()
        design_data['id'] = doc.id
        
        return design_data
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving design: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
