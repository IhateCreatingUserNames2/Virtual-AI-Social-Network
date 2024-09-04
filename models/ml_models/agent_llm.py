import os
import requests
from transformers import AutoModelForCausalLM, AutoTokenizer
from config.config import Config
import json

class AgentLLM:
    def __init__(self, model_name=None):
        self.model_name = model_name or Config.LLM_MODEL_NAME
        self.llm_provider = Config.LLM_PROVIDER

        if self.llm_provider == 'openai':
            self.api_key = Config.OPENAI_API_KEY
            self.api_url = f"https://api.openai.com/v1/engines/{self.model_name}/completions"
        elif self.llm_provider == 'ollama':
            self.api_url = Config.OLLAMA_API_URL
        elif self.llm_provider == 'llama':
            self.model_path = Config.LLAMA_MODEL_PATH
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_path)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.llm_provider}")

    def generate_response(self, prompt, personality, tuning=None):
        if tuning is None:
            tuning = {}

        # Ensure tuning is a dict and not a JSON string
        if isinstance(tuning, str):
            tuning = json.loads(tuning)
        elif isinstance(tuning, dict):
            pass  # Do nothing, it's already in the correct format
        else:
            raise ValueError(f"Unsupported tuning type: {type(tuning)}")

        prompt_with_tuning = self._apply_tuning_to_prompt(prompt, personality, tuning)

        if self.llm_provider == 'openai':
            return self._generate_with_openai(prompt_with_tuning)
        elif self.llm_provider == 'ollama':
            return self._generate_with_ollama(prompt_with_tuning)
        elif self.llm_provider == 'llama':
            return self._generate_with_llama(prompt_with_tuning)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.llm_provider}")

    def _apply_tuning_to_prompt(self, prompt, personality, tuning):
        modified_prompt = f"{personality}: {prompt}"
        if 'intro' in tuning:
            modified_prompt = f"{tuning['intro']} {modified_prompt}"
        if 'tone' in tuning:
            modified_prompt += f" {tuning['tone']}"
        return modified_prompt

    def _generate_with_openai(self, prompt):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'prompt': prompt,
            'max_tokens': 37,  # Adjusted to 1/4 of the original size
            'temperature': 0.7,
            'top_p': 1.0,
            'n': 1,
            'stop': None
        }
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            response_json = response.json()
            if 'choices' in response_json and len(response_json['choices']) > 0:
                return response_json['choices'][0]['text'].strip()
            else:
                return ""
        except requests.exceptions.RequestException as e:
            print(f"OpenAI API request error: {e}")
            return ""
        except ValueError as e:
            print(f"OpenAI API response error: {e}")
            return ""

    def _generate_with_ollama(self, prompt):
        data = {
            'model': 'llama3',
            'prompt': prompt,
            'max_length': 15,  # Adjusted to 1/4 of the original size
            'temperature': 0.7,
        }
        try:
            response = requests.post(f'{self.api_url}/api/generate', json=data)
            response.raise_for_status()
            response_text = ""
            response_lines = response.text.strip().split('\n')
            for line in response_lines:
                try:
                    response_json = json.loads(line)
                    if 'response' in response_json:
                        response_text += response_json['response']
                        if response_json.get('done'):
                            break
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
            return response_text.strip() if response_text else ""
        except requests.exceptions.RequestException as e:
            print(f"Ollama API request error: {e}")
            return ""
        except ValueError as e:
            print(f"Ollama API response error: {e}")
            return ""

    def _generate_with_llama(self, prompt):
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            outputs = self.model.generate(inputs['input_ids'], max_length=37)  # Adjusted to 1/4 of the original size
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            print(f"Llama model error: {e}")
            return ""
