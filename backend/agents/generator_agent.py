from .base_agent import BaseAgent
from typing import Dict, Any
import json
import urllib.parse

class GeneratorAgent(BaseAgent):
    """agent responsible for generating 3d house design from drawing"""
    
    def __init__(self):
        super().__init__(
            name="GeneratorAgent",
            description="analyzes house drawings and generates detailed 3d architectural designs"
        )
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        execute design generation
        input_data: {
            'image_base64': str (optional if text_description provided),
            'image_width': int,
            'image_height': int,
            'text_description': str (optional if image_base64 provided)
        }
        """
        image_base64 = input_data.get('image_base64')
        text_description = input_data.get('text_description')
        
        if not image_base64 and not text_description:
            raise ValueError("Either image_base64 or text_description is required")
        
        # create detailed prompt for architectural analysis
        prompt = """you are an expert architectural designer and 3d modeling specialist. 
        analyze this hand-drawn house sketch and provide a detailed 3d design description.
        
        provide two things:
        
        1. detailed architectural analysis with:
           - overall architectural style and structure
           - dimensions and proportions (estimated)
           - key features identified (windows, doors, roof type, etc.)
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
        
        # call anthropic api with vision or text
        try:
            # Build content based on input type
            if image_base64:
                # Image-based input (drawing mode)
                content = [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": image_base64,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            else:
                # Text-based input (voice mode)
                text_prompt = f"""you are an expert architectural designer and 3d modeling specialist.
                a user has described their house design: "{text_description}"
                
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
                content = [{"type": "text", "text": text_prompt}]
            
            message = self.anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2048,
                messages=[
                    {
                        "role": "user",
                        "content": content
                    }
                ],
            )
            
            ai_response = message.content[0].text
            
            # parse response and generate image url
            generated_image_url = None
            image_prompt = None
            
            try:
                # clean markdown code blocks
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
                # fallback: create a generic prompt from the text response
                image_prompt = f"modern house design based on architectural sketch, {ai_response[:200]}"
            except Exception as e:
                print(f"⚠️  {self.name}: parsing error: {e}")
                image_prompt = "modern residential house, 3d architectural rendering"
            
            # always generate an image url, even with fallback prompt
            if image_prompt:
                full_prompt = f"photorealistic 3d architectural rendering, {image_prompt}, professional architecture visualization, high quality, detailed, 4k"
                encoded_prompt = urllib.parse.quote(full_prompt)
                generated_image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=768&model=flux&nologo=true&enhance=true"
                print(f"✅ {self.name}: generated image url")
            else:
                print(f"⚠️  {self.name}: no image prompt available")
            
            # update context for other agents
            self.update_context('design_description', ai_response)
            self.update_context('generated_image_url', generated_image_url)
            
            return {
                'success': True,
                'design_description': ai_response,
                'generated_image_url': generated_image_url,
                'agent': self.name
            }
            
        except Exception as e:
            raise Exception(f"{self.name} execution failed: {str(e)}")
