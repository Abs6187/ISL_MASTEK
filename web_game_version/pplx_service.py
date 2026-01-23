import os
import requests
import json

class PPLXService:
    def __init__(self):
        self.api_key = os.environ.get('PERPLEXITY_API_KEY')
        self.api_url = "https://api.perplexity.ai/chat/completions"
        self.model = "sonar"
        self.cache = {}  # Simple in-memory cache

    def get_intelligent_response(self, word):
        """
        Fetches an intelligent response/hint for the given word using Perplexity API.
        Includes caching to reduce API calls.
        """
        if not self.api_key:
            return {"error": "API Key not configured."}
            
        # Check cache first
        word_lower = word.lower().strip()
        if word_lower in self.cache:
            print(f"PPLX: Serving '{word}' from cache.")
            return {"content": self.cache[word_lower]}

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant for a sign language game. Provide a very short, fun fact or hint (max 1 sentence) about the given word."
                },
                {
                    "role": "user", 
                    "content": f"Tell me about: {word}"
                }
            ],
            "max_tokens": 60  # Reduced tokens for speed/cost
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=5)
            
            if response.status_code == 429:
                return {"error": "Too many requests. Please wait a moment."}
                
            response.raise_for_status()
            data = response.json()
            
            if 'choices' in data and len(data['choices']) > 0:
                content = data['choices'][0]['message']['content']
                # Cache the successful response
                self.cache[word_lower] = content
                return {"content": content}
            else:
                return {"error": "No response from AI."}

        except requests.exceptions.Timeout:
            return {"error": "Request timed out."}
        except requests.exceptions.RequestException as e:
            print(f"PPLX API Error: {e}")
            return {"error": "Connection failed."}
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return {"error": "An unexpected error occurred."}
