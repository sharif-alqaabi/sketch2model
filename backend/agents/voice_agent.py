from .base_agent import BaseAgent
from typing import Dict, Any
import os
import base64
from fish_audio_sdk import Session, ASRRequest

class VoiceAgent(BaseAgent):
    """agent responsible for converting voice input to text using Fish Audio API"""
    
    def __init__(self):
        super().__init__(
            name="VoiceAgent",
            description="converts audio input to text description using Fish Audio speech-to-text API"
        )
        self.fish_audio_api_key = os.getenv("FISH_AUDIO_API_KEY")
        if not self.fish_audio_api_key:
            raise ValueError("FISH_AUDIO_API_KEY environment variable is required")
        
        # Initialize Fish Audio SDK session
        self.session = Session(self.fish_audio_api_key)
        print(f"✅ {self.name}: initialized with Fish Audio SDK")
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        execute voice-to-text conversion
        input_data: {
            'audio_data': bytes or base64 string,
            'audio_format': str (e.g., 'wav', 'mp3', 'webm')
        }
        """
        audio_data = input_data.get('audio_data')
        audio_format = input_data.get('audio_format', 'webm')
        
        if not audio_data:
            raise ValueError("audio_data is required")
        
        print(f"🎤 {self.name}: processing audio input (format: {audio_format})")
        
        try:
            # convert base64 to bytes if needed
            if isinstance(audio_data, str):
                audio_bytes = base64.b64decode(audio_data)
            else:
                audio_bytes = audio_data
            
            print(f"🌐 {self.name}: calling Fish Audio SDK for ASR...")
            
            # Create ASR request using Fish Audio SDK
            asr_request = ASRRequest(
                audio=audio_bytes,
                language="en",  # Auto-detect or specify language
                ignore_timestamps=True  # We don't need timestamps for our use case
            )
            
            # Call Fish Audio ASR
            asr_response = self.session.asr(asr_request)
            
            # Extract transcribed text from response
            transcribed_text = asr_response.text
            
            if not transcribed_text:
                raise Exception("No text transcribed from audio")
            
            print(f"✅ {self.name}: successfully transcribed audio")
            print(f"📝 Transcribed text: {transcribed_text[:100]}...")
            
            # update context for other agents
            self.update_context('transcribed_text', transcribed_text)
            
            return {
                'success': True,
                'transcribed_text': transcribed_text,
                'audio_format': audio_format,
                'duration': asr_response.duration if hasattr(asr_response, 'duration') else None,
                'agent': self.name
            }
                
        except Exception as e:
            print(f"❌ {self.name}: ASR failed - {str(e)}")
            raise Exception(f"{self.name} execution failed: {str(e)}")
    
    async def generate_design_from_text(self, text: str) -> Dict[str, Any]:
        """
        Generate complete 3D house design from transcribed voice text.
        This makes VoiceAgent a complete standalone agent like GeneratorAgent.
        
        Returns same format as GeneratorAgent for consistency.
        """
        prompt = f"""you are an expert architectural designer and 3d modeling specialist.
        a user has described their house design verbally: "{text}"
        
        provide a detailed 3d design description with:
        
        1. detailed architectural analysis with:
           - overall architectural style and structure
           - dimensions and proportions (estimated)
           - key features (windows, doors, roof type, etc.)
           - suggested materials and textures
           - 3d modeling recommendations
        
        2. detailed image generation prompt (in a section called "image_prompt") that describes 
           a photorealistic 3d rendering of this house design. include:
           - architectural style
           - exterior materials and colors
           - roof style and material
           - window and door placement
           - landscaping elements
           - lighting and atmosphere
           - camera angle (front view, 3/4 view, etc.)
        
        format your response as json with these sections:
        - style: architectural style
        - structure: overall structure description
        - dimensions: estimated dimensions
        - features: list of identified features
        - materials: suggested materials
        - recommendations: 3d modeling and design recommendations
        - image_prompt: detailed prompt for generating a 3d rendering image
        """
        
        try:
            # Call Claude to analyze and structure the voice description
            ai_response = await self.call_llm(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2048
            )
            
            print(f"✨ {self.name}: generated design description from voice")
            
            # Parse response and generate image url (same as GeneratorAgent)
            import json
            import urllib.parse
            
            generated_image_url = None
            image_prompt = None
            
            try:
                # Clean markdown code blocks
                cleaned_response = ai_response.strip()
                if cleaned_response.startswith('```json'):
                    cleaned_response = cleaned_response[7:]
                if cleaned_response.startswith('```'):
                    cleaned_response = cleaned_response[3:]
                if cleaned_response.endswith('```'):
                    cleaned_response = cleaned_response[:-3]
                cleaned_response = cleaned_response.strip()
                
                response_json = json.loads(cleaned_response)
                image_prompt = response_json.get('image_prompt', '')
                    
            except json.JSONDecodeError as e:
                print(f"⚠️  {self.name}: response is not valid json: {e}")
                image_prompt = f"modern house design, {ai_response[:200]}"
            except Exception as e:
                print(f"⚠️  {self.name}: parsing error: {e}")
                image_prompt = "modern residential house, 3d architectural rendering"
            
            # Generate image URL (same method as GeneratorAgent)
            if image_prompt:
                full_prompt = f"photorealistic 3d architectural rendering, {image_prompt}, professional architecture visualization, high quality, detailed, 4k"
                encoded_prompt = urllib.parse.quote(full_prompt)
                generated_image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=768&model=flux&nologo=true&enhance=true"
                print(f"✅ {self.name}: generated image url")
            else:
                print(f"⚠️  {self.name}: no image prompt available")
            
            # Update context for other agents
            self.update_context('design_description', ai_response)
            self.update_context('generated_image_url', generated_image_url)
            
            return {
                'success': True,
                'design_description': ai_response,
                'generated_image_url': generated_image_url,
                'agent': self.name
            }
            
        except Exception as e:
            print(f"⚠️  {self.name}: failed to generate design: {str(e)}")
            raise Exception(f"{self.name} design generation failed: {str(e)}")
