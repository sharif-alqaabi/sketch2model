from .base_agent import BaseAgent
from typing import Dict, Any
import json
import os
import anthropic

class EstimatorAgent(BaseAgent):
    """agent responsible for estimating construction costs and materials"""
    
    def __init__(self):
        super().__init__(
            name="EstimatorAgent",
            description="estimates construction costs and required materials for house design"
        )
        self.anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute AI-powered cost estimation using Claude to analyze the house design
        and calculate realistic costs based on current market prices.
        
        input_data: {
            'image_base64': str,
            'design_description': str (from generator agent)
        }
        """
        print(f"💰 {self.name}: analyzing house design for cost estimation...")
        
        image_base64 = input_data.get('image_base64', '')
        design_description = input_data.get('design_description', '')
        
        # Create detailed prompt for cost estimation
        estimation_prompt = f"""You are a professional construction cost estimator. Analyze this house design and provide a detailed cost estimation.

DESIGN DESCRIPTION:
{design_description}

YOUR TASK:
1. Estimate the total square footage of the house based on the image and description
2. Calculate required materials with realistic quantities based on the estimated size
3. Use current 2024-2025 market prices for materials (US market average)
4. Provide itemized costs for each material

MATERIAL CATEGORIES TO ESTIMATE:
- Structural: Foundation (concrete), walls (bricks/blocks), cement, steel rebar, sand
- Finishing: Interior paint, exterior paint, flooring (tiles/wood), doors, door frames
- Roofing: Roofing tiles/shingles, timber trusses, waterproofing membrane
- Fixtures: Windows, electrical fixtures, plumbing fixtures

PRICING GUIDELINES (2024-2025 US Market):
- Concrete: $150-200 per cubic yard
- Bricks: $0.50-0.80 per brick
- Cement: $10-15 per 50kg bag
- Steel Rebar: $1,200-1,800 per ton
- Paint: $30-50 per gallon
- Floor Tiles: $25-40 per sq meter
- Roofing Tiles: $25-35 per sq meter
- Windows: $400-600 per standard unit
- Doors: $300-500 per unit
- Electrical: $40-60 per point
- Plumbing: $150-200 per fixture

IMPORTANT:
- Calculate quantities based on the ACTUAL estimated square footage
- Use realistic market prices from the ranges above
- Include labor costs (typically 30-40% of material costs)
- Be specific with quantities and units

OUTPUT FORMAT (JSON):
{{
    "total_area": "estimated square footage",
    "materials": {{
        "structural": [
            {{"material": "Material Name", "quantity": "X units", "cost": cost_in_dollars}}
        ],
        "finishing": [...],
        "roofing": [...],
        "fixtures": [...]
    }},
    "labor_cost": labor_cost_in_dollars,
    "notes": "Brief explanation of estimation methodology and assumptions"
}}

Provide ONLY the JSON output, no additional text."""

        try:
            # Call Claude API with vision
            print(f"💰 {self.name}: calling Claude API for cost analysis...")
            
            response = self.anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": [
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
                                "text": estimation_prompt
                            }
                        ],
                    }
                ],
            )
            
            # Extract the response
            ai_response_text = response.content[0].text
            print(f"💰 {self.name}: received cost estimation from Claude")
            
            # Parse JSON from response
            try:
                # Try to extract JSON from the response
                json_start = ai_response_text.find('{')
                json_end = ai_response_text.rfind('}') + 1
                
                if json_start != -1 and json_end > json_start:
                    json_str = ai_response_text[json_start:json_end]
                    estimation_data = json.loads(json_str)
                else:
                    raise ValueError("No JSON found in response")
                
            except (json.JSONDecodeError, ValueError) as e:
                print(f"⚠️ {self.name}: Failed to parse JSON, using fallback format")
                # Fallback: return the text response
                estimation_data = {
                    "total_area": "Estimated from design",
                    "materials": {},
                    "notes": ai_response_text
                }
            
            # Calculate total cost
            total_material_cost = 0
            materials_with_formatted_cost = {}
            
            if "materials" in estimation_data and isinstance(estimation_data["materials"], dict):
                for category, items in estimation_data["materials"].items():
                    materials_with_formatted_cost[category] = []
                    if isinstance(items, list):
                        for item in items:
                            cost = item.get("cost", 0)
                            total_material_cost += cost
                            materials_with_formatted_cost[category].append({
                                "material": item.get("material", "Unknown"),
                                "quantity": item.get("quantity", "N/A"),
                                "cost": f"${cost:,.2f}"
                            })
            
            # Add labor cost
            labor_cost = estimation_data.get("labor_cost", int(total_material_cost * 0.35))
            total_cost = total_material_cost + labor_cost
            
            formatted_total_cost = f"${total_cost:,.2f}"
            formatted_material_cost = f"${total_material_cost:,.2f}"
            formatted_labor_cost = f"${labor_cost:,.2f}"
            
            print(f"💰 {self.name}: Total cost calculated: {formatted_total_cost}")
            
            # Prepare response
            response_json = {
                "total_cost": formatted_total_cost,
                "material_cost": formatted_material_cost,
                "labor_cost": formatted_labor_cost,
                "total_area": estimation_data.get("total_area", "Estimated from design"),
                "materials": materials_with_formatted_cost,
                "notes": estimation_data.get("notes", "Cost estimation based on current market prices and house dimensions.")
            }
            
            summary = f"""Total Construction Cost Estimate: {formatted_total_cost}

Construction Area: {estimation_data.get('total_area', 'Estimated from design')}

Cost Breakdown:
- Materials: {formatted_material_cost}
- Labor: {formatted_labor_cost}
- Total: {formatted_total_cost}

This estimate is based on current 2024-2025 market prices and the analyzed house dimensions."""
            
            # Update context
            self.update_context('cost_estimation', summary)
            
            return {
                'success': True,
                'cost_estimation': summary,
                'cost_estimation_json': response_json,
                'agent': self.name
            }
            
        except Exception as e:
            print(f"❌ {self.name}: Error during cost estimation: {str(e)}")
            
            # Return error response
            return {
                'success': False,
                'cost_estimation': f"Error estimating costs: {str(e)}",
                'cost_estimation_json': {
                    "total_cost": "Error",
                    "materials": {},
                    "notes": f"Failed to estimate costs: {str(e)}"
                },
                'agent': self.name
            }
