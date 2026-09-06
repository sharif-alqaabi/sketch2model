from .base_agent import BaseAgent
from .generator_agent import GeneratorAgent
from .estimator_agent import EstimatorAgent
from .voice_agent import VoiceAgent
from typing import Dict, Any
from datetime import datetime

class RootAgent(BaseAgent):
    """root agent that orchestrates all other agents"""
    
    def __init__(self):
        super().__init__(
            name="RootAgent",
            description="orchestrates generator, estimator, and voice agents for complete house design workflow"
        )
        
        # initialize sub-agents
        self.generator_agent = GeneratorAgent()
        self.estimator_agent = EstimatorAgent()
        self.voice_agent = VoiceAgent()
        
        print(f"✅ {self.name}: initialized with sub-agents")
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        execute complete workflow
        input_data: {
            'image_base64': str,
            'image_width': int,
            'image_height': int
        }
        """
        print(f"🚀 {self.name}: starting workflow execution")
        
        workflow_results = {
            'success': True,
            'timestamp': datetime.utcnow().isoformat(),
            'workflow': []
        }
        
        try:
            # step 1: run generator agent
            print(f"📝 {self.name}: executing generator agent")
            generator_result = await self.generator_agent.execute(input_data)
            workflow_results['workflow'].append({
                'step': 1,
                'agent': 'GeneratorAgent',
                'status': 'completed',
                'result': generator_result
            })
            
            # step 2: run estimator agent with context from generator
            print(f"💰 {self.name}: executing estimator agent")
            estimator_input = {
                'image_base64': input_data.get('image_base64'),
                'design_description': generator_result.get('design_description', '')
            }
            estimator_result = await self.estimator_agent.execute(estimator_input)
            workflow_results['workflow'].append({
                'step': 2,
                'agent': 'EstimatorAgent',
                'status': 'completed',
                'result': estimator_result
            })
            
            # compile final results
            workflow_results['design'] = {
                'description': generator_result.get('design_description'),
                'generated_image_url': generator_result.get('generated_image_url')
            }
            
            workflow_results['estimation'] = {
                'cost_estimation': estimator_result.get('cost_estimation'),
                'cost_estimation_json': estimator_result.get('cost_estimation_json')
            }
            
            print(f"✅ {self.name}: workflow completed successfully")
            
            return workflow_results
            
        except Exception as e:
            print(f"❌ {self.name}: workflow failed - {str(e)}")
            workflow_results['success'] = False
            workflow_results['error'] = str(e)
            return workflow_results
