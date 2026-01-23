### Chat Completions API

Source: https://docs.perplexity.ai/guides/perplexity-sdk

Get started with AI responses using the Chat Completions API, which provides web-grounded knowledge, conversation context, and streaming support.

```APIDOC
## Chat Completions API

### Description
Provides AI-generated responses with web-grounded knowledge, conversation context, and streaming capabilities.

### Method
(Not specified in text, typically POST for completion APIs)

### Endpoint
(Not specified in text, typically a path like /chat/completions)

### Parameters
(Details not provided in the text)

### Request Example
(Not provided in the text)

### Response
#### Success Response (200)
(Details not provided in the text)

#### Response Example
(Not provided in the text)
```

--------------------------------

### Pro Search for Sonar Pro - Quickstart

Source: https://docs.perplexity.ai/guides/pro-search-quickstart

This section details how to get started with Pro Search for Sonar Pro, which enhances search with automated tools, multi-step reasoning, and real-time thought streaming. It requires setting `stream` to `true` and `search_type` to `pro`.

```APIDOC
## 
Pro Search for Sonar Pro

### Description
Pro Search enhances Sonar Pro with automated tool usage, enabling multi-step reasoning through intelligent tool orchestration including web search and URL content fetching. Pro Search only works when streaming is enabled. Non-streaming requests will fall back to standard Sonar Pro behavior.

### Method
POST

### Endpoint
`/chat/completions`

### Parameters
#### Query Parameters
None

#### Request Body
- **model** (string) - Required - The model to use, e.g., `"sonar-pro"`.
- **messages** (array) - Required - An array of message objects representing the conversation.
  - **role** (string) - Required - The role of the message (e.g., `"user"`, `"assistant"`).
  - **content** (string) - Required - The content of the message.
- **stream** (boolean) - Required - Set to `true` to enable streaming and Pro Search.
- **web_search_options** (object) - Required when `stream` is `true` and `search_type` is `pro`.
  - **search_type** (string) - Required - Must be set to `"pro"` to enable Pro Search.

### Request Example
```json
{
  "model": "sonar-pro",
  "messages": [
    {
      "role": "user",
      "content": "Analyze the latest developments in quantum computing and their potential impact on cryptography. Include recent research findings and expert opinions."
    }
  ],
  "stream": true,
  "web_search_options": {
    "search_type": "pro"
  }
}
```

### Response
#### Success Response (200)
- **id** (string) - Unique identifier for the response.
- **model** (string) - The model used for the response.
- **created** (integer) - Timestamp of when the response was created.
- **usage** (object) - Token usage information.
  - **prompt_tokens** (integer) - Number of tokens in the prompt.
  - **completion_tokens** (integer) - Number of tokens in the completion.
  - **total_tokens** (integer) - Total tokens used.
  - **search_context_size** (string) - Size of the search context (e.g., "low", "medium", "high").
  - **cost** (object) - Cost details.
    - **input_tokens_cost** (float) - Cost for input tokens.
    - **output_tokens_cost** (float) - Cost for output tokens.
    - **request_cost** (float) - Cost per request.
    - **total_cost** (float) - Total cost for the request.
- **search_results** (array) - List of search results obtained.
  - **title** (string) - Title of the search result.
  - **url** (string) - URL of the search result.
  - **date** (string) - Date associated with the search result.
  - **snippet** (string) - A short snippet from the search result.
  - **source** (string) - The source of the result (e.g., "web").
- **reasoning_steps** (array) - Steps taken by the model to arrive at the answer.
  - **thought** (string) - The model's thought process.
  - **type** (string) - The type of action taken (e.g., "web_search", "fetch_url_content").
  - **web_search** (object) - Details if the type is "web_search".
    - **search_keywords** (array) - Keywords used for the web search.
    - **search_results** (array) - Results from the web search.
  - **fetch_url_content** (object) - Details if the type is "fetch_url_content".
    - **contents** (array) - Content fetched from the URL.
- **object** (string) - The type of object, usually "chat.completion.chunk".
- **choices** (array) - Array of choices for the completion.
  - **index** (integer) - Index of the choice.
  - **delta** (object) - The delta content for the choice (used in streaming).
    - **role** (string) - Role of the assistant.
    - **content** (string) - The generated content chunk.

#### Response Example
```json
{
  "id": "2f16f4a0-e1d7-48c7-832f-8757b96ec221",
  "model": "sonar-pro",
  "created": 1759957470,
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 98,
    "total_tokens": 113,
    "search_context_size": "low",
    "cost": {
      "input_tokens_cost": 0.0,
      "output_tokens_cost": 0.001,
      "request_cost": 0.014,
      "total_cost": 0.015
    }
  },
  "search_results": [
    {
      "title": "Quantum Computing Breakthrough 2024",
      "url": "https://example.com/quantum-breakthrough",
      "date": "2024-03-15",
      "snippet": "Researchers at MIT have developed a new quantum error correction method...",
      "source": "web"
    }
  ],
  "reasoning_steps": [
    {
      "thought": "I need to search for recent quantum computing developments first.",
      "type": "web_search",
      "web_search": {
        "search_keywords": [
          "quantum computing developments 2024 cryptography impact",
          "post-quantum cryptography"
        ],
        "search_results": [
          {
            "title": "Quantum Computing Breakthrough 2024",
            "url": "https://example.com/quantum-breakthrough",
            "date": "2024-03-15",
            "last_updated": "2024-03-20",
            "snippet": "Researchers at MIT have developed a new quantum error correction method...",
            "source": "web"
          }
        ]
      }
    },
    {
      "thought": "Let me fetch detailed content from this research paper.",
      "type": "fetch_url_content",
      "fetch_url_content": {
        "contents": [
          {
            "title": "Quantum Error Correction Paper",
            "url": "https://arxiv.org/abs/2024.quantum",
            "date": null,
            "last_updated": null,
            "snippet": "Abstract: This paper presents a novel approach to quantum error correction...",
            "source": "web"
          }
        ]
      }
    }
  ],
  "object": "chat.completion.chunk",
  "choices": [
    {
      "index": 0,
      "delta": {
        "role": "assistant",
        "content": "## Latest Quantum Computing Developments\n\nBased on my re"
      }
    }
  ]
}
```
```

--------------------------------

### Start Perplexity MCP Server from Command Line (Shell)

Source: https://docs.perplexity.ai/guides/mcp-server

This command starts the Perplexity MCP server directly from the command line for any MCP-compatible client. It requires Node.js and npm to be installed. The API key must be set as an environment variable.

```shell
npx @perplexity-ai/mcp-server

# Set environment variable:
# PERPLEXITY_API_KEY=your_key_here
```

--------------------------------

### Install Perplexity MCP Server in Cursor/VS Code (Shell)

Source: https://docs.perplexity.ai/guides/mcp-server

These commands facilitate the one-click installation of the Perplexity MCP server in supported clients like Cursor and VS Code. It assumes a shell environment where marketplace commands are available. Ensure you have the necessary client and permissions for installation.

```shell
# Add the Perplexity marketplace
/plugin marketplace add perplexityai/modelcontextprotocol

# Install the plugin
/plugin install perplexity

# Set your API key
export PERPLEXITY_API_KEY="your_key_here"
```

--------------------------------

### Install Perplexity SDK for Python

Source: https://docs.perplexity.ai/guides/perplexity-sdk

Installs the official Perplexity SDK for Python using pip. This SDK provides type-safe and asynchronous access to Perplexity APIs.

```bash
pip install perplexityai
```

--------------------------------

### Install Perplexity SDK for TypeScript/JavaScript

Source: https://docs.perplexity.ai/guides/perplexity-sdk

Installs the official Perplexity SDK for TypeScript/JavaScript using npm. This SDK enables type-safe and asynchronous interaction with Perplexity APIs.

```bash
npm install perplexityai
```

--------------------------------

### Basic API Call and Response Handling

Source: https://docs.perplexity.ai/getting-started/quickstart

Illustrates a fundamental API call to Perplexity AI for text generation. This example focuses on making the request and retrieving a non-streaming response. Error handling and specific parameter configuration are key.

```python
import os
import requests

# Ensure you have your Perplexity API key set as an environment variable
API_KEY = os.environ.get("PERPLEXITY_API_KEY")
API_URL = "https://api.perplexity.ai/chat/completions"

def get_perplexity_response(prompt, model="llama-3-sonar-small", max_tokens=1000):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "Be a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": max_tokens
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        result = response.json()
        
        # Extracting the main content from the response
        if result and result.get("choices"):
            return result["choices"][0]["message"]["content"]
        else:
            return "No content found in the response."
            
    except requests.exceptions.RequestException as e:
        return f"API request failed: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Example usage:
# user_prompt = "Explain the significance of the 2025 French Open."
# response_text = get_perplexity_response(user_prompt)
# print(response_text)
```

--------------------------------

### Install and Run Briefo App

Source: https://docs.perplexity.ai/cookbook/showcase/briefo

Instructions to clone the Briefo repository, install dependencies, and run the Expo development server. Briefo is a personalized AI newsfeed and social discussion app powered by the Sonar API.

```bash
git clone https://github.com/adamblackman/briefo-public.git
cd briefo-public
npm install
```

```bash
npx expo start
```

--------------------------------

### Chat Completions API (Python SDK)

Source: https://docs.perplexity.ai/getting-started/quickstart

Demonstrates how to make a non-streaming and streaming chat completion request using the Perplexity Python SDK. It requires the Perplexity SDK to be installed and the API key to be set as an environment variable.

```APIDOC
## POST /chat/completions

### Description
This endpoint allows you to generate chat completions using Perplexity's language models. You can choose between non-streaming and streaming responses.

### Method
`POST`

### Endpoint
`https://api.perplexity.ai/chat/completions`

### Parameters
#### Query Parameters
None

#### Request Body
- **model** (string) - Required - The model to use for the chat completion (e.g., "sonar-pro").
- **messages** (array) - Required - An array of message objects, where each object has a `role` (`user` or `assistant`) and `content` (string).
- **stream** (boolean) - Optional - If set to `true`, the response will be streamed.

### Request Example (Non-streaming)
```python
from perplexity import Perplexity

client = Perplexity()
completion = client.chat.completions.create(
    model="sonar-pro",
    messages=[
        {"role": "user", "content": "What were the results of the 2025 French Open Finals?"}
    ]
)
print(completion.choices[0].message.content)
```

### Request Example (Streaming - conceptual, requires specific SDK handling)
```python
# Streaming response handling depends on the SDK implementation
# Example concept:
# stream = client.chat.completions.create(
#     model="sonar-pro",
#     messages=[
#         {"role": "user", "content": "What were the results of the 2025 French Open Finals?"}
#     ],
#     stream=True
# )
# for chunk in stream:
#     print(chunk.choices[0].delta.content)
```

### Response
#### Success Response (200)
- **choices** (array) - An array containing the completion choice(s).
  - **message** (object)
    - **role** (string) - The role of the message (e.g., "assistant").
    - **content** (string) - The generated content of the message.

#### Response Example (Non-streaming)
```json
{
  "id": "chatcmpl-xxxxxxxxxxxxxxxxxxxxxxxxx",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "sonar-pro",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "## 2025 French Open Finals Results\n**Men's Singles Final**\n- **Champion:** Carlos Alcaraz\n- **Runner-up:** Jannik Sinner\n- **Score:** 4–6, 6–7^(4–7), 6–4, 7–6^(7–3), 7–6^(10–2)\n- **Details:** Carlos Alcaraz successfully defended his title..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 500
  }
}
```
```

--------------------------------

### Streaming API Response Handling in Python

Source: https://docs.perplexity.ai/getting-started/quickstart

Demonstrates how to process streaming API responses using Python. This includes parsing the JSON content, handling potential errors, and managing citations. It's crucial for real-time applications.

```python
import json

def process_stream(response_stream):
    full_content = ""
    for chunk in response_stream:
        try:
            # Assuming each chunk is a JSON object or contains JSON
            # Real-world implementation might need more robust chunking and parsing
            content = chunk.decode('utf-8')
            # This is a simplified example, actual parsing depends on API response format
            # For Perplexity's streaming, you'd likely parse JSON objects within the stream
            if '"content"' in content:
                # Extracting content from a simplified JSON-like string
                start = content.find('"content":') + len('"content":')
                end = content.find(',', start)
                if end == -1: # Handle cases where it's the last field
                    end = content.find('}', start)
                
                json_part = content[start:end]
                # Basic cleaning for quotes and potential escape characters
                json_part = json_part.strip().strip('"')
                full_content += json_part.replace('\\n', '\n').replace('\\"', '"')

            # Process other fields like citations if needed
            # Example: extract citations here

        except json.JSONDecodeError:
            print(f"Warning: Could not decode JSON from chunk: {chunk}")
        except Exception as e:
            print(f"An error occurred: {e}")
    return full_content

# Example usage (assuming response_stream is an iterable of bytes chunks)
# response_stream = api_call_that_returns_stream()
# complete_text = process_stream(response_stream)
# print(complete_text)
```

--------------------------------

### TypeScript: Perplexity AI Search API Call Example

Source: https://docs.perplexity.ai/chat-summary-memory-buffer

Illustrates how to initiate a search using the Perplexity AI API with TypeScript. This example assumes a client setup and demonstrates sending a search query, which would typically return ranked web search results.

```typescript
import Perplexity from 'perplexity';

const client = new Perplexity({
  apiKey: 'YOUR_API_KEY',
});

async function performSearch() {
  const response = await client.search.create({
    query: 'Perplexity AI', 
  });
  console.log(response);
}
```

--------------------------------

### Chat Completions API (TypeScript SDK)

Source: https://docs.perplexity.ai/getting-started/quickstart

Demonstrates how to make a non-streaming and streaming chat completion request using the Perplexity TypeScript SDK. It requires the Perplexity SDK to be installed and the API key to be set as an environment variable.

```APIDOC
## POST /chat/completions

### Description
This endpoint allows you to generate chat completions using Perplexity's language models. You can choose between non-streaming and streaming responses.

### Method
`POST`

### Endpoint
`https://api.perplexity.ai/chat/completions`

### Parameters
#### Query Parameters
None

#### Request Body
- **model** (string) - Required - The model to use for the chat completion (e.g., "sonar-pro").
- **messages** (array) - Required - An array of message objects, where each object has a `role` (`user` or `assistant`) and `content` (string).
- **stream** (boolean) - Optional - If set to `true`, the response will be streamed.

### Request Example (Non-streaming)
```typescript
import Perplexity from '@perplexity-ai/perplexity_ai';

const client = new Perplexity();
const completion = await client.chat.completions.create({
    model: "sonar-pro",
    messages: [
        { role: "user", content: "What were the results of the 2025 French Open Finals?" }
    ]
});
console.log(completion.choices[0].message.content);
```

### Request Example (Streaming - conceptual, requires specific SDK handling)
```typescript
// Streaming response handling depends on the SDK implementation
// Example concept:
// const stream = await client.chat.completions.create({
//     model: "sonar-pro",
//     messages: [
//         { role: "user", content: "What were the results of the 2025 French Open Finals?" }
//     ],
//     stream: true
// });
// for await (const chunk of stream) {
//     console.log(chunk.choices[0].delta.content);
// }
```

### Response
#### Success Response (200)
- **choices** (array) - An array containing the completion choice(s).
  - **message** (object)
    - **role** (string) - The role of the message (e.g., "assistant").
    - **content** (string) - The generated content of the message.

#### Response Example (Non-streaming)
```json
{
  "id": "chatcmpl-xxxxxxxxxxxxxxxxxxxxxxxxx",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "sonar-pro",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "## 2025 French Open Finals Results\n**Men's Singles Final**\n- **Champion:** Carlos Alcaraz\n- **Runner-up:** Jannik Sinner\n- **Score:** 4–6, 6–7^(4–7), 6–4, 7–6^(7–3), 7–6^(10–2)\n- **Details:** Carlos Alcaraz successfully defended his title..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 500
  }
}
```
```

--------------------------------

### Authentication and Environment Variables

Source: https://docs.perplexity.ai/guides/perplexity-sdk

Instructions on how to obtain an API key and set it as an environment variable for authentication with the Perplexity SDKs.

```APIDOC
## Authentication and Environment Variables

### Description
Guides users on generating an API key from the Perplexity API Portal and configuring it as an environment variable for SDK authentication.

### Method
N/A

### Endpoint
N/A

### Parameters
#### Environment Variable
- **PERPLEXITY_API_KEY** (string) - Required - Your Perplexity API key.

### Request Example
(Authentication is typically handled by the SDK using the environment variable)

### Response
(N/A for authentication setup)

### Response Example
(N/A for authentication setup)
```

--------------------------------

### Models API

Source: https://docs.perplexity.ai/getting-started/quickstart

This section provides information about the various models available through the Perplexity AI API, including their capabilities and identifiers.

```APIDOC
## Models

### Description

Perplexity AI offers a range of models optimized for different tasks and performance characteristics. Understanding these models is crucial for selecting the most appropriate one for your specific application.

### Available Models

- **llama-3-sonar-small-32k-online**: A powerful model with a large context window, suitable for complex reasoning and tasks requiring access to up-to-date information via online search.
- **llama-3-sonar-large-32k-online**: An even larger and more capable version of the Sonar model, offering enhanced performance on demanding tasks.
- **mistral-large-latest**: A high-performance model from Mistral AI, known for its strong capabilities across various natural language understanding and generation tasks.
- **mistral-small-latest**: A more cost-effective and faster model from Mistral AI, suitable for less complex tasks.
- **opus-2024-04-07**: A leading model known for its advanced reasoning and generation abilities.
- **sonnet-2024-04-07**: A balanced model offering good performance and efficiency.
- **haiku-2024-04-07**: A fast and cost-effective model for simpler tasks.

### Usage

Models are specified using their unique identifiers in the `model` parameter of the Chat Completion API endpoint.
```

--------------------------------

### Initialize Perplexity Client with Environment Variable (Python)

Source: https://docs.perplexity.ai/guides/perplexity-sdk

Initializes the Perplexity client in Python. It automatically uses the PERPLEXITY_API_KEY environment variable for authentication.

```python
import os
from perplexity import Perplexity

client = Perplexity()
# Automatically uses PERPLEXITY_API_KEY
```

--------------------------------

### Python SDK Example

Source: https://docs.perplexity.ai/chat-with-persistence

Example of how to use the Perplexity AI Python SDK to perform a search.

```APIDOC
## Python SDK - Search Example

### Description
This code snippet demonstrates how to use the Perplexity AI Python SDK to perform a search and print the results.

### Language
Python

### Code
```python
from perplexity import Perplexity

client = Perplexity()

search = client.search.create(
  query=[
    "What is Comet Browser?",
    "Perplexity AI",
    "Perplexity Changelog"
  ]
)

for result in search.results:
  print(f"{result.title}: {result.url}")
```
```

--------------------------------

### Basic Usage Examples

Source: https://docs.perplexity.ai/guides/chat-completions-guide

Provides simple code examples in Python and TypeScript to help you make your first API calls to the Perplexity Sonar API using OpenAI's client libraries.

```APIDOC
## Examples with OpenAI’s client libraries

### Basic Usage

Start with these simple examples to make your first API calls:

#### Python Example
```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.perplexity.ai"
)

response = client.chat.completions.create(
    model="sonar-pro",
    messages=[
        {"role": "user", "content": "What are the latest developments in AI?"}
    ]
)

print(response.choices[0].message.content)
```

#### TypeScript Example
```typescript
import OpenAI from 'openai';

const client = new OpenAI({
    apiKey: "YOUR_API_KEY",
    baseURL: "https://api.perplexity.ai"
});

const response = await client.chat.completions.create({
    model: "sonar-pro",
    messages: [
        { role: "user", content: "What are the latest developments in AI?" }
    ]
});

console.log(response.choices[0].message.content);
```
```

--------------------------------

### Initialize Perplexity Client with Environment Variable (TypeScript/JavaScript)

Source: https://docs.perplexity.ai/guides/perplexity-sdk

Initializes the Perplexity client in TypeScript/JavaScript. The client automatically picks up the PERPLEXITY_API_KEY from environment variables for authentication.

```typescript
import os from 'perplexity'

const client = new Perplexity()
// Automatically uses PERPLEXITY_API_KEY
```

--------------------------------

### Load Environment Variable from .env file (Python)

Source: https://docs.perplexity.ai/guides/perplexity-sdk

Loads the PERPLEXITY_API_KEY from a .env file using python-dotenv and initializes the Perplexity client. This is useful for managing API keys in development.

```python
import os
from dotenv import load_dotenv
from perplexity import Perplexity

load_dotenv()
client = Perplexity()
# Uses PERPLEXITY_API_KEY from .env file
```

--------------------------------

### Setting Perplexity API Key (.env File)

Source: https://docs.perplexity.ai/cookbook/examples/README

Sets the Perplexity API key by creating a .env file within the example directory. This method is useful for managing environment-specific configurations.

```dotenv
PERPLEXITY_API_KEY=your-api-key-here
```

--------------------------------

### Python SDK Example

Source: https://docs.perplexity.ai/daily-knowledge-bot

Example usage of the Perplexity AI Python SDK for making search queries.

```APIDOC
## Perplexity Python SDK - Search Example

### Description
This code snippet demonstrates how to use the Perplexity AI Python SDK to perform a search query and print the results.

### Language
Python

### Code
```python
from perplexity import Perplexity

client = Perplexity()

search_results = client.search.create(
  query=[
    "What is Comet Browser?",
    "Perplexity AI",
    "Perplexity Changelog"
  ]
)

for result in search_results.results:
  print(f"{result.title}: {result.url}")
```
```

--------------------------------

### Search API

Source: https://docs.perplexity.ai/guides/perplexity-sdk

Utilize the Search API for ranked web search results with options for filtering, multi-query support, and domain controls.

```APIDOC
## Search API

### Description
Fetches ranked web search results, offering features for filtering, multi-query execution, and domain-specific searches.

### Method
(Not specified in text, typically GET or POST for search APIs)

### Endpoint
(Not specified in text, typically a path like /search)

### Parameters
(Details not provided in the text)

### Request Example
(Not provided in the text)

### Response
#### Success Response (200)
(Details not provided in the text)

#### Response Example
(Not provided in the text)
```

--------------------------------

### Unsupported JSON Schemas Example (Python)

Source: https://docs.perplexity.ai/guides/structured-outputs

Illustrates Python code snippets for JSON schemas that are not supported by Perplexity's structured output feature, specifically recursive schemas and unconstrained dictionaries.

```python
# UNSUPPORTED!
from typing import Any

class UnconstrainedDict(BaseModel):
    unconstrained: dict[str, Any]

class RecursiveJson(BaseModel):
    value: str
    child: list["RecursiveJson"]
```

--------------------------------

### Chat Completions API (cURL)

Source: https://docs.perplexity.ai/getting-started/quickstart

Demonstrates how to make a non-streaming chat completion request using cURL. This method requires setting the API key in the Authorization header and providing the request body as JSON.

```APIDOC
## POST /chat/completions

### Description
This endpoint allows you to generate chat completions using Perplexity's language models. This example shows how to use cURL for a non-streaming request.

### Method
`POST`

### Endpoint
`https://api.perplexity.ai/chat/completions`

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
- **model** (string) - Required - The model to use for the chat completion (e.g., "sonar-pro").
- **messages** (array) - Required - An array of message objects, where each object has a `role` (`user` or `assistant`) and `content` (string).

### Request Example
```bash
curl --location 'https://api.perplexity.ai/chat/completions' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--header "Authorization: Bearer $SONAR_API_KEY" \
--data '{ 
    "model": "sonar-pro", 
    "messages": [
        { "role": "user", "content": "What were the results of the 2025 French Open Finals?" }
    ]
}' | jq
```

### Response
#### Success Response (200)
- **choices** (array) - An array containing the completion choice(s).
  - **message** (object)
    - **role** (string) - The role of the message (e.g., "assistant").
    - **content** (string) - The generated content of the message.

#### Response Example
```json
{
  "id": "chatcmpl-xxxxxxxxxxxxxxxxxxxxxxxxx",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "sonar-pro",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "## 2025 French Open Finals Results\n**Men's Singles Final**\n- **Champion:** Carlos Alcaraz\n- **Runner-up:** Jannik Sinner\n- **Score:** 4–6, 6–7^(4–7), 6–4, 7–6^(7–3), 7–6^(10–2)\n- **Details:** Carlos Alcaraz successfully defended his title..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 500
  }
}
```
```

--------------------------------

### Set Perplexity API Key on Windows

Source: https://docs.perplexity.ai/guides/perplexity-sdk

Sets the Perplexity API key as an environment variable on a Windows system. This key is required for authenticating with the Perplexity API.

```bash
setx PERPLEXITY_API_KEY "your_api_key_here"
```

--------------------------------

### Perform Location-Aware Search with Country (US)

Source: https://docs.perplexity.ai/guides/user-location-filter-guide

This example demonstrates how to configure a web search to be specific to a country, using the United States as an example. It utilizes the `sonar-pro` model and specifies the user's country within the `web_search_options`.

```python
from perplexity import Perplexity

client = Perplexity()
completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are an expert on US news and events."}, 
        {"role": "user", "content": "What major events are happening in the US this week?"}
    ],
    model="sonar-pro",
    web_search_options={"user_location": { "country": "US" }}
)

print(f"Response: {completion.choices[0].message.content}")
```

--------------------------------

### Chat Completion API

Source: https://docs.perplexity.ai/getting-started/quickstart

This endpoint allows you to make chat completion requests to the Perplexity AI LLMs. You can specify the model, messages, and other parameters to get a conversational response. It also supports streaming responses for real-time updates.

```APIDOC
## POST /chat/completions

### Description

This endpoint facilitates chat-based interactions with Perplexity AI's language models. It allows users to send a series of messages and receive a coherent, contextually relevant response generated by the AI. The endpoint supports streaming for real-time delivery of responses.

### Method

POST

### Endpoint

/chat/completions

### Parameters

#### Request Body

- **model** (string) - Required - The ID of the model to use for generation. (e.g., "llama-3-sonar-small-32k-online", "mistral-large-latest")
- **messages** (array) - Required - A list of message objects, each with a `role` and `content`.
  - **role** (string) - Required - The role of the author of the message (e.g., "system", "user", "assistant").
  - **content** (string) - Required - The content of the message.
- **stream** (boolean) - Optional - Whether to stream back partial message deltas as they become available. Defaults to false.
- **max_tokens** (integer) - Optional - The maximum number of tokens to generate in the completion.
- **temperature** (number) - Optional - Controls randomness. Lower values make the output more focused and deterministic, while higher values increase randomness. Range is 0.0 to 2.0.
- **top_p** (number) - Optional - Controls nucleus sampling. An alternative to sampling with temperature, where the model considers the smallest set of tokens whose cumulative probability exceeds top_p. Range is 0.0 to 1.0.
- **stop** (array of strings) - Optional - Sequences where the API will stop generating further tokens.
- **presence_penalty** (number) - Optional - Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics. Range is -2.0 to 2.0.
- **frequency_penalty** (number) - Optional - Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim. Range is -2.0 to 2.0.
- **user** (string) - Optional - A unique identifier representing your end-user, which can help Perplexity to monitor and detect abuse.

### Request Example

```json
{
  "model": "llama-3-sonar-small-32k-online",
  "messages": [
    {"role": "user", "content": "What's the weather like today?"}
  ],
  "stream": false
}
```

### Response

#### Success Response (200)

- **id** (string) - A unique identifier for the completion.
- **object** (string) - The type of object returned, e.g., "chat.completion".
- **created** (integer) - Unix timestamp of when the completion was created.
- **model** (string) - The model used for the completion.
- **choices** (array) - A list of completion choices.
  - **index** (integer) - The index of the choice.
  - **message** (object) - The message content.
    - **role** (string) - The role of the author (e.g., "assistant").
    - **content** (string) - The generated message content.
  - **finish_reason** (string) - The reason the model stopped generating tokens (e.g., "stop", "length").
- **usage** (object) - Information on token usage.
  - **prompt_tokens** (integer) - Number of tokens in the prompt.
  - **completion_tokens** (integer) - Number of tokens in the completion.
  - **total_tokens** (integer) - Total tokens used.

#### Response Example (Non-streaming)

```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1700000000,
  "model": "llama-3-sonar-small-32k-online",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "The weather today is sunny with a high of 75 degrees Fahrenheit."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 15,
    "total_tokens": 25
  }
}
```

#### Response Example (Streaming)

```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion.chunk",
  "created": 1700000001,
  "model": "llama-3-sonar-small-32k-online",
  "choices": [
    {
      "index": 0,
      "delta": {
        "role": "assistant"
      },
      "finish_reason": null
    }
  ]
}
{
  "id": "chatcmpl-123",
  "object": "chat.completion.chunk",
  "created": 1700000002,
  "model": "llama-3-sonar-small-32k-online",
  "choices": [
    {
      "index": 0,
      "delta": {
        "content": "The weather"
      },
      "finish_reason": null
    }
  ]
}
{
  "id": "chatcmpl-123",
  "object": "chat.completion.chunk",
  "created": 1700000003,
  "model": "llama-3-sonar-small-32k-online",
  "choices": [
    {
      "index": 0,
      "delta": {
        "content": " today is sunny."
      },
      "finish_reason": null
    }
  ]
}
{
  "id": "chatcmpl-123",
  "object": "chat.completion.chunk",
  "created": 1700000004,
  "model": "llama-3-sonar-small-32k-online",
  "choices": [
    {
      "index": 0,
      "delta": {
        "content": ""
      },
      "finish_reason": "stop"
    }
  ]
}
```

### Error Handling

- **400 Bad Request**: Indicates invalid parameters in the request.
- **401 Unauthorized**: If API key is missing or invalid.
- **404 Not Found**: If the requested model does not exist.
- **500 Internal Server Error**: If there's an issue on the server side.
```

--------------------------------

### Load Environment Variable from .env file (TypeScript/JavaScript)

Source: https://docs.perplexity.ai/guides/perplexity-sdk

Loads the PERPLEXITY_API_KEY from a .env file using dotenv and initializes the Perplexity client. This simplifies API key management in Node.js projects.

```typescript
import 'dotenv/config'
import { Perplexity } from 'perplexity'

const client = new Perplexity()
// Uses PERPLEXITY_API_KEY from .env file
```

--------------------------------

### Financial News Tracker Example (Python)

Source: https://docs.perplexity.ai/cookbook/examples/README

A command-line tool for real-time financial news monitoring and market analysis. It aggregates news, analyzes market sentiment, and provides investment insights. Requires Python 3.7+ and a Perplexity API key.

```python
cd financial-news-tracker/
python financial_news_tracker.py "tech stocks"
```

--------------------------------

### TypeScript Search API Call Example

Source: https://docs.perplexity.ai/fact-checker-cli

This TypeScript snippet demonstrates how to use the Perplexity SDK to perform a search query and log the titles and URLs of the results. Ensure the Perplexity SDK is properly installed and configured in your TypeScript project.

```typescript
import { Perplexity } from 'perplexity';

const client = new Perplexity();

async function performSearch() {
  const search = await client.search.create({
    query: [
      "What is Comet Browser?",
      "Perplexity AI",
      "Perplexity Changelog"
    ]
  });
  search.results.forEach(result => {
    console.log(`${result.title}: ${result.url}`);
  });
}

performSearch();
```

--------------------------------

### Fact Checker CLI Example (Python)

Source: https://docs.perplexity.ai/cookbook/examples/README

A command-line tool to verify factual accuracy of claims and articles. It provides structured claim analysis, source citation, and JSON output for automation. Requires Python 3.7+ and a Perplexity API key.

```python
cd fact-checker-cli/
python fact_checker.py --text "The Earth is flat"
```

--------------------------------

### Daily Knowledge Bot Example (Python)

Source: https://docs.perplexity.ai/cookbook/examples/README

A scheduled Python application for automated daily fact delivery. Features topic rotation, persistent storage, configurable scheduling, and educational content generation. Requires Python 3.7+ and a Perplexity API key.

```python
cd daily-knowledge-bot/
python daily_knowledge_bot.py
```

--------------------------------

### TypeScript: Perplexity AI Search API Example

Source: https://docs.perplexity.ai/home

This TypeScript code snippet illustrates how to use the Perplexity AI Search API. It involves creating a client instance and initiating a search with a specified query. The results are then processed to display relevant information. This example assumes the existence of a Perplexity client library for TypeScript.

```typescript
import { Perplexity } from 'perplexity';

const client = new Perplexity({
  apiKey: 'YOUR_API_KEY',
});

async function performSearch() {
  try {
    const search = await client.search.create({
      query: [
        "Latest advancements in AI",
        "Perplexity AI features"
      ]
    });
    search.results.forEach(result => {
      console.log(`${result.title}: ${result.url}`);
    });
  } catch (error) {
    console.error('Error performing search:', error);
  }
}

performSearch();
```

--------------------------------

### Configure Perplexity MCP Server Manually (JSON)

Source: https://docs.perplexity.ai/guides/mcp-server

Manual configuration of the Perplexity MCP server for various clients using JSON. This method requires editing client-specific configuration files and setting the API key as an environment variable. It is suitable for users who prefer manual control over their setup.

```json
{
  "mcpServers": {
    "perplexity": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "perplexity-mcp"
      ],
      "env": {
        "PERPLEXITY_API_KEY": "your_key_here"
      }
    }
  }
}
```

```json
{
  "mcpServers": {
    "perplexity": {
      "command": "npx",
      "args": [
        "-y",
        "@perplexity-ai/mcp-server"
      ],
      "env": {
        "PERPLEXITY_API_KEY": "your_key_here"
      }
    }
  }
}
```

```json
{
  "mcpServers": {
    "perplexity": {
      "command": "npx",
      "args": [
        "-y",
        "@perplexity-ai/mcp-server"
      ],
      "env": {
        "PERPLEXITY_API_KEY": "your_key_here"
      }
    }
  }
}
```

--------------------------------

### Set Perplexity API Key on MacOS/Linux

Source: https://docs.perplexity.ai/guides/perplexity-sdk

Sets the Perplexity API key as an environment variable on MacOS or Linux. This environment variable is used for authenticating requests to the Perplexity API.

```bash
export PERPLEXITY_API_KEY="your_api_key_here"
```

--------------------------------

### Enable Automatic Query Classification in Python

Source: https://docs.perplexity.ai/guides/pro-search-quickstart

Demonstrates how to set `search_type` to 'auto' in the Python SDK to enable automatic query classification. The system intelligently routes queries based on complexity, optimizing performance and cost.

```python
from perplexity import Perplexity

client = Perplexity(api_key="YOUR_API_KEY")
response = client.chat.completions.create(
    model="sonar-pro",
    messages=[
        {
            "role": "user",
            "content": "Compare the energy efficiency of Tesla Model 3, Chevrolet Bolt, and Nissan Leaf"
        }
    ],
    stream=True,
    web_search_options={
        "search_type": "auto"  # Automatic classification
    }
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

--------------------------------

### Academic Research Finder Example (Python)

Source: https://docs.perplexity.ai/cookbook/examples/README

A command-line research tool for academic literature discovery and summarization. It prioritizes academic sources, extracts citations with DOI links, and supports scholarly workflows. Requires Python 3.7+ and a Perplexity API key.

```python
cd research-finder/
python research_finder.py "quantum computing advances"
```

--------------------------------

### Quick Start: Create Chat Completion (Python)

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Demonstrates how to initiate a chat completion request using the Perplexity Python SDK. It requires initializing the Perplexity client and calling the `chat.completions.create` method with user messages and a specified model.

```python
from perplexity import Perplexity

client = Perplexity()
completion = client.chat.completions.create(
  messages=[
    {
      "role": "user",
      "content": "Tell me about the latest developments in AI",
    }
  ],
  model="sonar",
)

print(f"Response: {completion.choices[0].message.content}")
```

--------------------------------

### Install Required Python Dependencies for Perplexity Integration

Source: https://docs.perplexity.ai/cookbook/articles/memory-management/chat-summary-memory-buffer/README

Lists the necessary Python packages to install for integrating LlamaIndex with the Perplexity API. These include core LlamaIndex libraries, the OpenAI LLM integration module, and the OpenAI client library itself. Ensure these are installed in your environment before running the application.

```bash
llama-index-core>=0.10.0
lama-index-llms-openai>=0.10.0
openai>=1.12.0
```

--------------------------------

### cURL: Example API Call

Source: https://docs.perplexity.ai/pricing

This example shows how to make a basic API call using cURL to interact with the Perplexity API. It demonstrates a POST request with a JSON payload containing a query. The output would be the API's response, typically in JSON format.

```bash
curl -X POST "https://api.perplexity.ai/chat/completions" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{ "model": "llama-3.8b-online", "messages": [{"role": "user", "content": "What is Perplexity AI?"}] }'
```

--------------------------------

### Extract Contact Information with Pydantic (Python)

Source: https://docs.perplexity.ai/guides/structured-outputs

Shows a Python example using Pydantic to define a `ContactInfo` schema for extracting email addresses. It requests contact information from the 'sonar' model and validates the output.

```python
from perplexity import Perplexity
from pydantic import BaseModel

class ContactInfo(BaseModel):
    email: str

client = Perplexity()
completion = client.chat.completions.create(
    model="sonar",
    messages=[
        {
            "role": "user",
            "content": "Find the direct email address for the investor relations contact at Tesla Inc."
        }
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "schema": ContactInfo.model_json_schema()
        }
    }
)

contact = ContactInfo.model_validate_json(completion.choices[0].message.content)
print(f"Investor Relations Email: {contact.email}")
```

--------------------------------

### Python SDK: Make Non-Streaming API Call

Source: https://docs.perplexity.ai/getting-started/quickstart

This Python snippet demonstrates how to initialize the Perplexity client and make a non-streaming chat completion request. It utilizes the PERPLEXITY_API_KEY environment variable for authentication. The output is the AI's response content.

```python
from perplexity import Perplexity

# Initialize the client (uses PERPLEXITY_API_KEY environment variable)
client = Perplexity()

# Make the API call
completion = client.chat.completions.create(
    model="sonar-pro",
    messages=[
        {"role": "user", "content": "What were the results of the 2025 French Open Finals?"}
    ]
)

# Print the AI's response
print(completion.choices[0].message.content)
```

--------------------------------

### Install Perplexity AI SDKs

Source: https://docs.perplexity.ai/changelog

Instructions for installing the official Perplexity AI SDKs for Python and TypeScript/JavaScript. These SDKs offer type-safe access to Perplexity APIs with support for synchronous and asynchronous operations.

```python
# Python
pip install perplexityai
```

```typescript
// TypeScript/JavaScript
npm install @perplexity-ai/perplexity_ai
```

--------------------------------

### Using City and Region for Better Accuracy

Source: https://docs.perplexity.ai/guides/user-location-filter-guide

This example demonstrates how to utilize `city` and `region` fields, along with coordinates, for Paris, France, to achieve optimal location accuracy in search queries.

```APIDOC
## POST /chat/completions

### Description
This endpoint allows for chat-based completions using the Perplexity AI API. It supports various models and can incorporate web search options, including detailed user location information, to tailor responses.

### Method
POST

### Endpoint
`/chat/completions`

### Parameters
#### Request Body
- **messages** (array) - Required - An array of message objects, each with a 'role' (system or user) and 'content'.
- **model** (string) - Required - The model to use for the completion (e.g., "sonar-pro").
- **web_search_options** (object) - Optional - Options for web search integration.
  - **user_location** (object) - Optional - Specifies the user's location for context-aware search.
    - **country** (string) - Required - The two-letter ISO 3166-1 alpha-2 country code (e.g., "US", "FR").
    - **region** (string) - Optional - The administrative region or state (e.g., "Île-de-France").
    - **city** (string) - Optional - The city name (e.g., "Paris").
    - **latitude** (number) - Optional - The geographical latitude (-90 to 90).
    - **longitude** (number) - Optional - The geographical longitude (-180 to 180).

### Request Example
```json
{
  "messages": [
    {"role": "system", "content": "You are an expert on French news and events."},
    {"role": "user", "content": "What major events are happening in the capital this week?"}
  ],
  "model": "sonar-pro",
  "web_search_options": {
    "user_location": {
      "country": "FR",
      "region": "Île-de-France",
      "city": "Paris",
      "latitude": 48.8566,
      "longitude": 2.3522
    }
  }
}
```

### Response
#### Success Response (200)
- **choices** (array) - Description of the completion choices.
  - **message** (object) - The message content from the AI.
    - **content** (string) - The generated text response.
```

--------------------------------

### Execute Python Script for Perplexity Integration Example

Source: https://docs.perplexity.ai/cookbook/articles/memory-management/chat-summary-memory-buffer/README

Provides the command to execute the Python script that demonstrates the usage of LlamaIndex's ChatSummaryMemoryBuffer with the Perplexity Sonar API. Ensure the script path 'scripts/example_usage.py' is correct relative to your project directory.

```bash
python3 scripts/example_usage.py
```

--------------------------------

### Specify User Location with City and Region (Python)

Source: https://docs.perplexity.ai/guides/user-location-filter-guide

This Python example demonstrates how to specify the 'user_location' using 'country', 'region', and 'city' for more precise geographic filtering. This is recommended when latitude and longitude are not available but city-level accuracy is desired.

```python
from perplexity import Perplexity
client = Perplexity()
completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a knowledgeable local historian."},
        {"role": "user", "content": "Tell me about historical landmarks in this area."}
    ],
    model="sonar-pro",
    web_search_options={
        "user_location": {
            "country": "US",
            "region": "New York",
            "city": "New York City"
        }
    }
)
print(f"Response: {completion.choices[0].message.content}")
```

--------------------------------

### Manually Specify Search Type as 'pro' or 'fast'

Source: https://docs.perplexity.ai/guides/pro-search-quickstart

Illustrates how to manually set the `search_type` parameter to either 'pro' or 'fast'. This is useful for specific scenarios where you know the query's complexity and want to ensure it's routed accordingly for cost or performance optimization.

```json
"search_type": "pro"  # Manually specify Pro Search for complex queries

```

```json
"search_type": "fast"  # Manually specify Fast Search for simple queries

```

--------------------------------

### Briefo Environment Variables Configuration

Source: https://docs.perplexity.ai/cookbook/showcase/briefo

Example environment variables required for the Briefo application, including Supabase credentials, Perplexity API key, and Alpaca API keys. These are typically stored in .env and .env.local files.

```dotenv
# .env (project root)
MY_SUPABASE_URL=https://.supabase.co
MY_SUPABASE_SERVICE_ROLE_KEY=...
PERPLEXITY_API_KEY=...
LINKPREVIEW_API_KEY=...
ALPACA_API_KEY=...
ALPACA_SECRET_KEY=...

# .env.local (inside supabase/)
# duplicate or override any secrets needed by Edge Functions
```

--------------------------------

### Disease Information App Example (Jupyter Notebook)

Source: https://docs.perplexity.ai/cookbook/examples/README

An interactive web application for medical information lookup. It offers a browser interface, structured medical knowledge cards, citation tracking, and standalone deployment. Requires a Perplexity API key.

```jupyter
cd disease-qa/
jupyter notebook disease_qa_tutorial.ipynb
```

--------------------------------

### Search API Playground

Source: https://docs.perplexity.ai/changelog

Test Perplexity AI's Search API queries and parameters in real time with this interactive playground. No API key is required to get started, allowing for easy experimentation with filtering options and response structures.

```APIDOC
## Interactive Search API Playground

### Description
Test Search API queries and parameters in real-time with our new Interactive Playground — no API key required to get started. Experiment with filtering options, see response structures, and refine your queries before implementing them in code.

### Method
GET (for playground interaction)

### Endpoint
`/search/interactive` (conceptual endpoint for the playground)

### Parameters
(Exploration within the playground, not direct API calls)

### Request Example
(N/A - Playground interface)

### Response
(Exploration within the playground, not direct API calls)

#### Success Response (200)
(Exploration within the playground, not direct API calls)
```

--------------------------------

### Setting Perplexity API Key (Command Line Argument)

Source: https://docs.perplexity.ai/cookbook/examples/README

Provides the Perplexity API key directly as a command-line argument when running a script. This is suitable for one-off executions or when environment variables are not feasible.

```python
python script.py --api-key your-api-key-here
```

--------------------------------

### Chat Completions API - Full Stream Mode

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

This example demonstrates how to use the Chat Completions API with `stream=True` and `stream_mode='full'`. The SDK handles the aggregation of chunks, and search results are printed if available.

```APIDOC
## POST /chat/completions (Streaming - Full Mode)

### Description
This endpoint allows for real-time, streamed responses from the chat model. In 'full' mode, the SDK aggregates the streamed chunks, and you receive the complete response content as it's generated. Search results, if any, can be accessed within the chunks.

### Method
POST

### Endpoint
/chat/completions

### Parameters
#### Query Parameters
- **stream** (boolean) - Required - Set to `true` to enable streaming.
- **stream_mode** (string) - Optional - Defaults to "full". Use "full" for SDK-managed aggregation.

#### Request Body
- **model** (string) - Required - The model to use (e.g., "sonar-pro").
- **messages** (array of objects) - Required - The conversation history.
  - **role** (string) - User or Assistant.
  - **content** (string) - The message content.
- **stream** (boolean) - Required - Set to `true` to enable streaming.

### Request Example
```json
{
  "model": "sonar-pro",
  "messages": [
    {"role": "user", "content": "What's the weather?"}
  ],
  "stream": true,
  "stream_mode": "full"
}
```

### Response
#### Success Response (200)
- **choices** (array of objects) - Contains the streamed content chunks.
  - **delta** (object)
    - **content** (string) - The text content of the chunk.
- **search_results** (array) - Information about search results, may appear in multiple chunks.

#### Response Example
```json
{
  "choices": [
    {
      "delta": {
        "content": "The weather is sunny."
      }
    }
  ],
  "search_results": [
    {
      "title": "Weather Report",
      "url": "https://example.com/weather"
    }
  ]
}
```
```

--------------------------------

### Quick Start: Create Chat Completion (TypeScript)

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Illustrates how to make a chat completion request using the Perplexity TypeScript SDK. This involves importing the `Perplexity` class, creating a client instance, and using the `chat.completions.create` method with messages and a model.

```typescript
import Perplexity from '@perplexity-ai/perplexity_ai';

const client = new Perplexity();
const completion = await client.chat.completions.create({
  messages: [
    {
      role: "user",
      content: "Tell me about the latest developments in AI",
    }
  ],
  model: "sonar",
});

console.log(`Response: ${completion.choices[0].message.content}`);
```

--------------------------------

### Search SEC Filings with cURL

Source: https://docs.perplexity.ai/changelog/changelog

This example demonstrates how to use the cURL command to make a POST request to the Perplexity AI chat completions endpoint, specifically filtering results to include only SEC regulatory documents by setting `search_domain` to 'sec'.

```bash
curl --request POST \
  --url https://api.perplexity.ai/chat/completions \
  --header 'accept: application/json' \
  --header 'authorization: Bearer YOUR_API_KEY' \
  --header 'content-type: application/json' \
  --data '{ "model": "sonar-pro", "messages": [{"role": "user", "content": "What was Apple\'s revenue growth in their latest quarterly report?"}], "stream": false, "search_domain": "sec", "web_search_options": {"search_context_size": "medium"} }' | jq
```

--------------------------------

### Specify User Location with Latitude and Longitude (Python)

Source: https://docs.perplexity.ai/guides/user-location-filter-guide

This Python example shows how to use 'latitude' and 'longitude' along with the 'country' code to specify a precise geographic point for refining search results. This method provides high accuracy when coordinates are known.

```python
from perplexity import Perplexity
client = Perplexity()
completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a weather expert."},
        {"role": "user", "content": "What's the weather like right now?"}
    ],
    model="sonar-pro",
    web_search_options={
        "user_location": {
            "country":"US",
            "latitude": 37.7749,
            "longitude": -122.4194
        }
    }
)
print(f"Response: {completion.choices[0].message.content}")
```

--------------------------------

### Perform Location-Aware Search with City and Region (Paris, France)

Source: https://docs.perplexity.ai/guides/user-location-filter-guide

This example shows how to achieve maximum location accuracy by specifying country, region, city, and coordinates for Paris, France. It uses the `sonar-pro` model and provides detailed location information within `web_search_options`.

```python
from perplexity import Perplexity

client = Perplexity()
completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are an expert on French news and events."},
        {"role": "user", "content": "What major events are happening in the capital this week?"}
    ],
    model="sonar-pro",
    web_search_options= {
        "user_location": {
            "country": "FR",
            "region": "Île-de-France",
            "city": "Paris",
            "latitude": 48.8566,
            "longitude": 2.3522
        }
    }
)

print(f"Response: {completion.choices[0].message.content}")
```

--------------------------------

### TypeScript SDK: Make Non-Streaming API Call

Source: https://docs.perplexity.ai/getting-started/quickstart

This TypeScript snippet shows how to initialize the Perplexity client and make a non-streaming chat completion request. It relies on the PERPLEXITY_API_KEY environment variable for authentication. The resulting AI response content is then logged to the console.

```typescript
import Perplexity from '@perplexity/perplexity_ai';

// Initialize the client (uses PERPLEXITY_API_KEY environment variable)
const client = new Perplexity();

// Make the API call
const completion = await client.chat.completions.create({
    model: "sonar-pro",
    messages: [
        { role: "user", content: "What were the results of the 2025 French Open Finals?" }
    ]
});

// Print the AI's response
console.log(completion.choices[0].message.content);
```

--------------------------------

### Basic SEC Filings Search using Python

Source: https://docs.perplexity.ai/guides/sec-guide

Perform a basic search targeting U.S. Securities and Exchange Commission (SEC) filings. This example uses Python to send a POST request to the Perplexity API with the 'sec' search mode enabled.

```python
import os
import requests

url = "https://api.perplexity.ai/chat/completions"

payload = {
    "model": "sonar-pro",
    "messages": [
        {
            "role": "user",
            "content": "Prepare me for markets opening."
        }
    ],
    "search_mode": "sec"
}

headers = {
    "accept": "application/json",
    "authorization": f"Bearer {os.environ.get('SONAR_API_KEY')}",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())
```

--------------------------------

### Basic SEC Filings Search using Node.js

Source: https://docs.perplexity.ai/guides/sec-guide

Perform a basic search targeting U.S. Securities and Exchange Commission (SEC) filings. This example uses Node.js to send a POST request to the Perplexity API with the 'sec' search mode enabled.

```javascript
import fetch from 'node-fetch';

const url = 'https://api.perplexity.ai/chat/completions';

const payload = {
    "model": "sonar-pro",
    "messages": [
        {
            "role": "user",
            "content": "Prepare me for markets opening."
        }
    ],
    "search_mode": "sec"
};

const headers = {
    "accept": "application/json",
    "authorization": `Bearer ${process.env.SONAR_API_KEY}`,
    "content-type": "application/json"
};

fetch(url, {
    method: 'POST',
    headers: headers,
    body: JSON.stringify(payload)
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error(error));
```

--------------------------------

### Combining SEC Mode with Other Parameters using Python

Source: https://docs.perplexity.ai/guides/sec-guide

Refine searches by combining the SEC filter with other parameters like date filters. This Python example demonstrates setting 'search_mode: "sec"' along with 'search_after_date_filter'.

```python
import os
import requests

url = "https://api.perplexity.ai/chat/completions"

payload = {
    "model": "sonar",
    "messages": [
        {
            "role": "user",
            "content": "Summarize the latest 10-K filings for Apple Inc."
        }
    ],
    "stream": False,
    "search_mode": "sec",
    "search_after_date_filter": "1/1/2023"
}

headers = {
    "accept": "application/json",
    "authorization": f"Bearer {os.environ.get('SONAR_API_KEY')}",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())
```

--------------------------------

### Basic Academic Search with Perplexity AI SDK (Python)

Source: https://docs.perplexity.ai/guides/academic-filter-guide

Demonstrates a basic search using the Perplexity AI Python SDK with the 'academic' search mode enabled. It sets the search context size to 'low' for potentially faster results. This function requires the 'perplexity' library to be installed.

```python
from perplexity import Perplexity

client = Perplexity()
completion = client.chat.completions.create(
    model="sonar-pro",
    messages=[
        {"role": "user", "content": "What is the scientific name of the lions mane mushroom?"}
    ],
    search_mode="academic",
    web_search_options={"search_context_size": "low"}
)

print(completion.choices[0].message.content)
```

--------------------------------

### Filter by Recency (TypeScript)

Source: https://docs.perplexity.ai/guides/search-date-time-filters

This TypeScript code snippet shows how to filter search results by recency, for example, to get content from the past 'month', using the `search_recency_filter` parameter.

```TypeScript
import Perplexity from 'perplexity-node';

const client = new Perplexity('YOUR_API_KEY');

async function search() {
  const response = await client.search({
    query: 'example query',
    search_recency_filter: 'month'
  });
  console.log(response);
}

search();
```

--------------------------------

### Enable Pro Search with Streaming (Python SDK)

Source: https://docs.perplexity.ai/guides/pro-search-quickstart

This Python code snippet demonstrates how to enable Pro Search for Sonar Pro by setting `stream` to `true` and specifying `search_type` as 'pro' within the `web_search_options`. It sends a user query and iterates through the streaming response.

```python
from perplexity import Perplexity
client = Perplexity(api_key="YOUR_API_KEY")
messages = [
  {
    "role": "user",
    "content": "Analyze the latest developments in quantum computing and their potential impact on cryptography. Include recent research findings and expert opinions."
  }
]
response = client.chat.completions.create(
  model="sonar-pro",
  messages=messages,
  stream=True,
  web_search_options={
    "search_type": "pro"
  }
)

for chunk in response:
  if chunk.choices[0].delta.content:
    print(chunk.choices[0].delta.content, end="")
```

--------------------------------

### Combining SEC Mode with Other Parameters using TypeScript

Source: https://docs.perplexity.ai/guides/sec-guide

Refine searches by combining the SEC filter with other parameters like date filters. This TypeScript example demonstrates setting 'search_mode: "sec"' along with 'search_after_date_filter'.

```typescript
import fetch from 'node-fetch';

const url = 'https://api.perplexity.ai/chat/completions';

const payload = {
    "model": "sonar",
    "messages": [
        {
            "role": "user",
            "content": "Summarize the latest 10-K filings for Apple Inc."
        }
    ],
    "stream": false,
    "search_mode": "sec",
    "search_after_date_filter": "1/1/2023"
};

const headers = {
    "accept": "application/json",
    "authorization": `Bearer ${process.env.SONAR_API_KEY}`,
    "content-type": "application/json"
};

fetch(url, {
    method: 'POST',
    headers: headers,
    body: JSON.stringify(payload)
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error(error));
```

--------------------------------

### Search Academic Sources with cURL

Source: https://docs.perplexity.ai/changelog/changelog

This example illustrates how to use cURL to send a request to the Perplexity AI API, specifically targeting academic and scholarly sources by setting `search_mode` to 'academic'. This is useful for research requiring peer-reviewed content.

```bash
curl --request POST \
  --url https://api.perplexity.ai/chat/completions \
  --header 'accept: application/json' \
  --header 'authorization: Bearer YOUR_API_KEY' \
  --header 'content-type: application/json' \
  --data '{ "model": "sonar-pro", "messages": [{"role": "user", "content": "What is the scientific name of the lions mane mushroom?"}], "stream": false, "search_mode": "academic", "web_search_options": {"search_context_size": "low"} }'
```

--------------------------------

### Perplexity API: Top-Level Domain (TLD) Filtering Example (JSON)

Source: https://docs.perplexity.ai/guides/search-domain-filter-guide

Demonstrates top-level domain (TLD) filtering using the search_domain_filter parameter. This example filters for all .gov domains, effectively targeting government websites. TLD filtering is useful for categorizing sites by organization type or country.

```json
"search_domain_filter": [".gov"]
```

--------------------------------

### cURL: Perplexity AI Search API Call Example

Source: https://docs.perplexity.ai/chat-summary-memory-buffer

Provides an example of how to make a search request to the Perplexity AI API using cURL. This snippet shows the basic structure of the request, including the endpoint and query parameters, to retrieve ranked web search results.

```bash
curl -X POST "https://api.perplexity.ai/chat/completions" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{ \
    "model": "llama-3-sonar-small", \
    "messages": [ \
      {"role": "user", "content": "Search: What is Comet Browser?"} \
    ] \
  }'
```

--------------------------------

### TypeScript: Basic Search Query with Perplexity SDK

Source: https://docs.perplexity.ai/

This TypeScript snippet illustrates how to perform a search query using the Perplexity SDK. It requires the Perplexity SDK to be installed and configured. The code initializes the client, sends a search request with a defined query, and processes the results by logging the title and URL.

```typescript
import Perplexity from 'perplexity';

const client = new Perplexity();

async function performSearch() {
  const searchResults = await client.search.create({
    query: [
      "What is Comet Browser?",
      "Perplexity AI",
      "Perplexity Changelog"
    ]
  });

  searchResults.results.forEach(result => {
    console.log(`${result.title}: ${result.url}`);
  });
}

performSearch();
```

--------------------------------

### Specify User Location with All Fields (Python)

Source: https://docs.perplexity.ai/guides/user-location-filter-guide

This Python example demonstrates how to set the 'user_location' parameter with all available fields (country, region, city, latitude, longitude) to refine search results for a specific geographic area. It utilizes the Perplexity SDK to create a chat completion.

```python
from perplexity import Perplexity
client = Perplexity()
completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a helpful local guide."},
        {"role": "user", "content": "What are some good coffee shops nearby?"}
    ],
    model="sonar-pro",
    web_search_options={
        "user_location": {
            "country": "US",
            "region": "California",
            "city": "San Francisco",
            "latitude": 37.7749,
            "longitude": -122.4194
        }
    }
)
print(f"Response: {completion.choices[0].message.content}")
```

--------------------------------

### Enable Pro Search with Streaming (TypeScript SDK)

Source: https://docs.perplexity.ai/guides/pro-search-quickstart

This TypeScript code snippet shows how to activate Pro Search for Sonar Pro by setting `stream` to `true` and `search_type` to 'pro' in the `webSearchOptions`. It sends a user query and processes the streaming results.

```typescript
import Perplexity from "@perplexity/perplexity-node";

const perplexity = new Perplexity("YOUR_API_KEY");

async function main() {
  const response = await perplexity.chat.completions.create({
    model: "sonar-pro",
    messages: [
      {
        role: "user",
        content: "Analyze the latest developments in quantum computing and their potential impact on cryptography. Include recent research findings and expert opinions.",
      },
    ],
    stream: true,
    webSearchOptions: {
      searchType: "pro",
    },
  });

  for await (const chunk of response) {
    if (chunk.choices[0]?.delta?.content) {
      process.stdout.write(chunk.choices[0].delta.content);
    }
  }
}

main();
```

--------------------------------

### Perplexity AI Search API Response Example

Source: https://docs.perplexity.ai/api-reference/search-post

Example JSON response structure for a successful search query to the Perplexity AI API. It shows the format of the returned results, including title, URL, snippet, and dates.

```json
{
  "results": [
    {
      "title": "",
      "url": "",
      "snippet": "",
      "date": "2025-03-20",
      "last_updated": "2025-09-19"
    }
  ]
}
```

--------------------------------

### Combining SEC Mode with Other Parameters using cURL

Source: https://docs.perplexity.ai/guides/sec-guide

Refine searches by combining the SEC filter with other parameters like date filters. This cURL example demonstrates setting 'search_mode: "sec"' along with 'search_after_date_filter'.

```shell
curl --request POST \
  --url https://api.perplexity.ai/chat/completions \
  --header "accept: application/json" \
  --header "authorization: Bearer $SONAR_API_KEY" \
  --header "content-type: application/json" \
  --data '{ "model": "sonar", "messages": [{"role": "user", "content": "Summarize the latest 10-K filings for Apple Inc."}] "stream": false "search_mode": "sec" "search_after_date_filter": "1/1/2023" }' | jq
```

--------------------------------

### Setting Perplexity API Key (Environment Variable)

Source: https://docs.perplexity.ai/cookbook/examples/README

Configures the Perplexity API key using an environment variable, which is the recommended method for security and ease of use across different environments.

```bash
export PPLX_API_KEY="your-api-key-here"
```

--------------------------------

### Perplexity API Key Environment Variable Setup

Source: https://docs.perplexity.ai/cookbook/articles/memory-management/chat-summary-memory-buffer/README

Sets the Perplexity API key as an environment variable. This is a standard security practice for managing API credentials, ensuring that sensitive information is not hardcoded directly into the script. Replace 'your_pplx_key_here' with your actual Perplexity API key.

```bash
export PERPLEXITY_API_KEY="your_pplx_key_here"
```

--------------------------------

### Content Localization Research Example (Python)

Source: https://docs.perplexity.ai/guides/search-language-filter

This Python snippet illustrates how to find product reviews or relevant content in specific target languages for localization projects. It demonstrates filtering by language and recency for a given search query.

```python
# Find product reviews in target markets
target_languages = ["ja", "ko", "zh"]  # Asian markets

# Assuming 'client' is an initialized Perplexity client object
# response = client.search.create(
#     query="smartphone reviews 2024",
#     max_results=15,
#     search_language_filter=target_languages,
#     search_recency_filter="month"
# )

```

--------------------------------

### Chat Completions API - Concise Stream Mode

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

This example demonstrates using the Chat Completions API with `stream=True` and `stream_mode='concise'`. This mode provides more granular control, separating reasoning steps, search results, and content chunks, optimizing for bandwidth and transparency.

```APIDOC
## POST /chat/completions (Streaming - Concise Mode)

### Description
This endpoint utilizes the 'concise' streaming mode for the Chat Completions API. It breaks down the response into distinct types of chunks: reasoning steps, search results, and content. This mode is ideal for bandwidth optimization, real-time chat interfaces requiring reasoning transparency, and cost-sensitive applications.

### Method
POST

### Endpoint
/chat/completions

### Parameters
#### Query Parameters
- **stream** (boolean) - Required - Set to `true` to enable streaming.
- **stream_mode** (string) - Optional - Set to "concise" for granular chunking.

#### Request Body
- **model** (string) - Required - The model to use (e.g., "sonar-pro").
- **messages** (array of objects) - Required - The conversation history.
  - **role** (string) - User or Assistant.
  - **content** (string) - The message content.
- **stream** (boolean) - Required - Set to `true` to enable streaming.

### Request Example
```json
{
  "model": "sonar-pro",
  "messages": [
    {"role": "user", "content": "What's the weather?"
  ],
  "stream": true,
  "stream_mode": "concise"
}
```

### Response
#### Success Response (200)
- **object** (string) - Type of chunk received (e.g., `"chat.reasoning"`, `"chat.search_results"`, `"chat.completion.chunk"`, `"chat.completion.done"`).
- **choices** (array of objects) - Contains response details based on the chunk object.
  - **delta** (object) - May contain `content` for completion chunks or `reasoning_steps`.
- **search_results** (array) - Information about search results, available for `"chat.reasoning.done"` object type.
- **usage** (object) - Metadata for the final chunk (`"chat.completion.done"`), including `total_tokens`.

#### Response Example (Reasoning Step)
```json
{
  "object": "chat.reasoning",
  "choices": [
    {
      "delta": {
        "reasoning_steps": "Thinking about how to answer the weather question..."
      }
    }
  ]
}
```

#### Response Example (Search Results Available)
```json
{
  "object": "chat.reasoning.done",
  "search_results": [
    {
      "title": "Weather Forecast",
      "url": "https://example.com/forecast"
    }
  ]
}
```

#### Response Example (Content Chunk)
```json
{
  "object": "chat.completion.chunk",
  "choices": [
    {
      "delta": {
        "content": "The weather today is expected to be..."
      }
    }
  ]
}
```

#### Response Example (Completion Done)
```json
{
  "object": "chat.completion.done",
  "usage": {
    "total_tokens": 150
  }
}
```
```

--------------------------------

### Model Selection for Chat Completions (Python & TypeScript)

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Illustrates how to select the appropriate Perplexity AI model based on the task requirements, using examples for Python and TypeScript. It highlights `sonar` for general queries, `sonar-pro` for complex analysis, and `sonar-reasoning-pro` for analytical tasks.

```python
# For quick factual queries
simple_query = client.chat.completions.create(
    messages=[{"role": "user", "content": "What is the capital of France?"}],
    model="sonar"
)

# For complex analysis
complex_query = client.chat.completions.create(
    messages=[{"role": "user", "content": "Analyze the economic impact of AI on employment"}],
    model="sonar-pro"
)
```

```javascript
// For quick factual queries
const simpleQuery = await client.chat.completions.create({
    messages: [{ role: "user", content: "What is the capital of France?" }],
    model: "sonar"
});

// For complex analysis
const complex
```

--------------------------------

### Robust Streaming with Retries

Source: https://docs.perplexity.ai/guides/streaming-responses

This example demonstrates how to implement robust streaming by handling network interruptions and implementing retry logic for increased reliability.

```APIDOC
## POST /chat/completions (Robust Streaming)

### Description
This endpoint provides a mechanism to handle potential network errors during streaming by implementing a retry strategy. It automatically retries the request upon encountering specific API connection or timeout errors, with a configurable number of retries.

### Method
POST

### Endpoint
/chat/completions

### Parameters
#### Query Parameters
- **query** (string) - Required - The user's query to the language model.
- **max_retries** (integer) - Optional - The maximum number of times to retry the request in case of connection errors. Defaults to 3.

### Request Example
```json
{
  "model": "sonar",
  "messages": [{"role": "user", "content": "Explain quantum computing"}],
  "stream": true
}
```

### Response
#### Success Response (200)
- The streamed content is printed directly to the console.

#### Response Example
(Output is streamed to console, no JSON response body for success)

#### Error Handling
- **APIConnectionError**, **APITimeoutError**: These errors trigger the retry mechanism. If all retries fail, the last error is re-raised.
- **Other Errors**: Other types of errors will be immediately re-raised without retrying.
```

--------------------------------

### Perplexity API: Search Domain Filter Examples (Python, TypeScript, cURL)

Source: https://docs.perplexity.ai/guides/search-domain-filter-guide

Demonstrates how to use the search_domain_filter parameter in the Perplexity API to limit search results to specific domains. This example shows allowlist mode, where only the specified domains are included. The filter accepts an array of domain strings, and domains should be provided without the protocol.

```python
from perplexity import Perplexity

client = Perplexity()
response = client.search.create(
    query="climate change research",
    max_results=10,
    search_domain_filter=[
        "nature.com",
        "science.org",
        "cell.com"
    ]
)

for result in response.results:
    print(f"{result.title}: {result.url}")
```

```typescript
import Perplexity from '@perplexity/perplexity';

const client = new Perplexity();

async function search() {
  const response = await client.search.create({
    query: 'climate change research',
    max_results: 10,
    search_domain_filter: [
      'nature.com',
      'science.org',
      'cell.com'
    ]
  });

  response.results.forEach(result => {
    console.log(`${result.title}: ${result.url}`);
  });
}
```

```curl
curl -X POST "https://api.perplexity.ai/search/create" \
-H "Authorization: Bearer YOUR_API_KEY" \
-H "Content-Type: application/json" \
-d '{
  "query": "climate change research",
  "max_results": 10,
  "search_domain_filter": [
    "nature.com",
    "science.org",
    "cell.com"
  ]
}'
```

--------------------------------

### Enable Pro Search with Streaming (cURL)

Source: https://docs.perplexity.ai/guides/pro-search-quickstart

This cURL command illustrates how to enable Pro Search for Sonar Pro by including `"stream": true` and `"search_type": "pro"` within the JSON payload. It sends a user query to the API.

```bash
curl "https://api.perplexity.ai/chat/completions" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ 
    "model": "sonar-pro", 
    "messages": [
      { 
        "role": "user", 
        "content": "Analyze the latest developments in quantum computing and their potential impact on cryptography. Include recent research findings and expert opinions."
      }
    ],
    "stream": true,
    "web_search_options": { 
      "search_type": "pro" 
    }
  }'
```

--------------------------------

### Advanced Academic Search with Perplexity AI SDK (Python)

Source: https://docs.perplexity.ai/guides/academic-filter-guide

Illustrates combining the 'academic' search mode with additional parameters like 'search_after_date_filter' and 'search_context_size' in the Perplexity AI Python SDK. This allows for more refined searches, focusing on recent academic findings. Ensure the 'perplexity' library is installed.

```python
from perplexity import Perplexity

client = Perplexity()
completion = client.chat.completions.create(
    model="sonar",
    messages=[
        {"role": "user", "content": "What are the latest findings on neural networks for image recognition?"}
    ],
    search_mode="academic",
    search_after_date_filter="1/1/2023",
    web_search_options={"search_context_size": "high"}
)

print(completion.choices[0].message.content)
```

--------------------------------

### Handle Reasoning Chunk in Python

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

A Python function example demonstrating how to process a 'chat.reasoning' chunk. It checks the chunk object type and extracts reasoning step information.

```python
def handle_reasoning_chunk(chunk):
    """Process reasoning stage updates"""
    if chunk.object == "chat.reasoning":
        # Access reasoning_steps and other relevant data here
        print("Received reasoning chunk")
        # Example: print(chunk.choices[0].delta.reasoning_steps)
```

--------------------------------

### Basic SEC Filings Search using cURL

Source: https://docs.perplexity.ai/guides/sec-guide

Perform a basic search targeting U.S. Securities and Exchange Commission (SEC) filings. This example utilizes cURL to send a POST request to the Perplexity API with the 'sec' search mode enabled.

```shell
curl --request POST \
  --url https://api.perplexity.ai/chat/completions \
  --header "accept: application/json" \
  --header "authorization: Bearer $SONAR_API_KEY" \
  --header "content-type: application/json" \
  --data '{ "model": "sonar-pro", "messages": [{"role": "user", "content": "Prepare me for markets opening."}] "search_mode": "sec" }' | jq
```

--------------------------------

### Basic Usage: Ask AI with Perplexity Sonar API (Python)

Source: https://docs.perplexity.ai/guides/chat-completions-guide

This Python example demonstrates a basic chat completion request to the Perplexity Sonar API using the OpenAI client. It asks a simple question and prints the AI's response, highlighting the integration with Perplexity's models.

```python
from openai import OpenAI

client = OpenAI(
  api_key="YOUR_API_KEY",
  base_url="https://api.perplexity.ai"
)

response = client.chat.completions.create(
  model="sonar-pro",
  messages=[
    {"role": "user", "content": "What are the latest developments in AI?"}
  ]
)

print(response.choices[0].message.content)
```

--------------------------------

### API Usage and Cost Tracking Example

Source: https://docs.perplexity.ai/changelog

This snippet shows the usage object returned in API responses, detailing token counts and associated costs. It helps users track and understand the expenses of their API calls.

```json
{
  "usage": {
    "prompt_tokens": 8,
    "completion_tokens": 439,
    "total_tokens": 447,
    "search_context_size": "low",
    "cost": {
      "input_tokens_cost": 2.4e-05,
      "output_tokens_cost": 0.006585,
      "request_cost": 0.006,
      "total_cost": 0.012609
    }
  }
}
```

--------------------------------

### Academic Filter Guide

Source: https://docs.perplexity.ai/guides/academic-filter-guide

This guide explains how to use the `search_mode: "academic"` parameter to tailor searches to academic and scholarly sources, prioritizing peer-reviewed papers and research publications.

```APIDOC
## POST /chat/completions

### Description
This endpoint allows you to perform searches using the Perplexity API. It supports various models and filtering options, including an academic search mode.

### Method
POST

### Endpoint
/chat/completions

### Parameters
#### Query Parameters
- **model** (string) - Required - The model to use for the completion (e.g., "sonar-pro", "sonar").
- **messages** (array) - Required - An array of message objects, where each object has a 'role' (user/assistant) and 'content'.
- **search_mode** (string) - Optional - Sets the search mode. Use "academic" to prioritize academic and scholarly sources.
- **search_after_date_filter** (string) - Optional - Filters search results to include only those published after the specified date (e.g., "1/1/2023").
- **web_search_options** (object) - Optional - Options to control web search behavior.
  - **search_context_size** (string) - Optional - Controls the context size for web search (e.g., "low", "high").

### Request Example
```json
{
  "model": "sonar-pro",
  "messages": [
    {
      "role": "user",
      "content": "What is the scientific name of the lions mane mushroom?"
    }
  ],
  "search_mode": "academic",
  "web_search_options": {
    "search_context_size": "low"
  }
}
```

### Response
#### Success Response (200)
- **choices** (array) - Contains the completion results.
  - **message** (object)
    - **content** (string) - The generated response content.

#### Response Example
```json
{
  "choices": [
    {
      "message": {
        "content": "The scientific name of the lion's mane mushroom is Hericium erinaceus."
      }
    }
  ]
}
```
```

--------------------------------

### Image Uploads for Multimodal Search

Source: https://docs.perplexity.ai/changelog/changelog

Announces the availability of image uploads for all users, enabling multimodal search experiences. Includes a link to the image upload guide.

```APIDOC
## Image Uploads for Multimodal Search

### Description
Image uploads are now available for all users, enhancing the Sonar model's multimodal capabilities. Use images as part of your search queries.

### Guide
Follow the image upload guide for implementation details: https://docs.perplexity.ai/guides/image-attachments
```

--------------------------------

### Sample Response with Structured JSON Output from Reasoning Model

Source: https://docs.perplexity.ai/guides/structured-outputs

Illustrates a sample response from a reasoning model when structured output is requested. It includes a preamble with reasoning tokens followed by the final JSON object containing the requested information.

```json
I need to provide information about France in a structured JSON format with specific fields: country, capital, population, official_language. For France: - Country: France - Capital: Paris - Population: About 67 million (as of 2023) - Official Language: French Let me format this information as required.
{"country":"France","capital":"Paris","population":67750000,"official_language":"French"}
```

--------------------------------

### cURL: Perplexity AI Search API Example

Source: https://docs.perplexity.ai/home

This cURL command demonstrates how to interact with the Perplexity AI Search API. It shows a basic request to search for information, likely requiring an API key for authentication. The output would typically be structured data containing search results.

```bash
curl -X POST "https://api.perplexity.ai/chat/completions" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{ "messages": [{"role": "user", "content": "What is Perplexity AI?"}]}'
```

--------------------------------

### Academic Research Across Languages Example (Python)

Source: https://docs.perplexity.ai/guides/search-language-filter

This example shows how to search for scholarly content across multiple languages and specific domains, such as academic repositories. It combines language filtering with domain filtering for targeted research.

```python
# Search for research papers in multiple languages
# Assuming 'client' is an initialized Perplexity client object
# response = client.search.create(
#     query="quantum computing algorithms",
#     max_results=20,
#     search_language_filter=["en", "de", "fr", "ru"],
#     search_domain_filter=["arxiv.org", "nature.com", "science.org"]
# )

```

--------------------------------

### POST /chat/completions - Combining SEC Mode with Other Parameters

Source: https://docs.perplexity.ai/guides/sec-guide

Demonstrates how to combine the SEC filter (`search_mode: "sec"`) with other parameters like `stream` and `search_after_date_filter` for more refined searches.

```APIDOC
## POST /chat/completions

### Description
Performs a chat completion request, combining the SEC filter with other parameters for more specific and refined search results.

### Method
POST

### Endpoint
/chat/completions

### Parameters
#### Request Body
- **model** (string) - Required - The model to use for the completion (e.g., "sonar").
- **messages** (array of objects) - Required - The conversation history, with each object having 'role' and 'content' fields.
  - **role** (string) - Required - The role of the message (e.g., "user").
  - **content** (string) - Required - The content of the message.
- **stream** (boolean) - Optional - Whether to stream the response.
- **search_mode** (string) - Required - Set to "sec" to filter for SEC filings.
- **search_after_date_filter** (string) - Optional - Filters results to those filed after the specified date (e.g., "1/1/2023").

### Request Example
```json
{
  "model": "sonar",
  "messages": [
    {
      "role": "user",
      "content": "Summarize the latest 10-K filings for Apple Inc."
    }
  ],
  "stream": false,
  "search_mode": "sec",
  "search_after_date_filter": "1/1/2023"
}
```

### Response
#### Success Response (200)
- **choices** (array) - An array of completion choices.
  - **message** (object) - The assistant's message.
    - **content** (string) - The content of the assistant's response.
    - **role** (string) - The role of the message (always "assistant").
  - **finish_reason** (string) - The reason the model stopped generating tokens.
  - **index** (integer) - The index of the choice.

#### Response Example
```json
{
  "choices": [
    {
      "message": {
        "content": "Apple Inc.'s latest 10-K filing, dated [date], highlights [summary of key points]...",
        "role": "assistant"
      },
      "finish_reason": "stop",
      "index": 0
    }
  ]
}
```
```

--------------------------------

### cURL: Make Non-Streaming API Call

Source: https://docs.perplexity.ai/getting-started/quickstart

This cURL command demonstrates how to make a non-streaming chat completion request to the Perplexity API. It requires setting the SONAR_API_KEY environment variable and specifies the model and messages in JSON format. The output is the raw JSON response.

```bash
curl --location 'https://api.perplexity.ai/chat/completions' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--header "Authorization: Bearer $SONAR_API_KEY" \
--data '{ "model": "sonar-pro", "messages": [ { "role": "user", "content": "What were the results of the 2025 French Open Finals?" } ] }' | jq
```

--------------------------------

### Specify User Location with Country Code Only (Python)

Source: https://docs.perplexity.ai/guides/user-location-filter-guide

This Python example shows how to use only the 'country' code within the 'user_location' parameter to provide a broader geographic context for search results. It's useful for general queries where a specific city or region is not necessary.

```python
from perplexity import Perplexity
client = Perplexity()
completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are an expert on international news."},
        {"role": "user", "content": "Summarize political news from today."}
    ],
    model="sonar-pro",
    web_search_options={
        "user_location": {
            "country": "US"
        }
    }
)
print(f"Response: {completion.choices[0].message.content}")
```

--------------------------------

### TypeScript: Perplexity AI Search Example

Source: https://docs.perplexity.ai/financial-news-tracker

This TypeScript code snippet shows how to initiate a search using the Perplexity AI API. It makes a POST request to the `/search` endpoint with an API key for authentication and a JSON body containing the search query. The results will be the ranked web search results.

```typescript
async function searchPerplexity() {
  const response = await fetch('https://api.perplexity.ai/search', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer YOUR_API_KEY',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      query: 'What is Comet Browser?'
    })
  });
  const data = await response.json();
  console.log(data);
}
```

--------------------------------

### Async Chat Completions API Endpoints

Source: https://docs.perplexity.ai/guides/usage-tiers

Documentation for the asynchronous chat completions endpoints, including POST for initiating completions and GET for status and results. Rate limits vary by usage tier.

```APIDOC
## Async Chat Completions API Endpoints

### Description
This section details the asynchronous chat completions endpoints. You can initiate a chat completion request via POST and monitor its status or retrieve results using GET requests.

### Endpoints

#### POST /async/chat/completions

##### Method
POST

##### Endpoint
`/async/chat/completions`

##### Description
Initiates an asynchronous chat completion request.

##### Request Body
*   **model** (string) - Required - The model to use for the chat completion.
*   **messages** (array) - Required - An array of message objects representing the conversation.
    *   **role** (string) - Required - The role of the author (`system`, `user`, or `assistant`).
    *   **content** (string) - Required - The content of the message.
*   **stream** (boolean) - Optional - Whether to stream the response.

##### Request Example
```json
{
  "model": "sonar-pro",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the weather today?"}
  ],
  "stream": false
}
```

#### GET /async/chat/completions

##### Method
GET

##### Endpoint
`/async/chat/completions`

##### Description
Retrieves the status of asynchronous chat completion requests. Use query parameters to filter.

##### Query Parameters
*   **request_id** (string) - Required - The ID of the request to check.

#### GET /async/chat/completions/{request_id}

##### Method
GET

##### Endpoint
`/async/chat/completions/{request_id}`

##### Description
Retrieves the results of a completed asynchronous chat completion request.

##### Path Parameters
*   **request_id** (string) - Required - The ID of the request for which to retrieve results.

### Rate Limits (Requests per minute - RPM)

| Tier      | `sonar-deep-research` | `sonar-reasoning-pro` | `sonar-pro` | `sonar` | POST `/async/chat/completions` | GET `/async/chat/completions` | GET `/async/chat/completions/{request_id}` |
| :-------- | :-------------------- | :-------------------- | :---------- | :------ | :----------------------------- | :-------------------------- | :--------------------------------------- |
| Tier 0    | 5                     | 50                    | 50          | 50      | 5                              | 3000                        | 6000                                     |
| Tier 1    | 10                    | 50                    | 50          | 50      | 10                             | 3000                        | 6000                                     |
| Tier 2    | 20                    | 500                   | 500         | 500     | 20                             | 3000                        | 6000                                     |
| Tier 3    | 40                    | 1000                  | 1000        | 1000    | 40                             | 3000                        | 6000                                     |
| Tier 4    | 60                    | 2000                  | 2000        | 2000    | 60                             | 3000                        | 6000                                     |
| Tier 5    | 100                   | 2000                  | 2000        | 2000    | 60                             | 3000                        | 6000                                     |

### Features by Model

*   **`sonar-deep-research`**: related questions, structured outputs
*   **`sonar-reasoning-pro`**: images, related questions, search domain filter, structured outputs
*   **`sonar-pro`**: images, related questions, search domain filter, structured outputs
*   **`sonar`**: images, related questions, search domain filter, structured outputs

### Usage Tiers

Usage tiers are based on cumulative credit purchases:

*   **Tier 0**: -
*   **Tier 1**: $50
*   **Tier 2**: $250
*   **Tier 3**: $500
*   **Tier 4**: $1000
*   **Tier 5**: $5000
```

--------------------------------

### Combine Language Filter with Other Search Parameters (Python, TypeScript, cURL)

Source: https://docs.perplexity.ai/guides/search-language-filter

This example demonstrates the flexibility of the `search_language_filter` by combining it with other filters, such as `search_domain_filter` and `search_recency_filter`. This allows for highly precise search queries targeting specific content, languages, and timeframes.

```python
from perplexity import Perplexity

client = Perplexity()

# Combine language filter with date and domain filters
response = client.search.create(
    query="climate change research",
    max_results=20,
    search_language_filter=["en", "de"],
    search_domain_filter=["nature.com", "science.org"],
    search_recency_filter="month"
)

for result in response.results:
    print(f"{result.title}")
    print(f"URL: {result.url}")
    print(f"Date: {result.date}")
    print("---")
```

```typescript
import { Perplexity } from 'perplexity';

const client = new Perplexity();

async function combinedFilters() {
  const response = await client.search.create({
    query: "climate change research",
    max_results: 20,
    search_language_filter: ["en", "de"],
    search_domain_filter: ["nature.com", "science.org"],
    search_recency_filter: "month",
  });

  response.results.forEach(result => {
    console.log(`${result.title}`);
    console.log(`URL: ${result.url}`);
    console.log(`Date: ${result.date}`);
    console.log("---");
  });
}
```

```curl
curl -X POST "https://api.perplexity.ai/search/create" \
-H "Authorization: Bearer YOUR_API_KEY" \
-H "Content-Type: application/json" \
-d '{ 
  "query": "climate change research", 
  "max_results": 20, 
  "search_language_filter": ["en", "de"], 
  "search_domain_filter": ["nature.com", "science.org"], 
  "search_recency_filter": "month" 
}'
```

--------------------------------

### Optimizing Streaming for Real-time Chat in Python

Source: https://docs.perplexity.ai/guides/streaming-responses

Provides a Python code example for optimizing streaming API calls for real-time chat applications. It uses a balanced temperature and a reasonable max_tokens limit for immediate responses.

```python
# Optimize for immediate response
stream = client.chat.completions.create(
    model="sonar",
    messages=messages,
    stream=True,
    max_tokens=1000,  # Reasonable limit
    temperature=0.7   # Balanced creativity
)
```

--------------------------------

### Perplexity API: Root Domain Filtering Example (JSON)

Source: https://docs.perplexity.ai/guides/search-domain-filter-guide

Shows how to use the search_domain_filter parameter to perform root domain filtering. By specifying a root domain like 'wikipedia.org', the filter will match all content from that domain and its subdomains, including different language versions.

```json
"search_domain_filter": ["wikipedia.org"]
```

--------------------------------

### Optimize Perplexity AI Parameters

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Configures API parameters to optimize for specific use cases. Examples are provided for factual question answering and creative writing.

```python
# For factual Q&A
factual_config = {
    "temperature": 0.1, # Low creativity for accuracy
    "top_p": 0.9,
    "search_recency_filter": "month"
}

# For creative writing
creative_config = {
    "temperature": 0.8, # Higher creativity
    "top_p": 0.95,
    "presence_penalty": 0.1,
    "frequency_penalty": 0.1
}

# Usage
factual_response = client.chat.completions.create(
    messages=[{"role": "user", "content": "What is the current inflation rate?"}],
    model="sonar",
    **factual_config
)
```

```typescript
// For factual Q&A
const factualConfig = {
  temperature: 0.1, // Low creativity for accuracy
  top_p: 0.9,
  search_recency_filter: "month" as const
};

// For creative writing
const creativeConfig = {
  temperature: 0.8, // Higher creativity
  top_p: 0.95,
  presence_penalty: 0.1,
  frequency_penalty: 0.1
};

// Usage
const factualResponse = await client.chat.completions.create({
  messages: [{ role: "user", content: "What is the current inflation rate?" }],
  model: "sonar",
  ...factualConfig
});
```

--------------------------------

### Financial Analysis with Pydantic (Python)

Source: https://docs.perplexity.ai/guides/structured-outputs

Demonstrates using Python and the Pydantic library to define a `FinancialMetrics` schema and request structured financial data from Perplexity's 'sonar-pro' model. The response is validated against the schema.

```python
from perplexity import Perplexity
from typing import List, Optional
from pydantic import BaseModel

class FinancialMetrics(BaseModel):
    company: str
    quarter: str
    revenue: float
    net_income: float
    eps: float
    revenue_growth_yoy: Optional[float] = None
    key_highlights: Optional[List[str]] = None

client = Perplexity()
completion = client.chat.completions.create(
    model="sonar-pro",
    messages=[
        {
            "role": "user",
            "content": "Analyze the latest quarterly earnings report for Apple Inc. Extract key financial metrics."
        }
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "schema": FinancialMetrics.model_json_schema()
        }
    }
)

metrics = FinancialMetrics.model_validate_json(completion.choices[0].message.content)
print(f"Revenue: ${metrics.revenue}B")
```

--------------------------------

### Perplexity AI Search API (cURL)

Source: https://docs.perplexity.ai/api-reference/search-post

Example of how to perform a search query using the Perplexity AI API via cURL. It demonstrates setting parameters like query, max_results, and various filters for domains, dates, and recency.

```curl
curl --request POST \
  --url https://api.perplexity.ai/search \
  --header 'Authorization: Bearer ' \
  --header 'Content-Type: application/json' \
  --data ' {
    "query": "latest AI developments 2024",
    "max_results": 10,
    "max_tokens": 25000,
    "search_domain_filter": [
      "science.org",
      "pnas.org",
      "cell.com"
    ],
    "max_tokens_per_page": 2048,
    "country": "US",
    "search_recency_filter": "week",
    "search_after_date": "10/15/2025",
    "search_before_date": "10/16/2025",
    "last_updated_after_filter": "07/01/2025",
    "last_updated_before_filter": "12/30/2025",
    "search_language_filter": [
      "en",
      "fr",
      "de"
    ]
  } '
```

--------------------------------

### Basic Usage: Ask AI with Perplexity Sonar API (TypeScript)

Source: https://docs.perplexity.ai/guides/chat-completions-guide

This TypeScript example shows a fundamental chat completion call to Perplexity's Sonar API via the OpenAI client library. It sends a query about AI developments and logs the received content.

```typescript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: "YOUR_API_KEY",
  baseURL: "https://api.perplexity.ai"
});

const response = await client.chat.completions.create({
  model: "sonar-pro",
  messages: [
    { role: "user", content: "What are the latest developments in AI?" }
  ]
});

console.log(response.choices[0].message.content);
```

--------------------------------

### Filter Search by Multiple Languages (Python, TypeScript, cURL)

Source: https://docs.perplexity.ai/guides/search-language-filter

This example shows how to search for content across multiple languages simultaneously, such as English, French, and German. The `search_language_filter` parameter accepts an array of ISO 639-1 codes to broaden the scope of results.

```python
from perplexity import Perplexity

client = Perplexity()
# Search for content in English, French, and German
response = client.search.create(
    query="renewable energy innovations",
    max_results=15,
    search_language_filter=["en", "fr", "de"]
)

for result in response.results:
    print(f"{result.title}: {result.url}")
```

```typescript
import { Perplexity } from 'perplexity';

const client = new Perplexity();

async function searchMultipleLanguages() {
  const response = await client.search.create({
    query: "renewable energy innovations",
    max_results: 15,
    search_language_filter: ["en", "fr", "de"],
  });

  response.results.forEach(result => {
    console.log(`${result.title}: ${result.url}`);
  });
}
```

```curl
curl -X POST "https://api.perplexity.ai/search/create" \
-H "Authorization: Bearer YOUR_API_KEY" \
-H "Content-Type: application/json" \
-d '{ 
  "query": "renewable energy innovations", 
  "max_results": 15, 
  "search_language_filter": ["en", "fr", "de"] 
}'
```

--------------------------------

### Advanced Usage: Content Localization Research

Source: https://docs.perplexity.ai/guides/search-language-filter

Example of finding product reviews or market-specific content in target languages for localization projects.

```APIDOC
## Advanced Usage: Content Localization Research

Find examples and references in target languages for localization projects:

```python
# Find product reviews in target markets
target_languages = ["ja", "ko", "zh"] # Asian markets
response = client.search.create(
    query="smartphone reviews 2024",
    max_results=15,
    search_language_filter=target_languages,
    search_recency_filter="month"
)
```
```

--------------------------------

### Streaming Responses

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Get real-time response streaming for a better user experience. This allows processing the response as it's generated.

```APIDOC
## POST /chat/completions (Streaming)

### Description
Generates a text completion with real-time streaming enabled.

### Method
POST

### Endpoint
/chat/completions

### Parameters
#### Request Body
- **messages** (array) - Required - A list of message objects.
- **model** (string) - Required - The model to use (e.g., "sonar").
- **stream** (boolean) - Required - Set to `true` to enable streaming.

### Request Example
```json
{
  "messages": [
    {"role": "user", "content": "Write a summary of recent AI breakthroughs"}
  ],
  "model": "sonar",
  "stream": true
}
```

### Response
#### Success Response (200)
- The response is a stream of chunks. Each chunk may contain a 'delta' object with 'content' representing a part of the generated text.

#### Response Example (Chunk)
```json
{
  "choices": [
    {
      "delta": {
        "content": "Recent AI breakthroughs include..."
      }
    }
  ]
}
```
```

--------------------------------

### Filter Government and Educational Sources by TLD

Source: https://docs.perplexity.ai/guides/search-domain-filter-guide

This example shows how to search exclusively within government (.gov) and educational (.edu) domains. It uses the `search_domain_filter` with TLDs to narrow down the search scope to official institutions.

```Python
from perplexity import Perplexity

client = Perplexity()
# Search all .gov and .edu domains
response = client.search.create(
    query="climate change policy research",
    max_results=15,
    search_domain_filter=[
        ".gov",
        ".edu"
    ]
)

for result in response.results:
    print(f"{result.title}")
    print(f"Source: {result.url}")
    print("---")
```

--------------------------------

### TypeScript: Initialize Perplexity Client

Source: https://docs.perplexity.ai/pricing

This TypeScript snippet shows the initialization of a Perplexity client, likely for interacting with the API. It sets up the client with an API key, which is essential for authentication. No specific input or output is detailed beyond client instantiation.

```typescript
import Perplexity from "@perplexity/perplexity-client";

const client = new Perplexity("YOUR_API_KEY");
```

--------------------------------

### Enable Concise Stream Mode in TypeScript

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

Shows how to utilize the 'concise' stream mode with the Perplexity TypeScript SDK. The example iterates over the stream and logs chunk types, processing text content as it arrives.

```typescript
import Perplexity from '@perplexity-ai/perplexity_ai';

const client = new Perplexity();
const stream = await client.chat.completions.create({
    model: "sonar-pro",
    messages: [{ role: "user", content: "What's the weather in Seattle?" }],
    stream: true,
    stream_mode: "concise"
});

for await (const chunk of stream) {
    console.log(`Chunk type: ${chunk.object}`);
    if (chunk.choices[0]?.delta?.content) {
        process.stdout.write(chunk.choices[0].delta.content);
    }
}
```

--------------------------------

### File Attachments Support

Source: https://docs.perplexity.ai/changelog

Upload and analyze documents in multiple formats (PDF, DOC, DOCX, TXT, RTF) using Sonar models. Ask questions, extract information, and get summaries from your documents.

```APIDOC
## New: File Attachments Support

### Description
Upload and analyze documents in multiple formats including PDF, DOC, DOCX, TXT, and RTF. This feature allows you to ask questions about document content, extract information, and generate summaries efficiently.

### Method
POST

### Endpoint
`/analyze/files`

### Parameters
#### Request Body
- **content_type** (string) - Required - Specifies the type of content, e.g., `file_url` or `file_upload`.
- **file_url** (string) - Required if `content_type` is `file_url` - A publicly accessible URL to the document.
- **file_upload** (file) - Required if `content_type` is `file_upload` - The document file to upload.
- **model** (string) - Optional - The Sonar model to use for analysis (e.g., `sonar`, `sonar-pro`). Defaults to `sonar`.
- **query** (string) - Optional - The question to ask about the document content.

### Request Example (using file_url)
```json
{
  "content_type": "file_url",
  "file_url": "https://example.com/document.pdf",
  "model": "sonar-pro",
  "query": "Summarize the key findings of this document."
}
```

### Response
#### Success Response (200)
- **analysis_result** (string) - The result of the document analysis, such as a summary or answers to questions.

#### Response Example
```json
{
  "analysis_result": "The document discusses the impact of AI on the job market, highlighting potential job displacement and the creation of new roles..."
}
```
```

--------------------------------

### Pose Query to Perplexity AI

Source: https://docs.perplexity.ai/guides/search-context-size-guide

This snippet demonstrates how to construct a JSON object to pose a query to Perplexity AI. It includes the query text and optional web search configurations. The 'high' setting for search context size is recommended for complex research.

```json
{
  "query": "Explain the economic causes of the 2008 financial crisis."
}
```

```json
{
  "query": "Explain the economic causes of the 2008 financial crisis.",
  "web_search_options": {
    "search_context_size": "high"
  }
}
```

--------------------------------

### Filter Search by Single Language (Python, TypeScript, cURL)

Source: https://docs.perplexity.ai/guides/search-language-filter

This example demonstrates how to filter search results to include only content in a single specified language, such as English. It utilizes the `search_language_filter` parameter with a list containing one ISO 639-1 code.

```python
from perplexity import Perplexity

client = Perplexity()
response = client.search.create(
    query="artificial intelligence",
    max_results=10,
    search_language_filter=["en"]
)

for result in response.results:
    print(f"{result.title}: {result.url}")
```

```typescript
import { Perplexity } from 'perplexity';

const client = new Perplexity();

async function searchWithLanguageFilter() {
  const response = await client.search.create({
    query: "artificial intelligence",
    max_results: 10,
    search_language_filter: ["en"],
  });

  response.results.forEach(result => {
    console.log(`${result.title}: ${result.url}`);
  });
}
```

```curl
curl -X POST "https://api.perplexity.ai/search/create" \
-H "Authorization: Bearer YOUR_API_KEY" \
-H "Content-Type: application/json" \
-d '{ 
  "query": "artificial intelligence", 
  "max_results": 10, 
  "search_language_filter": ["en"] 
}'
```

--------------------------------

### Regional Language Search (Python, TypeScript, cURL)

Source: https://docs.perplexity.ai/guides/search-language-filter

This example demonstrates how to perform regional language searches, focusing on specific geographic areas. It uses ISO 639-1 codes for languages like Chinese, Japanese, Korean, and various European languages to target regional content.

```python
from perplexity import Perplexity

client = Perplexity()
# Search for Asian market news in Chinese, Japanese, and Korean
response = client.search.create(
    query="technology market trends",
    max_results=10,
    search_language_filter=["zh", "ja", "ko"]
)

# Search for European tech news in multiple European languages
eu_response = client.search.create(
    query="tech startups",
    max_results=10,
    search_language_filter=["en", "de", "fr", "es", "it"]
)
```

```typescript
import { Perplexity } from 'perplexity';

const client = new Perplexity();

async function regionalLanguageSearch() {
  // Search for Asian market news in Chinese, Japanese, and Korean
  const response = await client.search.create({
    query: "technology market trends",
    max_results: 10,
    search_language_filter: ["zh", "ja", "ko"],
  });

  // Search for European tech news in multiple European languages
  const eu_response = await client.search.create({
    query: "tech startups",
    max_results: 10,
    search_language_filter: ["en", "de", "fr", "es", "it"],
  });

  console.log("Asian Market Search Results:", response.results);
  console.log("European Tech News Results:", eu_response.results);
}
```

```curl
# Search for Asian market news in Chinese, Japanese, and Korean
curl -X POST "https://api.perplexity.ai/search/create" \
-H "Authorization: Bearer YOUR_API_KEY" \
-H "Content-Type: application/json" \
-d '{ 
  "query": "technology market trends", 
  "max_results": 10, 
  "search_language_filter": ["zh", "ja", "ko"] 
}'

# Search for European tech news in multiple European languages
curl -X POST "https://api.perplexity.ai/search/create" \
-H "Authorization: Bearer YOUR_API_KEY" \
-H "Content-Type: application/json" \
-d '{ 
  "query": "tech startups", 
  "max_results": 10, 
  "search_language_filter": ["en", "de", "fr", "es", "it"] 
}'
```

--------------------------------

### cURL: Perplexity AI Search Example

Source: https://docs.perplexity.ai/financial-news-tracker

This cURL command demonstrates how to perform a search using the Perplexity AI API. It sends a POST request to the `/search` endpoint with a JSON payload containing the search query. The response includes ranked web search results.

```bash
curl -X POST "https://api.perplexity.ai/search" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{ "query": "What is Comet Browser?" }'
```

--------------------------------

### Multiple Recency Filter Examples

Source: https://docs.perplexity.ai/guides/search-date-time-filters

Illustrates using `search_recency_filter` for different relative timeframes: 'day', 'month', and 'year'.

```APIDOC
## POST /api/search

### Description
Demonstrates fetching search results for different relative time periods using the `search_recency_filter` parameter.

### Method
POST

### Endpoint
/api/search

### Parameters
#### Query Parameters
- **query** (string) - Required - The search query.
- **max_results** (integer) - Optional - The maximum number of results to return.
- **search_recency_filter** (string) - Optional - Filters results by predefined time periods. Allowed values: "day", "week", "month", "year".

### Request Example
```python
from perplexity import Perplexity

client = Perplexity()

# Get content from the past day
day_response = client.search(
    query="breaking tech news",
    max_results=5,
    search_recency_filter="day"
)

# Get content from the past month
month_response = client.search(
    query="AI research developments",
    max_results=10,
    search_recency_filter="month"
)

# Get content from the past year
year_response = client.search(
    query="major tech trends",
    max_results=15,
    search_recency_filter="year"
)
```

### Response
#### Success Response (200)
- **results** (array) - A list of search results.
  - **title** (string) - The title of the search result.
  - **url** (string) - The URL of the search result.
  - **snippet** (string) - A short snippet of the search result content.
  - **published_date** (string) - The publication date of the content.
  - **last_updated** (string) - The last updated date of the content.

#### Response Example (for day_response)
```json
{
  "results": [
    {
      "title": "Urgent Security Alert Issued",
      "url": "http://example.com/security-alert",
      "snippet": "A critical security vulnerability was discovered today...",
      "published_date": "2024-07-21",
      "last_updated": "2024-07-21"
    }
  ]
}
```
```

--------------------------------

### Example of a Successful Chat Completion Response

Source: https://docs.perplexity.ai/api-reference/chat-completions-post

Illustrates the structure of a successful 200 OK response for a chat completion request. It includes essential information like the response ID, model used, creation timestamp, usage statistics, and the actual completion choices.

```json
{
  "id": "string",
  "model": "string",
  "created": 1234567890,
  "usage": {
    "object": "chat.completion"
  },
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "This is the assistant's response."
      }
    }
  ],
  "search_results": null,
  "videos": null
}
```

--------------------------------

### News Monitoring by Language Example (Python)

Source: https://docs.perplexity.ai/guides/search-language-filter

This Python code snippet demonstrates how to monitor breaking news across different language regions. It uses a dictionary to map regions to language codes and performs searches for a specified query, filtering by language and recency.

```python
# Monitor breaking news in different languages
news_queries = {
    "English": ["en"],
    "Chinese": ["zh"],
    "Spanish": ["es"],
    "Arabic": ["ar"]
}

# Assuming 'client' is an initialized Perplexity client object
# for region, langs in news_queries.items():
#     response = client.search.create(
#         query="breaking news technology",
#         max_results=5,
#         search_language_filter=langs,
#         search_recency_filter="day"
#     )
#     print(f"{region} News: {len(response.results)} found")

```

--------------------------------

### Combining Publication and Last Updated Filters

Source: https://docs.perplexity.ai/guides/date-range-filter-guide

This example shows how to combine publication date filters with last updated date filters to refine search results.

```APIDOC
## POST /chat/completions

### Description
Combines publication date filters and last updated date filters to find content that meets both criteria.

### Method
POST

### Endpoint
/chat/completions

### Parameters
#### Query Parameters
- **search_after_date_filter** (string) - Optional - Filters results to include content published on or after this date.
- **search_before_date_filter** (string) - Optional - Filters results to include content published on or before this date.
- **last_updated_after_filter** (string) - Optional - Filters results to include content last updated on or after this date.

### Request Example
```json
{
  "model": "sonar-pro",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Show me articles published last year but updated recently."}
  ],
  "search_after_date_filter": "1/1/2024",
  "search_before_date_filter": "12/31/2024",
  "last_updated_after_filter": "3/1/2025"
}
```

### Response
#### Success Response (200)
- **choices** (array) - List of completion choices.
  - **message** (object) - The message content from the completion.
    - **content** (string) - The generated text response.

#### Response Example
```json
{
  "choices": [
    {
      "message": {
        "content": "Example article content published last year and updated recently..."
      }
    }
  ]
}
```
```

--------------------------------

### Chat Completions with Stream Mode

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

This section details how to use the chat completions endpoint with the `stream_mode` parameter to control the format of streaming responses. It explains the 'full' and 'concise' modes and provides code examples for Python, TypeScript, and cURL.

```APIDOC
## POST /chat/completions

### Description
Creates a streaming chat completion request with specified model and messages. Allows control over the streaming response format using `stream_mode`.

### Method
POST

### Endpoint
/chat/completions

### Parameters
#### Query Parameters
None

#### Request Body
- **model** (string) - Required - The model to use for the chat completion (e.g., "sonar-pro").
- **messages** (array) - Required - An array of message objects representing the conversation history.
  - **role** (string) - Required - The role of the message sender ('user' or 'assistant').
  - **content** (string) - Required - The content of the message.
- **stream** (boolean) - Optional - Whether to stream the response. Defaults to false.
- **stream_mode** (string) - Optional - The format for streaming responses. Options: "full" (default), "concise".

### Request Example (cURL)
```bash
curl -X POST "https://api.perplexity.ai/chat/completions" \
 -H "Authorization: Bearer YOUR_API_KEY" \
 -H "Content-Type: application/json" \
 -d '{ "model": "sonar-pro", "messages": [{"role": "user", "content": "What is the weather in Seattle?"}], "stream": true, "stream_mode": "concise" }'
```

### Response
#### Success Response (200)
The response is a stream of chunks. The structure of these chunks depends on the `stream_mode`.

#### Response Example (Concise Mode - `chat.reasoning` chunk)
```json
{
  "id": "cfa38f9d-fdbc-4ac6-a5d2-a3010b6a33a6",
  "model": "sonar-pro",
  "created": 1759441590,
  "object": "chat.reasoning",
  "choices": [
    {
      "index": 0,
      "finish_reason": null,
      "message": {
        "role": "assistant",
        "content": ""
      },
      "delta": {
        "role": "assistant",
        "content": "",
        "reasoning_steps": [
          {
            "thought": "Searching the web for Seattle's current weather...",
            "type": "web_search",
            "web_search": {
              "search_results": [],
              "search_keywords": ["Seattle current weather"]
            }
          }
        ]
      }
    }
  ],
  "type": "message"
}
```
```

--------------------------------

### User Location Filter Guide

Source: https://docs.perplexity.ai/guides/user-location-filter-guide

The `user_location` parameter within `web_search_options` allows you to refine search results based on the user’s approximate geographic location. This helps provide more contextually relevant information. You can specify the location using latitude/longitude coordinates, country code, city, and region.

```APIDOC
## User Location Filter Guide

### Description
The `user_location` parameter within `web_search_options` allows you to refine search results based on the user’s approximate geographic location. This helps provide more contextually relevant information. You can specify the location using latitude/longitude coordinates, country code, city, and region.

For the most accurate results, we recommend providing as much location information as possible, including `city` and `region` fields. For supported country codes, please refer to the list here. The `city` and `region` fields significantly improve location accuracy. We strongly recommend including them alongside coordinates and country code for the best results. Latitude and longitude must be provided alongside the country parameter, they cannot be provided on their own.

### Overview
The `user_location` filter helps tailor search results by incorporating geographic context. This is particularly useful for queries where location significantly impacts relevance, such as:
* Finding local businesses or services.
* Getting information about regional events or news.
* Understanding location-specific regulations or customs.

To refine search results by location, include the `user_location` object within the `web_search_options` in your request payload. You can provide coordinates, country code, city, region, or combine them for maximum accuracy:

**Using All Available Fields (Recommended for Best Accuracy):**
```json
{
  "web_search_options": {
    "user_location": {
      "country": "US",
      "region": "California",
      "city": "San Francisco",
      "latitude": 37.7749,
      "longitude": -122.4194
    }
  }
}
```

**Using City and Region with Country:**
```json
{
  "web_search_options": {
    "user_location": {
      "country": "US",
      "region": "New York",
      "city": "New York City"
    }
  }
}
```

**Using Latitude/Longitude:**
```json
{
  "web_search_options": {
    "user_location": {
      "country":"US",
      "latitude": 37.7749,
      "longitude": -122.4194
    }
  }
}
```

**Using Country Code Only:**
```json
{
  "web_search_options": {
    "user_location": {
      "country": "US"
    }
  }
}
```

These filters work alongside other search parameters like date range or domain filters.

### Examples

**1. Refining Results with All Location Fields (Recommended)**
This example provides all available location fields for San Francisco to get the most accurate geographically relevant search results.

**Request Example**
```python
from perplexity import Perplexity

client = Perplexity()
completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a helpful local guide."},
        {"role": "user", "content": "What are some good coffee shops nearby?"}
    ],
    model="sonar-pro",
    web_search_options={
        "user_location": {
            "country": "US",
            "region": "California",
            "city": "San Francisco",
            "latitude": 37.7749,
            "longitude": -122.4194
        }
    }
)

print(f"Response: {completion.choices[0].message.content}")
```

**2. Refining Results with Country Code**
This example uses a two-letter ISO country code (United States) to provide broader geographic context.

**Request Example**
```python
from perplexity import Perplexity

client = Perplexity()
completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are an expert on international news."},
        {"role": "user", "content": "Summarize political news from today."}
    ],
    model="sonar-pro",
    web_search_options={
        "user_location": {
            "country": "US"
        }
    }
)

print(f"Response: {completion.choices[0].message.content}")
```
```

--------------------------------

### Combine Domain Filter with Other Search Parameters

Source: https://docs.perplexity.ai/guides/search-domain-filter-guide

This example shows how to integrate the `search_domain_filter` with other Perplexity API parameters like `search_recency_filter` and `search_language_filter`. This allows for highly precise search queries, focusing on specific domains, timeframes, and languages.

```Python
from perplexity import Perplexity

client = Perplexity()
# Combine domain filter with date and language filters
response = client.search.create(
    query="quantum computing breakthroughs",
    max_results=20,
    search_domain_filter=[
        "nature.com",
        "science.org",
        "arxiv.org"
    ],
    search_recency_filter="month",
    search_language_filter=["en"]
)

for result in response.results:
    print(f"{result.title}")
    print(f"URL: {result.url}")
    print(f"Date: {result.date}")
    print("---")
```

--------------------------------

### Multilingual Research Example (Python)

Source: https://docs.perplexity.ai/guides/search-language-filter

This code demonstrates how to conduct multilingual research by iterating through groups of language codes and performing separate searches. It shows how to gather and process results across different language regions for a given query.

```python
from perplexity import Perplexity

client = Perplexity()

# Research a global topic in multiple languages
languages = [
    ["en"],  # English-speaking countries
    ["zh", "ja"],  # East Asia
    ["es", "pt"],  # Latin America and Iberia
    ["fr", "de", "it"]  # Western Europe
]

results_by_region = {}
for lang_group in languages:
    response = client.search.create(
        query="sustainable development goals progress",
        max_results=10,
        search_language_filter=lang_group
    )
    results_by_region[', '.join(lang_group)] = response.results

# Analyze results by language/region
for region, results in results_by_region.items():
    print(f"Results in {region}: {len(results)} found")

```

--------------------------------

### Advanced Usage: News Monitoring by Language

Source: https://docs.perplexity.ai/guides/search-language-filter

Example of tracking news stories across different language regions by specifying language filters.

```APIDOC
## Advanced Usage: News Monitoring by Language

Track news stories across different language regions:

```python
# Monitor breaking news in different languages
news_queries = {
    "English": ["en"],
    "Chinese": ["zh"],
    "Spanish": ["es"],
    "Arabic": ["ar"]
}

for region, langs in news_queries.items():
    response = client.search.create(
        query="breaking news technology",
        max_results=5,
        search_language_filter=langs,
        search_recency_filter="day"
    )
    print(f"{region} News: {len(response.results)} found")
```
```

--------------------------------

### Sonar Search Context Size

Source: https://docs.perplexity.ai/guides/search-context-size-guide

Controls the amount of search context retrieved from the web by Sonar models to balance cost and comprehensiveness. Options include 'low', 'medium', and 'high'.

```APIDOC
## POST /chat/completions

### Description
This endpoint allows you to send chat messages to the Sonar model and control the amount of web search context retrieved using the `search_context_size` parameter.

### Method
POST

### Endpoint
`https://api.perplexity.ai/chat/completions`

### Parameters
#### Request Body
- **model** (string) - Required - The model to use (e.g., "sonar").
- **messages** (array) - Required - An array of message objects, each with a `role` (system or user) and `content`.
- **web_search_options** (object) - Optional - Options for web search.
  - **search_context_size** (string) - Optional - Controls the amount of search context. Allowed values: "low", "medium", "high". Defaults to "medium".

### Request Example
```json
{
  "model": "sonar",
  "messages": [
    { "role": "system", "content": "Be precise and concise.") },
    { "role": "user", "content": "How many stars are there in our galaxy?") }
  ],
  "web_search_options": {
    "search_context_size": "low"
  }
}
```

### Response
#### Success Response (200)
- **choices** (array) - Contains the model's response(s).
  - **message** (object) - The message object from the model.
    - **role** (string) - The role of the message sender (e.g., "assistant").
    - **content** (string) - The content of the message.

#### Response Example
```json
{
  "id": "chatcmpl-xxxxxxxxxxxxxxxxx",
  "object": "chat.completion",
  "created": 1700000000,
  "model": "sonar-yyyy-mm-dd",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Our galaxy, the Milky Way, is estimated to contain between 100 and 400 billion stars."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 50,
    "completion_tokens": 20,
    "total_tokens": 70
  }
}
```

### Best Practices
- Use `low` for cost optimization when answer completeness is less critical.
- Use `medium` (default) for general use cases.
- Use `high` for deep research or when detailed evidence is crucial.
- Combine `search_context_size` with other filters like `search_domain_filter` for more precise results.
- Test different settings to balance response latency and user experience, especially for real-time applications.
```

--------------------------------

### Filter Search by Language (JSON Example)

Source: https://docs.perplexity.ai/api-reference

Demonstrates how to use the 'search_language_filter' parameter to restrict search results to specific languages. This parameter accepts an array of ISO 639-1 language codes.

```json
{
  "search_language_filter": ["en", "fr", "de"]
}
```

--------------------------------

### POST /chat/completions - Basic SEC Filings Search

Source: https://docs.perplexity.ai/guides/sec-guide

This endpoint allows you to perform a basic search specifically targeting SEC filings by using the `search_mode: "sec"` parameter.

```APIDOC
## POST /chat/completions

### Description
Performs a chat completion request, with the option to filter results specifically for U.S. Securities and Exchange Commission (SEC) filings.

### Method
POST

### Endpoint
/chat/completions

### Parameters
#### Request Body
- **model** (string) - Required - The model to use for the completion (e.g., "sonar-pro").
- **messages** (array of objects) - Required - The conversation history, with each object having 'role' and 'content' fields.
  - **role** (string) - Required - The role of the message (e.g., "user").
  - **content** (string) - Required - The content of the message.
- **search_mode** (string) - Required - Set to "sec" to filter for SEC filings.

### Request Example
```json
{
  "model": "sonar-pro",
  "messages": [
    {
      "role": "user",
      "content": "Prepare me for markets opening."
    }
  ],
  "search_mode": "sec"
}
```

### Response
#### Success Response (200)
- **choices** (array) - An array of completion choices.
  - **message** (object) - The assistant's message.
    - **content** (string) - The content of the assistant's response.
    - **role** (string) - The role of the message (always "assistant").
  - **finish_reason** (string) - The reason the model stopped generating tokens.
  - **index** (integer) - The index of the choice.

#### Response Example
```json
{
  "choices": [
    {
      "message": {
        "content": "The market is expected to open with a focus on [details about market opening]...",
        "role": "assistant"
      },
      "finish_reason": "stop",
      "index": 0
    }
  ]
}
```
```

--------------------------------

### Filter Tech News Websites by Domain

Source: https://docs.perplexity.ai/guides/search-domain-filter-guide

This example demonstrates how to filter search results to include only articles from specific technology news websites using their domain names. It utilizes the `search_domain_filter` parameter with a list of allowed domains.

```Python
from perplexity import Perplexity

client = Perplexity()
response = client.search.create(
    query="latest tech trends 2025",
    max_results=10,
    search_domain_filter=[
        "techcrunch.com",
        "theverge.com",
        "arstechnica.com",
        "wired.com"
    ]
)

for result in response.results:
    print(f"{result.title}")
    print(f"Source: {result.url}")
    print(f"Date: {result.date}")
    print("---")
```

--------------------------------

### Advanced Usage: Multilingual Research

Source: https://docs.perplexity.ai/guides/search-language-filter

Example of conducting comprehensive research across multiple languages to cover different regions.

```APIDOC
## Advanced Usage: Multilingual Research

Conduct comprehensive research by searching across multiple languages:

```python
from perplexity import Perplexity

client = Perplexity()

# Research a global topic in multiple languages
languages = [
    ["en"],        # English-speaking countries
    ["zh", "ja"],  # East Asia
    ["es", "pt"],  # Latin America and Iberia
    ["fr", "de", "it"] # Western Europe
]

results_by_region = {}
for lang_group in languages:
    response = client.search.create(
        query="sustainable development goals progress",
        max_results=10,
        search_language_filter=lang_group
    )
    results_by_region[', '.join(lang_group)] = response.results

# Analyze results by language/region
for region, results in results_by_region.items():
    print(f"Results in {region}: {len(results)} found")
```
```

--------------------------------

### Limit Results by Publication Date Range (Python)

Source: https://docs.perplexity.ai/guides/date-range-filter-guide

A Python example demonstrating how to limit search results by a publication date range using the Perplexity SDK. It shows the instantiation of the client and the inclusion of date filters in the search parameters.

```python
from perplexity import Perplexity

client = Perplexity("YOUR_API_KEY")

response = client.search(
    query="your search query",
    search_after_date_filter="3/1/2025",
    search_before_date_filter="3/5/2025"
)
```

--------------------------------

### Concurrent Chat Operations (Python & TypeScript)

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Provides examples for handling multiple chat conversations concurrently using Python's `asyncio` and TypeScript's `Promise.all`. This enables efficient parallel processing of multiple user queries to the AI.

```python
async def handle_multiple_chats(user_messages):
    client = AsyncPerplexity()
    tasks = [
        client.chat.completions.create(
            messages=[{"role": "user", "content": msg}],
            model="sonar-deep-reseach"
        )
        for msg in user_messages
    ]
    return await asyncio.gather(*tasks, return_exceptions=True)
```

```javascript
async function processQuestions(questions: string[]) {
    const tasks = questions.map(question => client.chat.completions.create({
        messages: [ { role: "user", content: question } ],
        model: "sonar-deep-research"
    }));
    const results = await Promise.all(tasks);
    return results.map(result => result.choices[0].message.content);
}

const questions = [
    "What is artificial intelligence?",
    "How does machine learning work?",
    "What are neural networks?"
];
const answers = await processQuestions(questions);
```

--------------------------------

### Get Async Chat Completion Status

Source: https://docs.perplexity.ai/api-reference/async-chat-completions-post

Retrieves the status and results of an asynchronous chat completion job using its unique identifier.

```APIDOC
## GET /chat/completions/{id}

### Description
Retrieves the status and results of a previously created asynchronous chat completion job.

### Method
GET

### Endpoint
/chat/completions/{id}

### Parameters
#### Path Parameters
- **id** (string) - Required - The unique identifier for the asynchronous job.

#### Query Parameters
None

### Request Example
```
GET /chat/completions/chatcmpl-xxxxxxxxxxxxxxxxx
```

### Response
#### Success Response (200)
- **id** (string) - Unique identifier for the asynchronous job.
- **model** (string) - The model used for the request.
- **created_at** (integer) - Unix timestamp of when the job was created.
- **status** (enum) - The status of an asynchronous processing job. Available options: `CREATED`, `IN_PROGRESS`, `COMPLETED`, `FAILED`.
- **started_at** (integer | null) - Unix timestamp of when processing started.
- **completed_at** (integer | null) - Unix timestamp of when processing completed.
- **response** (object | null) - The actual chat completion response, available when status is COMPLETED.
- **failed_at** (integer | null) - Unix timestamp of when processing failed.
- **error_message** (string | null) - Error message if the job failed.

#### Response Example
```json
{
  "id": "chatcmpl-xxxxxxxxxxxxxxxxx",
  "model": "gpt-4",
  "created_at": 1677652715,
  "status": "COMPLETED",
  "started_at": 1677652720,
  "completed_at": 1677652800,
  "response": {
    "choices": [
      {
        "message": {
          "role": "assistant",
          "content": "The weather today is sunny."
        },
        "finish_reason": "stop"
      }
    ]
  },
  "failed_at": null,
  "error_message": null
}
```
```

--------------------------------

### cURL: Perform Web Search with Perplexity API

Source: https://docs.perplexity.ai/chat-with-persistence

This example shows how to perform a web search using the Perplexity API via cURL. It constructs a POST request to the search endpoint with a JSON payload containing the search query. This is useful for testing or integrating with systems that do not have direct SDK support.

```bash
curl -X POST "https://api.perplexity.ai/search"
  -H "Authorization: Bearer YOUR_API_KEY"
  -H "Content-Type: application/json"
  -d '{ "query": "What is Comet Browser?" }'
```

--------------------------------

### Minimal Search Context with Sonar (cURL)

Source: https://docs.perplexity.ai/guides/search-context-size-guide

This cURL command illustrates how to make a POST request to the Perplexity API to retrieve chat completions using the 'sonar' model with a `search_context_size` set to 'low'. This is recommended for cost optimization when answer completeness is less critical.

```curl
curl --request POST \
--url https://api.perplexity.ai/chat/completions \
--header "Authorization: Bearer $SONAR_API_KEY" \
--header "Content-Type: application/json" \
--data '{ \
  "model": "sonar", \
  "messages": [ \
    { "role": "system", "content": "Be precise and concise." }, \
    { "role": "user", "content": "How many stars are there in our galaxy?" } \
  ], \
  "web_search_options": { \
    "search_context_size": "low" \
  }
}' | jq
```

--------------------------------

### Enable JSON Schema Structured Outputs

Source: https://docs.perplexity.ai/guides/structured-outputs

This JSON snippet shows how to configure the `response_format` field in your API request to enable structured JSON outputs using a specified JSON schema.

```json
{
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "schema": {
        /* your JSON schema object */
      }
    }
  }
}
```

--------------------------------

### Search Wikipedia Across Languages using Root Domain

Source: https://docs.perplexity.ai/guides/search-domain-filter-guide

This example demonstrates how to search across all language editions of Wikipedia by specifying the root domain 'wikipedia.org'. This utilizes the `search_domain_filter` to match all subdomains associated with Wikipedia.

```Python
from perplexity import Perplexity

client = Perplexity()
# Matches en.wikipedia.org, fr.wikipedia.org, de.wikipedia.org, etc.
response = client.search.create(
    query="quantum mechanics",
    max_results=10,
    search_domain_filter=["wikipedia.org"]
)

for result in response.results:
    print(f"{result.title}")
    print(f"URL: {result.url}")
    print("---")
```

--------------------------------

### Denylist Specific Domains from Search Results

Source: https://docs.perplexity.ai/guides/search-domain-filter-guide

This example illustrates how to exclude specific domains, such as social media and Q&A sites, from search results. It uses the `search_domain_filter` with a minus prefix (-) before the domain names to create a denylist.

```Python
from perplexity import Perplexity

client = Perplexity()
# Exclude social media and Q&A sites from search results
response = client.search.create(
    query="latest advancements in renewable energy",
    max_results=10,
    search_domain_filter=[
        "-pinterest.com",
        "-reddit.com",
        "-quora.com"
    ]
)

for result in response.results:
    print(f"{result.title}: {result.url}")
```

--------------------------------

### Advanced Usage: Academic Research Across Languages

Source: https://docs.perplexity.ai/guides/search-language-filter

Example of searching for scholarly content in different languages, potentially across specific academic domains.

```APIDOC
## Advanced Usage: Academic Research Across Languages

Access scholarly content in different languages:

```python
# Search for research papers in multiple languages
response = client.search.create(
    query="quantum computing algorithms",
    max_results=20,
    search_language_filter=["en", "de", "fr", "ru"],
    search_domain_filter=["arxiv.org", "nature.com", "science.org"]
)
```
```

--------------------------------

### Search with Start Date Filter (Python)

Source: https://docs.perplexity.ai/guides/search-date-time-filters

Performs a search query and filters results to include only content published on or after a specific date. Requires the perplexity library. Returns a response object.

```python
from perplexity import Perplexity
client = Perplexity()
response = client.search(
  query="tech news published after March 1, 2025",
  max_results=10,
  search_after_date="3/1/2025"
)
print(response)
```

--------------------------------

### Filter by Recency (Python)

Source: https://docs.perplexity.ai/guides/search-date-time-filters

This Python example filters search results to include only content from the past week using the `search_recency_filter` parameter.

```Python
from perplexity import Perplexity

client = Perplexity(api_key="YOUR_API_KEY")

response = client.search(query="example query", 
    search_recency_filter="week")

print(response)
```

--------------------------------

### Initialize ChatSummaryMemoryBuffer with Perplexity Sonar API

Source: https://docs.perplexity.ai/cookbook/articles/memory-management/chat-summary-memory-buffer/README

Initializes the ChatSummaryMemoryBuffer for token-aware summarization. It reserves 25% of the Sonar API's context window for responses and utilizes a shared LLM instance for both summarization and chat completion. This setup is crucial for managing conversation history within token limits.

```python
memory = ChatSummaryMemoryBuffer.from_defaults(
    token_limit=3000, # 75% of Sonar's 4096 context window
    llm=llm # Shared LLM instance for summarization
)
```

--------------------------------

### Filter by Search Recency (Python)

Source: https://docs.perplexity.ai/guides/date-range-filter-guide

This Python example shows how to use the `search_recency_filter` to easily filter results by predefined time periods like 'week', 'month', or 'year', without specifying exact dates.

```python
from perplexity import Perplexity

client = Perplexity()
completion = client.chat.completions.create(
    model="sonar-pro",
    messages=[
        {"role": "system", "content": "You are an expert on current events."},
        {"role": "user", "content": "What are the latest AI developments?"}
    ],
    search_recency_filter="week"
)

print(completion.choices[0].message.content)
```

--------------------------------

### Filter by Last Updated Date Range (Python)

Source: https://docs.perplexity.ai/guides/date-range-filter-guide

This Python example demonstrates filtering Perplexity AI search results based on when the content was last updated, using `last_updated_after_filter` and `last_updated_before_filter`.

```python
from perplexity import Perplexity

client = Perplexity()
completion = client.chat.completions.create(
    model="sonar-pro",
    messages=[
        {"role": "system", "content": "You are an expert on current events."},
        {"role": "user", "content": "Show me recently updated tech articles."}
    ],
    last_updated_after_filter="3/1/2025",
    last_updated_before_filter="3/5/2025"
)

print(completion.choices[0].message.content)
```

--------------------------------

### Trend Analysis by Comparing Time Periods

Source: https://docs.perplexity.ai/guides/search-date-time-filters

Provides an example of trend analysis by executing multiple searches with different date filters. This allows for comparing recent trends against historical data to identify patterns and changes over time.

```python
# Recent trends
recent = client.search(
    query="machine learning trends",
    search_recency_filter="month"
)

# Older trends for comparison
older = client.search(
    query="machine learning trends",
    search_after_date="1/1/2023",
    search_before_date="1/31/2023"
)
```

--------------------------------

### Model Selection

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Demonstrates how to select different Sonar models for various query complexities.

```APIDOC
## Model Selection Examples

### Description
Perplexity offers several Sonar models optimized for different tasks. Choose the appropriate model based on the complexity and nature of your query.

### Available Models
- **sonar**: Standard model for general queries.
- **sonar-pro**: For more complex queries requiring deeper analysis.
- **sonar-reasoning-pro**: For complex analytical tasks, including step-by-step problem-solving.

### Request Examples

#### Standard Sonar Model
```json
{
  "messages": [
    { "role": "user", "content": "What is quantum computing?" }
  ],
  "model": "sonar"
}
```

#### Sonar Pro Model
```json
{
  "messages": [
    { "role": "user", "content": "Analyze the economic implications of renewable energy adoption" }
  ],
  "model": "sonar-pro"
}
```

#### Sonar Reasoning Pro Model
```json
{
  "messages": [
    { "role": "user", "content": "Solve this complex mathematical problem step by step" }
  ],
  "model": "sonar-reasoning-pro"
}
```
```

--------------------------------

### Comprehensive Search Context with Sonar (cURL)

Source: https://docs.perplexity.ai/guides/search-context-size-guide

This cURL command demonstrates how to make a POST request to the Perplexity API for chat completions using the 'sonar' model with `search_context_size` set to 'high'. This maximizes search context for more thorough and nuanced responses, suitable for deep research.

```curl
curl --request POST \
--url https://api.perplexity.ai/chat/completions \
--header "Authorization: Bearer $SONAR_API_KEY" \
--header "Content-Type: application/json" \
--data '{ \
  "model": "sonar", \
  "messages": [ \
    { "role": "system", "content": "Be precise and concise." }, \
    { "role": "user", "content": "How many stars are there in our galaxy?" } \
  ], \
  "web_search_options": { \
    "search_context_size": "high" \
  }
}' | jq
```

--------------------------------

### Enhanced Search Results in API Responses

Source: https://docs.perplexity.ai/changelog/changelog

This example shows the structure of the new 'search_results' field in API responses, which provides detailed information about the search results used by the models. This replaces the deprecated 'citations' field and offers more transparency, including title, URL, and publication date for each result.

```json
"search_results": [
  {
    "title": "Understanding Large Language Models",
    "url": "https://example.com/llm-article",
    "date": "2023-12-25"
  },
  {
    "title": "Advances in AI Research",
    "url": "https://example.com/ai-research",
    "date": "2024-03-15"
  }
]
```

--------------------------------

### JSON Schema Definition: Perplexity vs. Other Providers

Source: https://docs.perplexity.ai/guides/structured-outputs

Compares the JSON schema definition syntax between Perplexity AI and other providers. Perplexity offers a simplified schema definition by automatically handling naming and strictness, requiring only the core schema object.

```json
{
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "financial_data",
      "strict": true,
      "schema": {
        /* your schema */
      }
    }
  }
}
```

```json
{
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "schema": {
        /* your schema */
      }
    }
  }
}
```

--------------------------------

### Limit Results by Publication Date Range (TypeScript)

Source: https://docs.perplexity.ai/guides/date-range-filter-guide

A TypeScript example showcasing how to limit search results by a publication date range using the Perplexity SDK. It includes client initialization and the application of date filters within the search request.

```typescript
import Perplexity from "perplexity-sdk";

const client = new Perplexity("YOUR_API_KEY");

const response = await client.search({
  query: "your search query",
  search_after_date_filter: "3/1/2025",
  search_before_date_filter: "3/5/2025"
});
```

--------------------------------

### Set Sonar Search Context Size to Medium (JSON)

Source: https://docs.perplexity.ai/guides/search-context-size-guide

This JSON snippet demonstrates how to set the `search_context_size` to 'medium' within the `web_search_options` object in an API request payload. This is useful for balancing cost and comprehensiveness in search results.

```json
{
  "web_search_options": {
    "search_context_size": "medium"
  }
}
```

--------------------------------

### Basic Chat Completion with System Message (Python & TypeScript)

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Demonstrates how to initiate a chat completion request using the Perplexity AI SDK. It includes setting up a system message and user prompts, followed by calling the chat completions endpoint with a specified model. This is fundamental for conversational AI interactions.

```python
messages = [
  {"role": "system", "content": "You are a helpful research assistant."},
  {"role": "user", "content": "What are the main causes of climate change?"},
  {"role": "assistant", "content": "The main causes of climate change include..."},
  {"role": "user", "content": "What are some potential solutions?"}
]
completion = client.chat.completions.create(
  messages=messages,
  model="sonar"
)
```

```typescript
const messages: Perplexity.ChatMessage[] = [
  { role: "system", content: "You are a helpful research assistant." },
  { role: "user", content: "What are the main causes of climate change?" },
  { role: "assistant", content: "The main causes of climate change include..." },
  { role: "user", content: "What are some potential solutions?" }
];
const completion = await client.chat.completions.create({
  messages,
  model: "sonar"
});
```

--------------------------------

### Call Perplexity API Chat Completions with Sonar Pro (Python)

Source: https://docs.perplexity.ai/getting-started/models/models/sonar-pro

This Python code snippet illustrates how to use the Perplexity API for chat completions with the 'sonar-pro' model. It sends a user query and receives a detailed response including usage statistics, citations, and search result snippets. This example is useful for integrating Perplexity's advanced search capabilities into Python applications.

```python
import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("PERPLEXITY_API_KEY"),
    base_url="https://api.perplexity.ai",
)

chat_completion = client.chat.completions.create(
    model="sonar-pro",
    messages=[
        {
            "role": "user",
            "content": "Analyze the competitive positioning of Perplexity in the AI search market and evaluate how Comet compares to similar offerings from other companies."
        }
    ],
)

print(json.dumps(chat_completion, indent=2))
```

--------------------------------

### Filter by Publication Date Range (Python)

Source: https://docs.perplexity.ai/guides/date-range-filter-guide

This example demonstrates how to filter Perplexity AI search results to include content published within a specific date range. It uses the `search_after_date_filter` and `search_before_date_filter` parameters.

```python
from perplexity import Perplexity

client = Perplexity()
completion = client.chat.completions.create(
    model="sonar",
    messages=[
        {"role": "system", "content": "You are an expert on current events."},
        {"role": "user", "content": "Show me tech news published this week."}
    ],
    search_after_date_filter="3/1/2025",
    search_before_date_filter="3/5/2025"
)

print(completion.choices[0].message.content)
```

--------------------------------

### Constrain Search Results by Recency

Source: https://docs.perplexity.ai/guides/date-range-filter-guide

This example illustrates how to use the `search_recency_filter` to easily filter results by predefined time periods relative to the current date, such as 'day', 'week', 'month', or 'year'.

```json
{
  "search_recency_filter": "week"
}
```

--------------------------------

### Constrain Search Results by Last Updated Date

Source: https://docs.perplexity.ai/guides/date-range-filter-guide

This example shows how to use `last_updated_after_filter` and `last_updated_before_filter` to filter search results based on when the content was last modified. The dates should be provided in 'MM/DD/YYYY' format.

```json
{
  "last_updated_after_filter": "3/1/2025",
  "last_updated_before_filter": "3/5/2025"
}
```

--------------------------------

### Constrain Search Results by Publication Date

Source: https://docs.perplexity.ai/guides/date-range-filter-guide

This example demonstrates how to use `search_after_date_filter` and `search_before_date_filter` to restrict search results to content published within a specific date range. The dates must be in 'MM/DD/YYYY' format.

```json
{
  "search_after_date_filter": "3/1/2025",
  "search_before_date_filter": "3/5/2025"
}
```

--------------------------------

### Web Search Configuration for Chat Completion (Python & TypeScript)

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Shows how to configure web search options for chat completions. This allows the model to focus on recent information or specific trusted domains, enhancing search relevance. Useful for research-oriented queries.

```python
completion = client.chat.completions.create(
  messages=[
    {"role": "user", "content": "What are the latest developments in renewable energy?"}
  ],
  model="sonar",
  web_search_options={
    "search_recency_filter": "week", # Focus on recent results
    "search_domain_filter": ["energy.gov", "iea.org", "irena.org"], # Trusted sources
    "max_search_results": 10
  }
)
```

```typescript
const completion = await client.chat.completions.create({
  messages: [
    {
      role: "user",
      content: "What are the latest developments in renewable energy?"
    }
  ],
  model: "sonar",
  search_recency_filter: "week", // Focus on recent results
  search_domain_filter: ["energy.gov", "iea.org", "irena.org"], // Trusted sources
  return_images: true, // Include image URLs
  return_related_questions: true // Get follow-up questions
});
```

--------------------------------

### Model Selection for Chat Completions (TypeScript)

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Demonstrates selecting various Sonar models for chat completions in TypeScript according to the query's nature. It covers using 'sonar' for general questions, 'sonar-pro' for in-depth analysis, and 'sonar-reasoning-pro' for advanced reasoning tasks.

```typescript
// Standard Sonar model for general queries
const completion = await client.chat.completions.create({
  messages: [{ role: "user", content: "What is quantum computing?" }],
  model: "sonar"
});

// Sonar Pro for more complex queries
const completion = await client.chat.completions.create({
  messages: [{ role: "user", content: "Analyze the economic implications of renewable energy adoption" }],
  model: "sonar-pro"
});

// Sonar Reasoning Pro for complex analytical tasks
const completion = await client.chat.completions.create({
  messages: [{ role: "user", content: "Solve this complex mathematical problem step by step" }],
  model: "sonar-reasoning-pro"
});
```

--------------------------------

### Filter by Publication Date (Single Parameter, cURL)

Source: https://docs.perplexity.ai/guides/date-range-filter-guide

This example shows how to restrict Perplexity AI search results to content published on or after a specific date using the `search_after_date_filter` parameter in a JSON payload for cURL.

```json
{
  "model": "sonar-pro",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Show me news articles published after March 1, 2025."}
  ],
  "search_after_date_filter": "3/1/2025"
}
```

--------------------------------

### Limit Results by Publication Date Range (cURL)

Source: https://docs.perplexity.ai/guides/date-range-filter-guide

A cURL example demonstrating how to limit search results by a publication date range using the Perplexity API. It shows the necessary headers and the JSON payload with date filters.

```bash
curl -X POST "https://api.perplexity.ai/chat/completions" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{ 
       "model": "pplx-7b-online", 
       "messages": [{"role": "user", "content": "search your search query"}], 
       "search_parameters": {
         "search_after_date_filter": "3/1/2025",
         "search_before_date_filter": "3/5/2025"
       }
     }'
```

--------------------------------

### Initialize Perplexity Client and Make Chat Completion Request (Python)

Source: https://docs.perplexity.ai/guides/chat-completions-guide

Initializes the OpenAI client for Perplexity AI using an API key and base URL. It then makes a chat completion request with specified model, messages, and search domain/recency filters. The response content and the number of found articles are printed.

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.perplexity.ai"
)

response = client.chat.completions.create(
    model="sonar-pro",
    messages=[
        {"role": "user", "content": "Latest climate research findings"}
    ],
    extra_body={
        "search_domain_filter": ["nature.com", "science.org"],
        "search_recency_filter": "month"
    }
)

print(response.choices[0].message.content)
print(f"Sources: {len(response.search_results)} articles found")
```

--------------------------------

### Custom Instructions with System Messages (Python & TypeScript)

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Explains how to use system messages for custom instructions in chat completions with both Python and TypeScript. This allows defining specific roles or behaviors for the AI, ensuring consistent responses tailored to the defined persona.

```python
system_prompt = """You are an expert research assistant specializing in technology and science. Always provide well-sourced, accurate information and cite your sources. Format your responses with clear headings and bullet points when appropriate."""
completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Explain quantum computing applications"}
    ],
    model="sonar-pro"
)
```

```javascript
const systemPrompt = `You are an expert research assistant specializing in technology and science. Always provide well-sourced, accurate information and cite your sources. Format your responses with clear headings and bullet points when appropriate.`;
const completion = await client.chat.completions.create({
    messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: "Explain quantum computing applications" }
    ],
    model: "sonar-pro"
});
```

--------------------------------

### Display Reasoning Steps for Transparency in Python

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

Provides a function to display reasoning steps from Perplexity AI's API response. This helps users understand the AI's thought process and build trust.

```python
def display_reasoning(step):
    """Show reasoning to users"""
    # Assuming 'step' is a chunk object with 'web_search' and 'thought' attributes
    # if hasattr(step, 'web_search'):
    #     print(f"🔍 Searching for: {step.web_search.search_keywords}")
    # print(f"💭 {step.thought}")
    pass # Placeholder for actual implementation

```

--------------------------------

### Deploy Briefo Edge Functions

Source: https://docs.perplexity.ai/cookbook/showcase/briefo

Commands to deploy the Edge Functions for the Briefo application. These functions interact with external APIs like Perplexity, Alpaca, and Alpha Vantage.

```bash
supabase functions deploy perplexity-news
supabase functions deploy perplexity-chat
supabase functions deploy perplexity-research
supabase functions deploy portfolio-tab-data
```

--------------------------------

### Model Selection for Chat Completions (Python)

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Shows how to select different Sonar models for chat completions in Python based on query complexity. Options include the standard 'sonar' for general queries, 'sonar-pro' for complex analysis, and 'sonar-reasoning-pro' for intricate problem-solving.

```python
# Standard Sonar model for general queries
completion = client.chat.completions.create(
  messages=[{"role": "user", "content": "What is quantum computing?"}],
  model="sonar"
)

# Sonar Pro for more complex queries
completion = client.chat.completions.create(
  messages=[{"role": "user", "content": "Analyze the economic implications of renewable energy adoption"}],
  model="sonar-pro"
)

# Sonar Reasoning Pro for complex analytical tasks
completion = client.chat.completions.create(
  messages=[{"role": "user", "content": "Solve this complex mathematical problem step by step"}],
  model="sonar-reasoning-pro"
)
```

--------------------------------

### Best Practices: Model Selection

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Guidance on choosing the most appropriate Perplexity AI model based on the specific use case, ranging from general queries to complex analysis.

```APIDOC
## POST /chat/completions (Model Selection)

### Description
Provides recommendations for selecting the optimal model based on the task requirements.

### Method
POST

### Endpoint
`/chat/completions`

### Parameters
#### Request Body
- **messages** (array) - Required - An array of message objects.
- **model** (string) - Required - The model to use for the completion. Options include:
    - `sonar`: For quick factual queries.
    - `sonar-pro`: For complex analysis.
    - `sonar-reasoning-pro`: For analytical tasks requiring reasoning.

### Request Example (Python)
```python
# For quick factual queries
simple_query = client.chat.completions.create(
    messages=[{"role": "user", "content": "What is the capital of France?"}],
    model="sonar"
)

# For complex analysis
complex_query = client.chat.completions.create(
    messages=[{"role": "user", "content": "Analyze the economic impact of AI on employment"}],
    model="sonar-pro"
)
```

### Request Example (TypeScript)
```typescript
// For quick factual queries
const simpleQuery = await client.chat.completions.create({
  messages: [{ role: "user", content: "What is the capital of France?" }],
  model: "sonar"
});

// For complex analysis
const complexQuery = await client.chat.completions.create({
  messages: [{ role: "user", content: "Analyze the economic impact of AI on employment" }],
  model: "sonar-pro"
});
```
```

--------------------------------

### Filter Content Updated Within a Date Range (cURL)

Source: https://docs.perplexity.ai/guides/date-range-filter-guide

This cURL example shows how to retrieve content updated within a specific date range using both 'last_updated_after_filter' and 'last_updated_before_filter'. The date format required is MM/DD/YYYY. The SONAR_API_KEY must be set as an environment variable.

```curl
curl --location 'https://api.perplexity.ai/chat/completions' \
--header "Authorization: Bearer $SONAR_API_KEY" \
--header "Content-Type: application/json" \
--data '{ "model": "sonar-pro", "messages": [ {"role": "system", "content": "You are an expert on technology trends."}, {"role": "user", "content": "Show me tech articles that were updated last week."} ], "last_updated_after_filter": "2/24/2025", "last_updated_before_filter": "3/3/2025" }' | jq
```

--------------------------------

### Grounded LLM Chat Completions

Source: https://docs.perplexity.ai/financial-news-tracker

Build AI applications with web-grounded chat completions and reasoning models using the Sonar model.

```APIDOC
## POST /chat/completions

### Description
Build AI applications with web-grounded chat completions and reasoning models.

### Method
POST

### Endpoint
/chat/completions

### Parameters
#### Request Body
- **model** (string) - Required - The model to use (e.g., 'sonar').
- **messages** (array) - Required - An array of message objects, each with 'role' ('user' or 'assistant') and 'content'.
- **stream** (boolean) - Optional - Whether to stream the response.

### Request Example
```json
{
  "model": "sonar",
  "messages": [
    {
      "role": "user",
      "content": "What is the weather like today?"
    }
  ],
  "stream": false
}
```

### Response
#### Success Response (200)
- **choices** (array) - An array of response choices, each containing 'message' with 'role' and 'content'.

#### Response Example
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "The weather today is sunny with a high of 75 degrees Fahrenheit."
      }
    }
  ]
}
```
```

--------------------------------

### Language Filtering for Perplexity AI Web Search

Source: https://docs.perplexity.ai/guides/search-quickstart

Filters search results to include only specified languages using ISO 639-1 language codes. Up to 10 language codes can be specified per request for targeted content retrieval. Examples include 'en' for English, 'fr' for French.

```python
from perplexity import Perplexity

client = Perplexity()
# Search for English, French, and German language results
search = client.search.create(
    query="latest AI news",
    search_language_filter=["en", "fr", "de"],
    max_results=10
)

for result in search.results:
    print(f"{result.title}: {result.url}")
```

--------------------------------

### Python: Perplexity AI Search API Call

Source: https://docs.perplexity.ai/chat-summary-memory-buffer

Demonstrates how to perform a search using the Perplexity AI SDK in Python. It initializes the client, makes a search request with multiple queries, and prints the title and URL of each result. Requires the 'perplexity' library.

```python
from perplexity import Perplexity

client = Perplexity()
search = client.search.create(
    query=[
        "What is Comet Browser?",
        "Perplexity AI",
        "Perplexity Changelog"
    ]
)

for result in search.results:
    print(f"{result.title}: {result.url}")
```

--------------------------------

### Implement Chunk Routing with Type Checking in Python

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

Shows how to use the `object` field of a chunk to route it to the appropriate handler function. This ensures correct processing based on the chunk type.

```python
def handle_reasoning(chunk):
    pass # Placeholder
def handle_reasoning_done(chunk):
    pass # Placeholder
def handle_content(chunk):
    pass # Placeholder
def handle_done(chunk):
    pass # Placeholder

chunk_handlers = {
    "chat.reasoning": handle_reasoning,
    "chat.reasoning.done": handle_reasoning_done,
    "chat.completion.chunk": handle_content,
    "chat.completion.done": handle_done
}

# Assuming 'chunk' is a processed chunk object
# handler = chunk_handlers.get(chunk.object)
# if handler:
#     handler(chunk)

```

--------------------------------

### Enable Streaming Completion (Python)

Source: https://docs.perplexity.ai/guides/streaming-responses

This Python code snippet demonstrates how to initiate a streaming chat completion request using the Perplexity SDK. It requires the 'perplexity' library and an API key set as an environment variable. The output is printed as it is received.

```python
from perplexity import Perplexity

# Initialize the client (uses PERPLEXITY_API_KEY environment variable)
client = Perplexity()

# Create streaming completion
stream = client.chat.completions.create(
    model="sonar",
    messages=[{"role": "user", "content": "What is the latest in AI research?"}],
    stream=True
)

# Process streaming response
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

--------------------------------

### Demonstrate Multi-Turn Conversation with Memory Persistence

Source: https://docs.perplexity.ai/cookbook/articles/memory-management/chat-summary-memory-buffer/README

Illustrates a multi-turn conversation using the ChatSummaryMemoryBuffer integrated with the Perplexity API. It shows how to handle follow-up questions contextually and demonstrates session persistence by saving and loading the conversation memory to a JSON file.

```python
# Initial query about astronomy
print(chat_with_memory("What causes neutron stars to form?"))

# Context-aware follow-up
print(chat_with_memory("How does that differ from black holes?"))

# Session persistence demo
memory.persist("astrophysics_chat.json")

# New session loading
loaded_memory = ChatSummaryMemoryBuffer.from_defaults(
    persist_path="astrophysics_chat.json",
    llm=llm
)
print(chat_with_memory("Recap our previous discussion"))
```

--------------------------------

### Custom Instructions with System Messages

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Utilize system messages to provide consistent behavior and context for the AI model, such as defining its role or specific instructions.

```APIDOC
## POST /chat/completions (Custom Instructions)

### Description
Sets custom instructions for the AI model using system messages to guide its behavior and responses.

### Method
POST

### Endpoint
`/chat/completions`

### Parameters
#### Request Body
- **messages** (array) - Required - An array of message objects, including a system message.
  - **role** (string) - 'system' for custom instructions.
  - **content** (string) - The content of the system message.
- **model** (string) - Required - The model to use for the completion.

### Request Example (Python)
```python
system_prompt = """You are an expert research assistant specializing in technology and science. Always provide well-sourced, accurate information and cite your sources. Format your responses with clear headings and bullet points when appropriate."""
completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Explain quantum computing applications"}
    ],
    model="sonar-pro"
)
```

### Request Example (TypeScript)
```typescript
const systemPrompt = `You are an expert research assistant specializing in technology and science. Always provide well-sourced, accurate information and cite your sources. Format your responses with clear headings and bullet points when appropriate.`;
const completion = await client.chat.completions.create({
  messages: [
    { role: "system", content: systemPrompt },
    { role: "user", content: "Explain quantum computing applications" }
  ],
  model: "sonar-pro"
});
```
```

--------------------------------

### Understanding Concise Stream Mode Chunks

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

Details the different types of chunks received when using `stream_mode: "concise"`. Includes descriptions for `chat.reasoning`, `chat.reasoning.done`, `chat.completion.chunk`, and `chat.completion.done`.

```APIDOC
## Concise Stream Mode Chunk Types

### Description
When `stream_mode` is set to `"concise"`, the API returns distinct chunk types to represent different stages of the response generation, optimizing for bandwidth and clarity.

### Chunk Types:

1.  **`chat.reasoning`**
    *   **Description:** Streamed during the reasoning stage, containing real-time reasoning steps and search operations. This chunk provides insight into the model's thought process before generating the final completion.
    *   **Fields:** Includes `reasoning_steps` which details thoughts, types of operations (e.g., `web_search`), and search results or keywords.
    *   **Example:**
        ```json
        {
          "id": "cfa38f9d-fdbc-4ac6-a5d2-a3010b6a33a6",
          "model": "sonar-pro",
          "created": 1759441590,
          "object": "chat.reasoning",
          "choices": [
            {
              "index": 0,
              "finish_reason": null,
              "message": {
                "role": "assistant",
                "content": ""
              },
              "delta": {
                "role": "assistant",
                "content": "",
                "reasoning_steps": [
                  {
                    "thought": "Searching the web for Seattle's current weather...",
                    "type": "web_search",
                    "web_search": {
                      "search_results": [],
                      "search_keywords": ["Seattle current weather"]
                    }
                  }
                ]
              }
            }
          ],
          "type": "message"
        }
        ```

2.  **`chat.reasoning.done`**
    *   **Description:** Indicates the end of the reasoning stage. No further reasoning steps will be provided in subsequent chunks.
    *   **Fields:** Typically contains `finish_reason` if applicable to the reasoning stage.

3.  **`chat.completion.chunk`**
    *   **Description:** Contains incremental parts of the final completion message content. This is similar to the traditional `chat.completion.chunk` but appears after the reasoning stage is complete.
    *   **Fields:** `choices[0].delta.content` provides the text fragment.

4.  **`chat.completion.done`**
    *   **Description:** Marks the final chunk of the streaming response, indicating that the entire completion has been sent. It includes the final `finish_reason`.
    *   **Fields:** Includes `finish_reason` (e.g., "stop", "length").
```

--------------------------------

### Async Chat Completion Request Creation (Python & TypeScript)

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Explains how to initiate an asynchronous chat completion request, suitable for long-running tasks with the 'sonar-deep-research' model. It shows how to submit the request and retrieve initial details like request ID and status.

```python
# Start an async completion request
async_request = client.async_.chat.completions.create(
  messages=[
    {"role": "user", "content": "Write a comprehensive analysis of renewable energy trends"}
  ],
  model="sonar-deep-research",
  max_tokens=2000
)
print(f"Request submitted with ID: {async_request.request_id}")
print(f"Status: {async_request.status}")
```

```typescript
// Start an async completion request
const asyncRequest = await client.async.chat.completions.create({
  messages: [
    {
      role: "user",
      content: "Write a comprehensive analysis of renewable energy trends"
    }
  ],
  model: "sonar-deep-reasearch",
  max_tokens: 2000
});
console.log(`Request submitted with ID: ${asyncRequest.request_id}`);
console.log(`Status: ${asyncRequest.status}`);
```

--------------------------------

### Perplexity API Key in .env file

Source: https://docs.perplexity.ai/guides/search-quickstart

Demonstrates how to store the Perplexity API key in a `.env` file. This is a common practice for managing environment-specific configurations and secrets.

```env
PERPLEXITY_API_KEY=your_api_key_here
```

--------------------------------

### Enable Concise Stream Mode in Python

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

Demonstrates how to enable and process responses in 'concise' stream mode using the Perplexity Python SDK. It iterates through chunks, printing content when available.

```python
from perplexity import Perplexity

client = Perplexity()
stream = client.chat.completions.create(
    model="sonar-pro",
    messages=[{"role": "user", "content": "What's the weather in Seattle?"}],
    stream=True,
    stream_mode="concise"
)

for chunk in stream:
    print(f"Chunk type: {chunk.object}")
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

--------------------------------

### POST /chat/completions (File Attachments with Sonar)

Source: https://docs.perplexity.ai/guides/file-attachments

Analyze documents by uploading them via public URLs or base64 encoded bytes using Sonar models. Supports summarization, question answering, and content extraction.

```APIDOC
## POST /chat/completions (File Attachments with Sonar)

### Description
Analyze documents by uploading them via public URLs or base64 encoded bytes using Sonar models. This endpoint supports various document formats including PDF, DOC, DOCX, TXT, and RTF, with a maximum file size of 50MB.

### Method
POST

### Endpoint
`/chat/completions`

### Parameters
#### Query Parameters
None

#### Request Body
```json
{
  "model": "string",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "string"
        },
        {
          "type": "file_url",
          "file_url": {
            "url": "string"
          },
          "file_name": "string" 
        }
      ]
    }
  ],
  "max_tokens": "integer (optional)",
  "temperature": "number (optional)",
  "stream": "boolean (optional)"
}
```

- **model** (string) - Required - The Sonar model to use (e.g., "sonar-pro").
- **messages** (array) - Required - An array of message objects.
  - **role** (string) - Required - The role of the message sender ('user').
  - **content** (array) - Required - An array containing message parts.
    - **type** (string) - Required - The type of content ('text' or 'file_url').
    - **text** (string) - Required if type is 'text' - The user's textual query.
    - **file_url** (object) - Required if type is 'file_url' - Contains the file information.
      - **url** (string) - Required - The public URL of the file or the base64 encoded file content.
    - **file_name** (string) - Optional - The name of the file, especially useful for base64 encoded files.
- **max_tokens** (integer) - Optional - The maximum number of tokens to generate.
- **temperature** (number) - Optional - Controls the randomness of the output. Higher values mean more random output.
- **stream** (boolean) - Optional - Whether to stream the response.

### Request Example
**Using a Public URL:**
```json
{
  "messages": [
    {
      "content": [
        {
          "type": "text",
          "text": "Summarize this document"
        },
        {
          "type": "file_url",
          "file_url": {
            "url": "https://example.com/document.pdf"
          }
        }
      ],
      "role": "user"
    }
  ],
  "model": "sonar-pro"
}
```

**Using Base64 Encoded Bytes:**
```json
{
  "messages": [
    {
      "content": [
        {
          "type": "text",
          "text": "Summarize this document"
        },
        {
          "type": "file_url",
          "file_url": {
            "url": "JVBERi0xLjQKJeLjz9MKNCAwIG9iago..."
          },
          "file_name": "report.pdf"
        }
      ],
      "role": "user"
    }
  ],
  "model": "sonar-pro"
}
```

### Response
#### Success Response (200)
```json
{
  "id": "chatcmpl-xxxxxxxxxxxxxxxxx",
  "object": "chat.completion",
  "created": 1700000000,
  "model": "sonar-pro",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "This document is a research paper detailing advancements in AI model training techniques..."
      },
      "logprobs": null
    }
  ],
  "usage": {
    "prompt_tokens": 100,
    "completion_tokens": 200,
    "total_tokens": 300
  }
}
```

- **id** (string) - Unique identifier for the completion.
- **object** (string) - Type of the object returned.
- **created** (integer) - Timestamp of creation.
- **model** (string) - The model used for the completion.
- **choices** (array) - An array of completion choices.
  - **index** (integer) - The index of the choice.
  - **message** (object) - The message object.
    - **role** (string) - The role of the message sender ('assistant').
    - **content** (string) - The generated content from the assistant.
  - **logprobs** (null) - Placeholder for log probabilities.
- **usage** (object) - Token usage statistics.
  - **prompt_tokens** (integer) - Number of tokens in the prompt.
  - **completion_tokens** (integer) - Number of tokens in the completion.
  - **total_tokens** (integer) - Total tokens used.

#### Error Response
```json
{
  "error": {
    "message": "string",
    "type": "string",
    "param": "string",
    "code": "string"
  }
}
```

- **error** (object) - Contains error details.
  - **message** (string) - A description of the error.
  - **type** (string) - The type of error.
  - **param** (string) - The parameter that caused the error.
  - **code** (string) - An error code.

### Common Issues
- Files exceeding the 50MB size limit will not be processed.
- Ensure text-based documents are provided, not scanned images.
- Password-protected files may not be processed unless they are publicly accessible without a password prompt.

```

--------------------------------

### Perplexity Search API - Basic Usage

Source: https://docs.perplexity.ai/guides/search-quickstart

Demonstrates how to perform a basic search query using the Perplexity Search API to retrieve relevant web results. The SDK automatically uses the PERPLEXITY_API_KEY environment variable for authentication.

```APIDOC
## POST /search

### Description
Performs a web search query to retrieve ranked search results.

### Method
POST

### Endpoint
/search

### Parameters
#### Query Parameters
- **query** (string) - Required - The search query string.
- **max_results** (integer) - Optional - The maximum number of search results to return. Defaults to 10.
- **max_tokens_per_page** (integer) - Optional - The maximum number of tokens to extract per result. Defaults to 2048.

### Request Body
This endpoint does not require a request body for basic usage when using the SDK, as parameters are passed as arguments to the SDK method.

### Request Example (Python SDK)
```python
from perplexity import Perplexity

client = Perplexity()
search = client.search.create(
    query="latest AI developments 2024",
    max_results=5,
    max_tokens_per_page=2048
)

for result in search.results:
    print(f"{result.title}: {result.url}")
```

### Response
#### Success Response (200)
- **results** (array) - An array of search result objects.
  - **title** (string) - The title of the search result.
  - **url** (string) - The URL of the search result.
  - **snippet** (string) - A brief snippet of the content from the search result.

#### Response Example
```json
{
  "results": [
    {
      "title": "2024: A year of extraordinary progress and advancement in AI - Google Blog",
      "url": "https://blog.google/technology/ai/2024-ai-extraordinary-progress-advancement/",
      "snippet": "## Relentless innovation in models, products and technologies\n\n2024 was a year of experimenting, fast shipping, and putting our latest technologies in the hands of developers.\n\nIn December 2024, we released the first models in our Gemini 2.0 experimental series — AI models designed for the agentic era. First out of the gate was Gemini 2.0 Flash, our workhorse model, followed by prototypes from the frontiers of our agentic research including: an updated Project Astra, which explores the capabilities of a universal AI assistant; Project Mariner, an early prototype capable of taking actions in Chrome as an experimental extension; and Jules, an AI-powered code agent. We're looking forward to bringing Gemini 2.0’s powerful capabilities to our flagship products — in Search, we've already started testing in AI Overviews, which are now used by over a billion people to ask new types of questions.\n\nWe also released Deep Research, a new agentic feature in Gemini Advanced that saves people hours of research work by creating and executing multi-step plans for finding answers to complicated questions; and introduced Gemini 2.0 Flash Thinking Experimental, an experimental model that explicitly shows its thoughts.\n\nThese advances followed swift progress earlier in the year"
    }
  ]
}
```
```

--------------------------------

### Grounded LLM API

Source: https://docs.perplexity.ai/chat-with-persistence

Build AI applications with web-grounded chat completions and reasoning models.

```APIDOC
## POST /chat/completions

### Description
Build AI applications with web-grounded chat completions and reasoning models. This endpoint allows for conversational AI powered by Perplexity's search capabilities.

### Method
POST

### Endpoint
/chat/completions

### Parameters
#### Request Body
- **messages** (array) - Required - An array of message objects, each with 'role' ('user' or 'assistant') and 'content'.
- **model** (string) - Optional - The model to use for generation (e.g., 'sonar'). Defaults to 'sonar'.
- **max_tokens** (integer) - Optional - The maximum number of tokens to generate.
- **temperature** (float) - Optional - Controls the randomness of the output (0.0 to 1.0).

### Request Example
```json
{
  "messages": [
    {"role": "user", "content": "What is the weather like in London today?"}
  ],
  "model": "sonar",
  "max_tokens": 150
}
```

### Response
#### Success Response (200)
- **choices** (array) - An array of choice objects, each containing a 'message' object with 'role' and 'content'.

#### Response Example
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "The weather in London today is partly cloudy with a high of 18°C."
      }
    }
  ]
}
```
```

--------------------------------

### Buffer Size Configuration for Streaming in Python

Source: https://docs.perplexity.ai/guides/streaming-responses

Demonstrates setting the buffer_size parameter for different use cases in real-time applications. The buffer_size affects how data chunks are processed, impacting responsiveness and efficiency.

```python
# Character-by-character for immediate display
buffer_size = 1

# Larger chunks for efficiency
buffer_size = 100

# Balance between responsiveness and efficiency
buffer_size = 500
```

--------------------------------

### Response Customization for Chat Completion (Python & TypeScript)

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Illustrates how to customize the LLM's response behavior using parameters like `max_tokens`, `temperature`, `top_p`, `presence_penalty`, and `frequency_penalty`. These controls help manage response length, creativity, and repetition.

```python
completion = client.chat.completions.create(
  messages=[
    {"role": "user", "content": "Explain machine learning in simple terms"}
  ],
  model="sonar",
  max_tokens=500, # Limit response length
  temperature=0.7, # Control creativity
  top_p=0.9, # Control diversity
  presence_penalty=0.1, # Reduce repetition
  frequency_penalty=0.1
)
```

```typescript
const completion = await client.chat.completions.create({
  messages: [
    {
      role: "user",
      content: "Explain machine learning in simple terms"
    }
  ],
  model: "sonar",
  max_tokens: 500, // Limit response length
  temperature: 0.7, // Control creativity (0-2)
  top_p: 0.9, // Control diversity (0-1)
  presence_penalty: 0.1, // Reduce repetition (-2 to 2)
  frequency_penalty: 0.1 // Reduce repetition (-2 to 2)
});
```

--------------------------------

### Process Reasoning Steps in Chat Chunks (Python & TypeScript)

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

Handles chunks related to the reasoning stage of a chat. It extracts and prints reasoning steps, including web search keywords if present. This is useful for understanding the AI's thought process.

```python
delta = chunk.choices[0].delta
if hasattr(delta, 'reasoning_steps'):
    for step in delta.reasoning_steps:
        print(f"\n[Reasoning] {step.thought}")
        if step.type == "web_search":
            keywords = step.web_search.search_keywords
            print(f"[Search] Keywords: {', '.join(keywords)}")
```

```typescript
function handleReasoningChunk(chunk: any) {
    if (chunk.object === "chat.reasoning") {
        const delta = chunk.choices[0].delta;
        if (delta.reasoning_steps) {
            for (const step of delta.reasoning_steps) {
                console.log(`\n[Reasoning] ${step.thought}`);
                if (step.type === "web_search") {
                    const keywords = step.web_search.search_keywords;
                    console.log(`[Search] Keywords: ${keywords.join(', ')}`);
                }
            }
        }
    }
}
```

--------------------------------

### Handling chat.reasoning Chunks

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

Processes chunks of type 'chat.reasoning' which contain intermediate reasoning steps and web search keywords.

```APIDOC
## POST /chat/completions (Hypothetical Endpoint for Streaming)

### Description
This endpoint is used for real-time chat interactions where the API streams back responses in chunks. This specific documentation focuses on handling the intermediate reasoning steps.

### Method
POST

### Endpoint
/chat/completions

### Parameters
#### Request Body
- **model** (string) - Required - The model to use for chat completion.
- **messages** (array) - Required - The messages to send to the model.
- **stream** (boolean) - Optional - Whether to stream the response chunks.

### Request Example
```json
{
  "model": "sonar-pro",
  "messages": [{"role": "user", "content": "What is the weather in Seattle?"}],
  "stream": true
}
```

### Response
#### Success Response (200 OK - Streaming Chunks)
- **object** (string) - The type of chunk received (e.g., 'chat.reasoning').
- **choices** (array) - Contains the streamed data, including delta information.
  - **delta** (object) - Contains reasoning steps if available.
    - **reasoning_steps** (array) - A list of reasoning steps taken by the model.
      - **thought** (string) - The reasoning thought process.
      - **type** (string) - The type of reasoning step (e.g., 'web_search').
      - **web_search** (object) - Details for web search steps.
        - **search_keywords** (array) - Keywords used for the web search.

#### Response Example (chat.reasoning chunk)
```json
{
  "id": "msg_abc123",
  "model": "sonar-pro",
  "object": "chat.reasoning",
  "choices": [
    {
      "index": 0,
      "delta": {
        "reasoning_steps": [
          {
            "thought": "I need to find the current weather in Seattle.",
            "type": "web_search",
            "web_search": {
              "search_keywords": ["weather Seattle"]
            }
          }
        ]
      }
    }
  ]
}
```

### Python Handler Example
```python
def handle_reasoning_chunk(chunk):
    if chunk.object == "chat.reasoning":
        delta = chunk.choices[0].delta
        if hasattr(delta, 'reasoning_steps'):
            for step in delta.reasoning_steps:
                print(f"\n[Reasoning] {step.thought}")
                if step.type == "web_search":
                    keywords = step.web_search.search_keywords
                    print(f"[Search] Keywords: {', '.join(keywords)}")
```

### TypeScript Handler Example
```typescript
function handleReasoningChunk(chunk: any) {
    if (chunk.object === "chat.reasoning") {
        const delta = chunk.choices[0].delta;
        if (delta.reasoning_steps) {
            for (const step of delta.reasoning_steps) {
                console.log(`\n[Reasoning] ${step.thought}`);
                if (step.type === "web_search") {
                    const keywords = step.web_search.search_keywords;
                    console.log(`[Search] Keywords: ${keywords.join(', ')}`);
                }
            }
        }
    }
}
```
```

--------------------------------

### Chat Completions

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

This section demonstrates how to use the chat completions API to generate responses based on a series of messages, including system, user, and assistant roles.

```APIDOC
## POST /chat/completions

### Description
Generates a text completion based on a list of messages.

### Method
POST

### Endpoint
/chat/completions

### Parameters
#### Request Body
- **messages** (array) - Required - A list of message objects, where each object has a 'role' (system, user, or assistant) and 'content'.
- **model** (string) - Required - The model to use for generating the completion (e.g., "sonar").

### Request Example
```json
{
  "messages": [
    {"role": "system", "content": "You are a helpful research assistant."}, 
    {"role": "user", "content": "What are the main causes of climate change?"},
    {"role": "assistant", "content": "The main causes of climate change include..."},
    {"role": "user", "content": "What are some potential solutions?"}
  ],
  "model": "sonar"
}
```

### Response
#### Success Response (200)
- **choices** (array) - A list of completion choices. Each choice contains a 'message' object with 'role' and 'content'.

#### Response Example
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Potential solutions include transitioning to renewable energy sources, improving energy efficiency, and implementing carbon capture technologies."
      }
    }
  ]
}
```
```

--------------------------------

### Configure OpenAI SDKs for Perplexity Sonar API (Python)

Source: https://docs.perplexity.ai/guides/chat-completions-guide

This Python code snippet demonstrates how to configure the OpenAI client library to communicate with Perplexity's Sonar API. It requires replacing 'YOUR_API_KEY' with your actual Perplexity API key and setting the base_url to 'https://api.perplexity.ai'.

```python
from openai import OpenAI

client = OpenAI(
  api_key="YOUR_API_KEY",
  base_url="https://api.perplexity.ai"
)

resp = client.chat.completions.create(
  model="sonar-pro",
  messages=[
    {"role": "user", "content": "Hello!"}
  ]
)

print(resp.choices[0].message.content)
```

--------------------------------

### Client-Side Content Aggregation in Python

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

Demonstrates how to manually aggregate content from streaming chunks in Perplexity AI's concise mode. This is necessary because the `choices.message` is not incrementally updated.

```python
# Track content yourself
content = ""
# Assuming 'stream' is an iterable of chunks from the API response
# for chunk in stream:
#     if chunk.object == "chat.completion.chunk":
#         if chunk.choices[0].delta.content:
#             content += chunk.choices[0].delta.content

```

--------------------------------

### Streaming Chat Responses (Python & TypeScript)

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Demonstrates how to enable and process streaming responses from the chat completions API. This is useful for interactive applications where immediate feedback is desired, providing a more dynamic user experience.

```python
stream = client.chat.completions.create(
  messages=[
    {"role": "user", "content": "Write a summary of recent AI breakthroughs"}
  ],
  model="sonar",
  stream=True
)
for chunk in stream:
  if chunk.choices[0].delta.content:
    print(chunk.choices[0].delta.content, end="")
```

```typescript
const stream = await client.chat.completions.create({
  messages: [
    {
      role: "user",
      content: "Write a summary of recent AI breakthroughs"
    }
  ],
  model: "sonar",
  stream: true
});
for await (const chunk of stream) {
  if (chunk.choices[0]?.delta?.content) {
    process.stdout.write(chunk.choices[0].delta.content);
  }
}
```

--------------------------------

### Multi-Query Search with Perplexity AI

Source: https://docs.perplexity.ai/guides/search-quickstart

Demonstrates how to perform searches with multiple queries simultaneously. This is useful for research tasks requiring exploration of various angles of a topic. Results are grouped per query.

```python
from perplexity import Perplexity

client = Perplexity()
search = client.search.create(
    queries=["climate change effects", "renewable energy solutions", "AI ethics"],
    max_results=5
)

for i, query_results in enumerate(search.results):
    print(f"Results for query {i+1}:")
    for result in query_results:
        print(f" {result.title}: {result.url}")
    print("---")
```

--------------------------------

### Handle Search Results Only from Done Chunks in Python

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

Explains that search results and usage information are only available in `chat.reasoning.done` and `chat.completion.done` chunks. Avoid checking for these in other chunk types.

```python
# Don't check for search_results in other chunk types
# if chunk.object in ["chat.reasoning.done", "chat.completion.done"]:
#     if hasattr(chunk, 'search_results'):
#         process_search_results(chunk.search_results)

```

--------------------------------

### Web Search Options

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Control how the model searches and uses web information for generating responses. This includes filtering by recency, domain, and the number of search results.

```APIDOC
## POST /chat/completions (with Web Search Options)

### Description
Generates a text completion while controlling the web search behavior.

### Method
POST

### Endpoint
/chat/completions

### Parameters
#### Request Body
- **messages** (array) - Required - A list of message objects.
- **model** (string) - Required - The model to use (e.g., "sonar").
- **web_search_options** (object) - Optional - Options to control web search.
  - **search_recency_filter** (string) - Optional - Filters search results by recency (e.g., "week", "month", "year").
  - **search_domain_filter** (array) - Optional - Filters search results to specific domains (e.g., ["energy.gov", "iea.org"]).
  - **max_search_results** (integer) - Optional - The maximum number of search results to consider.
- **return_images** (boolean) - Optional - Whether to include image URLs in the response.
- **return_related_questions** (boolean) - Optional - Whether to include related questions in the response.

### Request Example
```json
{
  "messages": [
    {"role": "user", "content": "What are the latest developments in renewable energy?"}
  ],
  "model": "sonar",
  "web_search_options": {
    "search_recency_filter": "week",
    "search_domain_filter": ["energy.gov", "iea.org", "irena.org"],
    "max_search_results": 10
  },
  "return_images": true,
  "return_related_questions": true
}
```

### Response
#### Success Response (200)
- **choices** (array) - Completion choices, potentially including message content, image URLs, and related questions.

#### Response Example
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Recent developments in renewable energy include advancements in solar panel efficiency and battery storage technologies..."
      },
      "images": ["http://example.com/image1.jpg"],
      "related_questions": ["What are the challenges of solar power?"]
    }
  ]
}
```
```

--------------------------------

### Optimizing Streaming for Document Generation in Python

Source: https://docs.perplexity.ai/guides/streaming-responses

Shows a Python code snippet for optimizing streaming API calls for document generation use cases. It prioritizes quality and completeness with a higher max_tokens and lower temperature.

```python
# Optimize for quality and completeness
stream = client.chat.completions.create(
    model="sonar-pro",
    messages=messages,
    stream=True,
    max_tokens=4000,  # Longer responses
    temperature=0.3   # More focused
)
```

--------------------------------

### Initialize Perplexity Client and Make Chat Completion Request (TypeScript)

Source: https://docs.perplexity.ai/guides/chat-completions-guide

Initializes the OpenAI client for Perplexity AI using an API key and base URL in TypeScript. It makes an asynchronous chat completion request with model, messages, and search filters directly as parameters. The response content and the number of found articles are logged to the console.

```typescript
import OpenAI from 'openai';

const client = new OpenAI({
    apiKey: "YOUR_API_KEY",
    baseURL: "https://api.perplexity.ai"
});

const response = await client.chat.completions.create({
    model: "sonar-pro",
    messages: [
        { role: "user", content: "Latest climate research findings" }
    ],
    // TypeScript SDK: Use direct parameters (not extra_body)
    search_domain_filter: ["nature.com", "science.org"],
    search_recency_filter: "month"
});

console.log(response.choices[0].message.content);
console.log(`Sources: ${response.search_results.length} articles found`);
```

--------------------------------

### Error Handling for Chat Completions

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Demonstrates how to handle specific API errors that may occur during chat completion requests, such as invalid parameters or rate limits.

```APIDOC
## POST /chat/completions (Error Handling)

### Description
Handles potential errors during chat completion requests, including bad requests and rate limits.

### Method
POST

### Endpoint
`/chat/completions`

### Parameters
#### Request Body
- **messages** (array) - Required - An array of message objects with 'role' and 'content'.
- **model** (string) - Required - The model to use for the completion.
- **max_tokens** (integer) - Optional - The maximum number of tokens to generate.

### Request Example (Python)
```python
import perplexity

try:
    completion = client.chat.completions.create(
        messages=["role": "user", "content": "What is AI?"}],
        model="sonar",
        max_tokens=50000 # Exceeds limit
    )
except perplexity.BadRequestError as e:
    print(f"Invalid request parameters: {e}")
except perplexity.RateLimitError as e:
    print("Rate limit exceeded, please retry later")
except perplexity.APIStatusError as e:
    print(f"API error: {e.status_code}")
```

### Request Example (TypeScript)
```typescript
try {
  const completion = await client.chat.completions.create({
    messages: [{ role: "user", content: "What is AI?" }],
    model: "sonar",
    max_tokens: 50000 // Exceeds limit
  });
} catch (error) {
  if (error instanceof Perplexity.BadRequestError) {
    console.error(`Invalid request parameters: ${error.message}`);
  } else if (error instanceof Perplexity.RateLimitError) {
    console.error("Rate limit exceeded, please retry later");
  } else if (error instanceof Perplexity.APIError) {
    console.error(`API error ${error.status}: ${error.message}`);
  }
}
```

### Response
#### Error Response Examples
- **400 Bad Request**: Returned for invalid request parameters.
- **429 Rate Limit Exceeded**: Returned when the API rate limit is hit.
- **5xx Server Error**: Returned for unexpected server issues.
```

--------------------------------

### Async Chat Completions (POST)

Source: https://docs.perplexity.ai/guides/usage-tiers

Initiates an asynchronous chat completion request. This endpoint allows for advanced features such as providing specific questions, search domain filters, and requesting structured outputs.

```APIDOC
## POST /async/chat/completions

### Description
Initiates an asynchronous chat completion request with support for questions, search domain filters, and structured outputs.

### Method
POST

### Endpoint
`/async/chat/completions`

### Parameters
#### Query Parameters
- **max_tokens** (integer) - Optional - Maximum number of tokens to generate in the response.
- **stream** (boolean) - Optional - Whether to stream the response. Defaults to false.

#### Request Body
- **messages** (array) - Required - An array of message objects representing the conversation history.
  - **role** (string) - Required - The role of the author of the message ('user' or 'assistant').
  - **content** (string) - Required - The content of the message.
- **model** (string) - Optional - The model to use for the chat completion. Defaults to 'sonar-desktop'.
- **search_parameter** (string) - Optional - Specifies the search domain filter.
- **structured_output** (object) - Optional - Defines the structure for the output.
  - **format** (string) - Required - The desired output format (e.g., 'json').
  - **schema** (object) - Optional - A JSON schema to guide the structured output.

### Request Example
```json
{
  "messages": [
    {"role": "user", "content": "What is the capital of France?"}
  ],
  "search_parameter": "google",
  "structured_output": {
    "format": "json"
  }
}
```

### Response
#### Success Response (200)
- **id** (string) - The unique identifier for the request.
- **status** (string) - The current status of the request (e.g., 'processing', 'completed', 'failed').

#### Response Example
```json
{
  "id": "req_abc123xyz",
  "status": "processing"
}
```
```

--------------------------------

### Chat Completions API - OpenAI Compatibility

Source: https://docs.perplexity.ai/guides/chat-completions-guide

This section details how to configure your OpenAI client libraries to interact with Perplexity's Sonar API. By changing the base URL to 'https://api.perplexity.ai' and providing your Perplexity API key, you can leverage Perplexity's models using the familiar Chat Completions API interface.

```APIDOC
## Configuring OpenAI SDKs to call Sonar

To start using Sonar with OpenAI’s client libraries, pass your Perplexity API key and change the base_url to `https://api.perplexity.ai`.

### Python Example
```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.perplexity.ai"
)

resp = client.chat.completions.create(
    model="sonar-pro",
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print(resp.choices[0].message.content)
```

### TypeScript Example
```typescript
import OpenAI from 'openai';

const client = new OpenAI({
    apiKey: "YOUR_API_KEY",
    baseURL: "https://api.perplexity.ai"
});

const resp = await client.chat.completions.create({
    model: "sonar-pro",
    messages: [
        { role: "user", content: "Hello!" }
    ]
});

console.log(resp.choices[0].message.content);
```

Your responses will match OpenAI’s format exactly. See the response structure section below for complete field details.
```

--------------------------------

### Perplexity AI Grounded LLM (Chat Completions)

Source: https://docs.perplexity.ai/[a-zA-Z0-9-]%7B0,61%7D[a-zA-Z0-9]

Build AI applications with web-grounded chat completions and reasoning models using the Grounded LLM API.

```APIDOC
## POST /chat/completions

### Description
Build AI applications with web-grounded chat completions and reasoning models.

### Method
POST

### Endpoint
/chat/completions

### Parameters
#### Request Body
- **model** (string) - Required - The model to use for chat completions (e.g., 'sonar').
- **messages** (array) - Required - An array of message objects representing the conversation.
  - **role** (string) - Required - The role of the author ('user' or 'assistant').
  - **content** (string) - Required - The content of the message.
- **search_parameters** (object) - Optional - Parameters for controlling search behavior.
  - **enable_auto_redirect** (boolean) - Optional - Whether to automatically redirect based on search results.
  - **exclude_linked_sites** (array) - Optional - A list of sites to exclude from search results.
  - **max_num_results** (integer) - Optional - The maximum number of search results to consider.
  - **site** (string) - Optional - A specific site to search within.

### Request Example
```json
{
  "model": "sonar",
  "messages": [
    {"role": "user", "content": "What is the latest news on AI development?"}
  ],
  "search_parameters": {
    "max_num_results": 5
  }
}
```

### Response
#### Success Response (200)
- **choices** (array) - A list of completion choices.
  - **message** (object) - The assistant's message.
    - **role** (string) - The role of the author ('assistant').
    - **content** (string) - The content of the assistant's message.
- **search_queries** (array) - Any search queries performed by the model.

#### Response Example
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "The latest news on AI development includes advancements in large language models, ethical AI discussions, and new applications in various industries..."
      }
    }
  ],
  "search_queries": [
    "latest AI development news"
  ]
}
```
```

--------------------------------

### Track Cost from Final Chunk in Python

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

Illustrates how to access and display the total cost of a request, which is only available in the `chat.completion.done` chunk.

```python
# if chunk.object == "chat.completion.done":
#     if hasattr(chunk.usage, 'cost'):
#         total_cost = chunk.usage.cost.total_cost
#         print(f"Request cost: ${total_cost:.4f}")

```

--------------------------------

### Proper SSE Parsing with Python using sseclient-py

Source: https://docs.perplexity.ai/guides/streaming-responses

This snippet demonstrates how to properly parse Server-Sent Events (SSE) from the Perplexity AI API using the `sseclient-py` library. It handles JSON decoding of chunks and prints the content, ensuring correct streaming output. Dependencies include `sseclient-py` and `requests`.

```python
import sseclient
import requests
import json

def stream_with_proper_sse():
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "sonar",
        "messages": [{"role": "user", "content": "Explain quantum computing"}],
        "stream": True
    }
    response = requests.post(url, headers=headers, json=payload, stream=True)
    client = sseclient.SSEClient(response)
    for event in client.events():
        if event.data == '[DONE]':
            break
        try:
            chunk_data = json.loads(event.data)
            content = chunk_data['choices'][0]['delta'].get('content', '')
            if content:
                print(content, end='')
        except json.JSONDecodeError:
            continue

stream_with_proper_sse()
```

--------------------------------

### Analyze Image at URL using Perplexity AI (Shell)

Source: https://docs.perplexity.ai/guides/image-attachments

This shell command demonstrates how to send an image URL to the Perplexity AI API for analysis. It specifies the model, disables streaming, and constructs a message containing both text and an image URL. The output is piped to `jq` for potential JSON parsing.

```shell
curl -X POST https://api.perplexity.ai/chat/completions \
 --header "accept: application/json" \
 --header "content-type: application/json" \
 --header "Authorization: Bearer $SONAR_API_KEY" \
 --data '{ "model": "sonar-pro", "stream": false, "messages": [ { "role": "user", "content": [ { "type": "text", "text": "Can you describe the image at this URL?" }, { "type": "image_url", "image_url": { "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg" } } ] } ] }' | jq
```

--------------------------------

### Create Chat Completion with Perplexity AI SDK

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Initiates a chat completion request to the Perplexity AI API. It takes a list of messages and a model name as input and returns the completion object.

```python
Query = await client.chat.completions.create({ messages: [{ role: "user", content: "Analyze the economic impact of AI on employment" }], model: "sonar-pro" });
```

--------------------------------

### API Parameters

Source: https://docs.perplexity.ai/guides/chat-completions-guide

This section outlines the parameters supported by the Perplexity Sonar API when used with OpenAI compatibility. It includes standard OpenAI parameters and Perplexity-specific parameters for enhanced control.

```APIDOC
## API compatibility

### Standard OpenAI parameters

These parameters work exactly the same as OpenAI’s API:

*   `model` - Model name (use Perplexity model names)
*   `messages` - Chat messages array
*   `temperature` - Sampling temperature (0-2)
*   `max_tokens` - Maximum tokens in response
*   `top_p` - Nucleus sampling parameter
*   `frequency_penalty` - Frequency penalty (-2.0 to 2.0)
*   `presence_penalty` - Presence penalty (-2.0 to 2.0)
*   `stream` - Enable streaming responses

### Perplexity-specific parameters

These Perplexity-specific parameters are also included:

*   `search_domain_filter` - Limit or exclude specific domains
*   `search_recency_filter` - Filter by content recency
*   `return_images` - Include image URLs in response
*   `return_related_questions` - Include related questions
*   `search_mode` - “web” (default) or “academic” mode selector. See API Reference for parameter details and models.
```

--------------------------------

### Chat Completions API

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Generate AI responses with web-grounded knowledge using the Perplexity SDKs. Supports chat completions, streaming responses, async operations, and comprehensive error handling.

```APIDOC
## POST /chat/completions

### Description
Generates AI responses grounded in web knowledge. This endpoint supports chat-style interactions and can provide responses with type safety, streaming capabilities, and asynchronous operations.

### Method
POST

### Endpoint
/chat/completions

### Parameters
#### Query Parameters
None

#### Request Body
- **messages** (array[object]) - Required - An array of message objects representing the conversation history. Each object should have a `role` (e.g., 'user', 'assistant') and `content` (string).
- **model** (string) - Required - The identifier for the model to use (e.g., "sonar", "sonar-pro", "sonar-reasoning-pro").
- **stream** (boolean) - Optional - If set to true, streams the response as chunks.
- **max_tokens** (integer) - Optional - The maximum number of tokens to generate in the response.
- **temperature** (number) - Optional - Controls randomness. Lower values make output more deterministic.

### Request Example
```json
{
  "messages": [
    { "role": "user", "content": "Tell me about the latest developments in AI" }
  ],
  "model": "sonar"
}
```

### Response
#### Success Response (200)
- **id** (string) - Unique identifier for the response.
- **object** (string) - Type of object returned (e.g., "chat.completion").
- **created** (integer) - Timestamp of creation.
- **model** (string) - The model used for generation.
- **choices** (array[object]) - An array of choices, where each choice contains:
    - **index** (integer) - Index of the choice.
    - **message** (object) - The message object containing the AI's response:
        - **role** (string) - Role of the message sender (usually "assistant").
        - **content** (string) - The generated text content.
    - **finish_reason** (string) - The reason the generation finished (e.g., "stop", "length").
- **usage** (object) - Information about token usage:
    - **prompt_tokens** (integer) - Number of tokens in the prompt.
    - **completion_tokens** (integer) - Number of tokens in the completion.
    - **total_tokens** (integer) - Total tokens used.

#### Response Example
```json
{
  "id": "chatcmpl-12345",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "sonar",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Based on the latest information, here are some key developments in AI for 2024..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 50,
    "total_tokens": 60
  }
}
```

#### Error Handling
- **400 Bad Request**: Invalid request parameters.
- **401 Unauthorized**: Invalid API key or authentication issue.
- **404 Not Found**: The requested resource was not found.
- **429 Too Many Requests**: Rate limit exceeded.
- **500 Internal Server Error**: An unexpected error occurred on the server.
```

--------------------------------

### Advanced Analysis with Web Search (cURL)

Source: https://docs.perplexity.ai/guides/file-attachments

This cURL command demonstrates advanced document analysis combined with web search. It sends a request to summarize a document and find additional context from recent studies. The request includes a public URL to the document and specifies the 'sonar-pro' model.

```shell
curl -X POST "https://api.perplexity.ai/chat/completions" \
-H "Authorization: Bearer YOUR_API_KEY" \
-H "Content-Type: application/json" \
-d '{ "messages": [ { "content": [ { "type": "text", "text": "What are the key findings in this research paper? Provide additional context from recent studies." }, { "type": "file_url", "file_url": { "url": "https://example.com/research-paper.pdf" }, "file_name": "research-paper.pdf" } ], "role": "user" } ], "model": "sonar-pro" }'
```

--------------------------------

### Error Handling for Chat Completions (Python & TypeScript)

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Illustrates comprehensive error handling for chat completion requests in both Python and TypeScript. It catches specific exceptions like `BadRequestError`, `RateLimitError`, and generic `APIStatusError` to provide informative feedback on request failures.

```python
import perplexity
try:
    completion = client.chat.completions.create(
        messages=["{\"role\": \"user\", \"content\": \"What is AI?\"}"],
        model="sonar",
        max_tokens=50000 # Exceeds limit
    )
except perplexity.BadRequestError as e:
    print(f"Invalid request parameters: {e}")
except perplexity.RateLimitError as e:
    print("Rate limit exceeded, please retry later")
except perplexity.APIStatusError as e:
    print(f"API error: {e.status_code}")
```

```javascript
try {
    const completion = await client.chat.completions.create({
        messages: [ { role: "user", content: "What is AI?" } ],
        model: "sonar",
        max_tokens: 50000 // Exceeds limit
    });
} catch (error) {
    if (error instanceof Perplexity.BadRequestError) {
        console.error(`Invalid request parameters: ${error.message}`);
    } else if (error instanceof Perplexity.RateLimitError) {
        console.error("Rate limit exceeded, please retry later");
    } else if (error instanceof Perplexity.APIError) {
        console.error(`API error ${error.status}: ${error.message}`);
    }
```

--------------------------------

### Stream LLM Responses with Callbacks (Python)

Source: https://docs.perplexity.ai/guides/streaming-responses

This Python snippet demonstrates how to stream responses from a Perplexity AI model using callbacks. It handles content chunks, search results, and completion events, allowing for real-time processing of LLM output. Dependencies include the 'perplexity' library.

```python
from perplexity import Perplexity

def stream_with_callbacks(query: str, on_content=None, on_search_results=None, on_complete=None):
    client = Perplexity()
    stream = client.chat.completions.create(
        model="sonar",
        messages=[{"role": "user", "content": query}],
        stream=True
    )
    full_content = ""
    metadata = {}
    for chunk in stream:
        # Handle content chunks
        if chunk.choices[0].delta.content:
            content_piece = chunk.choices[0].delta.content
            full_content += content_piece
            if on_content:
                on_content(content_piece)
        # Handle search results
        if hasattr(chunk, 'search_results') and chunk.search_results:
            metadata['search_results'] = chunk.search_results
            if on_search_results:
                on_search_results(chunk.search_results)
        # Handle other metadata
        if hasattr(chunk, 'usage') and chunk.usage:
            metadata['usage'] = chunk.usage
        # Handle completion
        if chunk.choices[0].finish_reason:
            if on_complete:
                on_complete(full_content, metadata)
    return full_content, metadata

# Usage example
def print_content(content: str):
    print(content, end='', flush=True)
def handle_search_results(results: list):
    print(f"\n[Found {len(results)} sources]", end='')
def handle_completion(content: str, metadata: dict):
    print(f"\n\nCompleted. Total length: {len(content)} characters")
    if 'usage' in metadata:
        print(f"Token usage: {metadata['usage']}")

stream_with_callbacks(
    "Explain the latest developments in renewable energy",
    on_content=print_content,
    on_search_results=handle_search_results,
    on_complete=handle_completion
)
```

--------------------------------

### Configure OpenAI SDKs for Perplexity Sonar API (TypeScript)

Source: https://docs.perplexity.ai/guides/chat-completions-guide

This TypeScript code snippet shows how to configure the OpenAI client library for use with Perplexity's Sonar API. Ensure you replace 'YOUR_API_KEY' with your Perplexity API key and set the baseURL to 'https://api.perplexity.ai'.

```typescript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: "YOUR_API_KEY",
  baseURL: "https://api.perplexity.ai"
});

const resp = await client.chat.completions.create({
  model: "sonar-pro",
  messages: [{ role: "user", content: "Hello!" }]
});

console.log(resp.choices[0].message.content);
```

--------------------------------

### Create Async Chat Completion

Source: https://docs.perplexity.ai/api-reference/async-chat-completions-post

Submits a request to create an asynchronous chat completion job. The response includes a job ID and details about the submitted job.

```APIDOC
## POST /chat/completions

### Description
Creates an asynchronous chat completion job. Use this endpoint to submit chat requests that will be processed in the background.

### Method
POST

### Endpoint
/chat/completions

### Parameters
#### Query Parameters
None

#### Request Body
- **model** (string) - Required - The model to use for the chat completion.
- **messages** (array) - Required - An array of message objects, each with a `role` and `content`.
- **stream** (boolean) - Optional - Whether to stream the response.

### Request Example
```json
{
  "model": "gpt-4",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the weather today?"}
  ]
}
```

### Response
#### Success Response (200)
- **id** (string) - Unique identifier for the asynchronous job.
- **model** (string) - The model used for the request.
- **created_at** (integer) - Unix timestamp of when the job was created.
- **status** (enum) - The status of an asynchronous processing job. Available options: `CREATED`, `IN_PROGRESS`, `COMPLETED`, `FAILED`.
- **started_at** (integer | null) - Unix timestamp of when processing started.
- **completed_at** (integer | null) - Unix timestamp of when processing completed.
- **response** (object | null) - The actual chat completion response, available when status is COMPLETED.
- **failed_at** (integer | null) - Unix timestamp of when processing failed.
- **error_message** (string | null) - Error message if the job failed.

#### Response Example
```json
{
  "id": "chatcmpl-xxxxxxxxxxxxxxxxx",
  "model": "gpt-4",
  "created_at": 1677652715,
  "status": "CREATED",
  "started_at": null,
  "completed_at": null,
  "response": null,
  "failed_at": null,
  "error_message": null
}
```
```

--------------------------------

### Stream Chat Completions in Full Mode - Python

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

Demonstrates streaming chat completions using the 'sonar-pro' model in 'full' stream mode. It prints content from completion chunks and indicates the presence of search results. This mode is suitable for simple integrations and backward compatibility.

```python
from perplexity import Perplexity

client = Perplexity()
stream = client.chat.completions.create(
    model="sonar-pro",
    messages=[{"role": "user", "content": "What's the weather?"}],
    stream=True  # stream_mode defaults to "full"
)

for chunk in stream:  # All chunks are chat.completion.chunk
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")

    # Search results may appear in multiple chunks
    if hasattr(chunk, 'search_results'):
        print(f"Sources: {len(chunk.search_results)}")
```

--------------------------------

### Handle Rate Limits with Exponential Backoff

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Gracefully handles API rate limits by implementing exponential backoff. This function retries the request with increasing delays between attempts.

```python
import time
import random
def chat_with_retry(messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(
                messages=messages,
                model="sonar"
            )
        except perplexity.RateLimitError:
            if attempt == max_retries - 1:
                raise
            delay = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(delay)
```

```typescript
async function chatWithRetry( messages: Perplexity.ChatMessage[], maxRetries: number = 3 ): Promise {
    for (let attempt = 0; attempt < maxRetries; attempt++) {
        try {
            return await client.chat.completions.create({
                messages,
                model: "sonar"
            });
        } catch (error) {
            if (error instanceof Perplexity.RateLimitError && attempt < maxRetries - 1) {
                const delay = Math.pow(2, attempt) * 1000 + Math.random() * 1000;
                await new Promise(resolve => setTimeout(resolve, delay));
                continue;
            }
            throw error;
        }
    }
    throw new Error("Max retries exceeded");
}
```

--------------------------------

### POST /async/chat/completions

Source: https://docs.perplexity.ai/api-reference/async-chat-completions-post

Creates an asynchronous chat completion job. This endpoint allows users to generate responses to chat-based prompts without waiting for an immediate reply, suitable for longer-running tasks.

```APIDOC
## POST /async/chat/completions

### Description
Creates an asynchronous chat completion job. This endpoint allows users to generate responses to chat-based prompts without waiting for an immediate reply, suitable for longer-running tasks.

### Method
POST

### Endpoint
/async/chat/completions

### Parameters
#### Query Parameters
None

#### Request Body
- **request** (object) - Required - The request object containing parameters for the chat completion.
  - **model** (string) - Required - The model to use for the chat completion (e.g., "sonar-deep-research").
  - **messages** (array) - Required - An array of message objects, where each object has a 'role' (system or user) and 'content'.
    - **role** (string) - Required - The role of the message sender ('system' or 'user').
    - **content** (string) - Required - The text content of the message.
  - **search_mode** (string) - Optional - The search mode to use (e.g., "web").
  - **reasoning_effort** (string) - Optional - The level of reasoning effort to apply (e.g., "low").
  - **max_tokens** (integer) - Optional - The maximum number of tokens to generate in the completion.
  - **temperature** (number) - Optional - Controls randomness; higher values mean more random output.
  - **top_p** (number) - Optional - Controls diversity via nucleus sampling.
  - **language_preference** (string) - Optional - Preferred language for the response.
  - **search_domain_filter** (string) - Optional - Filter search results by domain.
  - **return_images** (boolean) - Optional - Whether to return images in the response.
  - **return_related_questions** (boolean) - Optional - Whether to return related questions.
  - **search_recency_filter** (string) - Optional - Filter search results by recency.
  - **search_after_date_filter** (string) - Optional - Filter search results after a specific date.
  - **search_before_date_filter** (string) - Optional - Filter search results before a specific date.
  - **last_updated_after_filter** (string) - Optional - Filter results last updated after a specific date.
  - **last_updated_before_filter** (string) - Optional - Filter results last updated before a specific date.
  - **top_k** (integer) - Optional - Controls diversity via top-k sampling.
  - **stream** (boolean) - Optional - Whether to stream the response.
  - **presence_penalty** (number) - Optional - Penalizes new tokens based on whether they appear in the text so far.
  - **frequency_penalty** (number) - Optional - Penalizes new tokens based on their existing frequency in the text so far.
  - **response_format** (object) - Optional - Specifies the desired response format.
  - **disable_search** (boolean) - Optional - Whether to disable search functionality.
  - **enable_search_classifier** (boolean) - Optional - Whether to enable search classification.
  - **web_search_options** (object) - Optional - Options for web search.
    - **search_context_size** (string) - Optional - Size of the search context.
    - **image_search_relevance_enhanced** (boolean) - Optional - Enhance relevance for image search.
  - **media_response** (object) - Optional - Options for media responses.
    - **overrides** (object) - Optional - Overrides for media settings.
      - **return_videos** (boolean) - Optional - Whether to return videos.
      - **return_images** (boolean) - Optional - Whether to return images.

### Request Example
```json
{
  "request": {
    "model": "sonar-deep-research",
    "messages": [
      { "role": "system", "content": "Be precise and concise."}, 
      { "role": "user", "content": "How many stars are there in our galaxy?"}
    ],
    "search_mode": "web",
    "reasoning_effort": "low",
    "max_tokens": 123,
    "temperature": 0.2,
    "top_p": 0.9,
    "language_preference": "",
    "search_domain_filter": "",
    "return_images": false,
    "return_related_questions": false,
    "search_recency_filter": "",
    "search_after_date_filter": "",
    "search_before_date_filter": "",
    "last_updated_after_filter": "",
    "last_updated_before_filter": "",
    "top_k": 0,
    "stream": false,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "response_format": {},
    "disable_search": false,
    "enable_search_classifier": false,
    "web_search_options": {
      "search_context_size": "low",
      "image_search_relevance_enhanced": false
    },
    "media_response": {
      "overrides": {
        "return_videos": false,
        "return_images": false
      }
    }
  }
}
```

### Response
#### Success Response (200)
- **id** (string) - The unique identifier for the job.
- **model** (string) - The model used for the completion.
- **created_at** (integer) - Timestamp of job creation.
- **status** (string) - The current status of the job (e.g., "CREATED").
- **started_at** (integer) - Timestamp when the job started processing.
- **completed_at** (integer) - Timestamp when the job completed.
- **response** (object) - The details of the chat completion response.
  - **id** (string) - Unique identifier for the completion.
  - **model** (string) - The model that generated the completion.
  - **created** (integer) - Timestamp of completion creation.
  - **usage** (object) - Token usage information.
    - **prompt_tokens** (integer) - Tokens used in the prompt.
    - **completion_tokens** (integer) - Tokens used in the completion.
    - **total_tokens** (integer) - Total tokens used.
    - **search_context_size** (string) - Size of the search context used.
    - **citation_tokens** (integer) - Tokens used for citations.
    - **num_search_queries** (integer) - Number of search queries performed.
    - **reasoning_tokens** (integer) - Tokens used for reasoning.
  - **object** (string) - The type of object returned (e.g., "chat.completion").
  - **choices** (array) - An array of completion choices.
    - **index** (integer) - Index of the choice.
    - **message** (object) - The message content and role.
      - **content** (string) - The generated text content.
      - **role** (string) - The role of the message sender (e.g., "system").
    - **finish_reason** (string) - The reason the completion finished (e.g., "stop").
  - **search_results** (array) - Search results used for the completion.
    - **title** (string) - Title of the search result.
    - **url** (string) - URL of the search result.
    - **date** (string) - Date of the search result.
  - **videos** (array) - Videos returned as part of the response.
    - **url** (string) - URL of the video.
    - **thumbnail_url** (string) - URL of the video thumbnail.
    - **thumbnail_width** (integer) - Width of the thumbnail.
    - **thumbnail_height** (integer) - Height of the thumbnail.
    - **duration** (integer) - Duration of the video.
- **failed_at** (integer) - Timestamp when the job failed.
- **error_message** (string) - Error message if the job failed.

#### Response Example
```json
{
  "id": "",
  "model": "",
  "created_at": 123,
  "status": "CREATED",
  "started_at": 123,
  "completed_at": 123,
  "response": {
    "id": "",
    "model": "",
    "created": 123,
    "usage": {
      "prompt_tokens": 123,
      "completion_tokens": 123,
      "total_tokens": 123,
      "search_context_size": "",
      "citation_tokens": 123,
      "num_search_queries": 123,
      "reasoning_tokens": 123
    },
    "object": "chat.completion",
    "choices": [
      {
        "index": 123,
        "message": {
          "content": "",
          "role": "system"
        },
        "finish_reason": "stop"
      }
    ],
    "search_results": [
      {
        "title": "",
        "url": "",
        "date": "2023-12-25"
      }
    ],
    "videos": [
      {
        "url": "",
        "thumbnail_url": "",
        "thumbnail_width": 123,
        "thumbnail_height": 123,
        "duration": 123
      }
    ]
  },
  "failed_at": 123,
  "error_message": ""
}
```

#### Authorizations 
- **Authorization** (string header) - Required - Bearer authentication token.
```

--------------------------------

### Handling chat.reasoning.done Chunks

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

Processes the 'chat.reasoning.done' chunk, which signifies the end of the reasoning stage and includes final search results and image findings.

```APIDOC
## POST /chat/completions (Hypothetical Endpoint for Streaming)

### Description
This chunk signals the completion of the model's reasoning process. It aggregates all gathered search results (web, images, videos) and detailed reasoning steps before moving to the content generation phase.

### Method
POST

### Endpoint
/chat/completions

### Parameters
(See previous section for request parameters; this focuses on the response chunk)

### Response
#### Success Response (200 OK - Streaming Chunks)
- **object** (string) - Should be 'chat.reasoning.done'.
- **search_results** (array) - A list of web search results.
- **images** (array) - A list of image search results.
- **usage** (object) - Partial token usage statistics.
- **choices** (array) - Contains message and delta information.
  - **message** (object) - The assistant's message, potentially empty at this stage.
  - **delta** (object) - Contains role and potentially an empty content field.

#### Response Example (chat.reasoning.done chunk)
```json
{
  "id": "3dd9d463-0fef-47e3-af70-92f9fcc4db1f",
  "model": "sonar-pro",
  "created": 1759459505,
  "object": "chat.reasoning.done",
  "usage": {
    "prompt_tokens": 6,
    "completion_tokens": 0,
    "total_tokens": 6,
    "search_context_size": "low"
  },
  "search_results": [
    { "title": "Seattle Weather Today", "url": "...", "snippet": "..." },
    { "title": "Seattle Climate", "url": "...", "snippet": "..." }
  ],
  "images": [],
  "choices": [
    {
      "index": 0,
      "finish_reason": null,
      "message": {
        "role": "assistant",
        "content": "",
        "reasoning_steps": [/* ... */]
      },
      "delta": {
        "role": "assistant",
        "content": ""
      }
    }
  ]
}
```

### Python Handler Example
```python
def handle_reasoning_done(chunk):
    if chunk.object == "chat.reasoning.done":
        print("\n[Reasoning Complete]")
        if hasattr(chunk, 'search_results'):
            print(f"Found {len(chunk.search_results)} sources")
            for result in chunk.search_results[:3]:
                print(f" • {result['title']}")
        if hasattr(chunk, 'images'):
            print(f"Found {len(chunk.images)} images")
        if hasattr(chunk, 'usage'):
            print(f"Tokens used so far: {chunk.usage.total_tokens}")
```

### TypeScript Handler Example
```typescript
function handleReasoningDone(chunk: any) {
    if (chunk.object === "chat.reasoning.done") {
        console.log("\n[Reasoning Complete]");
        if (chunk.search_results) {
            console.log(`Found ${chunk.search_results.length} sources`);
            chunk.search_results.slice(0, 3).forEach((result: any) => {
                console.log(` • ${result.title}`);
            });
        }
        if (chunk.images) {
            console.log(`Found ${chunk.images.length} images`);
        }
        if (chunk.usage) {
            console.log(`Tokens used so far: ${chunk.usage.total_tokens}`);
        }
    }
}
```
```

--------------------------------

### API Portal for Organization Management

Source: https://docs.perplexity.ai/changelog/changelog

Introduces the new API portal for managing organizations, API keys, and monitoring usage. This portal aims to streamline administrative tasks and collaboration.

```APIDOC
## API Portal for Organization Management

### Description
A new portal is available to help organizations manage API keys, monitor usage, and streamline collaboration. Access it via the provided URL.

### Features
- **API Key Management**: Organize and manage API keys effectively.
- **Usage Insights**: Gain visibility into API consumption and team activity.
- **Collaboration Tools**: Enhance teamwork within your organization.

### Access
Visit: https://www.perplexity.ai/account/api/group
```

--------------------------------

### Chat Completions with Search Filtering

Source: https://docs.perplexity.ai/guides/chat-completions-guide

This section demonstrates how to use the Perplexity AI API's chat completions endpoint, including how to apply search filters for domain and recency.

```APIDOC
## POST /chat/completions

### Description
This endpoint allows you to generate chat completions using Perplexity's language models, with the ability to filter search results by domain and recency.

### Method
POST

### Endpoint
`https://api.perplexity.ai/chat/completions`

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
- **model** (string) - Required - The model name to use for completions (e.g., `sonar-pro`).
- **messages** (array) - Required - An array of message objects, where each object has a `role` (`user` or `assistant`) and `content`.
- **search_domain_filter** (array of strings) - Optional - Filters search results to specific domains (e.g., `["nature.com", "science.org"]`).
- **search_recency_filter** (string) - Optional - Filters search results by recency (e.g., `"month"`, `"week"`, `"day"`).

### Request Example
```json
{
  "model": "sonar-pro",
  "messages": [
    {
      "role": "user",
      "content": "Latest climate research findings"
    }
  ],
  "search_domain_filter": [
    "nature.com",
    "science.org"
  ],
  "search_recency_filter": "month"
}
```

### Response
#### Success Response (200)
- **choices** (array) - Contains the completion choices.
  - **message.content** (string) - The AI-generated response.
- **model** (string) - The model name used.
- **usage** (object) - Token consumption details.
  - **search_context_size** (integer) - Search context setting used.
- **id** (string) - Unique identifier for the response.
- **created** (integer) - Timestamp of creation.
- **object** (string) - Type of object returned.
- **search_results** (array) - Array of web sources with titles, URLs, and dates.

#### Response Example
```json
{
  "id": "chatcmpl-xxxxxxxxxxxxxxxxxxxxxxxxx",
  "object": "chat.completion",
  "created": 1700000000,
  "model": "sonar-pro",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "The latest climate research findings indicate..."
      },
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 100,
    "total_tokens": 125,
    "search_context_size": 5
  },
  "search_results": [
    {
      "title": "Study on Recent Climate Trends",
      "url": "https://www.nature.com/articles/s41558-023-01800-y",
      "date": "2023-10-26"
    },
    {
      "title": "Advances in Climate Modeling",
      "url": "https://www.science.org/doi/10.1126/science.adx9876",
      "date": "2023-11-01"
    }
  ]
}
```

### Error Handling
Perplexity API uses the same error format as OpenAI's API for compatibility.
```

--------------------------------

### Stream LLM Responses with Callbacks (TypeScript)

Source: https://docs.perplexity.ai/guides/streaming-responses

This TypeScript snippet demonstrates how to stream responses from a Perplexity AI model using callbacks. It handles content chunks, search results, and completion events, allowing for real-time processing of LLM output. Dependencies include the Perplexity client library.

```typescript
import { Perplexity } from "perplexity";

interface StreamCallbacks {
  onContent?: (content: string) => void;
  onSearchResults?: (results: any[]) => void;
  onComplete?: (content: string, metadata: any) => void;
}

async function streamWithCallbacks(query: string, callbacks: StreamCallbacks = {}) {
  const client = new Perplexity();
  const stream = await client.chat.completions.create({
    model: "sonar",
    messages: [{ role: "user", content: query }],
    stream: true
  });
  let fullContent = "";
  const metadata: any = {};

  for await (const chunk of stream) {
    // Handle content chunks
    if (chunk.choices[0]?.delta?.content) {
      const contentPiece = chunk.choices[0].delta.content;
      fullContent += contentPiece;
      callbacks.onContent?.(contentPiece);
    }
    // Handle search results
    if (chunk.search_results) {
      metadata.search_results = chunk.search_results;
      callbacks.onSearchResults?.(chunk.search_results);
    }
    // Handle other metadata
    if (chunk.usage) {
      metadata.usage = chunk.usage;
    }
    // Handle completion
    if (chunk.choices[0]?.finish_reason) {
      callbacks.onComplete?.(fullContent, metadata);
    }
  }
  return { content: fullContent, metadata };
}

// Usage example
const result = await streamWithCallbacks(
  "Explain the latest developments in renewable energy",
  {
    onContent: (content) => process.stdout.write(content),
    onSearchResults: (results) => process.stdout.write(`\n[Found ${results.length} sources]`),
    onComplete: (content, metadata) => {
      console.log(`\n\nCompleted. Total length: ${content.length} characters`);
      if (metadata.usage) {
        console.log(`Token usage:`, metadata.usage);
      }
    }
  }
);
```

--------------------------------

### Handling Metadata After Stream Completion in Python

Source: https://docs.perplexity.ai/guides/streaming-responses

Illustrates how to process search results and usage statistics, which become available only after the stream has completed. This is crucial for applications that rely on this data.

```python
# Don't expect search results until the stream is complete
if chunk.choices[0].finish_reason == "stop":
    # Now search results and usage info are available
    process_search_results(chunk.search_results)
    log_usage_stats(chunk.usage)
```

--------------------------------

### Basic Search with Perplexity Python SDK

Source: https://docs.perplexity.ai/guides/search-quickstart

Performs a basic web search query using the Perplexity Python SDK. It retrieves the latest AI developments from 2024, with a limit of 5 results and 2048 tokens per page. The code iterates through the results and prints the title and URL of each.

```python
from perplexity import Perplexity

client = Perplexity()
search = client.search.create(
  query="latest AI developments 2024",
  max_results=5,
  max_tokens_per_page=2048
)

for result in search.results:
  print(f"{result.title}: {result.url}")
```

--------------------------------

### Manual SSE Parsing with Python

Source: https://docs.perplexity.ai/guides/streaming-responses

This Python function demonstrates manual parsing of Server-Sent Events (SSE) without relying on an external library. It iterates through the response lines, decodes them, identifies SSE data, parses the JSON, and prints the content. This approach is useful when external libraries are not desired or feasible.

```python
import requests
import json

def stream_with_manual_parsing():
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "sonar",
        "messages": [{"role": "user", "content": "Explain quantum computing"}],
        "stream": True
    }
    response = requests.post(url, headers=headers, json=payload, stream=True)
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith('data: '):
                data_str = line[6:] # Remove 'data: ' prefix
                if data_str == '[DONE]':
                    break
                try:
                    chunk_data = json.loads(data_str)
                    content = chunk_data['choices'][0]['delta'].get('content', '')
                    if content:
                        print(content, end='')
                except json.JSONDecodeError:
                    continue

stream_with_manual_parsing()
```

--------------------------------

### Parse Perplexity API Response Content and Sources (Python)

Source: https://docs.perplexity.ai/guides/chat-completions-guide

Demonstrates how to extract the main AI-generated content and iterate through the search results (title, URL, date) from a Perplexity API response in Python. It also shows how to access token usage details.

```python
# Access the main response
content = response.choices[0].message.content
print(content)

# Access search sources
for result in response.search_results:
    print(f"Source: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"Date: {result['date']}")
    print("---")

# Check token usage
print(f"Tokens used: {response.usage.total_tokens}")
```

--------------------------------

### List Async Requests

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Retrieve a list of recent asynchronous chat completion requests, with options to filter by status and limit the number of results.

```APIDOC
## GET /async/chat/completions

### Description
Lists recent asynchronous chat completion requests.

### Method
GET

### Endpoint
`/async/chat/completions`

### Parameters
#### Query Parameters
- **limit** (integer) - Optional - The maximum number of requests to return.
- **status** (string) - Optional - Filters requests by their status (e.g., 'completed', 'failed').

### Response
#### Success Response (200)
- **data** (array) - An array of request objects.
  - **id** (string) - The ID of the request.
  - **status** (string) - The status of the request.

### Request Example (Python)
```python
requests = client.async_.chat.completions.list( limit=10, status="completed" )
for request in requests.data:
    print(f"ID: {request.id}, Status: {request.status}")
```

### Request Example (TypeScript)
```typescript
const requests = await client.async.chat.completions.list({ limit: 10, status: "completed" });
requests.data.forEach(request => {
  console.log(`ID: ${request.id}, Status: ${request.status}`);
});
```

### Response Example (JSON)
```json
{
  "data": [
    {
      "id": "req_123",
      "status": "completed"
    },
    {
      "id": "req_456",
      "status": "completed"
    }
  ]
}
```
```

--------------------------------

### Stream Chat Completions in Concise Mode - Python

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

Illustrates streaming chat completions with the 'sonar-pro' model in 'concise' stream mode. This mode provides more granular chunk types, including reasoning steps and completion chunks, allowing for better control and transparency. It also prints search result counts and total token usage.

```python
from perplexity import Perplexity

client = Perplexity()
stream = client.chat.completions.create(
    model="sonar-pro",
    messages=[{"role": "user", "content": "What's the weather?"}],
    stream=True,
    stream_mode="concise"  # Enable concise mode
)

for chunk in stream:  # Multiple chunk types - route appropriately
    if chunk.object == "chat.reasoning":  # New: Handle reasoning steps
        if chunk.choices[0].delta.reasoning_steps:
            print("Reasoning in progress...")
    elif chunk.object == "chat.reasoning.done":  # New: Reasoning complete, search results available
        if hasattr(chunk, 'search_results'):
            print(f"Sources: {len(chunk.search_results)}")
    elif chunk.object == "chat.completion.chunk":  # Content chunks (similar to full mode)
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="")
    elif chunk.object == "chat.completion.done":  # Final chunk with complete metadata
        print(f"\nTotal tokens: {chunk.usage.total_tokens}")
```

--------------------------------

### Enable Streaming Completion (TypeScript)

Source: https://docs.perplexity.ai/guides/streaming-responses

This TypeScript code snippet shows how to create a streaming chat completion using the Perplexity SDK. It requires the '@perplexity-ai/perplexity_ai' package. The response content is written to standard output as it arrives.

```typescript
import Perplexity from '@perplexity-ai/perplexity_ai';

const client = new Perplexity();

// Create streaming completion
const stream = await client.chat.completions.create({
    model: "sonar",
    messages: [{ role: "user", content: "What is the latest in AI research?" }],
    stream: true
});

// Process streaming response
for await (const chunk of stream) {
    if (chunk.choices[0]?.delta?.content) {
        process.stdout.write(chunk.choices[0].delta.content);
    }
}
```

--------------------------------

### Image Uploads for Multimodal Search

Source: https://docs.perplexity.ai/changelog

Utilize images as part of your multimodal search experience by uploading them directly. This feature is now available for all users.

```APIDOC
## Image Uploads for Multimodal Search

### Description
Allows users to upload images and integrate them into multimodal search queries with Sonar. 

### Documentation
For detailed instructions on how to use image uploads, please refer to the image upload guide: [https://docs.perplexity.ai/guides/image-attachments](https://docs.perplexity.ai/guides/image-attachments)
```

--------------------------------

### List Async Requests (Python & TypeScript)

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Shows how to list recent asynchronous chat completion requests using the Perplexity AI SDK in both Python and TypeScript. It allows filtering by status and iterates through the results to display request IDs and their statuses.

```python
# List recent async requests requests = client.async_.chat.completions.list( limit=10, status="completed" )
for request in requests.data:
    print(f"ID: {request.id}, Status: {request.status}")
```

```javascript
// List recent async requests const requests = await client.async.chat.completions.list({ limit: 10, status: "completed" });
requests.data.forEach(request => {
    console.log(`ID: ${request.id}, Status: ${request.status}`);
});
```

--------------------------------

### Streaming Responses with Perplexity SDKs and APIs

Source: https://docs.perplexity.ai/guides/streaming-responses

Learn how to stream real-time responses from the Perplexity API as they are generated. This is useful for real-time user experiences, long responses, and interactive applications.

```APIDOC
## Overview
Streaming allows you to receive partial responses from the Perplexity API as they are generated, rather than waiting for the complete response. This is particularly useful for:
*   **Real-time user experiences** - Display responses as they’re generated
*   **Long responses** - Start showing content immediately for lengthy analyses
*   **Interactive applications** - Provide immediate feedback to users

Streaming is supported across all Perplexity models including Sonar, Sonar Pro, and reasoning models.
```

```APIDOC
## Quick Start - Python SDK

### Method
POST

### Endpoint
(Implicitly handled by SDK)

### Description
This example demonstrates how to enable streaming for chat completions using the Perplexity Python SDK and process the streaming response.

### Request Example
```python
from perplexity import Perplexity

# Initialize the client (uses PERPLEXITY_API_KEY environment variable)
client = Perplexity()

# Create streaming completion
stream = client.chat.completions.create(
    model="sonar",
    messages=[{"role": "user", "content": "What is the latest in AI research?"}],
    stream=True
)

# Process streaming response
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### Response Example
(Output will be streamed token by token to the console.)
```

```APIDOC
## Quick Start - TypeScript SDK

### Method
POST

### Endpoint
(Implicitly handled by SDK)

### Description
This example shows how to enable streaming for chat completions using the Perplexity TypeScript SDK and process the streaming response.

### Request Example
```typescript
import Perplexity from '@perplexity-ai/perplexity_ai';

const client = new Perplexity();

// Create streaming completion
const stream = await client.chat.completions.create({
    model: "sonar",
    messages: [{ role: "user", content: "What is the latest in AI research?" }],
    stream: true
});

// Process streaming response
for await (const chunk of stream) {
    if (chunk.choices[0]?.delta?.content) {
        process.stdout.write(chunk.choices[0].delta.content);
    }
}
```

### Response Example
(Output will be streamed token by token to the console.)
```

```APIDOC
## Quick Start - cURL

### Method
POST

### Endpoint
/chat/completions

### Description
This example demonstrates how to enable streaming for chat completions using a cURL command.

### Request Example
```bash
curl -X POST "https://api.perplexity.ai/chat/completions" \
 -H "Authorization: Bearer YOUR_API_KEY" \
 -H "Content-Type: application/json" \
 -d '{ "model": "sonar", "messages": [{"role": "user", "content": "What is the latest in AI research?"}], "stream": true }'
```

### Response Example
(Output will be streamed chunk by chunk to the console.)
```

--------------------------------

### Async Chat Completions

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Use async endpoints for long-running or batch processing tasks, particularly with the 'sonar-deep-research' model. This allows initiating a request and checking its status later.

```APIDOC
## Async Chat Completions

### Description
Initiates and manages asynchronous chat completion requests.

### Method
POST (for creating requests), GET (for checking status)

### Endpoints
- **POST /async/chat/completions**: Creates an asynchronous completion request.
- **GET /async/chat/completions/{request_id}**: Retrieves the status and result of an asynchronous request.

### Parameters
#### POST /async/chat/completions
##### Request Body
- **messages** (array) - Required - A list of message objects.
- **model** (string) - Required - The model to use (e.g., "sonar-deep-research").
- **max_tokens** (integer) - Optional - Maximum tokens for the response.

#### GET /async/chat/completions/{request_id}
##### Path Parameters
- **request_id** (string) - Required - The unique identifier for the async request.

### Request Example (Create Async Request)
```json
{
  "messages": [
    {"role": "user", "content": "Write a comprehensive analysis of renewable energy trends"}
  ],
  "model": "sonar-deep-research",
  "max_tokens": 2000
}
```

### Response Example (Create Async Request)
```json
{
  "request_id": "req_123abc456def789",
  "status": "submitted"
}
```

### Response Example (Check Status - Completed)
```json
{
  "request_id": "req_123abc456def789",
  "status": "completed",
  "result": {
    "choices": [
      {
        "message": {
          "role": "assistant",
          "content": "Renewable energy trends show significant growth in solar and wind power..."
        }
      }
    ]
  }
}
```

### Response Example (Check Status - In Progress)
```json
{
  "request_id": "req_123abc456def789",
  "status": "processing"
}
```
```

--------------------------------

### API Usage Cost Breakdown

Source: https://docs.perplexity.ai/changelog/changelog

This snippet shows the structure of the usage object returned by the Perplexity AI API, detailing token counts and associated costs for input, output, and the total request. It helps users track and understand the billing for each API call.

```json
{
  "usage": {
    "prompt_tokens": 8,
    "completion_tokens": 439,
    "total_tokens": 447,
    "search_context_size": "low",
    "cost": {
      "input_tokens_cost": 0.000024,
      "output_tokens_cost": 0.006585,
      "request_cost": 0.006,
      "total_cost": 0.012609
    }
  }
}
```

--------------------------------

### Response Customization

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Customize the response format and behavior, including limiting response length, controlling creativity, diversity, and repetition.

```APIDOC
## POST /chat/completions (with Response Customization)

### Description
Generates a text completion with customized response parameters.

### Method
POST

### Endpoint
/chat/completions

### Parameters
#### Request Body
- **messages** (array) - Required - A list of message objects.
- **model** (string) - Required - The model to use (e.g., "sonar").
- **max_tokens** (integer) - Optional - Limits the length of the generated response.
- **temperature** (number) - Optional - Controls the creativity of the response (0.0 to 2.0).
- **top_p** (number) - Optional - Controls the diversity of the response (0.0 to 1.0).
- **presence_penalty** (number) - Optional - Reduces repetition of tokens already present in the response (-2.0 to 2.0).
- **frequency_penalty** (number) - Optional - Reduces repetition of tokens based on their frequency in the response (-2.0 to 2.0).

### Request Example
```json
{
  "messages": [
    {"role": "user", "content": "Explain machine learning in simple terms"}
  ],
  "model": "sonar",
  "max_tokens": 500,
  "temperature": 0.7,
  "top_p": 0.9,
  "presence_penalty": 0.1,
  "frequency_penalty": 0.1
}
```

### Response
#### Success Response (200)
- **choices** (array) - Completion choices containing the generated message content.

#### Response Example
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Machine learning is a type of artificial intelligence that allows computer systems to learn from data without being explicitly programmed..."
      }
    }
  ]
}
```
```

--------------------------------

### Analyze Document via Base64 Encoded Bytes (cURL)

Source: https://docs.perplexity.ai/guides/file-attachments

This cURL command shows how to analyze a document by sending its content as base64 encoded bytes in the request payload. It includes the API endpoint, authorization, content type, and a JSON body with the user message and the base64 encoded file content, along with a file name. The 'sonar-pro' model is specified.

```shell
curl -X POST "https://api.perplexity.ai/chat/completions" \
-H "Authorization: Bearer YOUR_API_KEY" \
-H "Content-Type: application/json" \
-d '{ "messages": [ { "content": [ { "type": "text", "text": "Summarize this document" }, { "type": "file_url", "file_url": { "url": "JVBERi0xLjQKJeLjz9MKNCAwIG9iago..." }, "file_name": "report.pdf" } ], "role": "user" } ], "model": "sonar-pro" }'
```

--------------------------------

### Chat Completion API

Source: https://docs.perplexity.ai/api-reference/chat-completions-post

This section details the parameters available for customizing chat completions, including temperature, response formatting, searchDisabling, and media response configurations. It also outlines the structure of the successful response.

```APIDOC
## POST /chat/completions

### Description
Generates a chat completion response based on the provided messages and model configuration. Allows for fine-tuning response characteristics such as creativity, search usage, and media inclusion.

### Method
POST

### Endpoint
/chat/completions

### Parameters
#### Query Parameters
- **temperature** (number) - Optional - Controls the randomness of the output. Values range from 0 to 2.0, with higher values reducing repetition.
- **response_format** (object) - Optional - Enables structured JSON output formatting.
  - **type** (string) - Required - Specifies the desired response format (e.g., 'json_object').
- **disable_search** (boolean) - Optional - Defaults to false. When true, disables web search and uses only training data for responses.
- **enable_search_classifier** (boolean) - Optional - Defaults to false. Enables a classifier to determine if web search is needed.
- **web_search_options** (object) - Optional - Configuration for using web search.
  - **search_context_size** (string) - Optional - Example: 'high'.
- **media_response** (object) - Optional - Configuration for controlling media content in responses.
  - **overrides** (object) - Optional - Enables specific media types.
    - **return_videos** (boolean) - Optional - Whether to return videos.
    - **return_images** (boolean) - Optional - Whether to return images.

### Request Example
```json
{
  "model": "model_name",
  "messages": [
    {"role": "user", "content": "Hello!"}
  ],
  "temperature": 0.7,
  "response_format": {"type": "json_object"},
  "disable_search": false,
  "enable_search_classifier": true,
  "web_search_options": {"search_context_size": "high"},
  "media_response": {"overrides": {"return_videos": true, "return_images": true}}
}
```

### Response
#### Success Response (200)
- **id** (string) - A unique identifier for the chat completion.
- **model** (string) - The model that generated the response.
- **created** (integer) - The Unix timestamp (in seconds) of when the chat completion was created.
- **usage** (object) - Information about the token usage.
- **object** (string) - The type of object, always 'chat.completion'.
- **choices** (array) - A list of chat completion choices.
- **search_results** (array | null) - A list of search results related to the response.
- **videos** (array | null) - A list of video results.

#### Response Example
```json
{
  "id": "chatcmpl-xxxxxxxxxx",
  "model": "gpt-4",
  "created": 1677652288,
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  },
  "object": "chat.completion",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello there! How can I help you today?"
      },
      "finish_reason": "stop"
    }
  ],
  "search_results": null,
  "videos": null
}
```
```

--------------------------------

### Handling chat.completion.chunk Chunks

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

Processes 'chat.completion.chunk' chunks, which are streamed during the response generation phase and contain the actual content being generated by the model.

```APIDOC
## POST /chat/completions (Hypothetical Endpoint for Streaming)

### Description
These chunks contain fragments of the final generated response. They are streamed sequentially and should be concatenated to form the complete answer. Each chunk typically includes a small piece of text content.

### Method
POST

### Endpoint
/chat/completions

### Parameters
(See previous section for request parameters; this focuses on the response chunk)

### Response
#### Success Response (200 OK - Streaming Chunks)
- **object** (string) - Should be 'chat.completion.chunk'.
- **choices** (array) - Contains the streamed content.
  - **delta** (object) - Contains the generated text content.
    - **role** (string) - The role of the speaker (usually 'assistant').
    - **content** (string) - The piece of text content generated in this chunk.
  - **finish_reason** (string) - Indicates why the stream has finished (e.g., 'stop', null).

#### Response Example (chat.completion.chunk chunk)
```json
{
  "id": "cfa38f9d-fdbc-4ac6-a5d2-a3010b6a33a6",
  "model": "sonar-pro",
  "created": 1759441592,
  "object": "chat.completion.chunk",
  "choices": [
    {
      "index": 0,
      "finish_reason": null,
      "message": {
        "role": "assistant",
        "content": ""
      },
      "delta": {
        "role": "assistant",
        "content": " tonight"
      }
    }
  ]
}
```

### Python Handler Example
```python
def handle_completion_chunk(chunk):
    if chunk.object == "chat.completion.chunk":
        delta = chunk.choices[0].delta
        if hasattr(delta, 'content') and delta.content:
            print(delta.content, end='', flush=True)
            return delta.content
    return ""
```

### TypeScript Handler Example
```typescript
function handleCompletionChunk(chunk: any): string {
    if (chunk.object === "chat.completion.chunk") {
        const delta = chunk.choices[0]?.delta;
        if (delta?.content) {
            process.stdout.write(delta.content);
            return delta.content;
        }
    }
    return "";
}
```
```

--------------------------------

### Chat Completions with Streaming and Callbacks

Source: https://docs.perplexity.ai/guides/streaming-responses

This endpoint allows you to create chat completions with streaming enabled. It supports callbacks for handling content chunks, search results, and completion events.

```APIDOC
## POST /chat/completions

### Description
Creates a chat completion request with streaming enabled, allowing for real-time processing of responses. It utilizes callbacks to handle different parts of the streamed response, including content, search results, and completion status.

### Method
POST

### Endpoint
/chat/completions

### Parameters
#### Query Parameters
- **query** (string) - Required - The user's query to the language model.
- **callbacks** (object) - Optional - An object containing callback functions for handling different parts of the stream:
  - **onContent** (function) - Optional - Callback for handling content chunks.
  - **onSearchResults** (function) - Optional - Callback for handling search result data.
  - **onComplete** (function) - Optional - Callback for handling the completion of the stream.

### Request Example
```json
{
  "model": "sonar",
  "messages": [{"role": "user", "content": "Explain the latest developments in renewable energy"}],
  "stream": true
}
```

### Response
#### Success Response (200)
- **content** (string) - The full content of the model's response.
- **metadata** (object) - Additional metadata, potentially including search results and token usage.

#### Response Example
```json
{
  "content": "The latest developments in renewable energy include advancements in solar panel efficiency...",
  "metadata": {
    "search_results": [...],
    "usage": {
      "prompt_tokens": 10,
      "completion_tokens": 50
    }
  }
}
```
```

--------------------------------

### Configure Web Search Options in Perplexity AI

Source: https://docs.perplexity.ai/api-reference/chat-completions-post

Defines how web search is utilized in Perplexity AI model responses. The `web_search_options` object allows for specific configurations, such as setting the search context size.

```json
{
  "search_context_size": "high"
}
```

--------------------------------

### API Key Rotation Mechanism

Source: https://docs.perplexity.ai/changelog

Enhance security and simplify key management with the new API key rotation system. Features seamless rotation, automated workflows, and zero downtime transitions.

```APIDOC
## New: API Key Rotation Mechanism

### Description
Implement a comprehensive API key rotation system to enhance security and simplify key management. This feature allows for seamless key replacement without service interruption, automated rotation schedules, and provides an audit trail for key usage.

### Method
POST / PUT / DELETE (for managing keys via API Portal)

### Endpoint
`/api-keys/rotate` (conceptual endpoint for rotation actions)

### Parameters
#### Path Parameters
- **key_id** (string) - Required - The ID of the API key to manage.

#### Request Body (for generation/rotation)
- **rotation_schedule** (string) - Optional - Defines the frequency of automatic rotation (e.g., '30d', '90d').

### Request Example (Initiating rotation)
```json
{
  "key_id": "your_existing_key_id",
  "rotation_schedule": "60d"
}
```

### Response
#### Success Response (200)
- **message** (string) - Confirmation of the action taken (e.g., 'New API key generated successfully', 'Rotation schedule updated').
- **new_key** (string) - The newly generated API key (if applicable).

#### Response Example
```json
{
  "message": "New API key generated successfully. Please update your applications before the old key expires.",
  "new_key": "new_secret_api_key_value"
}
```
```

--------------------------------

### Usage and Cost Tracking

Source: https://docs.perplexity.ai/changelog

Information on how to track API usage and associated costs, which are included directly in the API response.

```APIDOC
## Usage and Cost Information

### Description
Each API response includes a "usage" object that details token consumption and associated costs for the request.

### Fields in Usage Object:
- **prompt_tokens** (integer) - The number of tokens consumed by the input prompt.
- **completion_tokens** (integer) - The number of tokens generated in the response.
- **total_tokens** (integer) - The sum of prompt and completion tokens.
- **search_context_size** (string) - The search context size used for the request (e.g., "low", "medium", "high").

### Cost Breakdown (within Usage Object):
- **input_tokens_cost** (float) - The cost attributed to input tokens.
- **output_tokens_cost** (float) - The cost attributed to output tokens.
- **request_cost** (float) - A fixed cost per API request.
- **total_cost** (float) - The total cost for the API call.

### Example Usage Object in Response:
```json
{
  "usage": {
    "prompt_tokens": 8,
    "completion_tokens": 439,
    "total_tokens": 447,
    "search_context_size": "low",
    "cost": {
      "input_tokens_cost": 0.000024,
      "output_tokens_cost": 0.006585,
      "request_cost": 0.006,
      "total_cost": 0.012609
    }
  }
}
```
```

--------------------------------

### Proper SSE Parsing with JavaScript using EventSource

Source: https://docs.perplexity.ai/guides/streaming-responses

This JavaScript function shows how to handle Server-Sent Events (SSE) in a browser environment using the native `EventSource` API. It connects to a specified server endpoint, parses incoming data, and appends content to an HTML element. Error handling for the connection is also included.

```javascript
// For browser environments
function streamInBrowser() {
    const eventSource = new EventSource('/api/stream'); // Your server endpoint
    eventSource.onmessage = function(event) {
        if (event.data === '[DONE]') {
            eventSource.close();
            return;
        }
        try {
            const chunk = JSON.parse(event.data);
            const content = chunk.choices[0]?.delta?.content;
            if (content) {
                document.getElementById('output').innerHTML += content;
            }
        } catch (e) {
            console.error('Error parsing chunk:', e);
        }
    };
    eventSource.onerror = function(event) {
        console.error('EventSource failed:', event);
        eventSource.close();
    };
}

```

--------------------------------

### Concurrent Operations

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Execute multiple chat completion requests concurrently to improve efficiency when handling several user inputs simultaneously.

```APIDOC
## POST /chat/completions (Concurrent Operations)

### Description
Handles multiple chat conversations concurrently using asynchronous operations for improved performance.

### Method
POST

### Endpoint
`/chat/completions`

### Parameters
#### Request Body (per request)
- **messages** (array) - Required - An array of message objects with 'role' and 'content'.
- **model** (string) - Required - The model to use for the completion.

### Request Example (Python)
```python
import asyncio
from perplexity import AsyncPerplexity

async def handle_multiple_chats(user_messages):
    client = AsyncPerplexity()
    tasks = [
        client.chat.completions.create(
            messages=[{"role": "user", "content": msg}],
            model="sonar-deep-reseach"
        )
        for msg in user_messages
    ]
    return await asyncio.gather(*tasks, return_exceptions=True)
```

### Request Example (TypeScript)
```typescript
async function processQuestions(questions: string[]) {
  const tasks = questions.map(question =>
    client.chat.completions.create({
      messages: [{ role: "user", content: question }],
      model: "sonar-deep-research"
    })
  );
  const results = await Promise.all(tasks);
  return results.map(result => result.choices[0].message.content);
}

const questions = [
  "What is artificial intelligence?",
  "How does machine learning work?",
  "What are neural networks?"
];
const answers = await processQuestions(questions);
```
```

--------------------------------

### Create Async Chat Completion Request (cURL)

Source: https://docs.perplexity.ai/api-reference/async-chat-completions-post

This cURL command demonstrates how to create an asynchronous chat completion job using the Perplexity AI API. It includes essential headers for authorization and content type, along with a JSON payload specifying the model, messages, search parameters, and various configuration options.

```curl
curl --request POST \
  --url https://api.perplexity.ai/async/chat/completions \
  --header 'Authorization: Bearer ' \
  --header 'Content-Type: application/json' \
  --data ' {
    "request": {
      "model": "sonar-deep-research",
      "messages": [
        { "role": "system", "content": "Be precise and concise." },
        { "role": "user", "content": "How many stars are there in our galaxy?" }
      ],
      "search_mode": "web",
      "reasoning_effort": "low",
      "max_tokens": 123,
      "temperature": 0.2,
      "top_p": 0.9,
      "language_preference": "",
      "search_domain_filter": "",
      "return_images": false,
      "return_related_questions": false,
      "search_recency_filter": "",
      "search_after_date_filter": "",
      "search_before_date_filter": "",
      "last_updated_after_filter": "",
      "last_updated_before_filter": "",
      "top_k": 0,
      "stream": false,
      "presence_penalty": 0,
      "frequency_penalty": 0,
      "response_format": {},
      "disable_search": false,
      "enable_search_classifier": false,
      "web_search_options": {
        "search_context_size": "low",
        "image_search_relevance_enhanced": false
      },
      "media_response": {
        "overrides": {
          "return_videos": false,
          "return_images": false
        }
      }
    }
  } '
```

--------------------------------

### TypeScript: Perform Web Search with Perplexity API

Source: https://docs.perplexity.ai/chat-with-persistence

This TypeScript code snippet illustrates how to perform a web search using the Perplexity API. It utilizes an asynchronous function to send a POST request to the search endpoint, including the necessary authorization header and a JSON body with the search query. Ensure you have the appropriate Perplexity SDK or HTTP client configured.

```typescript
import fetch from 'node-fetch';

async function searchPerplexity(query: string) {
  const response = await fetch('https://api.perplexity.ai/search', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer YOUR_API_KEY`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ query: query })
  });
  const data = await response.json();
  console.log(data);
}

searchPerplexity('What is Comet Browser?');
```

--------------------------------

### Enable Concise Stream Mode with cURL

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

Provides a cURL command to make a request to the Perplexity API enabling 'concise' stream mode. It includes necessary headers and a JSON payload for a chat completion.

```bash
curl -X POST "https://api.perplexity.ai/chat/completions" \
 -H "Authorization: Bearer YOUR_API_KEY" \
 -H "Content-Type: application/json" \
 -d '{ "model": "sonar-pro", "messages": [{"role": "user", "content": "What is the weather in Seattle?"}], "stream": true, "stream_mode": "concise" }'
```

--------------------------------

### Search Government and Educational Sources

Source: https://docs.perplexity.ai/guides/search-domain-filter-guide

Use top-level domain filtering to search across all government (.gov) or educational (.edu) institutions.

```APIDOC
## POST /search

### Description
Filters search results to include only content from government (.gov) or educational (.edu) domains.

### Method
POST

### Endpoint
/search

### Parameters
#### Query Parameters
- **query** (string) - Required - The search query.
- **max_results** (integer) - Optional - The maximum number of results to return.
- **search_domain_filter** (array of strings) - Optional - Filters search results to include or exclude content from specified domains.

### Request Example
```json
{
  "query": "climate change policy research",
  "max_results": 15,
  "search_domain_filter": [
    ".gov",
    ".edu"
  ]
}
```

### Response
#### Success Response (200)
- **results** (array) - A list of search results.
  - **title** (string) - The title of the search result.
  - **url** (string) - The URL of the search result.

#### Response Example
```json
{
  "results": [
    {
      "title": "Report on Climate Policy",
      "url": "https://www.epa.gov/climate-policy"
    }
  ]
}
```
```

--------------------------------

### Check Async Request Status (Python & TypeScript)

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Demonstrates how to retrieve the status of an asynchronous chat completion request using both Python and TypeScript SDKs. It checks if the request has completed successfully or failed, logging the outcome and any associated errors.

```python
lif status.status == "failed": print(f"Error: {status.error}")
```

```javascript
// Check the status of an async request const requestId = "req_123abc456def789"; const status = await client.async.chat.completions.get(requestId); console.log(`Status: ${status.status}`); if (status.status === "completed") { console.log(`Response: ${status.result?.choices[0]?.message?.content}`); } else if (status.status === "failed") { console.log(`Error: ${status.error}`); }
```

--------------------------------

### POST /search

Source: https://docs.perplexity.ai/api-reference

Retrieves ranked search results from Perplexity's index with advanced filtering and customization options.

```APIDOC
## POST /search

### Description
Get ranked search results from Perplexity’s continuously refreshed index with advanced filtering and customization options.

### Method
POST

### Endpoint
https://api.perplexity.ai/search

### Parameters
#### Query Parameters
(None)

#### Headers
- **Authorization** (string) - Required - Bearer authentication token.
- **Content-Type** (string) - Required - Must be `application/json`.

#### Request Body
- **query** (string) - Required - A search query.
- **max_results** (integer) - Optional - The maximum number of search results to return. (1-20, default: 10)
- **max_tokens** (integer) - Optional - The maximum total number of tokens of webpage content returned. (1-1000000, default: 25000)
- **search_domain_filter** (array of strings) - Optional - A list of domains/URLs to limit search results to. (Max 20 domains)
- **max_tokens_per_page** (integer) - Optional - Controls the maximum number of tokens retrieved from each webpage. (default: 2048)
- **country** (string) - Optional - Country code to filter search results by geographic location (e.g., 'US', 'GB', 'DE').
- **search_recency_filter** (enum) - Optional - Filters search results based on recency. Available options: `day`, `week`, `month`, `year`. (default: 'week')
- **search_after_date** (string) - Optional - Filters search results to only include content published after this date. Format: `MM/DD/YYYY`.
- **search_before_date** (string) - Optional - Filters search results to only include content published before this date. Format: `MM/DD/YYYY`.
- **last_updated_after_filter** (string) - Optional - Filters search results to only include content last updated after this date. Format: `MM/DD/YYYY`.
- **last_updated_before_filter** (string) - Optional - Filters search results to only include content last updated before this date. Format: `MM/DD/YYYY`.

### Request Example
```json
{
  "query": "latest AI developments 2024",
  "max_results": 10,
  "max_tokens": 25000,
  "search_domain_filter": [
    "science.org",
    "pnas.org",
    "cell.com"
  ],
  "max_tokens_per_page": 2048,
  "country": "US",
  "search_recency_filter": "week",
  "search_after_date": "10/15/2025",
  "search_before_date": "10/16/2025",
  "last_updated_after_filter": "07/01/2025",
  "last_updated_before_filter": "12/30/2025",
  "search_language_filter": [
    "en",
    "fr",
    "de"
  ]
}
```

### Response
#### Success Response (200)
- **results** (array) - An array of search result objects.
  - **title** (string) - The title of the search result.
  - **url** (string) - The URL of the search result.
  - **snippet** (string) - A short snippet of the content from the search result.
  - **date** (string) - The publication date of the content.
  - **last_updated** (string) - The last updated date of the content.

#### Response Example
```json
{
  "results": [
    {
      "title": "",
      "url": "",
      "snippet": "",
      "date": "2025-03-20",
      "last_updated": "2025-09-19"
    }
  ]
}
```
```

--------------------------------

### Handle End of Reasoning Stage (Python & TypeScript)

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

Processes the 'chat.reasoning.done' chunk, signaling the end of the reasoning phase. It aggregates and displays information about search results, images, and token usage.

```python
def handle_reasoning_done(chunk):
    """Process end of reasoning stage"""
    if chunk.object == "chat.reasoning.done":
        print("\n[Reasoning Complete]")
        # Access all search results
        if hasattr(chunk, 'search_results'):
            print(f"Found {len(chunk.search_results)} sources")
            for result in chunk.search_results[:3]:
                print(f" • {result['title']}")
        # Access image results
        if hasattr(chunk, 'images'):
            print(f"Found {len(chunk.images)} images")
        # Partial usage stats available
        if hasattr(chunk, 'usage'):
            print(f"Tokens used so far: {chunk.usage.total_tokens}")
```

```typescript
function handleReasoningDone(chunk: any) {
    if (chunk.object === "chat.reasoning.done") {
        console.log("\n[Reasoning Complete]");
        // Access all search results
        if (chunk.search_results) {
            console.log(`Found ${chunk.search_results.length} sources`);
            chunk.search_results.slice(0, 3).forEach((result: any) => {
                console.log(` • ${result.title}`);
            });
        }
        // Access image results
        if (chunk.images) {
            console.log(`Found ${chunk.images.length} images`);
        }
        // Partial usage stats available
        if (chunk.usage) {
            console.log(`Tokens used so far: ${chunk.usage.total_tokens}`);
        }
    }
}
```

--------------------------------

### Search Mode Configuration

Source: https://docs.perplexity.ai/api-reference/chat-completions-post

Specifies the type of search to be performed. Options include 'academic' for scholarly sources, 'sec' for SEC filings, and 'web' for general web search. This parameter influences the data sources used to generate responses.

```text
search_mode: 'academic' | 'sec' | 'web'
```

--------------------------------

### Analyze Document via Public URL (cURL)

Source: https://docs.perplexity.ai/guides/file-attachments

This cURL command demonstrates how to send a POST request to the Perplexity API to analyze a document provided via a public URL. It includes the API endpoint, authorization header, content type, and a JSON payload specifying the user's message and the file URL. The 'sonar-pro' model is used for analysis.

```shell
curl -X POST "https://api.perplexity.ai/chat/completions" \
-H "Authorization: Bearer YOUR_API_KEY" \
-H "Content-Type: application/json" \
-d '{ "messages": [ { "content": [ { "type": "text", "text": "Summarize this document" }, { "type": "file_url", "file_url": { "url": "https://example.com/document.pdf" } } ], "role": "user" } ], "model": "sonar-pro" }'
```

--------------------------------

### Handling chat.completion.done Chunks

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

Processes the final 'chat.completion.done' chunk, which signals the end of the response stream and includes complete usage statistics, cost information, and the full generated message.

```APIDOC
## POST /chat/completions (Hypothetical Endpoint for Streaming)

### Description
This is the final chunk in a streaming response. It indicates that the content generation is complete and provides crucial metadata such as total token usage, cost incurred, final search results, and the complete assistant message.

### Method
POST

### Endpoint
/chat/completions

### Parameters
(See previous section for request parameters; this focuses on the response chunk)

### Response
#### Success Response (200 OK - Streaming Chunks)
- **object** (string) - Should be 'chat.completion.done'.
- **usage** (object) - Complete usage statistics and cost breakdown.
  - **prompt_tokens** (integer) - Tokens used for the prompt.
  - **completion_tokens** (integer) - Tokens used for the completion.
  - **total_tokens** (integer) - Total tokens used in the request.
  - **cost** (object) - Cost details.
    - **input_tokens_cost** (float) - Cost of input tokens.
    - **output_tokens_cost** (float) - Cost of output tokens.
    - **request_cost** (float) - Total cost for the request.
    - **total_cost** (float) - Aggregated total cost.
- **search_results** (array) - Final list of search results used.
- **images** (array) - Final list of images found.
- **choices** (array) - Contains the final message and delta.
  - **index** (integer) - Index of the choice.
  - **finish_reason** (string) - Indicates why the stream finished (e.g., 'stop').
  - **message** (object) - The complete assistant message.
    - **role** (string) - Role of the speaker ('assistant').
    - **content** (string) - The full generated content.
    - **reasoning_steps** (array) - All reasoning steps.
  - **delta** (object) - Final delta, often empty content.

#### Response Example (chat.completion.done chunk)
```json
{
  "id": "cfa38f9d-fdbc-4ac6-a5d2-a3010b6a33a6",
  "model": "sonar-pro",
  "created": 1759441595,
  "object": "chat.completion.done",
  "usage": {
    "prompt_tokens": 6,
    "completion_tokens": 238,
    "total_tokens": 244,
    "search_context_size": "low",
    "cost": {
      "input_tokens_cost": 0.0,
      "output_tokens_cost": 0.004,
      "request_cost": 0.006,
      "total_cost": 0.01
    }
  },
  "search_results": [/* ... */],
  "images": [/* ... */],
  "choices": [
    {
      "index": 0,
      "finish_reason": "stop",
      "message": {
        "role": "assistant",
        "content": "## Seattle Weather Forecast\n\nSeattle is experiencing...",
        "reasoning_steps": [/* ... */]
      },
      "delta": {
        "role": "assistant",
        "content": ""
      }
    }
  ]
}
```

### Python Handler Example
```python
def handle_completion_done(chunk):
    if chunk.object == "chat.completion.done":
        print("\n\n[Stream Complete]")
        full_message = chunk.choices[0].message.content
        if hasattr(chunk, 'search_results'):
            print(f"\nFinal sources: {len(chunk.search_results)}")
        # Process final usage and cost information here
        if hasattr(chunk, 'usage') and hasattr(chunk.usage, 'cost'):
            print(f"Total Cost: ${chunk.usage.cost.total_cost:.4f}")
```

### TypeScript Handler Example
```typescript
function handleCompletionDone(chunk: any) {
    if (chunk.object === "chat.completion.done") {
        console.log("\n\n[Stream Complete]");
        const fullMessage = chunk.choices[0].message.content;
        if (chunk.search_results) {
            console.log(`\nFinal sources: ${chunk.search_results.length}`);
        }
        // Process final usage and cost information here
        if (chunk.usage && chunk.usage.cost) {
            console.log(`Total Cost: $${chunk.usage.cost.total_cost.toFixed(4)}`);
        }
    }
}
```
```

--------------------------------

### Stream Processing with Callbacks in Python

Source: https://docs.perplexity.ai/guides/streaming-responses

This Python function outlines a structure for processing streaming data with callbacks. It allows custom functions to be defined for handling content chunks (`on_content`), search results (`on_search_results`), and overall completion (`on_complete`). This enables flexible integration of streaming data into various application logic. Dependencies: `perplexity` SDK.

```python
from perplexity import Perplexity
from typing import Callable, Optional

def stream_with_callbacks( 
    query: str,
    on_content: Optional[Callable[[str], None]] = None,
    on_search_results: Optional[Callable[[list], None]] = None,
    on_complete: Optional[Callable[[str, dict], None]] = None
):
    client = Perplexity()
    stream = client.chat.completions.create(
        model="sonar",
        messages=[{"role": "user", "content": query}],
        stream=True
    )
    # Logic to process stream and call callbacks would go here...
    # Example placeholder:
    full_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            if on_content:
                on_content(content)
            full_response += content
        # Handle other event types like search_results if applicable
        # if chunk.choices[0].delta.search_results:
        #     if on_search_results:
        #         on_search_results(chunk.choices[0].delta.search_results)

    # Call on_complete with the full response and any metadata
    # if on_complete:
    #     on_complete(full_response, metadata)

# Example usage:
# def handle_content(content):
#     print(f"Received content: {content}")
#
# stream_with_callbacks("Explain AI", on_content=handle_content)
```

--------------------------------

### Buffered Streaming with Python SDK

Source: https://docs.perplexity.ai/guides/streaming-responses

This Python function implements buffered streaming for processing chunks in batches. It collects content into a buffer and flushes it when a specified size is reached or a time interval has passed. This is useful for managing output frequency or performing batch processing. Dependencies: `perplexity` SDK.

```python
from perplexity import Perplexity
import time

def buffered_streaming(buffer_size=50, flush_interval=1.0):
    client = Perplexity()
    stream = client.chat.completions.create(
        model="sonar",
        messages=[{"role": "user", "content": "Write a detailed explanation of machine learning"}],
        stream=True
    )
    buffer = ""
    last_flush = time.time()
    for chunk in stream:
        if chunk.choices[0].delta.content:
            buffer += chunk.choices[0].delta.content
            # Flush buffer if it's full or enough time has passed
            if len(buffer) >= buffer_size or (time.time() - last_flush) >= flush_interval:
                print(buffer, end='', flush=True)
                buffer = ""
                last_flush = time.time()
    # Flush remaining buffer
    if buffer:
        print(buffer, end='', flush=True)

buffered_streaming()
```

--------------------------------

### Perplexity API: Search Domain Filter Syntax (JSON)

Source: https://docs.perplexity.ai/guides/search-domain-filter-guide

Illustrates the JSON syntax for using the search_domain_filter parameter in the Perplexity API for both allowlist and denylist modes. Allowlist mode includes only specified domains, while denylist mode excludes specified domains using a '-' prefix. A maximum of 20 domains can be specified per request.

```json
// Allowlist: Only search these domains
"search_domain_filter": ["nature.com", "science.org", "cell.com"]

// Denylist: Exclude these domains
"search_domain_filter": ["-reddit.com", "-pinterest.com", "-quora.com"]
```

--------------------------------

### Domain Filtering for Search Results

Source: https://docs.perplexity.ai/api-reference/chat-completions-post

Limits search results to a specified list of domains. Can be used for allowlisting or denylisting (by prefixing with '-'). Currently supports up to 20 domains.

```text
search_domain_filter: string[]
```

--------------------------------

### Basic Search Response Structure

Source: https://docs.perplexity.ai/guides/search-quickstart

Illustrates the JSON response structure for a basic Perplexity Search API query. It includes a list of search results, each with a title, URL, and snippet.

```json
{
  "results": [
    {
      "title": "2024: A year of extraordinary progress and advancement in AI - Google Blog",
      "url": "https://blog.google/technology/ai/2024-ai-extraordinary-progress-advancement/",
      "snippet": "## Relentless innovation in models, products and technologies\\n\\n2024 was a year of experimenting, fast shipping, and putting our latest technologies in the hands of developers.\\n\nIn December 2024, we released the first models in our Gemini 2.0 experimental series — AI models designed for the agentic era. First out of the gate was Gemini 2.0 Flash, our workhorse model, followed by prototypes from the frontiers of our agentic research including: an updated Project Astra, which explores the capabilities of a universal AI assistant; Project Mariner, an early prototype capable of taking actions in Chrome as an experimental extension; and Jules, an AI-powered code agent. We're looking forward to bringing Gemini 2.0’s powerful capabilities to our flagship products — in Search, we've already started testing in AI Overviews, which are now used by over a billion people to ask new types of questions.\n\nWe also released Deep Research, a new agentic feature in Gemini Advanced that saves people hours of research work by creating and executing multi-step plans for finding answers to complicated questions; and introduced Gemini 2.0 Flash Thinking Experimental, an experimental model that explicitly shows its thoughts.\n\nThese advances followed swift progress earlier in the year"
    }
  ]
}
```

--------------------------------

### Stream Responses with Perplexity AI SDK

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Implements streaming for lengthy responses to improve user experience. This function sends a query to the Perplexity AI API and prints the response in chunks as they arrive.

```python
def stream_response(query):
    stream = client.chat.completions.create(
        messages=[{"role": "user", "content": query}],
        model="sonar", stream=True
    )
    response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            response += content
    return response
```

```typescript
async function streamResponse(query: string): Promise {
    const stream = await client.chat.completions.create({
        messages: [{ role: "user", content: query }],
        model: "sonar", stream: true
    });
    let response = "";
    for await (const chunk of stream) {
        if (chunk.choices[0]?.delta?.content) {
            const content = chunk.choices[0].delta.content;
            process.stdout.write(content);
            response += content;
        }
    }
    return response;
}
```

--------------------------------

### Call Perplexity API Chat Completions with Sonar Pro (cURL)

Source: https://docs.perplexity.ai/getting-started/models/models/sonar-pro

This snippet demonstrates how to make a POST request to the Perplexity API's chat completions endpoint using cURL. It specifies the 'sonar-pro' model and provides a user message for analysis. The response includes metadata like ID, model used, creation timestamp, token usage, cost, citations, and search results.

```curl
--request POST \
--url https://api.perplexity.ai/chat/completions \
--header "Authorization: Bearer " \
--header "Content-Type: application/json" \
--data '{ "model": "sonar-pro", "messages": [ { "role": "user", "content": "Analyze the competitive positioning of Perplexity in the AI search market and evaluate how Comet compares to similar offerings from other companies." } ] }' | jq
```

--------------------------------

### Search with Language Filter

Source: https://docs.perplexity.ai/guides/search-language-filter

Demonstrates how to use the `search_language_filter` parameter to retrieve content in specific languages.

```APIDOC
## POST /api/search

### Description
Filters search results to only include content in the specified languages.

### Method
POST

### Endpoint
/api/search

### Parameters
#### Query Parameters
- **query** (string) - Required - The search query.
- **search_language_filter** (array of strings) - Optional - Filters search results to only include content in the specified languages. Maximum 10 language codes per request. Example: `["en", "fr", "de"]`.
- **max_results** (integer) - Optional - The maximum number of results to return.
- **search_recency_filter** (string) - Optional - Filters results by recency (e.g., "day", "week", "month").
- **search_domain_filter** (array of strings) - Optional - Filters results to specific domains.

### Request Example
```json
{
  "query": "technology news",
  "search_language_filter": ["en", "fr", "de"],
  "max_results": 10
}
```

### Response
#### Success Response (200)
- **results** (array) - A list of search result objects.
  - **title** (string) - The title of the search result.
  - **url** (string) - The URL of the search result.
  - **snippet** (string) - A brief snippet of the search result content.

#### Response Example
```json
{
  "results": [
    {
      "title": "New Advancements in AI Technology",
      "url": "https://example.com/ai-advancements",
      "snippet": "Exploring the latest breakthroughs in artificial intelligence..."
    }
  ]
}
```
```

--------------------------------

### Parse Perplexity API Response Content and Sources (TypeScript)

Source: https://docs.perplexity.ai/guides/chat-completions-guide

Shows how to access the main AI-generated content and iterate over search results (title, URL, date) from a Perplexity API response in TypeScript. Token usage is also logged to the console.

```typescript
// Access the main response
const content = response.choices[0].message.content;
console.log(content);

// Access search sources
response.search_results.forEach(result => {
    console.log(`Source: ${result.title}`);
    console.log(`URL: ${result.url}`);
    console.log(`Date: ${result.date}`);
    console.log("---");
});

// Check token usage
console.log(`Tokens used: ${response.usage.total_tokens}`);
```

--------------------------------

### Enable Streaming Completion (cURL)

Source: https://docs.perplexity.ai/guides/streaming-responses

This cURL command demonstrates how to make a streaming chat completion request to the Perplexity API. It sends a POST request with JSON payload including the model, messages, and a 'stream': true parameter. Replace YOUR_API_KEY with your actual API key.

```bash
curl -X POST "https://api.perplexity.ai/chat/completions" \
-H "Authorization: Bearer YOUR_API_KEY" \
-H "Content-Type: application/json" \
-d '{
  "model": "sonar",
  "messages": [{"role": "user", "content": "What is the latest in AI research?"}],
  "stream": true
}'
```

--------------------------------

### Concise Streaming Handler Implementation (TypeScript)

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

A TypeScript class for handling concise streaming responses from the Perplexity API. It utilizes async iteration to process chunks related to reasoning, content, and completion, aggregating the results.

```typescript
import Perplexity from '@perplexity-ai/perplexity_ai';

interface StreamResult {
    content: string;
    reasoning_steps: any[];
    search_results: any[];
    images: any[];
    usage: any;
}

class ConciseStreamHandler {
    private content: string = "";
    private reasoning_steps: any[] = [];
    private search_results: any[] = [];
    private images: any[] = [];
    private usage: any = null;

    async streamQuery(query: string, model: string = "sonar-pro"): Promise<StreamResult> {
        const client = new Perplexity();
        const stream = await client.chat.completions.create({
            model,
            messages: [{ role: "user", content: query }],
            stream: true,
            stream_mode: "concise"
        });

        for await (const chunk of stream) {
            this.processChunk(chunk);
        }

        return this.getResult();
    }

    private processChunk(chunk: any) {
        const chunkType = chunk.object;
        switch (chunkType) {
            case "chat.reasoning":
                this.handleReasoning(chunk);
                break;
            case "chat.reasoning.done":
                this.handleReasoningDone(chunk);
                break;
            case "chat.completion.chunk":
                this.handleContent(chunk);
                break;
            case "chat.completion.done":
                this.handleDone(chunk);
                break;
        }
    }

    private handleReasoning(chunk: any) {
        const delta = chunk.choices[0].delta;
        if (delta.reasoning_steps) {
            for (const step of delta.reasoning_steps) {
                this.reasoning_steps.push(step);
                console.log(`💭 ${step.thought}`);
            }
        }
    }

    private handleReasoningDone(chunk: any) {
        if (chunk.search_results) {
            this.search_results = chunk.search_results;
            console.log(`\n🔍 Found ${this.search_results.length} sources`);
        }
        if (chunk.images) {
            this.images = chunk.images;
            console.log(`🖼️ Found ${this.images.length} images`);
        }
        console.log("\n📝 Generating response...\n");
    }

    private handleContent(chunk: any) {
        const delta = chunk.choices[0].delta;
        if (delta.content && delta.content) {
            this.content += delta.content;
            process.stdout.write(delta.content); // Use process.stdout.write for non-newline output
        }
    }

    private handleDone(chunk: any) {
        if (chunk.usage) {
            this.usage = chunk.usage;
            console.log(`\n\n✅ Complete | Tokens: ${this.usage.total_tokens}`);
            if (this.usage.cost) {
                console.log(`💰 Cost: $${this.usage.cost.total_cost.toFixed(4)}`);
            }
        }
    }

    private getResult(): StreamResult {
        return {
            content: this.content,
            reasoning_steps: this.reasoning_steps,
            search_results: this.search_results,
            images: this.images,
            usage: this.usage
        };
    }
}

// Usage example:
// async function main() {
//     const handler = new ConciseStreamHandler();
//     const result = await handler.streamQuery("What is the capital of France?");
//     console.log(`\n\nFinal content length: ${result.content.length} characters`);
//     console.log(`Sources used: ${result.search_results.length}`);
// }
// main();
```

--------------------------------

### Detailed Cost Information in API Responses

Source: https://docs.perplexity.ai/changelog

API responses now include detailed cost information for each request, providing transparency into usage and associated costs.

```APIDOC
## New: Detailed Cost Information in API Responses

### Description
API response JSON now includes detailed cost information for each request, offering greater transparency into usage and expenditure. This feature helps users track and manage their API consumption effectively.

### Method
GET / POST / etc. (Applicable to all methods returning cost info)

### Endpoint
(Applies to all Perplexity API endpoints)

### Parameters
N/A (Cost info is part of the response)

### Request Example
(Standard request examples for respective endpoints)

### Response
#### Success Response (200)
- **cost_details** (object) - An object containing cost information.
  - **model_used** (string) - The model that processed the request.
  - **tokens_input** (integer) - The number of input tokens.
  - **tokens_output** (integer) - The number of output tokens.
  - **cost_usd** (float) - The estimated cost in USD for the request.

#### Response Example
```json
{
  "response_data": { ... },
  "cost_details": {
    "model_used": "sonar-pro",
    "tokens_input": 500,
    "tokens_output": 150,
    "cost_usd": 0.0015
  }
}
```
```

--------------------------------

### Perplexity AI Search API - Basic Usage

Source: https://docs.perplexity.ai/guides/search-quickstart

This section details the basic usage of the Perplexity AI search API, including how to set the maximum number of results.

```APIDOC
## POST /search

### Description
Performs a web search and returns relevant results. The `max_results` parameter controls the number of results returned per query.

### Method
POST

### Endpoint
/search

### Parameters
#### Query Parameters
- **query** (string) - Required - The search query string.
- **max_results** (integer) - Optional - The maximum number of results to return. Accepts values from 1 to 20, with a default of 10.

### Request Example
```json
{
  "query": "example search query",
  "max_results": 5
}
```

### Response
#### Success Response (200)
- **results** (array) - A list of search result objects, each containing title, url, etc.

#### Response Example
```json
{
  "results": [
    {
      "title": "Example Result Title",
      "url": "http://example.com",
      "snippet": "This is a summary of the search result."
    }
  ]
}
```
```

--------------------------------

### Handle Chat Completion Done Chunk (Python)

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

Processes the final chunk of a chat completion in Python, extracting aggregated content, search results, images, and usage information. It prints token count and total cost if available.

```python
def handleCompletionDone(chunk):
    if chunk.object == "chat.completion.done":
        full_message = chunk.choices[0].message.content
        if chunk.search_results:
            print(f"\nFinal sources: {len(chunk.search_results)}")
        if chunk.usage:
            print(f"\nTokens: {chunk.usage.total_tokens}")
            if hasattr(chunk.usage, 'cost'):
                print(f"Cost: ${chunk.usage.cost.total_cost:.4f}")
        return { 'content': full_message, 'search_results': getattr(chunk, 'search_results', []), 'images': getattr(chunk, 'images', []), 'usage': getattr(chunk, 'usage', None) }
```

--------------------------------

### Chat Completions API with SEC Filings Filter

Source: https://docs.perplexity.ai/changelog/changelog

This endpoint allows you to search specifically within SEC regulatory documents and filings by setting the `search_domain` parameter to 'sec'. It is useful for financial analysts, investment professionals, and compliance officers.

```APIDOC
## POST /api/chat/completions

### Description
Sends a request to the chat completions endpoint, with the option to filter search results to SEC filings.

### Method
POST

### Endpoint
/api/chat/completions

### Parameters
#### Query Parameters
- **search_domain** (string) - Optional - Set to "sec" to search exclusively within SEC regulatory documents.
- **web_search_options.search_context_size** (string) - Optional - Defines the size of the search context (e.g., "low", "medium").

#### Request Body
- **model** (string) - Required - The model to use for the completion (e.g., "sonar-pro").
- **messages** (array of objects) - Required - An array of message objects, each with a `role` and `content`.
- **stream** (boolean) - Required - Whether to stream the response.
- **search_domain** (string) - Optional - Set to "sec" to search exclusively within SEC regulatory documents.
- **web_search_options** (object) - Optional - Object containing web search configurations.
  - **search_context_size** (string) - Optional - Defines the size of the search context (e.g., "low", "medium").

### Request Example
```json
{
  "model": "sonar-pro",
  "messages": [
    {"role": "user", "content": "What was Apple's revenue growth in their latest quarterly report?"}
  ],
  "stream": false,
  "search_domain": "sec",
  "web_search_options": {
    "search_context_size": "medium"
  }
}
```

### Response
#### Success Response (200)
- **id** (string) - Unique identifier for the response.
- **object** (string) - Type of the object.
- **created** (integer) - Timestamp of creation.
- **model** (string) - The model used for the response.
- **choices** (array) - Array of completion choices.
- **usage** (object) - Usage statistics for the request.
  - **prompt_tokens** (integer) - Number of tokens in the prompt.
  - **completion_tokens** (integer) - Number of tokens in the completion.
  - **total_tokens** (integer) - Total tokens used.
  - **cost** (object) - Cost details.
    - **input_tokens_cost** (number) - Cost of input tokens.
    - **output_tokens_cost** (number) - Cost of output tokens.
    - **request_cost** (number) - Fixed cost per request.
    - **total_cost** (number) - Total cost for the API call.

#### Response Example
```json
{
  "id": "chatcmpl-xxxxxxxxxxxxxxxxxxxx",
  "object": "chat.completion",
  "created": 1721409100,
  "model": "sonar-pro",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "According to Apple's latest quarterly report (Q3 2024), revenue was $83.0 billion, a decrease of 5% year-over-year..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 75,
    "total_tokens": 100,
    "search_context_size": "medium",
    "cost": {
      "input_tokens_cost": 0.000375,
      "output_tokens_cost": 0.001125,
      "request_cost": 0.005,
      "total_cost": 0.0065
    }
  }
}
```
```

--------------------------------

### Message Formatting for AI Conversations

Source: https://docs.perplexity.ai/api-reference/chat-completions-post

Defines the structure for providing conversation history to AI models. It requires a list of message objects, each with a 'role' (e.g., 'system', 'user') and 'content'. This format is crucial for maintaining context in multi-turn interactions.

```json
[
  { "role": "system", "content": "Be precise and concise." },
  { "role": "user", "content": "How many stars are there in our galaxy?" }
]
```

--------------------------------

### Search API

Source: https://docs.perplexity.ai/chat-with-persistence

Retrieve ranked web search results with advanced filtering and real-time data.

```APIDOC
## GET /search

### Description
Get ranked web search results with advanced filtering and real-time data.

### Method
GET

### Endpoint
/search

### Parameters
#### Query Parameters
- **query** (string) - Required - The search query.
- **filter** (string) - Optional - Filter for search results (e.g., 'images', 'videos').
- **limit** (integer) - Optional - The number of results to return.

### Request Example
```
GET /search?query=What+is+Comet+Browser?&filter=images&limit=10
```

### Response
#### Success Response (200)
- **results** (array) - An array of search result objects, each containing 'title', 'url', and 'snippet'.

#### Response Example
```json
{
  "results": [
    {
      "title": "Comet Browser - Wikipedia",
      "url": "https://en.wikipedia.org/wiki/Comet_Browser",
      "snippet": "Comet is a web browser developed by Google."
    }
  ]
}
```
```

--------------------------------

### Control Reasoning Effort with Sonar Deep Research API (curl)

Source: https://docs.perplexity.ai/changelog/changelog

This snippet demonstrates how to use the 'reasoning_effort' parameter with the sonar-deep-research model via a curl request. It allows users to control the computational effort, balancing speed and thoroughness of responses. The available options are 'low', 'medium', and 'high'.

```curl
curl --request POST \
 --url https://api.perplexity.ai/chat/completions \
 --header 'accept: application/json' \
 --header 'authorization: Bearer ${PPLX_KEY}' \
 --header 'content-type: application/json' \
 --data '{ "model": "sonar-deep-research", "messages": [{"role": "user", "content": "What should I know before markets open today?"}], "stream": true, "reasoning_effort": "low" }'
```

--------------------------------

### Asynchronous API for Sonar Deep Research

Source: https://docs.perplexity.ai/changelog/changelog

This section outlines the asynchronous API endpoints for Sonar Deep Research, designed for long-running, research-intensive tasks. It includes endpoints for listing, creating, and retrieving asynchronous job statuses and results.

```APIDOC
## Asynchronous Chat Completions API

### Description
Provides asynchronous endpoints for handling long-running research queries with the Sonar Deep Research model. Jobs have a 7-day TTL.

### Endpoints

1.  **List Asynchronous Requests**
    *   **Method**: GET
    *   **Endpoint**: `/async/chat/completions`
    *   **Description**: Lists all asynchronous chat completion requests for the authenticated user.

2.  **Create Asynchronous Chat Completion Job**
    *   **Method**: POST
    *   **Endpoint**: `/async/chat/completions`
    *   **Description**: Creates a new asynchronous chat completion job. The request body is similar to the synchronous API but initiates a background process.
    *   **Request Body Example**:
        ```json
        {
          "model": "sonar-deep-research",
          "messages": [
            {"role": "user", "content": "Perform a deep analysis of the economic impact of renewable energy policies."}
          ],
          "reasoning_effort": "high"
        }
        ```
    *   **Response Example (Job Creation)**:
        ```json
        {
          "id": "async-job-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
          "status": "pending",
          "created_at": "2024-07-01T10:00:00Z"
        }
        ```

3.  **Retrieve Asynchronous Job Status and Result**
    *   **Method**: GET
    *   **Endpoint**: `/async/chat/completions/{request_id}`
    *   **Description**: Retrieves the status and, if completed, the result of a specific asynchronous chat completion job.
    *   **Path Parameters**:
        *   **request_id** (string) - Required - The unique identifier of the asynchronous job.
    *   **Response Example (Job Status)**:
        ```json
        {
          "id": "async-job-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
          "status": "processing",
          "created_at": "2024-07-01T10:00:00Z",
          "updated_at": "2024-07-01T10:05:00Z"
        }
        ```
    *   **Response Example (Job Result)**:
        ```json
        {
          "id": "async-job-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
          "status": "completed",
          "created_at": "2024-07-01T10:00:00Z",
          "updated_at": "2024-07-01T10:30:00Z",
          "result": {
            "choices": [
              {
                "message": {
                  "role": "assistant",
                  "content": "The economic impact of renewable energy policies is multifaceted..."
                }
              }
            ],
            "search_results": [
              {
                "title": "Economic Effects of Renewables",
                "url": "https://example.com/econ-renewables",
                "date": "2024-01-15"
              }
            ]
          }
        }
        ```
```

--------------------------------

### Historical Research with Specific Date Ranges

Source: https://docs.perplexity.ai/guides/search-date-time-filters

Illustrates how to perform historical research by specifying a date range using `search_after_date` and `search_before_date`. This allows for focused analysis of events or trends within a particular period.

```python
response = client.search(
    query="AI developments",
    max_results=20,
    search_after_date="1/1/2023",
    search_before_date="12/31/2023"
)
```

--------------------------------

### Handle Concise Streaming Response in Python

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

Processes concise streaming responses from the Perplexity API, extracting and printing reasoning steps, search results, content, and usage information. It aggregates content and handles potential JSON decoding errors.

```python
import requests
import json

def stream_concise_mode(query: str):
    """Handle concise streaming with raw HTTP"""
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "sonar-pro",
        "messages": [{"role": "user", "content": query}],
        "stream": True,
        "stream_mode": "concise"
    }
    response = requests.post(url, headers=headers, json=payload, stream=True)
    content = ""
    search_results = []
    usage = None
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith('data: '):
                data_str = line[6:]
                if data_str == '[DONE]':
                    break
                try:
                    chunk = json.loads(data_str)
                    chunk_type = chunk.get('object')
                    if chunk_type == 'chat.reasoning':
                        # Handle reasoning delta = chunk['choices'][0]['delta']
                        if 'reasoning_steps' in delta:
                            for step in delta['reasoning_steps']:
                                print(f"💭 {step['thought']}")
                    elif chunk_type == 'chat.reasoning.done':
                        # Handle reasoning completion
                        if 'search_results' in chunk:
                            search_results = chunk['search_results']
                            print(f"\n🔍 Found {len(search_results)} sources\n")
                    elif chunk_type == 'chat.completion.chunk':
                        # Handle content
                        delta = chunk['choices'][0]['delta']
                        if 'content' in delta and delta['content']:
                            content += delta['content']
                            print(delta['content'], end='', flush=True)
                    elif chunk_type == 'chat.completion.done':
                        # Handle completion
                        if 'usage' in chunk:
                            usage = chunk['usage']
                            print(f"\n\n✅ Tokens: {usage['total_tokens']}")
                except json.JSONDecodeError:
                    continue
    return {
        'content': content,
        'search_results': search_results,
        'usage': usage
    }

# Usage
# result = stream_concise_mode("What's the latest news in AI?")

```

--------------------------------

### Stream Chat Completion with Error Handling (Python)

Source: https://docs.perplexity.ai/guides/streaming-responses

This Python code demonstrates how to stream chat completions using the Perplexity SDK and implement comprehensive error handling. It catches specific Perplexity API errors such as `APIConnectionError`, `RateLimitError`, and `APIStatusError`, as well as general exceptions, providing informative messages for each case.

```python
import perplexity

client = perplexity.Perplexity()
try:
    stream = client.chat.completions.create(
        model="sonar-pro",
        messages=[
            {"role": "user", "content": "Explain machine learning concepts"}
        ],
        stream=True
    )
    content = ""
    for chunk in stream:
        if chunk.choices[0].delta.content:
            content_chunk = chunk.choices[0].delta.content
            content += content_chunk
            print(content_chunk, end="")
except perplexity.APIConnectionError as e:
    print(f"Network connection failed: {e}")
except perplexity.RateLimitError as e:
    print(f"Rate limit exceeded, please retry later: {e}")
except perplexity.APIStatusError as e:
    print(f"API error {e.status_code}: {e.response}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

--------------------------------

### Image Token Calculation (Shell)

Source: https://docs.perplexity.ai/guides/image-attachments

This snippet shows the formula used to calculate the number of tokens an image consumes based on its width and height in pixels. This calculation is crucial for understanding API costs.

```shell
tokens = (width px × height px) / 750
```

--------------------------------

### Buffered Streaming with TypeScript SDK

Source: https://docs.perplexity.ai/guides/streaming-responses

This TypeScript asynchronous function implements buffered streaming for processing chunks in batches, suitable for Node.js environments. It accumulates content in a buffer and flushes it based on buffer size or time intervals. It utilizes the Perplexity SDK for streaming. Dependencies: `@perplexity/client`.

```typescript
async function bufferedStreaming(bufferSize: number = 50, flushInterval: number = 1000) {
    const client = new Perplexity();
    const stream = await client.chat.completions.create({
        model: "sonar",
        messages: [{"role": "user", "content": "Write a detailed explanation of machine learning"}],
        stream: true
    });
    let buffer = "";
    let lastFlush = Date.now();
    for await (const chunk of stream) {
        if (chunk.choices[0]?.delta?.content) {
            buffer += chunk.choices[0].delta.content;
            // Flush buffer if it's full or enough time has passed
            if (buffer.length >= bufferSize || (Date.now() - lastFlush) >= flushInterval) {
                process.stdout.write(buffer);
                buffer = "";
                lastFlush = Date.now();
            }
        }
    }
    // Flush remaining buffer
    if (buffer) {
        process.stdout.write(buffer);
    }
}

bufferedStreaming();
```

--------------------------------

### Search Results API

Source: https://docs.perplexity.ai/api-reference/search-post

This endpoint allows you to search for content and retrieve relevant results based on specified filters and language preferences.

```APIDOC
## GET /search

### Description
Retrieves search results based on a query and optional filters.

### Method
GET

### Endpoint
/search

### Parameters
#### Query Parameters
- **query** (string) - Required - The search query string.
- **limit** (integer) - Optional - Maximum number of search results to return. Default is 10.
- **start** (integer) - Optional - Offset for pagination. Default is 0.
- **filter** (string) - Optional - Filters search results. Accepts values like 'videos', 'images', 'news', 'academic'.
- **safesearch** (string) - Optional - Controls the level of safe search. Accepts 'on' or 'off'.
- **time_range** (string) - Optional - Filters results by time. Accepts '24h', '7d', '30d', 'month', 'year'.
- **search_past** (string) - Optional - Filters results by date range. Accepts values in MM/DD/YYYY format (e.g., '12/30/2025').
- **search_language_filter** (string[]) - Optional - Filters search results to specific languages. Accepts an array of ISO 639-1 language codes (e.g., `["en", "fr", "de"]`). Maximum 10 language codes.

### Response
#### Success Response (200)
- **results** (SearchResult[]) - Required - An array of search results.

#### Response Example
```json
{
  "results": [
    {
      "title": "Example Title",
      "url": "https://example.com",
      "snippet": "This is an example snippet from the search result.",
      "is_indexable": true,
      "language": "en"
    }
  ]
}
```
```

--------------------------------

### Search API

Source: https://docs.perplexity.ai/disease-qa

Retrieve ranked web search results with advanced filtering and real-time data using the Search API.

```APIDOC
## GET /search

### Description
Get ranked web search results with advanced filtering and real-time data.

### Method
GET

### Endpoint
/search

### Parameters
#### Query Parameters
- **query** (string) - Required - The search query string. Can be a single query or an array of queries.

### Request Example
```json
{
  "query": [
    "What is Comet Browser?",
    "Perplexity AI",
    "Perplexity Changelog"
  ]
}
```

### Response
#### Success Response (200)
- **results** (array) - An array of search result objects, each containing:
    - **title** (string) - The title of the search result.
    - **url** (string) - The URL of the search result.

#### Response Example
```json
{
  "results": [
    {
      "title": "Comet Browser - Faster, Smarter, More Private",
      "url": "https://www.cometbrowser.com/"
    },
    {
      "title": "Perplexity AI - Search Engine",
      "url": "https://www.perplexity.ai/"
    },
    {
      "title": "Perplexity AI Changelog",
      "url": "https://www.perplexity.ai/changelog"
    }
  ]
}
```
```

--------------------------------

### Search API

Source: https://docs.perplexity.ai/daily-knowledge-bot

Retrieve ranked web search results with advanced filtering and real-time data using the Search API.

```APIDOC
## GET /search

### Description
Get ranked web search results with advanced filtering and real-time data.

### Method
GET

### Endpoint
/search

### Parameters
#### Query Parameters
- **query** (string) - Required - The search query.
- **limit** (integer) - Optional - The maximum number of results to return.
- **filter** (string) - Optional - Specifies filters for the search results.

### Request Example
```
curl -X GET "https://api.perplexity.ai/search?query=What is Comet Browser?&limit=5"
```

### Response
#### Success Response (200)
- **results** (array) - A list of search results, each containing title, url, snippet, etc.

#### Response Example
```json
{
  "results": [
    {
      "title": "Comet Browser - Wikipedia",
      "url": "https://en.wikipedia.org/wiki/Comet_Browser",
      "snippet": "Comet is a web browser developed by Google."
    }
  ]
}
```
```

--------------------------------

### Search API Capabilities

Source: https://docs.perplexity.ai/changelog

Utilize the Search API with new capabilities like language preference, domain filtering, and enhanced date/time filters for more targeted and refined search results.

```APIDOC
## New Search API Capabilities

### Description
Enhance your search queries with new parameters for specifying language preference, filtering results to specific domains, and controlling result freshness with publication and update date/time filters.

### Method
GET

### Endpoint
`/search`

### Parameters
#### Query Parameters
- **language_preference** (string) - Optional - Specify preferred languages for search results (available for `sonar` and `sonar-pro`).
- **search_domain_filter** (string) - Optional - Filter results to specific domains for more targeted searches.
- **startDate** (string) - Optional - Filter results by publication date (e.g., `YYYY-MM-DD`).
- **endDate** (string) - Optional - Filter results by publication date (e.g., `YYYY-MM-DD`).
- **updateStartDate** (string) - Optional - Filter results by update date (e.g., `YYYY-MM-DD`).
- **updateEndDate** (string) - Optional - Filter results by update date (e.g., `YYYY-MM-DD`).

### Request Example
```json
{
  "query": "AI trends",
  "language_preference": "en",
  "search_domain_filter": "news",
  "startDate": "2023-01-01"
}
```

### Response
#### Success Response (200)
- **results** (array) - List of search results.
  - **title** (string) - The title of the search result.
  - **url** (string) - The URL of the search result.
  - **snippet** (string) - A brief snippet of the search result content.
  - **publication_date** (string) - The publication date of the result.

#### Response Example
```json
{
  "query": "AI trends",
  "results": [
    {
      "title": "The Latest AI Trends in 2023",
      "url": "https://example.com/ai-trends-2023",
      "snippet": "An overview of the most significant artificial intelligence trends shaping the industry this year...",
      "publication_date": "2023-10-26"
    }
  ]
}
```
```

--------------------------------

### Top-K Filtering for Response Focus

Source: https://docs.perplexity.ai/api-reference/chat-completions-post

Limits the model to consider only the 'k' most likely next tokens at each step. Lower values increase focus, higher values allow more diversity. A value of 0 disables the filter. OpenAI Compatible.

```text
top_k: number (integer)
```

--------------------------------

### Concise Streaming Handler Implementation (Python)

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

A Python class that handles concise streaming responses from the Perplexity API. It processes different chunk types for reasoning, content, and completion, managing state and returning a consolidated result.

```python
from perplexity import Perplexity

class ConciseStreamHandler:
    def __init__(self):
        self.content = ""
        self.reasoning_steps = []
        self.search_results = []
        self.images = []
        self.usage = None

    def stream_query(self, query: str, model: str = "sonar-pro"):
        """Handle a complete concise streaming request"""
        client = Perplexity()
        stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": query}],
            stream=True,
            stream_mode="concise"
        )
        for chunk in stream:
            self.process_chunk(chunk)
        return self.get_result()

    def process_chunk(self, chunk):
        """Route chunk to appropriate handler"""
        chunk_type = chunk.object
        if chunk_type == "chat.reasoning":
            self.handle_reasoning(chunk)
        elif chunk_type == "chat.reasoning.done":
            self.handle_reasoning_done(chunk)
        elif chunk_type == "chat.completion.chunk":
            self.handle_content(chunk)
        elif chunk_type == "chat.completion.done":
            self.handle_done(chunk)

    def handle_reasoning(self, chunk):
        """Process reasoning updates"""
        delta = chunk.choices[0].delta
        if hasattr(delta, 'reasoning_steps'):
            for step in delta.reasoning_steps:
                self.reasoning_steps.append(step)
                print(f"💭 {step.thought}")

    def handle_reasoning_done(self, chunk):
        """Process end of reasoning"""
        if hasattr(chunk, 'search_results'):
            self.search_results = chunk.search_results
            print(f"\n🔍 Found {len(self.search_results)} sources")
        if hasattr(chunk, 'images'):
            self.images = chunk.images
            print(f"🖼️ Found {len(self.images)} images")
        print("\n📝 Generating response...\n")

    def handle_content(self, chunk):
        """Process content chunks"""
        delta = chunk.choices[0].delta
        if hasattr(delta, 'content') and delta.content:
            self.content += delta.content
            print(delta.content, end='', flush=True)

    def handle_done(self, chunk):
        """Process completion"""
        if hasattr(chunk, 'usage'):
            self.usage = chunk.usage
            print(f"\n\n✅ Complete | Tokens: {self.usage.total_tokens}")
            if hasattr(self.usage, 'cost'):
                print(f"💰 Cost: ${self.usage.cost.total_cost:.4f}")

    def get_result(self):
        """Return complete result"""
        return {
            'content': self.content,
            'reasoning_steps': self.reasoning_steps,
            'search_results': self.search_results,
            'images': self.images,
            'usage': self.usage
        }

# Usage
# handler = ConciseStreamHandler()
# result = handler.stream_query("What's the latest news in AI?")
# print(f"\n\nFinal content length: {len(result['content'])} characters")
# print(f"Sources used: {len(result['search_results'])}")
```

--------------------------------

### Finding Recently Maintained Content with Last Updated Filter

Source: https://docs.perplexity.ai/guides/search-date-time-filters

Shows how to find content that has been recently updated or maintained by using `last_updated_after_filter`. This is beneficial for ensuring you are accessing the latest information on a topic.

```python
response = client.search(
    query="React best practices",
    max_results=10,
    last_updated_after_filter="07/01/2025"
)
```

--------------------------------

### Search API Endpoint

Source: https://docs.perplexity.ai/guides/search-quickstart

This section describes the main search functionality of the Perplexity AI API. It covers how to perform searches, handle results for single and multi-query requests, and the parameters available for filtering and controlling content extraction.

```APIDOC
## POST /search

### Description
This endpoint allows you to perform searches using various parameters to refine results. It supports multi-query requests and various filtering options.

### Method
POST

### Endpoint
/search

### Parameters
#### Query Parameters
- **query** (string) - Required - The search query.
- **search_domain_filter** (array of strings) - Optional - Filters search results to specific domains (allowlist) or excludes them (denylist).
  - Allowlist mode: Include only specified domains (e.g., `"science.org"`).
  - Denylist mode: Exclude specified domains (e.g., `"-pinterest.com"`).
  - Cannot use both modes simultaneously.
  - Maximum of 20 domains.
- **search_language_filter** (array of strings) - Optional - Filters search results by language using ISO 639-1 codes (e.g., `"en"`, `"fr"`).
  - Maximum of 10 language codes.
- **max_results** (integer) - Optional - The maximum number of results to return per query.
- **max_tokens_per_page** (integer) - Optional - Controls the amount of content extracted from each webpage. Defaults to 2048 tokens.
- **max_tokens** (integer) - Optional - Sets the maximum total tokens of webpage content returned across all search results. Defaults to 25,000 tokens. Maximum allowed is 1,000,000 tokens.

### Request Example
```json
{
  "query": "climate change research",
  "search_domain_filter": [
    "science.org",
    "pnas.org",
    "cell.com"
  ],
  "max_results": 10
}
```

### Response
#### Success Response (200)
- **results** (array) - A list of search results. For multi-query requests, results are grouped per query.
  - **title** (string) - The title of the search result.
  - **url** (string) - The URL of the search result.
  - **date** (string) - The publication date of the result.
  - **snippet** (string) - A brief snippet of the content from the result page.

#### Response Example
```json
{
  "results": [
    {
      "title": "Example Title",
      "url": "http://example.com",
      "date": "2023-10-27",
      "snippet": "This is a sample snippet of the search result content..."
    }
  ]
}
```

### Error Handling
- **400 Bad Request**: Invalid input parameters.
- **500 Internal Server Error**: Server error during processing.
```

--------------------------------

### Chat Completions API

Source: https://docs.perplexity.ai/api-reference/chat-completions-post

Generates a model's response for a given chat conversation using Perplexity's Sonar models. Supports various parameters for controlling search, reasoning, and response content.

```APIDOC
## POST /chat/completions

### Description
Generates a model's response for the given chat conversation.

### Method
POST

### Endpoint
/chat/completions

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
- **model** (enum) - Required - The name of the model to use. Options: `sonar`, `sonar-pro`, `sonar-deep-research`, `sonar-reasoning-pro`.
- **messages** (array of objects) - Required - The conversation history. Each object should have `role` (`system` or `user`) and `content` (string).
- **search_mode** (string) - Optional - Specifies the search mode. Example: `web`.
- **reasoning_effort** (string) - Optional - Controls the effort for reasoning. Example: `low`.
- **max_tokens** (integer) - Optional - Maximum number of tokens to generate in the response.
- **temperature** (float) - Optional - Controls randomness. Values between 0 and 2.
- **top_p** (float) - Optional - Controls diversity via nucleus sampling. Values between 0 and 1.
- **language_preference** (string) - Optional - Preferred language for the response.
- **search_domain_filter** (string) - Optional - Filter search results by domain.
- **return_images** (boolean) - Optional - Whether to return images in the response.
- **return_related_questions** (boolean) - Optional - Whether to return related questions.
- **search_recency_filter** (string) - Optional - Filter search results by recency.
- **search_after_date_filter** (string) - Optional - Filter search results after a specific date.
- **search_before_date_filter** (string) - Optional - Filter search results before a specific date.
- **last_updated_after_filter** (string) - Optional - Filter results updated after a specific date.
- **last_updated_before_filter** (string) - Optional - Filter results updated before a specific date.
- **top_k** (integer) - Optional - Controls the number of top tokens to consider.
- **stream** (boolean) - Optional - Whether to stream the response.
- **presence_penalty** (float) - Optional - Penalizes new tokens based on their presence in the text.
- **frequency_penalty** (float) - Optional - Penalizes new tokens based on their frequency in the text.
- **response_format** (object) - Optional - Specifies the response format.
- **disable_search** (boolean) - Optional - Disables search functionality.
- **enable_search_classifier** (boolean) - Optional - Enables search classification.
- **web_search_options** (object) - Optional - Options for web search.
  - **search_context_size** (string) - Optional - Size of the search context. Example: `low`.
  - **image_search_relevance_enhanced** (boolean) - Optional - Enhances image search relevance.
- **media_response** (object) - Optional - Options for media responses.
  - **overrides** (object) - Optional - Overrides for media response settings.
    - **return_videos** (boolean) - Optional - Whether to return videos.
    - **return_images** (boolean) - Optional - Whether to return images.

### Request Example
```json
{
  "model": "sonar-deep-research",
  "messages": [
    { "role": "system", "content": "Be precise and concise.", 
    { "role": "user", "content": "How many stars are there in our galaxy?"
  ],
  "search_mode": "web",
  "reasoning_effort": "low",
  "max_tokens": 123,
  "temperature": 0.2,
  "top_p": 0.9,
  "language_preference": "",
  "search_domain_filter": "",
  "return_images": false,
  "return_related_questions": false,
  "search_recency_filter": "",
  "search_after_date_filter": "",
  "search_before_date_filter": "",
  "last_updated_after_filter": "",
  "last_updated_before_filter": "",
  "top_k": 0,
  "stream": false,
  "presence_penalty": 0,
  "frequency_penalty": 0,
  "response_format": {},
  "disable_search": false,
  "enable_search_classifier": false,
  "web_search_options": {
    "search_context_size": "low",
    "image_search_relevance_enhanced": false
  },
  "media_response": {
    "overrides": {
      "return_videos": false,
      "return_images": false
    }
  }
}
```

### Response
#### Success Response (200)
- **id** (string) - Unique identifier for the response.
- **model** (string) - The model used for completion.
- **created** (integer) - Timestamp of creation.
- **usage** (object) - Token usage information.
  - **prompt_tokens** (integer) - Tokens used in the prompt.
  - **completion_tokens** (integer) - Tokens used in the completion.
  - **total_tokens** (integer) - Total tokens used.
  - **search_context_size** (string) - Size of the search context used.
  - **citation_tokens** (integer) - Tokens used for citations.
  - **num_search_queries** (integer) - Number of search queries performed.
  - **reasoning_tokens** (integer) - Tokens used for reasoning.
- **object** (string) - Type of the object, typically "chat.completion".
- **choices** (array of objects) - List of completion choices.
  - **index** (integer) - Index of the choice.
  - **message** (object) - The message content.
    - **content** (string) - The generated text.
    - **role** (string) - Role of the message sender (e.g., `system`).
  - **finish_reason** (string) - The reason the generation finished (e.g., `stop`).
- **search_results** (array of objects) - Search results that influenced the response.
  - **title** (string) - Title of the search result.
  - **url** (string) - URL of the search result.
  - **date** (string) - Publication date of the search result.
- **videos** (array of objects) - Videos returned in the response.
  - **url** (string) - URL of the video.
  - **thumbnail_url** (string) - URL of the video thumbnail.
  - **thumbnail_width** (integer) - Width of the thumbnail.
  - **thumbnail_height** (integer) - Height of the thumbnail.
  - **duration** (integer) - Duration of the video.

#### Response Example
```json
{
  "id": "",
  "model": "",
  "created": 123,
  "usage": {
    "prompt_tokens": 123,
    "completion_tokens": 123,
    "total_tokens": 123,
    "search_context_size": "",
    "citation_tokens": 123,
    "num_search_queries": 123,
    "reasoning_tokens": 123
  },
  "object": "chat.completion",
  "choices": [
    {
      "index": 123,
      "message": {
        "content": "",
        "role": "system"
      },
      "finish_reason": "stop"
    }
  ],
  "search_results": [
    {
      "title": "",
      "url": "",
      "date": "2023-12-25"
    }
  ],
  "videos": [
    {
      "url": "",
      "thumbnail_url": "",
      "thumbnail_width": 123,
      "thumbnail_height": 123,
      "duration": 123
    }
  ]
}
```

#### Authorizations
Bearer authentication header of the form `Bearer <YOUR_AUTH_TOKEN>`.
```

--------------------------------

### New API Portal for Organization Management

Source: https://docs.perplexity.ai/changelog

Manage your organization's API keys, view usage insights, and streamline team collaboration through the new Perplexity AI API portal.

```APIDOC
## Organization Management Portal

### Description
Access the Perplexity AI API portal to manage API keys, monitor usage, and facilitate team collaboration within your organization. 

### Access
[https://www.perplexity.ai/account/api/group](https://www.perplexity.ai/account/api/group)
```

--------------------------------

### Domain Filtering for Perplexity AI Search Results (Allowlist)

Source: https://docs.perplexity.ai/guides/search-quickstart

Filters search results to include only specified domains using an allowlist. This ensures results come from authoritative or relevant sources for focused research. Up to 20 domains can be included.

```python
from perplexity import Perplexity

client = Perplexity()
search = client.search.create(
    query="climate change research",
    search_domain_filter=[
        "science.org",
        "pnas.org",
        "cell.com"
    ],
    max_results=10
)

for result in search.results:
    print(f"{result.title}: {result.url}")
    print(f"Published: {result.date}")
    print("---")
```

--------------------------------

### Checking Async Request Status and Retrieving Results (Python & TypeScript)

Source: https://docs.perplexity.ai/guides/chat-completions-sdk

Details how to check the status of an asynchronous chat completion request using its ID and retrieve the results once completed. This is crucial for managing background tasks and processing their outputs.

```python
# Check the status of an async request
request_id = "req_123abc456def789"
status = client.async_.chat.completions.get(request_id)
print(f"Status: {status.status}")
if status.status == "completed":
  print(f"Response: {status.result.choices[0].message.content}")
```

```typescript
// Check the status of an async request
const requestId = "req_123abc456def789";
const status = await client.async.chat.completions.get(requestId);
console.log(`Status: ${status.status}`);
if (status.status === "completed") {
  console.log(`Response: ${status.result.choices[0].message.content}`);
}
```

--------------------------------

### Chat Completions with SEC Filings Filter

Source: https://docs.perplexity.ai/changelog

This endpoint allows you to perform chat completions while specifically searching within SEC regulatory documents. It's useful for financial analysis and due diligence.

```APIDOC
## POST /chat/completions

### Description
Performs chat completions with the ability to filter search results to SEC regulatory documents.

### Method
POST

### Endpoint
https://api.perplexity.ai/chat/completions

### Parameters
#### Query Parameters
- **search_domain** (string) - Optional - Set to "sec" to filter results to SEC filings.
- **web_search_options.search_context_size** (string) - Optional - Controls the size of the search context (e.g., "low", "medium", "high").

#### Request Body
- **model** (string) - Required - The model to use for completions (e.g., "sonar-pro").
- **messages** (array) - Required - An array of message objects, where each object has a "role" and "content".
- **stream** (boolean) - Required - Whether to stream the response.

### Request Example
```json
{
  "model": "sonar-pro",
  "messages": [
    {"role": "user", "content": "What was Apple's revenue growth in their latest quarterly report?"}
  ],
  "stream": false,
  "search_domain": "sec",
  "web_search_options": {
    "search_context_size": "medium"
  }
}
```

### Response
#### Success Response (200)
- **id** (string) - Unique identifier for the response.
- **object** (string) - Type of the object returned.
- **created** (integer) - Timestamp of creation.
- **model** (string) - The model used for the response.
- **choices** (array) - An array of completion choices.
- **usage** (object) - Object detailing token usage and cost.

#### Response Example
```json
{
  "id": "chatcmpl-xxxxxxxxxxxxxxxxx",
  "object": "chat.completion",
  "created": 1720458000,
  "model": "sonar-pro",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "According to Apple's latest quarterly report (Q3 2024), revenue was $83.0 billion, a decrease of 1% year-over-year. Earnings per share were $1.19."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 45,
    "total_tokens": 70
  }
}
```
```

--------------------------------

### Image Analysis API Endpoint

Source: https://docs.perplexity.ai/guides/image-attachments

This endpoint allows you to send an image, either via URL or base64 encoding, along with a text prompt to the Perplexity AI model for analysis. The model can then describe the image, extract text, or answer questions about its content.

```APIDOC
## POST /chat/completions

### Description
Analyzes an image provided via URL or base64 encoding, in conjunction with a text prompt, to extract information or answer questions about the image content.

### Method
POST

### Endpoint
`/chat/completions`

### Parameters
#### Request Body
- **model** (string) - Required - The model to use for the request (e.g., `sonar-pro`).
- **stream** (boolean) - Optional - Whether to stream the response.
- **messages** (array) - Required - An array of message objects.
  - **role** (string) - Required - The role of the message sender (`user`).
  - **content** (array) - Required - An array of content blocks.
    - **type** (string) - Required - The type of content (`text` or `image_url`).
    - **text** (string) - Required if type is `text` - The user's textual prompt.
    - **image_url** (object) - Required if type is `image_url` - An object containing the image URL.
      - **url** (string) - Required - The publicly accessible URL of the image.

### Request Example
```json
{
  "model": "sonar-pro",
  "stream": false,
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Can you describe the image at this URL?"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
          }
        }
      ]
    }
  ]
}
```

### Response
#### Success Response (200)
- **choices** (array) - An array of response choices.
  - **message** (object) - The message object containing the AI's response.
    - **content** (string) - The AI-generated text content.

#### Response Example
```json
{
  "choices": [
    {
      "message": {
        "content": "This is an image of a nature boardwalk in Madison, Wisconsin."
      }
    }
  ]
}
```

### Limitations
- `sonar-deep-research` does not support image input.
- Ensure provided HTTPS URLs are publicly accessible.
- Base64 images have a 50MB size limit.
- Supported formats: PNG, JPEG, WEBP, and GIF.

```

--------------------------------

### Perplexity API: Perform Multi-Query Web Search (Python)

Source: https://docs.perplexity.ai/guides/search-quickstart

This Python code snippet shows how to execute multiple related search queries simultaneously using the Perplexity API. It allows for comprehensive research by defining a list of queries in a single request and processing the results for each query individually. Requires the `perplexity` library.

```python
from perplexity import Perplexity

client = Perplexity()

search = client.search.create(
    query=[
        "artificial intelligence trends 2024",
        "machine learning breakthroughs recent",
        "AI applications in healthcare"
    ],
    max_results=5
)

# Access results for each query
for i, query_results in enumerate(search.results):
    print(f"Results for query {i+1}:")
    for result in query_results:
        print(f"  {result.title}: {result.url}")
```

--------------------------------

### Handle Chat Completion Done Chunk (TypeScript)

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

Processes the final chunk of a chat completion in TypeScript, extracting aggregated content, search results, images, and usage information. It logs token count and total cost to the console.

```typescript
function handleCompletionDone(chunk: any) {
  if (chunk.object === "chat.completion.done") {
    console.log("\n\n[Stream Complete]");
    const fullMessage = chunk.choices[0].message.content;
    if (chunk.search_results) {
      console.log(`\nFinal sources: ${chunk.search_results.length}`);
    }
    if (chunk.usage) {
      console.log(`\nTokens: ${chunk.usage.total_tokens}`);
      if (chunk.usage.cost) {
        console.log(`Cost: $${chunk.usage.cost.total_cost.toFixed(4)}`);
      }
    }
    return { content: fullMessage, search_results: chunk.search_results || [], images: chunk.images || [], usage: chunk.usage || null };
  }
}
```

--------------------------------

### Search Results and Metadata During Streaming

Source: https://docs.perplexity.ai/guides/streaming-responses

Understand how search results and metadata are delivered during a streaming response from the Perplexity API.

```APIDOC
## Search Results and Metadata During Streaming

Search results and metadata are delivered in the **final chunk(s)** of a streaming response, not progressively during the stream.

### How Metadata Works with Streaming

When streaming, you receive:
1.  **Content chunks** which arrive progressively in real-time
2.  **Search results** (delivered in the final chunk(s))
3.  **Usage stats** and other metadata
```

```APIDOC
## Collecting Metadata During Streaming - Python SDK

### Method
POST

### Endpoint
(Implicitly handled by SDK)

### Description
This example shows how to collect search results and usage information from the final chunks of a streaming response using the Perplexity Python SDK.

### Request Example
```python
from perplexity import Perplexity

def stream_with_metadata():
    client = Perplexity()
    stream = client.chat.completions.create(
        model="sonar",
        messages=[{"role": "user", "content": "Explain quantum computing"}],
        stream=True
    )
    content = ""
    search_results = []
    usage_info = None
    for chunk in stream:
        # Process content
        if chunk.choices[0].delta.content:
            content_piece = chunk.choices[0].delta.content
            content += content_piece
            print(content_piece, end='', flush=True)
        
        # Collect metadata from final chunks
        if hasattr(chunk, 'search_results') and chunk.search_results:
            search_results = chunk.search_results
        if hasattr(chunk, 'usage') and chunk.usage:
            usage_info = chunk.usage

    # Now you can access collected metadata
    # print("\nSearch Results:", search_results)
    # print("Usage Info:", usage_info)
```

### Response Example
(Content streamed to console, with metadata available in variables `search_results` and `usage_info` after the loop completes.)
```

--------------------------------

### Perplexity Python: Language Filter Error Handling

Source: https://docs.perplexity.ai/guides/search-language-filter

Demonstrates how to perform a language-filtered search using the Perplexity Python SDK, including validation of language codes and handling potential API or validation errors. It ensures language codes are provided as a list, within the allowed limit, and are in the correct format (2-letter lowercase strings).

```python
from perplexity import Perplexity, BadRequestError

client = Perplexity()

def safe_language_search(query, languages):
    """ Perform a language-filtered search with error handling. """
    try:
        # Validate language codes
        if not isinstance(languages, list):
            raise ValueError("Languages must be provided as a list")
        if len(languages) > 10:
            raise ValueError("Maximum 10 language codes allowed")

        # Validate each code format
        for lang in languages:
            if not isinstance(lang, str) or len(lang) != 2 or not lang.islower():
                raise ValueError(f"Invalid language code format: {lang}")

        # Perform search
        response = client.search.create(
            query=query,
            search_language_filter=languages,
            max_results=10
        )
        return response
    except ValueError as e:
        print(f"Validation error: {e}")
        return None
    except BadRequestError as e:
        print(f"API error: {e.message}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

# Usage
results = safe_language_search(
    "artificial intelligence",
    ["en", "fr", "de"]
)

if results:
    print(f"Found {len(results.results)} results")

```

--------------------------------

### Reasoning Effort Parameter for Sonar Deep Research

Source: https://docs.perplexity.ai/changelog

Control the computational effort for Sonar Deep Research queries. Choose 'low', 'medium', or 'high' to balance speed, thoroughness, and token consumption.

```APIDOC
## POST /chat/completions

### Description
Sends a chat completion request to the Perplexity API, with an option to control the reasoning effort for 'sonar-deep-research' model.

### Method
POST

### Endpoint
https://api.perplexity.ai/chat/completions

### Parameters
#### Request Body
- **model** (string) - Required - The model to use for the chat completion (e.g., "sonar-deep-research").
- **messages** (array) - Required - An array of message objects representing the conversation history.
  - **role** (string) - Required - The role of the message sender (e.g., "user").
  - **content** (string) - Required - The content of the message.
- **stream** (boolean) - Optional - Whether to stream the response.
- **reasoning_effort** (string) - Optional - Controls the computational effort for 'sonar-deep-research'. Options: "low", "medium" (default), "high".

### Request Example
```json
{
  "model": "sonar-deep-research",
  "messages": [
    {"role": "user", "content": "What should I know before markets open today?"}
  ],
  "stream": true,
  "reasoning_effort": "low"
}
```

### Response
#### Success Response (200)
- **id** (string) - The ID of the chat completion.
- **object** (string) - The type of object returned (e.g., "chat.completion").
- **created** (integer) - The Unix timestamp of when the completion was created.
- **model** (string) - The model used for the completion.
- **choices** (array) - An array of completion choices.
  - **index** (integer) - The index of the choice.
  - **message** (object) - The message object.
    - **role** (string) - The role of the message sender.
    - **content** (string) - The content of the message.
  - **finish_reason** (string) - The reason the generation was finished.
- **usage** (object) - Information about token usage.
  - **prompt_tokens** (integer) - The number of tokens in the prompt.
  - **completion_tokens** (integer) - The number of tokens in the completion.
  - **total_tokens** (integer) - The total number of tokens used.
- **search_results** (array) - An array of search result objects (if available).
  - **title** (string) - The title of the search result page.
  - **url** (string) - The URL of the search result.
  - **date** (string) - The publication date of the content.

#### Response Example
```json
{
  "id": "chatcmpl-70Q5hQ0mH4C164O4qL2oWb78X2345",
  "object": "chat.completion",
  "created": 1677652702,
  "model": "sonar-deep-research",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Here's what you should know before markets open today..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 50,
    "total_tokens": 60
  },
  "search_results": [
    {
      "title": "Market Open Today",
      "url": "https://example.com/market-open",
      "date": "2023-01-01"
    }
  ]
}
```
```

--------------------------------

### Presence Penalty for New Topics

Source: https://docs.perplexity.ai/api-reference/chat-completions-post

Applies a penalty to tokens already present in the text, encouraging the discussion of new topics. Positive values increase the likelihood of new topics. Ranges typically from 0 to 2.0. OpenAI Compatible.

```text
presence_penalty: number (0 <= x <= 2.0)
```

--------------------------------

### Handle Concise Streaming Response in TypeScript

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

Manages the streaming response chunks in concise mode, processing search results, images, content, and usage information. It aggregates content and logs informational messages to the console.

```typescript
class ConciseStreamHandler {
  private content: string = '';
  private reasoning_steps: any[] = [];
  private search_results: any[] = [];
  private images: any[] = [];
  private usage: any = null;

  private handleReasoningDone(chunk: any): void {
    if (chunk.search_results) {
      this.search_results = chunk.search_results;
      console.log(`\n🔍 Found ${this.search_results.length} sources`);
    }
    if (chunk.images) {
      this.images = chunk.images;
      console.log(`🖼️ Found ${this.images.length} images`);
    }
    console.log("\n📝 Generating response...\n");
  }

  private handleContent(chunk: any): void {
    const delta = chunk.choices[0]?.delta;
    if (delta?.content) {
      this.content += delta.content;
      process.stdout.write(delta.content);
    }
  }

  private handleDone(chunk: any): void {
    if (chunk.usage) {
      this.usage = chunk.usage;
      console.log(`\n\n✅ Complete | Tokens: ${this.usage.total_tokens}`);
      if (this.usage.cost) {
        console.log(`💰 Cost: $${this.usage.cost.total_cost.toFixed(4)}`);
      }
    }
  }

  private getResult(): StreamResult {
    return {
      content: this.content,
      reasoning_steps: this.reasoning_steps,
      search_results: this.search_results,
      images: this.images,
      usage: this.usage
    };
  }

  // This method would typically be part of a larger class that handles the streaming.
  // For demonstration, we assume it exists and is called appropriately.
  public async streamQuery(query: string): Promise<StreamResult> {
    // Placeholder for actual streaming logic
    // This would involve calling the Perplexity API and processing chunks
    console.log(`Streaming query: ${query}`);
    // Simulate response processing
    await new Promise(resolve => setTimeout(resolve, 1000));
    this.handleReasoningDone({ search_results: [{ url: 'example.com' }], images: [] });
    this.handleContent({ choices: [{ delta: { content: 'This is the first part of the response.' } }] });
    this.handleContent({ choices: [{ delta: { content: ' This is the second part.' } }] });
    this.handleDone({ usage: { total_tokens: 100, cost: { total_cost: 0.001 } } });
    return this.getResult();
  }
}

// Usage (assuming StreamResult is defined elsewhere)
interface StreamResult {
  content: string;
  reasoning_steps: any[];
  search_results: any[];
  images: any[];
  usage: any;
}

// const handler = new ConciseStreamHandler();
// const result = await handler.streamQuery("What's the latest news in AI?");
// console.log(`\n\nFinal content length: ${result.content.length} characters`);
// console.log(`Sources used: ${result.search_results.length}`);

```

--------------------------------

### Asynchronous API for Sonar Deep Research

Source: https://docs.perplexity.ai/changelog

Submit research-intensive requests and retrieve results later using the asynchronous API for Sonar Deep Research. Ideal for complex queries requiring extended processing.

```APIDOC
## Asynchronous Chat Completion API

### Description
Provides endpoints for managing asynchronous chat completion jobs for Sonar Deep Research. Allows submitting requests and retrieving results at a later time.

### Method
POST

### Endpoint
https://api.perplexity.ai/async/chat/completions

### Parameters
#### Request Body
- **model** (string) - Required - The model to use (e.g., "sonar-deep-research").
- **messages** (array) - Required - An array of message objects.
  - **role** (string) - Required - The role of the message sender (e.g., "user").
  - **content** (string) - Required - The content of the message.
- **stream** (boolean) - Optional - Whether to stream the response (Note: Async requests do not support streaming).

### Request Example
```json
{
  "model": "sonar-deep-research",
  "messages": [
    {"role": "user", "content": "Perform a deep analysis of the impact of quantum computing on cryptography."}
  ]
}
```

### Response
#### Success Response (200)
- **id** (string) - The unique ID for the asynchronous request.
- **status** (string) - The current status of the request (e.g., "processing", "completed", "failed").
- **created_at** (string) - Timestamp when the request was created.

#### Response Example
```json
{
  "id": "async-req-12345abcdef",
  "status": "processing",
  "created_at": "2023-10-27T10:00:00Z"
}
```

## List Asynchronous Chat Completion Requests

### Description
Lists all asynchronous chat completion requests submitted by the authenticated user.

### Method
GET

### Endpoint
https://api.perplexity.ai/async/chat/completions

### Response
#### Success Response (200)
- **requests** (array) - An array of asynchronous request objects.
  - **id** (string) - The unique ID for the asynchronous request.
  - **status** (string) - The current status of the request.
  - **created_at** (string) - Timestamp when the request was created.

#### Response Example
```json
{
  "requests": [
    {
      "id": "async-req-12345abcdef",
      "status": "completed",
      "created_at": "2023-10-27T10:00:00Z"
    },
    {
      "id": "async-req-67890ghijkl",
      "status": "processing",
      "created_at": "2023-10-27T11:00:00Z"
    }
  ]
}
```

## Retrieve Asynchronous Chat Completion Result

### Description
Retrieves the status and result of a specific asynchronous chat completion job.

### Method
GET

### Endpoint
https://api.perplexity.ai/async/chat/completions/{request_id}

### Parameters
#### Path Parameters
- **request_id** (string) - Required - The ID of the asynchronous request.

### Response
#### Success Response (200)
- **id** (string) - The unique ID for the asynchronous request.
- **status** (string) - The final status of the request (e.g., "completed", "failed").
- **created_at** (string) - Timestamp when the request was created.
- **completed_at** (string) - Timestamp when the request was completed.
- **error** (object) - Error details if the request failed.
  - **message** (string) - The error message.
- **result** (object) - The result of the chat completion if successful.
  - **message** (object)
    - **role** (string) - The role of the message sender.
    - **content** (string) - The content of the message.
  - **usage** (object) - Information about token usage.
    - **prompt_tokens** (integer) - The number of tokens in the prompt.
    - **completion_tokens** (integer) - The number of tokens in the completion.
    - **total_tokens** (integer) - The total number of tokens used.
  - **search_results** (array) - An array of search result objects (if available).
    - **title** (string) - The title of the search result page.
    - **url** (string) - The URL of the search result.
    - **date** (string) - The publication date of the content.

#### Response Example
```json
{
  "id": "async-req-12345abcdef",
  "status": "completed",
  "created_at": "2023-10-27T10:00:00Z",
  "completed_at": "2023-10-27T10:15:00Z",
  "result": {
    "message": {
      "role": "assistant",
      "content": "The impact of quantum computing on cryptography is significant..."
    },
    "usage": {
      "prompt_tokens": 10,
      "completion_tokens": 100,
      "total_tokens": 110
    },
    "search_results": [
      {
        "title": "Quantum Computing and Cryptography",
        "url": "https://example.com/quantum-crypto",
        "date": "2023-05-20"
      }
    ]
  }
}
```
```

--------------------------------

### Chat Completions API Request (cURL)

Source: https://docs.perplexity.ai/api-reference/chat-completions-post

This cURL command demonstrates how to send a POST request to the Perplexity AI Chat Completions API. It includes parameters for model selection, conversation messages, search mode, and various response control options. The request body is a JSON object specifying the query and desired output format.

```curl
curl --request POST \
--url https://api.perplexity.ai/chat/completions \
--header 'Authorization: Bearer ' \
--header 'Content-Type: application/json' \
--data ' {
  "model": "sonar-deep-research",
  "messages": [
    { "role": "system", "content": "Be precise and concise."
    },
    { "role": "user", "content": "How many stars are there in our galaxy?"
    }
  ],
  "search_mode": "web",
  "reasoning_effort": "low",
  "max_tokens": 123,
  "temperature": 0.2,
  "top_p": 0.9,
  "language_preference": "",
  "search_domain_filter": "",
  "return_images": false,
  "return_related_questions": false,
  "search_recency_filter": "",
  "search_after_date_filter": "",
  "search_before_date_filter": "",
  "last_updated_after_filter": "",
  "last_updated_before_filter": "",
  "top_k": 0,
  "stream": false,
  "presence_penalty": 0,
  "frequency_penalty": 0,
  "response_format": {},
  "disable_search": false,
  "enable_search_classifier": false,
  "web_search_options": {
    "search_context_size": "low",
    "image_search_relevance_enhanced": false
  },
  "media_response": {
    "overrides": {
      "return_videos": false,
      "return_images": false
    }
  }
} '
```

--------------------------------

### Domain Filtering for Perplexity AI Search Results (Denylist)

Source: https://docs.perplexity.ai/guides/search-quickstart

Filters search results to exclude specific domains using a denylist. This helps to remove irrelevant or unwanted sources, such as social media, from the search results. Use a '-' prefix for domains to exclude.

```python
from perplexity import Perplexity

client = Perplexity()
# Exclude social media sites from search results
search = client.search.create(
    query="renewable energy innovations",
    search_domain_filter=[
        "-pinterest.com",
        "-reddit.com",
        "-quora.com"
    ],
    max_results=10
)

for result in search.results:
    print(f"{result.title}: {result.url}")
```

--------------------------------

### Search Filtering Capabilities

Source: https://docs.perplexity.ai/changelog/changelog

Details the new search filtering options, including filtering by user location and specific date ranges, to refine search results.

```APIDOC
## New Search Filtering Capabilities

### Description
New functionalities have been added to filter search results based on user location and specific date ranges.

### Location Filtering
- **Description**: Allows retrieval of search results relevant to a particular user location.
- **Usage**: Refer to the guide for implementation details.

### Date Range Filtering
- **Description**: Enables narrowing down search results to a specific period.
- **Usage**: Check the documentation for instructions on setting date ranges.
```

--------------------------------

### Analyze Image from URL (cURL)

Source: https://docs.perplexity.ai/guides/image-attachments

This cURL command shows how to analyze an image hosted online by providing its public HTTPS URL to the Perplexity API. The image URL is embedded within the 'messages' array. Replace '$SONAR_API_KEY' with your actual API key. The API will fetch and process the image from the given URL.

```cURL
curl --location 'https://api.perplexity.ai/chat/completions' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--header "Authorization: Bearer $SONAR_API_KEY" \
--data '{ "model": "sonar-pro", "stream": false, "messages": [ { "role": "user", "content": [ { "type": "text", "text": "Describe this image from the URL." }, { "type": "image_url", "image_url": { "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg" } } ] } ] }' | jq
```

--------------------------------

### Process Stream Completion (Python & TypeScript)

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

Handles the final 'chat.completion.done' chunk, indicating the end of the response stream. It logs completion, provides final message content, and displays aggregated usage and cost information.

```python
def handle_completion_done(chunk):
    """Process stream completion"""
    if chunk.object == "chat.completion.done":
        print("\n\n[Stream Complete]")
        # Final aggregated message
        full_message = chunk.choices[0].message.content
        # Final search results
        if hasattr(chunk, 'search_results'):
            print(f"\nFinal sources: {len(chunk.search_results)}")
        # Complete usage and cost
```

```typescript
function handleCompletionDone(chunk: any) {
    if (chunk.object === "chat.completion.done") {
        console.log("\n\n[Stream Complete]");
        // Final aggregated message
        const fullMessage = chunk.choices[0].message.content;
        // Final search results
        if (chunk.search_results) {
            console.log(`\nFinal sources: ${chunk.search_results.length}`);
        }
        // Complete usage and cost
```

--------------------------------

### Chat Reasoning Chunk Structure

Source: https://docs.perplexity.ai/guides/pro-search-stream-mode-guide

Illustrates the JSON structure of a 'chat.reasoning' chunk received in 'concise' stream mode. This chunk type provides details about the model's reasoning steps, including web search operations.

```json
{
  "id": "cfa38f9d-fdbc-4ac6-a5d2-a3010b6a33a6",
  "model": "sonar-pro",
  "created": 1759441590,
  "object": "chat.reasoning",
  "choices": [
    {
      "index": 0,
      "finish_reason": null,
      "message": {
        "role": "assistant",
        "content": ""
      },
      "delta": {
        "role": "assistant",
        "content": "",
        "reasoning_steps": [
          {
            "thought": "Searching the web for Seattle's current weather...",
            "type": "web_search",
            "web_search": {
              "search_results": [...],
              "search_keywords": ["Seattle current weather"]
            }
          }
        ]
      }
    }
  ],
  "type": "message"
}
```

--------------------------------

### Enhanced API Responses with Search Results

Source: https://docs.perplexity.ai/changelog

Understand the search data used by models with the new `search_results` field in API responses. This provides transparency and allows for better source verification.

```APIDOC
## Search Results Field

### Description
Models now include a `search_results` field in their JSON responses, providing direct access to the search data used to generate the response. The deprecated `citations` field has been removed.

### Response
#### Success Response (200)
- **search_results** (array) - An array containing details of the search results used.
  - **title** (string) - The title of the search result page.
  - **url** (string) - The URL of the search result.
  - **date** (string) - The publication date of the content.

### Response Example
```json
{
  "search_results": [
    {
      "title": "Understanding Large Language Models",
      "url": "https://example.com/llm-article",
      "date": "2023-12-25"
    },
    {
      "title": "Advances in AI Research",
      "url": "https://example.com/ai-research",
      "date": "2024-03-15"
    }
  ]
}
```
```

--------------------------------

### Chat Completion API

Source: https://docs.perplexity.ai/api-reference/chat-completions-post

This endpoint allows for chat-based interactions with Perplexity AI models. You can provide a list of messages to simulate a conversation and control various aspects of the AI's response generation.

```APIDOC
## POST /chat/completions

### Description
Generates a model response based on the provided conversation history and parameters.

### Method
POST

### Endpoint
/chat/completions

### Parameters
#### Request Body
- **model** (string) - Required - The ID of the model to use for generation. Example: `sonar-reasoning-pro`, `sonar-deep-research`
- **messages** (object[]) - Required - A list of message objects representing the conversation.
  - **role** (string) - Required - The role of the message sender (e.g., `system`, `user`, `assistant`).
  - **content** (string) - Required - The content of the message.
- **search_mode** (enum) - Optional - Controls search mode: `academic` prioritizes scholarly sources, `sec` prioritizes SEC filings, `web` uses general web search. Defaults to `web`.
  - Available options: `academic`, `sec`, `web`
- **reasoning_effort** (enum) - Optional - Controls computational effort for deep research models. Only applicable for `sonar-deep-research`. Defaults to `medium`.
  - Available options: `low`, `medium`, `high`
- **max_tokens** (integer) - Optional - The maximum number of tokens to be generated in the completion. Controls response length.
- **temperature** (number) - Optional - Controls the randomness and creativity of the output. Range: `0 <= x < 2`. Defaults to `0.2`.
- **top_p** (number) - Optional - Nucleus sampling threshold. Controls diversity by considering tokens with cumulative probability exceeding this value. Range: `0` to `1`. Defaults to `0.9`.
- **language_preference** (string) - Optional - Preferred language for the response content. Supported by `sonar` and `sonar-pro` models.
- **search_domain_filter** (array) - Optional - A list of domains to limit search results to (allowlisting or denylisting).
- **return_images** (boolean) - Optional - Whether to include images in search results. Defaults to `false`.
- **return_related_questions** (boolean) - Optional - Whether to return related questions. Defaults to `false`.
- **search_recency_filter** (string) - Optional - Filters search results based on time (e.g., 'week', 'day').
- **search_after_date_filter** (string) - Optional - Filters search results to include content published after this date. Format: `MM/DD/YYYY`.
- **search_before_date_filter** (string) - Optional - Filters search results to include content published before this date. Format: `MM/DD/YYYY`.
- **last_updated_after_filter** (string) - Optional - Filters search results to include content last updated after this date. Format: `MM/DD/YYYY`.
- **last_updated_before_filter** (string) - Optional - Filters search results to include content last updated before this date. Format: `MM/DD/YYYY`.
- **top_k** (number) - Optional - Number of tokens to keep for top-k filtering. A value of `0` disables this filter. Defaults to `0`.
- **stream** (boolean) - Optional - Whether to stream the response incrementally. Defaults to `false`.
- **presence_penalty** (number) - Optional - Penalizes new tokens based on whether they appear in the text so far. Encourages discussion of new topics. Range: `0` to `2.0`. Defaults to `0`.
- **frequency_penalty** (number) - Optional - Penalizes new tokens based on their existing frequency in the text. Decreases repetition. Range: `0` to `2.0`. Defaults to `0`.

### Request Example
```json
{
  "model": "sonar-reasoning-pro",
  "messages": [
    { "role": "system", "content": "Be precise and concise."},
    { "role": "user", "content": "How many stars are there in our galaxy?"}
  ],
  "search_mode": "web",
  "reasoning_effort": "medium",
  "return_images": true
}
```

### Response
#### Success Response (200)
- **id** (string) - Unique identifier for the response.
- **object** (string) - Type of object, e.g., `chat.completion`.
- **created** (integer) - Unix timestamp of when the response was created.
- **model** (string) - The model used for the response.
- **choices** (array) - A list of completion choices.
  - **index** (integer) - Index of the choice.
  - **message** (object) - The generated message.
    - **role** (string) - The role of the message sender (e.g., `assistant`).
    - **content** (string) - The content of the message.
  - **finish_reason** (string) - The reason the model stopped generating tokens (e.g., `stop`, `length`).
- **usage** (object) - Information about token usage.
  - **prompt_tokens** (integer) - Number of tokens in the prompt.
  - **completion_tokens** (integer) - Number of tokens in the completion.
  - **total_tokens** (integer) - Total tokens used.

#### Response Example
```json
{
  "id": "chatcmpl-12345",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "sonar-reasoning-pro",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Our galaxy, the Milky Way, is estimated to contain between 100 and 400 billion stars."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 20,
    "total_tokens": 45
  }
}
```
```

--------------------------------

### Analyze Image from Base64 Data (cURL)

Source: https://docs.perplexity.ai/guides/image-attachments

This cURL command demonstrates how to send an image, encoded as Base64 data, to the Perplexity API for analysis. It specifies the 'sonar-pro' model and includes both text and image data within the 'messages' array. Ensure you replace '$BASE64_ENCODED_IMAGE' with your actual Base64 image string and '$SONAR_API_KEY' with your API key.

```cURL
curl --location 'https://api.perplexity.ai/chat/completions' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--header "Authorization: Bearer $SONAR_API_KEY" \
--data '{ "model": "sonar-pro", "stream": false, "messages": [ { "role": "user", "content": [ { "type": "text", "text": "Can you describe this image?" }, { "type": "image_url", "image_url": { "url": "data:image/png;base64,$BASE64_ENCODED_IMAGE" } } ] } ] }' | jq
```

--------------------------------

### Chat Completions API with Date Range Filtering

Source: https://docs.perplexity.ai/changelog/changelog

This endpoint enhances date range filtering with new fields like `latest_updated` for controlling search results based on content freshness. Useful for finding the most current information.

```APIDOC
## POST /api/chat/completions

### Description
Sends a request to the chat completions endpoint, with enhanced date range filtering capabilities using `latest_updated`.

### Method
POST

### Endpoint
/api/chat/completions

### Parameters
#### Query Parameters
- **web_search_options.latest_updated** (string) - Optional - Filter results based on when the webpage was last modified or updated (YYYY-MM-DD).
- **web_search_options.published_after** (string) - Optional - Filter by original publication date (YYYY-MM-DD).
- **web_search_options.published_before** (string) - Optional - Filter by original publication date (YYYY-MM-DD).
- **web_search_options.search_context_size** (string) - Optional - Defines the size of the search context (e.g., "low", "medium").

#### Request Body
- **model** (string) - Required - The model to use for the completion (e.g., "sonar-pro").
- **messages** (array of objects) - Required - An array of message objects, each with a `role` and `content`.
- **stream** (boolean) - Required - Whether to stream the response.
- **web_search_options** (object) - Optional - Object containing web search configurations.
  - **latest_updated** (string) - Optional - Filter results based on when the webpage was last modified or updated (YYYY-MM-DD).
  - **published_after** (string) - Optional - Filter by original publication date (YYYY-MM-DD).
  - **published_before** (string) - Optional - Filter by original publication date (YYYY-MM-DD).
  - **search_context_size** (string) - Optional - Defines the size of the search context (e.g., "low", "medium").

### Request Example
```json
{
  "model": "sonar-pro",
  "messages": [
    {"role": "user", "content": "What are the latest developments in AI research?"}
  ],
  "stream": false,
  "web_search_options": {
    "latest_updated": "2025-06-01",
    "search_context_size": "medium"
  }
}
```

### Response
#### Success Response (200)
- **id** (string) - Unique identifier for the response.
- **object** (string) - Type of the object.
- **created** (integer) - Timestamp of creation.
- **model** (string) - The model used for the response.
- **choices** (array) - Array of completion choices.
- **usage** (object) - Usage statistics for the request.
  - **prompt_tokens** (integer) - Number of tokens in the prompt.
  - **completion_tokens** (integer) - Number of tokens in the completion.
  - **total_tokens** (integer) - Total tokens used.
  - **cost** (object) - Cost details.
    - **input_tokens_cost** (number) - Cost of input tokens.
    - **output_tokens_cost** (number) - Cost of output tokens.
    - **request_cost** (number) - Fixed cost per request.
    - **total_cost** (number) - Total cost for the API call.

#### Response Example
```json
{
  "id": "chatcmpl-xxxxxxxxxxxxxxxxxxxx",
  "object": "chat.completion",
  "created": 1719836400,
  "model": "sonar-pro",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Recent developments in AI research include advancements in large language models, reinforcement learning, and computer vision..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 20,
    "completion_tokens": 150,
    "total_tokens": 170,
    "search_context_size": "medium",
    "cost": {
      "input_tokens_cost": 0.0003,
      "output_tokens_cost": 0.00225,
      "request_cost": 0.005,
      "total_cost": 0.00755
    }
  }
}
```
```

--------------------------------

### Total Content Budget Control with Perplexity AI (max_tokens)

Source: https://docs.perplexity.ai/guides/search-quickstart

Sets the maximum total tokens of webpage content returned across all search results. This parameter, used with `max_tokens_per_page`, controls the overall content volume in snippets. Defaults to 25,000 tokens, with a maximum of 1,000,000.

```python
from perplexity import Perplexity

client = Perplexity()
# Higher token budget = more content in snippets
detailed_search = client.search.create(
    query="renewable energy technologies",
    max_results=10,
    max_tokens=50000, # Total content budget across all results
    max_tokens_per_page=2048 # Per-result limit
)

# Lower token budget = shorter snippets
brief_search = client.search.create(
    query="latest stock market news",
    max_results=5,
    max_tokens=5000
)

for result in detailed_search.results:
    print(f"{result.title}: {result.url}")
```

--------------------------------

### Chat Completions API - Sonar Pro Model

Source: https://docs.perplexity.ai/getting-started/models/models/sonar-pro

This endpoint allows you to use the Sonar Pro model for advanced search and complex query analysis. It provides enhanced search results with reasoning and a higher volume of search data compared to standard models.

```APIDOC
## POST /chat/completions

### Description
Use the Sonar Pro model to perform advanced searches, analyze complex queries, and get enhanced, reasoned search results with a higher volume of information.

### Method
POST

### Endpoint
/chat/completions

### Parameters
#### Request Body
- **model** (string) - Required - The model to use for the chat completion (e.g., "sonar-pro").
- **messages** (array) - Required - An array of message objects, where each object has a `role` (e.g., "user", "system", "assistant") and `content` (string).

### Request Example
```json
{
  "model": "sonar-pro",
  "messages": [
    {
      "role": "user",
      "content": "Analyze the competitive positioning of Perplexity in the AI search market and evaluate how Comet compares to similar offerings from other companies."
    }
  ]
}
```

### Response
#### Success Response (200)
- **id** (string) - Unique identifier for the completion.
- **model** (string) - The model used for the completion.
- **created** (integer) - Timestamp of when the completion was created.
- **usage** (object) - Information about token usage and cost.
  - **prompt_tokens** (integer) - Number of tokens in the prompt.
  - **completion_tokens** (integer) - Number of tokens in the completion.
  - **total_tokens** (integer) - Total tokens used.
  - **search_context_size** (string) - The size of the search context used (e.g., "low", "medium", "high").
  - **cost** (object) - Cost breakdown.
    - **input_tokens_cost** (float) - Cost for input tokens.
    - **output_tokens_cost** (float) - Cost for output tokens.
    - **request_cost** (float) - Cost per request.
    - **total_cost** (float) - Total cost for the completion.
- **citations** (array) - Array of URLs for the sources used in the response.
- **search_results** (array) - Array of objects, each containing details about a search result.
  - **title** (string) - Title of the search result.
  - **url** (string) - URL of the search result.
  - **date** (string) - Publication date of the result.
  - **last_updated** (string) - Last updated date of the result.
  - **snippet** (string) - A short excerpt from the search result.

#### Response Example
```json
{
  "id": "12572668-b12a-4ce5-a697-57e22816a2ce",
  "model": "sonar-pro",
  "created": 1756486047,
  "usage": {
    "prompt_tokens": 26,
    "completion_tokens": 832,
    "total_tokens": 858,
    "search_context_size": "low",
    "cost": {
      "input_tokens_cost": 0.0,
      "output_tokens_cost": 0.012,
      "request_cost": 0.006,
      "total_cost": 0.019
    }
  },
  "citations": [
    "https://explodingtopics.com/blog/perplexity-ai-stats",
    "https://opentools.ai/news/perplexity-ceo-challenges-googles-ai-strategy-in-the-browser-wars",
    "https://taptwicedigital.com/stats/perplexity",
    "https://www.leanware.co/insights/comet-perplexity-everything-you-need-to-know",
    "https://www.index.dev/blog/perplexity-statistics"
  ],
  "search_results": [
    {
      "title": "The Latest Perplexity AI Stats (2025)",
      "url": "https://explodingtopics.com/blog/perplexity-ai-stats",
      "date": "2025-06-23",
      "last_updated": "2025-08-29",
      "snippet": "As of 2025, the AI space is valued at approximately $600 billion, with projections to increase by 500% over the next 5 years."
    },
    {
      "title": "Perplexity CEO Challenges Google's AI Strategy in the ...",
      "url": "https://opentools.ai/news/perplexity-ceo-challenges-googles-ai-strategy-in-the-browser-wars",
      "date": "2025-07-17",
      "last_updated": "2025-07-17",
      "snippet": "For example, Perplexity's AI-driven browser, Comet, represents a direct challenge to Google's traditional search engine model by prioritizing ..."
    },
    {
      "title": "7 Perplexity AI Statistics (2025): Revenue, Valuation, ...",
      "url": "https://taptwicedigital.com/stats/perplexity",
      "date": "2025-04-19",
      "last_updated": "2025-08-29",
      "snippet": "Perplexity AI holds a 6.2% market share in the AI search market. Perplexity AI is valued at $18 billion as of March 2025. Perplexity AI has ..."
    },
    {
      "title": "Comet Perplexity: Everything You Need to Know -"
    }
  ]
}
```
```

--------------------------------

### Async Chat Completion Response Structure

Source: https://docs.perplexity.ai/api-reference/async-chat-completions-post

This JSON object represents the successful response from an asynchronous chat completion request. It includes details about the job status, timestamps, model information, usage statistics (tokens), the generated message content, search results, and any available media like videos.

```json
{
  "id": "",
  "model": "",
  "created_at": 123,
  "status": "CREATED",
  "started_at": 123,
  "completed_at": 123,
  "response": {
    "id": "",
    "model": "",
    "created": 123,
    "usage": {
      "prompt_tokens": 123,
      "completion_tokens": 123,
      "total_tokens": 123,
      "search_context_size": "",
      "citation_tokens": 123,
      "num_search_queries": 123,
      "reasoning_tokens": 123
    },
    "object": "chat.completion",
    "choices": [
      {
        "index": 123,
        "message": {
          "content": "",
          "role": "system"
        },
        "finish_reason": "stop"
      }
    ],
    "search_results": [
      {
        "title": "",
        "url": "",
        "date": "2023-12-25"
      }
    ],
    "videos": [
      {
        "url": "",
        "thumbnail_url": "",
        "thumbnail_width": 123,
        "thumbnail_height": 123,
        "duration": 123
      }
    ]
  },
  "failed_at": 123,
  "error_message": ""
}
```

--------------------------------

### Stream Chat Completion with Metadata (TypeScript)

Source: https://docs.perplexity.ai/guides/streaming-responses

This TypeScript function demonstrates how to stream chat completions from the Perplexity API and collect metadata such as search results and usage information. It iterates over the stream, processing content pieces and extracting metadata from relevant chunks. The function returns the complete content, search results, and usage data.

```typescript
async function streamWithMetadata(query: string) {
  const client = new Perplexity();
  const stream = await client.chat.completions.create({
    model: "sonar",
    messages: [{ role: "user", content: query }],
    stream: true
  });
  let content = "";
  let searchResults: any[] = [];
  let usage: any = undefined;
  for await (const chunk of stream) {
    // Process content
    if (chunk.choices[0]?.delta?.content) {
      const contentPiece = chunk.choices[0].delta.content;
      content += contentPiece;
      process.stdout.write(contentPiece);
    }
    // Collect metadata from final chunks
    if (chunk.search_results) {
      searchResults = chunk.search_results;
    }
    if (chunk.usage) {
      usage = chunk.usage;
    }
    // Check if streaming is complete
    if (chunk.choices[0]?.finish_reason) {
      console.log(`\n\nSearch Results:`, searchResults);
      console.log(`Usage:`, usage);
    }
  }
  return { content, searchResults, usage };
}

// Usage
const result = await streamWithMetadata("Explain quantum computing");
```

--------------------------------

### Preferred Language for AI Responses

Source: https://docs.perplexity.ai/api-reference/chat-completions-post

Specifies the desired language for the AI's response content. Supported by 'sonar' and 'sonar-pro' models. Using with other models is best-effort.

```text
language_preference: string
```

--------------------------------

### Language Code Validation Best Practices

Source: https://docs.perplexity.ai/guides/search-language-filter

Guidelines for validating language codes to ensure API compatibility and prevent errors.

```APIDOC
## Language Code Validation Best Practices

### Use Valid Codes
Always use valid 2-letter ISO 639-1 codes. Invalid codes will result in an API error.

### Lowercase Only
Language codes must be lowercase (e.g., "en" not "EN").

### Client-Side Validation
Validate language codes on the client side using a regex pattern.

**Python Example:**
```python
import re

def validate_language_code(code):
    pattern = r'^[a-z]{2}$'
    return bool(re.match(pattern, code))

def validate_language_filters(codes):
    if len(codes) > 10:
        raise ValueError("Maximum 10 language codes allowed")
    for code in codes:
        if not validate_language_code(code):
            raise ValueError(f"Invalid language code: {code}")
    return True

# Usage
try:
    codes = ["en", "fr", "de"]
    validate_language_filters(codes)
    # Proceed with API call
except ValueError as e:
    print(f"Validation error: {e}")
```

**TypeScript Example:**
```typescript
function validateLanguageCode(code: string): boolean {
  const pattern = /^[a-z]{2}$/;
  return pattern.test(code);
}

function validateLanguageFilters(codes: string[]): boolean {
  if (codes.length > 10) {
    throw new Error("Maximum 10 language codes allowed");
  }
  for (const code of codes) {
    if (!validateLanguageCode(code)) {
      throw new Error(`Invalid language code: ${code}`);
    }
  }
  return true;
}

// Usage
try {
  const codes = ["en", "fr", "de"];
  validateLanguageFilters(codes);
  // Proceed with API call
} catch (error: any) {
  console.error(`Validation error: ${error.message}`);
}
```
```

--------------------------------

### Using Search Recency Filter

Source: https://docs.perplexity.ai/guides/date-range-filter-guide

This demonstrates how to use the `search_recency_filter` for convenient filtering by predefined time periods like 'week', 'month', etc.

```APIDOC
## POST /chat/completions

### Description
Filters search results by predefined time periods using the `search_recency_filter` parameter.

### Method
POST

### Endpoint
/chat/completions

### Parameters
#### Query Parameters
- **search_recency_filter** (string) - Required - Filters results by predefined time periods (e.g., "week", "month").

### Request Example
```python
from perplexity import Perplexity

client = Perplexity()
completion = client.chat.completions.create(
    model="sonar-pro",
    messages=[
        {"role": "system", "content": "You are an expert on current events."},
        {"role": "user", "content": "What are the latest AI developments?"}
    ],
    search_recency_filter="week"
)

print(completion.choices[0].message.content)
```

### Response
#### Success Response (200)
- **choices** (array) - List of completion choices.
  - **message** (object) - The message content from the completion.
    - **content** (string) - The generated text response.

#### Response Example
```json
{
  "choices": [
    {
      "message": {
        "content": "Latest AI developments from the past week..."
      }
    }
  ]
}
```
```

--------------------------------

### Convert LlamaIndex Messages to Perplexity API Format

Source: https://docs.perplexity.ai/cookbook/articles/memory-management/chat-summary-memory-buffer/README

This code snippet demonstrates how to convert LlamaIndex's ChatMessage objects into a dictionary format compatible with the Perplexity API. It ensures that the core message structure (role and content) is preserved while omitting internal metadata, facilitating seamless API integration.

```python
messages_dict = [
    {"role": m.role, "content": m.content}
    for m in messages
]
```

--------------------------------

### Search with Different Recency Filter Options (Python)

Source: https://docs.perplexity.ai/guides/search-date-time-filters

Demonstrates using the search_recency_filter with different values ('day', 'month', 'year') to retrieve content from the past day, month, or year. Requires the perplexity library. Returns response objects.

```python
from perplexity import Perplexity
client = Perplexity()

# Get content from the past day
day_response = client.search(
  query="breaking tech news",
  max_results=5,
  search_recency_filter="day"
)

# Get content from the past month
month_response = client.search(
  query="AI research developments",
  max_results=10,
  search_recency_filter="month"
)

# Get content from the past year
year_response = client.search(
  query="major tech trends",
  max_results=15,
  search_recency_filter="year"
)

```

--------------------------------

### Filter Search by Language (Perplexity-Specific)

Source: https://docs.perplexity.ai/api-reference/search-post

Filters search results to include only content in specified languages using ISO 639-1 codes. Accepts an array of up to 10 language codes.

```json
["en", "fr", "de"]
```

--------------------------------

### Chat Completions API with Academic Filter

Source: https://docs.perplexity.ai/changelog/changelog

This endpoint enables tailoring searches specifically to academic and scholarly sources by setting the `search_mode` parameter to 'academic'. It prioritizes results from peer-reviewed papers and research publications.

```APIDOC
## POST /api/chat/completions

### Description
Sends a request to the chat completions endpoint, with the option to filter search results to academic and scholarly sources.

### Method
POST

### Endpoint
/api/chat/completions

### Parameters
#### Query Parameters
- **search_mode** (string) - Optional - Set to "academic" to prioritize results from academic and scholarly sources.
- **web_search_options.search_context_size** (string) - Optional - Defines the size of the search context (e.g., "low", "medium").

#### Request Body
- **model** (string) - Required - The model to use for the completion (e.g., "sonar-pro").
- **messages** (array of objects) - Required - An array of message objects, each with a `role` and `content`.
- **stream** (boolean) - Required - Whether to stream the response.
- **search_mode** (string) - Optional - Set to "academic" to prioritize results from academic and scholarly sources.
- **web_search_options** (object) - Optional - Object containing web search configurations.
  - **search_context_size** (string) - Optional - Defines the size of the search context (e.g., "low", "medium").

### Request Example
```json
{
  "model": "sonar-pro",
  "messages": [
    {"role": "user", "content": "What is the scientific name of the lions mane mushroom?"}
  ],
  "stream": false,
  "search_mode": "academic",
  "web_search_options": {
    "search_context_size": "low"
  }
}
```

### Response
#### Success Response (200)
- **id** (string) - Unique identifier for the response.
- **object** (string) - Type of the object.
- **created** (integer) - Timestamp of creation.
- **model** (string) - The model used for the response.
- **choices** (array) - Array of completion choices.
- **usage** (object) - Usage statistics for the request.
  - **prompt_tokens** (integer) - Number of tokens in the prompt.
  - **completion_tokens** (integer) - Number of tokens in the completion.
  - **total_tokens** (integer) - Total tokens used.
  - **cost** (object) - Cost details.
    - **input_tokens_cost** (number) - Cost of input tokens.
    - **output_tokens_cost** (number) - Cost of output tokens.
    - **request_cost** (number) - Fixed cost per request.
    - **total_cost** (number) - Total cost for the API call.

#### Response Example
```json
{
  "id": "chatcmpl-xxxxxxxxxxxxxxxxxxxx",
  "object": "chat.completion",
  "created": 1717238400,
  "model": "sonar-pro",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "The scientific name for the Lion's Mane mushroom is Hericium erinaceus."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 18,
    "completion_tokens": 10,
    "total_tokens": 28,
    "search_context_size": "low",
    "cost": {
      "input_tokens_cost": 0.00027,
      "output_tokens_cost": 0.00015,
      "request_cost": 0.005,
      "total_cost": 0.00542
    }
  }
}
```
```

--------------------------------

### SEC Filings Filter for Financial Research using cURL

Source: https://docs.perplexity.ai/changelog

This cURL command demonstrates how to use the 'sec' search domain to filter API results for SEC regulatory documents. It's useful for financial analysts and investment professionals.

```bash
curl --request POST \
  --url https://api.perplexity.ai/chat/completions \
  --header 'accept: application/json' \
  --header 'authorization: Bearer YOUR_API_KEY' \
  --header 'content-type: application/json' \
  --data '{ "model": "sonar-pro", "messages": [{"role": "user", "content": "What was Apple's revenue growth in their latest quarterly report?"}], "stream": false, "search_domain": "sec", "web_search_options": {"search_context_size": "medium"} }' | jq
```

--------------------------------

### Search Results Enhancement

Source: https://docs.perplexity.ai/changelog/changelog

This documentation describes the 'search_results' field added to API responses, providing direct access to the search data used by models. It replaces the deprecated 'citations' field and includes titles, URLs, and publication dates.

```APIDOC
## Enhanced API Responses with Search Results

### Description
API responses now include a `search_results` field, offering detailed information about the sources used by the models. This field replaces the deprecated `citations` field.

### Response Structure
- **search_results** (array) - An array of objects, where each object represents a search result.
  - **title** (string) - The title of the search result page.
  - **url** (string) - The URL of the search result.
  - **date** (string) - The publication date of the content in 'YYYY-MM-DD' format.

### Usage
This field is available across all search-enabled models and helps in verifying sources, creating custom citations, and filtering information.

### Deprecation Notice
The `citations` field has been fully deprecated and removed. Use `search_results` instead.

### Example Snippet within Response
```json
{
  "search_results": [
    {
      "title": "Understanding Large Language Models",
      "url": "https://example.com/llm-article",
      "date": "2023-12-25"
    },
    {
      "title": "Advances in AI Research",
      "url": "https://example.com/ai-research",
      "date": "2024-03-15"
    }
  ]
}
```
```

--------------------------------

### Perplexity API: Perform Regional Web Search (Python)

Source: https://docs.perplexity.ai/guides/search-quickstart

This Python code snippet demonstrates how to use the Perplexity API to perform a web search focused on a specific country. It utilizes the `country` parameter to refine results geographically and iterates through the search results to print titles and URLs. Requires the `perplexity` library.

```python
from perplexity import Perplexity

client = Perplexity()

# Search for results from a specific country
search = client.search.create(
    query="government policies on renewable energy",
    country="US",  # ISO country code
    max_results=5
)

for result in search.results:
    print(f"{result.title}: {result.url}")
```

--------------------------------

### Robust LLM Streaming with Retries (TypeScript)

Source: https://docs.perplexity.ai/guides/streaming-responses

This TypeScript snippet implements robust streaming for Perplexity AI LLMs by incorporating automatic retry logic for network interruptions. It attempts to reconnect and resume streaming up to a specified number of times, with exponential backoff. Dependencies include the Perplexity client library.

```typescript
import { Perplexity } from "perplexity";

async function robustStreaming(query: string, maxRetries: number = 3) {
  const client = new Perplexity();
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const stream = await client.chat.completions.create({
        model: "sonar",
        messages: [{ role: "user", content: query }],
        stream: true
      });
      for await (const chunk of stream) {
        if (chunk.choices[0]?.delta?.content) {
          process.stdout.write(chunk.choices[0].delta.content);
        }
      }
      return; // Success, exit retry loop
    } catch (error) {
      if (error instanceof Perplexity.APIConnectionError && attempt < maxRetries - 1) {
        const delay = Math.pow(2, attempt) * 1000 + Math.random() * 1000;
        console.log(`\nConnection error, retrying in ${delay / 1000:.1f}s...`);
        await new Promise(resolve => setTimeout(resolve, delay));
      } else {
        console.error(`\nFailed after ${maxRetries} attempts:`, error);
        throw error;
      }
    }
  }
}

robustStreaming("Explain quantum computing");
```

--------------------------------

### Robust LLM Streaming with Retries (Python)

Source: https://docs.perplexity.ai/guides/streaming-responses

This Python snippet implements robust streaming for Perplexity AI LLMs by incorporating automatic retry logic for network interruptions. It attempts to reconnect and resume streaming up to a specified number of times, with exponential backoff. Dependencies include the 'perplexity' library, 'time', and 'random'.

```python
import time
import random
from perplexity import Perplexity
import perplexity

def robust_streaming(query: str, max_retries: int = 3):
    client = Perplexity()
    for attempt in range(max_retries):
        try:
            stream = client.chat.completions.create(
                model="sonar",
                messages=[{"role": "user", "content": query}],
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    print(chunk.choices[0].delta.content, end='', flush=True)
            return  # Success, exit retry loop
        except (perplexity.APIConnectionError, perplexity.APITimeoutError) as e:
            if attempt < max_retries - 1:
                delay = (2 ** attempt) + random.uniform(0, 1)
                print(f"\nConnection error, retrying in {delay:.1f}s...")
                time.sleep(delay)
            else:
                print(f"\nFailed after {max_retries} attempts: {e}")
                raise

robust_streaming("Explain quantum computing")
```

--------------------------------

### Content Extraction Control with Perplexity AI (max_tokens_per_page)

Source: https://docs.perplexity.ai/guides/search-quickstart

Controls the maximum number of tokens extracted from each webpage during search processing. Higher values provide more content but increase processing time; lower values prioritize speed. Defaults to 2048 tokens.

```python
from perplexity import Perplexity

client = Perplexity()
# Extract more content for comprehensive analysis
detailed_search = client.search.create(
    query="artificial intelligence research methodology",
    max_results=5,
    max_tokens_per_page=2048
)

# Use default extraction for faster processing
quick_search = client.search.create(
    query="AI news headlines",
    max_results=10,
    max_tokens_per_page=512
)

for result in detailed_search.results:
    print(f"{result.title}: {result.snippet[:100]}...")
```

--------------------------------

### Stream Chat Completion with Error Handling (TypeScript)

Source: https://docs.perplexity.ai/guides/streaming-responses

This TypeScript code shows how to stream chat completions using the Perplexity AI SDK and includes robust error handling. It catches various error types, including network connection issues, rate limiting, and general API errors, providing specific feedback to the user.

```typescript
import Perplexity from '@perplexity-ai/perplexity_ai';

const client = new Perplexity();
try {
  const stream = await client.chat.completions.create({
    model: "sonar-pro",
    messages: [
      { role: "user", content: "Explain machine learning concepts" }
    ],
    stream: true
  });
  for await (const chunk of stream) {
    if (chunk.choices[0]?.delta?.content) {
      process.stdout.write(chunk.choices[0].delta.content);
    }
  }
} catch (error) {
  if (error instanceof Perplexity.APIConnectionError) {
    console.error("Network connection failed:", error.cause);
  } else if (error instanceof Perplexity.RateLimitError) {
    console.error("Rate limit exceeded, please retry later");
  } else if (error instanceof Perplexity.APIError) {
    console.error(`API error ${error.status}: ${error.message}`);
  } else {
    console.error("Unexpected error:", error);
  }
}
```

--------------------------------

### Search Wikipedia Across Languages

Source: https://docs.perplexity.ai/guides/search-domain-filter-guide

Search across all Wikipedia language editions by specifying the root domain 'wikipedia.org'.

```APIDOC
## POST /search

### Description
Searches across all Wikipedia language editions by specifying the root domain 'wikipedia.org'.

### Method
POST

### Endpoint
/search

### Parameters
#### Query Parameters
- **query** (string) - Required - The search query.
- **max_results** (integer) - Optional - The maximum number of results to return.
- **search_domain_filter** (array of strings) - Optional - Filters search results to include or exclude content from specified domains.

### Request Example
```json
{
  "query": "quantum mechanics",
  "max_results": 10,
  "search_domain_filter": [
    "wikipedia.org"
  ]
}
```

### Response
#### Success Response (200)
- **results** (array) - A list of search results.
  - **title** (string) - The title of the search result.
  - **url** (string) - The URL of the search result.

#### Response Example
```json
{
  "results": [
    {
      "title": "Quantum Mechanics",
      "url": "https://en.wikipedia.org/wiki/Quantum_mechanics"
    }
  ]
}
```
```

--------------------------------

### Combine Domain Filter with Other Filters

Source: https://docs.perplexity.ai/guides/search-domain-filter-guide

Combine domain filters with other search parameters like date and language for precise control over results.

```APIDOC
## POST /search

### Description
Combines domain filters with other search parameters like date and language for precise control over results.

### Method
POST

### Endpoint
/search

### Parameters
#### Query Parameters
- **query** (string) - Required - The search query.
- **max_results** (integer) - Optional - The maximum number of results to return.
- **search_domain_filter** (array of strings) - Optional - Filters search results to include or exclude content from specified domains.
- **search_recency_filter** (string) - Optional - Filters results by recency (e.g., "day", "week", "month").
- **search_language_filter** (array of strings) - Optional - Filters results by language code (e.g., "en" for English).

### Request Example
```json
{
  "query": "quantum computing breakthroughs",
  "max_results": 20,
  "search_domain_filter": [
    "nature.com",
    "science.org",
    "arxiv.org"
  ],
  "search_recency_filter": "month",
  "search_language_filter": ["en"]
}
```

### Response
#### Success Response (200)
- **results** (array) - A list of search results.
  - **title** (string) - The title of the search result.
  - **url** (string) - The URL of the search result.
  - **date** (string) - The publication date of the search result.

#### Response Example
```json
{
  "results": [
    {
      "title": "Major Advance in Quantum Computing",
      "url": "https://www.nature.com/articles/quantum-advance",
      "date": "2023-10-25"
    }
  ]
}
```
```

--------------------------------

### Model Deprecation Notice

Source: https://docs.perplexity.ai/changelog

Notice regarding the deprecation of the R1-1776 model. Developers are advised to migrate to 'Sonar Pro Reasoning' for similar behavior with improved performance.

```APIDOC
## API Model Deprecation Notice

### Description
This notice informs users that the R1-1776 model will be removed from the available API models as of August 1, 2025. Users are recommended to migrate to the 'Sonar Pro Reasoning' model, which offers similar capabilities with enhanced performance.

### Method
N/A (Informational)

### Endpoint
N/A

### Parameters
N/A

### Request Example
N/A

### Response
N/A
```

--------------------------------

### Collect Metadata During Streaming (Python)

Source: https://docs.perplexity.ai/guides/streaming-responses

This Python function illustrates how to stream responses and simultaneously collect search results and usage metadata. Metadata is typically found in the final chunks of the stream. The function prints content as it arrives and then processes the collected metadata.

```python
from perplexity import Perplexity

def stream_with_metadata():
    client = Perplexity()
    stream = client.chat.completions.create(
        model="sonar",
        messages=[{"role": "user", "content": "Explain quantum computing"}],
        stream=True
    )

    content = ""
    search_results = []
    usage_info = None

    for chunk in stream:
        # Process content
        if chunk.choices[0].delta.content:
            content_piece = chunk.choices[0].delta.content
            content += content_piece
            print(content_piece, end='', flush=True)

        # Collect metadata from final chunks
        if hasattr(chunk, 'search_results') and chunk.search_results:
            search_results = chunk.search_results
        if hasattr(chunk, 'usage') and chunk.usage:
            usage_info = chunk.usage

    print("\n---")
    print("Collected Search Results:", search_results)
    print("Collected Usage Info:", usage_info)

stream_with_metadata()
```

--------------------------------

### Sonar Deep Research with Reasoning Effort

Source: https://docs.perplexity.ai/changelog/changelog

This endpoint allows you to control the computational effort for Sonar Deep Research queries. You can set 'reasoning_effort' to 'low', 'medium', or 'high' to balance response speed, thoroughness, and token consumption.

```APIDOC
## POST /chat/completions (Sonar Deep Research)

### Description
Allows control over the computational effort dedicated to each query for the sonar-deep-research model. Choose 'low', 'medium', or 'high' for varying levels of response depth and speed.

### Method
POST

### Endpoint
https://api.perplexity.ai/chat/completions

### Parameters
#### Query Parameters
None

#### Request Body
- **model** (string) - Required - The model to use, e.g., "sonar-deep-research".
- **messages** (array) - Required - An array of message objects, each with 'role' and 'content'.
- **stream** (boolean) - Optional - Whether to stream the response.
- **reasoning_effort** (string) - Optional - Controls computational effort. Options: "low", "medium", "high". Defaults to "medium".

### Request Example
```json
{
  "model": "sonar-deep-research",
  "messages": [
    {"role": "user", "content": "What should I know before markets open today?"}
  ],
  "stream": true,
  "reasoning_effort": "low"
}
```

### Response
#### Success Response (200)
- **choices** (array) - An array of response choices, each containing message content.
- **search_results** (array) - An array of search result objects, each with 'title', 'url', and 'date'.

#### Response Example
```json
{
  "id": "chatcmpl-xxxxxxxxxxxxxxxxxxxx",
  "object": "chat.completion",
  "created": 1719874567,
  "model": "sonar-deep-research",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Here's what you should know before markets open..."
      },
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 100,
    "total_tokens": 125
  },
  "search_results": [
    {
      "title": "Top Financial News Today",
      "url": "https://finance.example.com/news/today",
      "date": "2024-07-01"
    }
  ]
}
```
```

--------------------------------

### Enable Media Content in Perplexity AI Responses

Source: https://docs.perplexity.ai/api-reference/chat-completions-post

Controls the inclusion of media types like videos and images in Perplexity AI's responses. The `media_response` object, specifically its `overrides` property, allows enabling or disabling `return_videos` and `return_images`.

```json
{
  "overrides": {
    "return_videos": true,
    "return_images": true
  }
}
```

--------------------------------

### Filter Search by Latest Updated Date with cURL

Source: https://docs.perplexity.ai/changelog/changelog

This cURL command shows how to query the Perplexity AI API and filter results based on when a webpage was last modified, using the `latest_updated` field within `web_search_options`. This ensures results are based on recent content updates.

```bash
curl --request POST \
  --url https://api.perplexity.ai/chat/completions \
  --header 'accept: application/json' \
  --header 'authorization: Bearer YOUR_API_KEY' \
  --header 'content-type: application/json' \
  --data '{ "model": "sonar-pro", "messages": [{"role": "user", "content": "What are the latest developments in AI research?"}], "stream": false, "web_search_options": { "latest_updated": "2025-06-01", "search_context_size": "medium" } }'
```

--------------------------------

### Search API Endpoint

Source: https://docs.perplexity.ai/api-reference

This endpoint allows you to search for content using Perplexity AI. You can specify your search query, filter by date, and limit results by language.

```APIDOC
## GET /search

### Description
This endpoint allows you to search for content using Perplexity AI. You can specify your search query, filter by date, and limit results by language.

### Method
GET

### Endpoint
/search

### Parameters
#### Query Parameters
- **query** (string) - Required - The search query string.
- **limit_date** (string) - Optional - Filters search results to only include content published on or before the specified date. Accepts dates in MM/DD/YYYY format (e.g., '12/30/2025').
- **search_language_filter** (string[]) - Optional - Perplexity-Specific: Filters search results to only include content in the specified languages. Accepts an array of ISO 639-1 language codes (2 lowercase letters). Maximum 10 language codes per request. Maximum array length: 10. Example: `["en", "fr", "de"]`

### Response
#### Success Response (200)
- **results** (SearchResult[]) - Required - An array of search results.

#### Response Example
```json
{
  "results": [
    {
      "title": "Example Title",
      "url": "https://example.com",
      "snippet": "This is an example snippet from the search result."
    }
  ]
}
```
```

--------------------------------

### Common Language Codes

Source: https://docs.perplexity.ai/guides/search-language-filter

Provides a list of commonly used ISO 639-1 language codes for the `search_language_filter` parameter.

```APIDOC
## Common Language Codes

Here’s a comprehensive list of frequently used ISO 639-1 language codes:

| Language      | Code |
|---------------|------|
| English       | `en` |
| Spanish       | `es` |
| French        | `fr` |
| German        | `de` |
| Italian       | `it` |
| Russian       | `ru` |
| Chinese       | `zh` |
| Japanese      | `ja` |
| Korean        | `ko` |
| Arabic        | `ar` |
| Hindi         | `hi` |
| Bengali       | `bn` |
| Indonesian    | `id` |
| Vietnamese    | `vi` |
| Portuguese    | `pt` |
| Dutch         | `nl` |
| Polish        | `pl` |
| Swedish       | `sv` |
| Norwegian     | `no` |
| Danish        | `da` |
| Finnish       | `fi` |
| Czech         | `cs` |
| Hungarian     | `hu` |
| Greek         | `el` |
| Turkish       | `tr` |
| Hebrew        | `he` |
| Thai          | `th` |
| Ukrainian     | `uk` |

For a complete list of ISO 639-1 language codes, see the ISO 639-1 standard.
```

--------------------------------

### Chat Completions with Academic Filter

Source: https://docs.perplexity.ai/changelog

This endpoint enables chat completions by prioritizing results from academic and scholarly sources, ideal for research and finding scientifically accurate information.

```APIDOC
## POST /chat/completions

### Description
Performs chat completions with a filter to prioritize academic and scholarly sources.

### Method
POST

### Endpoint
https://api.perplexity.ai/chat/completions

### Parameters
#### Query Parameters
- **search_mode** (string) - Optional - Set to "academic" to focus on scholarly sources.
- **web_search_options.search_context_size** (string) - Optional - Controls the size of the search context (e.g., "low", "medium", "high").

#### Request Body
- **model** (string) - Required - The model to use for completions (e.g., "sonar-pro").
- **messages** (array) - Required - An array of message objects, where each object has a "role" and "content".
- **stream** (boolean) - Required - Whether to stream the response.

### Request Example
```json
{
  "model": "sonar-pro",
  "messages": [
    {"role": "user", "content": "What is the scientific name of the lions mane mushroom?"}
  ],
  "stream": false,
  "search_mode": "academic",
  "web_search_options": {
    "search_context_size": "low"
  }
}
```

### Response
#### Success Response (200)
- **id** (string) - Unique identifier for the response.
- **object** (string) - Type of the object returned.
- **created** (integer) - Timestamp of creation.
- **model** (string) - The model used for the response.
- **choices** (array) - An array of completion choices.
- **usage** (object) - Object detailing token usage and cost.

#### Response Example
```json
{
  "id": "chatcmpl-zzzzzzzzzzzzzzz",
  "object": "chat.completion",
  "created": 1716758400,
  "model": "sonar-pro",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "The scientific name for the lion's mane mushroom is *Hericium erinaceus*. This is according to several mycological databases and peer-reviewed studies."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 30,
    "total_tokens": 42
  }
}
```
```

--------------------------------

### Reasoning Effort Control for Deep Research Models

Source: https://docs.perplexity.ai/api-reference/chat-completions-post

Adjusts the computational effort for deep research queries, impacting answer depth and token usage. Options are 'low' (faster, fewer tokens), 'medium' (balanced), and 'high' (thorough, more tokens). This is specific to 'sonar-deep-research' models.

```text
reasoning_effort: 'low' | 'medium' | 'high'
```

--------------------------------

### Stream Chat Completion with Metadata (Python)

Source: https://docs.perplexity.ai/guides/streaming-responses

This Python function uses the `requests` library to stream chat completions from the Perplexity API. It iterates through the response lines, decodes them, and parses JSON data to extract content and metadata like search results and usage. The function returns the accumulated content and metadata.

```python
import requests
import json
def stream_with_requests_metadata():
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "sonar",
        "messages": [{"role": "user", "content": "Explain quantum computing"}],
        "stream": True
    }
    response = requests.post(url, headers=headers, json=payload, stream=True)
    content = ""
    metadata = {}
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith('data: '):
                data_str = line[6:]
                if data_str == '[DONE]':
                    break
                try:
                    chunk = json.loads(data_str)
                    # Process content
                    if 'choices' in chunk and chunk['choices'][0]['delta'].get('content'):
                        content_piece = chunk['choices'][0]['delta']['content']
                        content += content_piece
                        print(content_piece, end='', flush=True)
                    # Collect metadata
                    for key in ['search_results', 'usage']:
                        if key in chunk:
                            metadata[key] = chunk[key]
                    # Check if streaming is complete
                    if chunk['choices'][0].get('finish_reason'):
                        print(f"\n\nMetadata: {metadata}")
                except json.JSONDecodeError:
                    continue
    return content, metadata

stream_with_requests_metadata()
```

--------------------------------

### cURL: Perplexity AI Search API Call

Source: https://docs.perplexity.ai/models/models/sonar-deep-research

This cURL command illustrates how to make a search request to the Perplexity AI API. It sends a POST request to the search endpoint with a JSON payload containing the query. Replace 'YOUR_API_KEY' with your actual API key.

```bash
curl -X POST "https://api.perplexity.ai/chat/completions" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -d '{
       "model": "llama-3-sonar-small",
       "messages": [
         {
           "role": "user",
           "content": "What is Comet Browser?"
         }
       ]
     }'
```

--------------------------------

### Chat Completions with Enhanced Date Range Filtering

Source: https://docs.perplexity.ai/changelog

This endpoint allows for chat completions with enhanced control over search results using date range filtering, including a new `latest_updated` field.

```APIDOC
## POST /chat/completions

### Description
Performs chat completions with enhanced date range filtering capabilities.

### Method
POST

### Endpoint
https://api.perplexity.ai/chat/completions

### Parameters
#### Query Parameters
- **web_search_options.latest_updated** (string) - Optional - Filter results based on when the webpage was last modified or updated (YYYY-MM-DD format).
- **web_search_options.published_after** (string) - Optional - Filter by original publication date (YYYY-MM-DD format).
- **web_search_options.published_before** (string) - Optional - Filter by original publication date (YYYY-MM-DD format).
- **web_search_options.search_context_size** (string) - Optional - Controls the size of the search context (e.g., "low", "medium", "high").

#### Request Body
- **model** (string) - Required - The model to use for completions (e.g., "sonar-pro").
- **messages** (array) - Required - An array of message objects, where each object has a "role" and "content".
- **stream** (boolean) - Required - Whether to stream the response.

### Request Example
```json
{
  "model": "sonar-pro",
  "messages": [
    {"role": "user", "content": "What are the latest developments in AI research?"}
  ],
  "stream": false,
  "web_search_options": {
    "latest_updated": "2025-06-01",
    "search_context_size": "medium"
  }
}
```

### Response
#### Success Response (200)
- **id** (string) - Unique identifier for the response.
- **object** (string) - Type of the object returned.
- **created** (integer) - Timestamp of creation.
- **model** (string) - The model used for the response.
- **choices** (array) - An array of completion choices.
- **usage** (object) - Object detailing token usage and cost.

#### Response Example
```json
{
  "id": "chatcmpl-yyyyyyyyyyyyyyy",
  "object": "chat.completion",
  "created": 1719763200,
  "model": "sonar-pro",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Recent developments in AI research include advancements in large language models, reinforcement learning, and explainable AI. For instance, a paper published on June 1st, 2025, discusses a new approach to unsupervised learning."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 50,
    "total_tokens": 65
  }
}
```
```

--------------------------------

### Search with Date Range

Source: https://docs.perplexity.ai/guides/search-date-time-filters

Demonstrates how to filter search results to a specific publication date range using `search_after_date` and `search_before_date`.

```APIDOC
## POST /api/search

### Description
Filters search results to include only content published within a specified date range.

### Method
POST

### Endpoint
/api/search

### Parameters
#### Query Parameters
- **query** (string) - Required - The search query.
- **max_results** (integer) - Optional - The maximum number of results to return.
- **search_after_date** (string) - Optional - Filters results to content published after this date. Format: "m/d/YYYY".
- **search_before_date** (string) - Optional - Filters results to content published before this date. Format: "m/d/YYYY".

### Request Example
```python
from perplexity import Perplexity

client = Perplexity()
response = client.search(
    query="latest AI developments",
    max_results=10,
    search_after_date="3/1/2025",
    search_before_date="3/5/2025"
)
print(response)
```

### Response
#### Success Response (200)
- **results** (array) - A list of search results.
  - **title** (string) - The title of the search result.
  - **url** (string) - The URL of the search result.
  - **snippet** (string) - A short snippet of the search result content.
  - **published_date** (string) - The publication date of the content.
  - **last_updated** (string) - The last updated date of the content.

#### Response Example
```json
{
  "results": [
    {
      "title": "AI Breakthroughs in 2025",
      "url": "http://example.com/ai-breakthroughs",
      "snippet": "Recent advancements in AI are transforming industries...",
      "published_date": "3/2/2025",
      "last_updated": "3/3/2025"
    }
  ]
}
```
```

--------------------------------

### Return Related Questions

Source: https://docs.perplexity.ai/api-reference/chat-completions-post

A boolean flag to control whether related questions are returned alongside the main answer. This is a Perplexity-Specific feature.

```text
return_related_questions: boolean
```

--------------------------------

### Validate Domain and Domain Filter (Python)

Source: https://docs.perplexity.ai/guides/search-domain-filter-guide

Validates individual domain formats, including TLD filters, and checks if a list of domains adheres to the maximum limit of 20. It uses regular expressions for pattern matching.

```python
import re

def validate_domain(domain):
    """Validate domain format including TLD filters."""
    # TLD filter (e.g., .gov, .edu)
    if domain.startswith('.'):
        tld_pattern = r'^\.[a-zA-Z]{2,}$'
        return bool(re.match(tld_pattern, domain))
    # Standard domain validation pattern
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$' 
    return bool(re.match(pattern, domain))

def validate_domain_filter(domains):
    """Validate domain filter array."""
    if len(domains) > 20:
        raise ValueError("Maximum 20 domains allowed")
    for domain in domains:
        if not validate_domain(domain):
            raise ValueError(f"Invalid domain format: {domain}")
    return True

# Usage examples
try:
    # Mix of regular domains and TLD filters
    domains = ["nature.com", "science.org", ".gov", ".edu"]
    validate_domain_filter(domains)
    # response = client.search.create(
    #     query="research topic", 
    #     search_domain_filter=domains
    # )
except ValueError as e:
    print(f"Validation error: {e}")
```

--------------------------------

### Filter Search Results by Last Update Date (Before)

Source: https://docs.perplexity.ai/api-reference/chat-completions-post

Filters search results to include only content last updated before a specified date. Requires the date in MM/DD/YYYY format. Perplexity-Specific.

```text
last_updated_before_filter: string (format: MM/DD/YYYY)
```

--------------------------------

### Search API

Source: https://docs.perplexity.ai/api-reference/search-post

Retrieve ranked search results from Perplexity’s continuously refreshed index with advanced filtering and customization options.

```APIDOC
## POST /search

### Description
Get ranked search results from Perplexity’s continuously refreshed index with advanced filtering and customization options.

### Method
POST

### Endpoint
https://api.perplexity.ai/search

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
- **query** (string) - Required - A search query. Can be a single query or a list of queries for multi-query search.
- **max_results** (integer) - Optional - The maximum number of search results to return. Required range: `1 <= x <= 20`. Default: 10.
- **max_tokens** (integer) - Optional - The maximum total number of tokens of webpage content returned across all search results. Required range: `1 <= x <= 1000000`. Default: 25000.
- **search_domain_filter** (array of strings) - Optional - A list of domains/URLs to limit search results to. Maximum 20 domains. Maximum array length: `20`.
- **max_tokens_per_page** (integer) - Optional - Controls the maximum number of tokens retrieved from each webpage during search processing. Default: 2048.
- **country** (string) - Optional - Country code to filter search results by geographic location (e.g., 'US', 'GB', 'DE').
- **search_recency_filter** (enum) - Optional - Filters search results based on recency. Available options: `day`, `week`, `month`, `year`. Example: `"week"
- **search_after_date** (string) - Optional - Filters search results to only include content published after this date. Format should be %m/%d/%Y (e.g., '10/15/2025').
- **search_before_date** (string) - Optional - Filters search results to only include content published before this date. Format should be %m/%d/%Y (e.g., '10/16/2025').
- **last_updated_after_filter** (string) - Optional - Perplexity-Specific: Filters search results to only include content last updated after this date. Format should be %m/%d/%Y (e.g., '07/01/2025').
- **last_updated_before_filter** (string) - Optional - Perplexity-Specific: Filters search results to only include content last updated before this date. Format should be %m/%d/%Y.

### Request Example
```json
{
  "query": "latest AI developments 2024",
  "max_results": 10,
  "max_tokens": 25000,
  "search_domain_filter": [
    "science.org",
    "pnas.org",
    "cell.com"
  ],
  "max_tokens_per_page": 2048,
  "country": "US",
  "search_recency_filter": "week",
  "search_after_date": "10/15/2025",
  "search_before_date": "10/16/2025",
  "last_updated_after_filter": "07/01/2025",
  "last_updated_before_filter": "12/30/2025",
  "search_language_filter": [
    "en",
    "fr",
    "de"
  ]
}
```

### Response
#### Success Response (200)
- **results** (array) - An array of search result objects.
  - **title** (string) - The title of the search result.
  - **url** (string) - The URL of the search result.
  - **snippet** (string) - A brief snippet from the search result.
  - **date** (string) - The publication date of the content.
  - **last_updated** (string) - The last updated date of the content.

#### Response Example
```json
{
  "results": [
    {
      "title": "",
      "url": "",
      "snippet": "",
      "date": "2025-03-20",
      "last_updated": "2025-09-19"
    }
  ]
}
```

#### Authorizations
- **Bearer Token**: Required. Authorization header of the form `Bearer <YOUR_AUTH_TOKEN>`.
```

--------------------------------

### Chat Completions API with Image Attachments

Source: https://docs.perplexity.ai/guides/image-attachments

This endpoint allows you to send chat completions requests to the Perplexity AI API, including image attachments for multi-modal analysis. You can provide images either via a URL or as base64 encoded data.

```APIDOC
## POST /chat/completions

### Description
Sends a chat completion request to the Perplexity AI API, supporting multi-modal input including text and images. This endpoint is useful for visual question answering, context analysis, and multi-modal conversations.

### Method
POST

### Endpoint
https://api.perplexity.ai/chat/completions

### Parameters
#### Request Body
- **model** (string) - Required - The model to use for the chat completion (e.g., "sonar-pro").
- **stream** (boolean) - Optional - Whether to stream the response. Defaults to false.
- **messages** (array) - Required - An array of message objects representing the conversation history.
  - **role** (string) - Required - The role of the message sender (e.g., "user", "assistant").
  - **content** (array) - Required - An array of content parts for the message. Each part can be text or an image URL.
    - **type** (string) - Required - The type of content ("text" or "image_url").
    - **text** (string) - Required if type is "text" - The text content of the message.
    - **image_url** (object) - Required if type is "image_url" - An object containing the image URL.
      - **url** (string) - Required - The URL of the image or a data URI for base64 encoded image data.

### Request Example (Base64 Encoded Image)
```json
{
  "model": "sonar-pro",
  "stream": false,
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Can you describe this image?"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,$BASE64_ENCODED_IMAGE"
          }
        }
      ]
    }
  ]
}
```

### Request Example (Image URL)
```json
{
  "model": "sonar-pro",
  "stream": false,
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Can you describe this image?"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
          }
        }
      ]
    }
  ]
}
```

### Response
#### Success Response (200)
- **id** (string) - Unique identifier for the response.
- **model** (string) - The model used for the completion.
- **choices** (array) - An array of completion choices.
  - **message** (object) - The message object containing the assistant's response.
    - **role** (string) - Role of the message sender (assistant).
    - **content** (string) - The text content of the assistant's response.
- **usage** (object) - Information about token usage.
  - **prompt_tokens** (integer) - Number of tokens in the prompt.
  - **completion_tokens** (integer) - Number of tokens in the completion.
  - **total_tokens** (integer) - Total number of tokens used.

#### Response Example
```json
{
  "id": "chatcmpl-12345",
  "model": "sonar-pro",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "This is an image of a nature boardwalk in Madison, Wisconsin."
      }
    }
  ],
  "usage": {
    "prompt_tokens": 150,
    "completion_tokens": 20,
    "total_tokens": 170
  }
}
```
```

--------------------------------

### Perplexity AI Search API - Multi-Query Search

Source: https://docs.perplexity.ai/guides/search-quickstart

Enables users to execute multiple related queries in a single request for more comprehensive research.

```APIDOC
## POST /search (Multi-Query)

### Description
Executes multiple related queries in a single request for comprehensive research. The API returns results for each query submitted.

### Method
POST

### Endpoint
/search

### Parameters
#### Query Parameters
- **query** (array of strings) - Required - A list of search queries to execute.
- **max_results** (integer) - Optional - The maximum number of results to return for each query.

### Request Example
```python
from perplexity import Perplexity
client = Perplexity()
search = client.search.create(
  query=[
    "artificial intelligence trends 2024",
    "machine learning breakthroughs recent",
    "AI applications in healthcare"
  ],
  max_results=5
)
```

### Response
#### Success Response (200)
- **results** (object) - An object where keys are query indices and values are lists of search results for each query.

#### Response Example
```json
{
  "results": {
    "0": [
      {
        "title": "AI Trends 2024",
        "url": "http://example-ai.com",
        "snippet": "Key trends in artificial intelligence for 2024."
      }
    ],
    "1": [
      {
        "title": "Recent ML Breakthroughs",
        "url": "http://example-ml.com",
        "snippet": "Latest advancements in machine learning."
      }
    ],
    "2": [
      {
        "title": "AI in Healthcare Applications",
        "url": "http://example-health.com",
        "snippet": "How AI is being used in the healthcare sector."
      }
    ]
  }
}
```
```

--------------------------------

### Chat Completions API Response Structure (JSON)

Source: https://docs.perplexity.ai/api-reference/chat-completions-post

This JSON object represents a successful response from the Perplexity AI Chat Completions API. It includes metadata such as the model used, creation timestamp, token usage, and the generated message content. It also contains search results and potential video data if requested.

```json
{
  "id": "",
  "model": "",
  "created": 123,
  "usage": {
    "prompt_tokens": 123,
    "completion_tokens": 123,
    "total_tokens": 123,
    "search_context_size": "",
    "citation_tokens": 123,
    "num_search_queries": 123,
    "reasoning_tokens": 123
  },
  "object": "chat.completion",
  "choices": [
    {
      "index": 123,
      "message": {
        "content": "",
        "role": "system"
      },
      "finish_reason": "stop"
    }
  ],
  "search_results": [
    {
      "title": "",
      "url": "",
      "date": "2023-12-25"
    }
  ],
  "videos": [
    {
      "url": "",
      "thumbnail_url": "",
      "thumbnail_width": 123,
      "thumbnail_height": 123,
      "duration": 123
    }
  ]
}
```

--------------------------------

### Finding Breaking News with Search Recency Filter

Source: https://docs.perplexity.ai/guides/search-date-time-filters

Demonstrates how to use the `search_recency_filter` set to 'day' to retrieve the most recent breaking news on a specific topic. This is useful for staying updated on current events.

```python
response = client.search(
    query="breaking news technology",
    max_results=5,
    search_recency_filter="day"
)
```

--------------------------------

### Frequency Penalty for Repetition

Source: https://docs.perplexity.ai/api-reference/chat-completions-post

Applies a penalty based on the frequency of prior token appearance, decreasing the likelihood of repetition. Values typically range from 0 to 2.0. OpenAI Compatible.

```text
frequency_penalty: number (0 <= x <= 2.0)
```

--------------------------------

### Filter Search Results by Last Update Date (After)

Source: https://docs.perplexity.ai/api-reference/chat-completions-post

Filters search results to include only content last updated after a specified date. Requires the date in MM/DD/YYYY format. Perplexity-Specific.

```text
last_updated_after_filter: string (format: MM/DD/YYYY)
```

--------------------------------

### Response Randomness Control (Temperature)

Source: https://docs.perplexity.ai/api-reference/chat-completions-post

Determines the randomness or creativity of the output. Values range from 0 to 2. Lower values yield deterministic results, suitable for factual retrieval, while higher values produce more creative and varied outputs.

```text
temperature: number (0 <= x < 2)
```

--------------------------------

### Filter by Publication Date Range (cURL)

Source: https://docs.perplexity.ai/guides/search-date-time-filters

This cURL command illustrates how to apply publication date filters, `search_after_date` and `search_before_date`, to restrict search results to a specific date range.

```bash
curl -X POST "https://api.perplexity.ai/chat/completions" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "perpleximax",
       "messages": [
         {"role": "user", "content": "What are the latest advancements in AI?"}
       ],
       "search_parameters": {
         "search_after_date": "3/1/2025",
         "search_before_date": "3/5/2025"
       }
     }'
```