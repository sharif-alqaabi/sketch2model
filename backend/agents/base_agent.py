from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import anthropic
import os

class BaseAgent(ABC):
    """base class for all agents in the system"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.context = {}
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """execute the agent's task"""
        pass
    
    def update_context(self, key: str, value: Any):
        """update agent context"""
        self.context[key] = value
    
    def get_context(self, key: str) -> Optional[Any]:
        """get value from context"""
        return self.context.get(key)
    
    async def call_llm(self, messages: list, max_tokens: int = 2048) -> str:
        """helper method to call anthropic api"""
        try:
            message = self.anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=max_tokens,
                messages=messages
            )
            return message.content[0].text
        except Exception as e:
            raise Exception(f"llm call failed: {str(e)}")
