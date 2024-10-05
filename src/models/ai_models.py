import google.generativeai as genai


class AIModel():
    def __init__(self, model_name: str, generation_config: dict, system_instruction: str):
        
        """Initialize the AI model with the specified parameters."""
        self.model = genai.GenerativeModel( 
            model_name=model_name ,
            generation_config=generation_config ,
            tools="code_execution",
            system_instruction=system_instruction
        )
        self.chat = self.model.start_chat(history=[]) #Initialsing chat for this model.
        
        
    def get_response(self,user_prompt: str) -> str:
        """Get a response from the ai model based on the user input  """
        return self.chat.send_message(user_prompt).text
    
