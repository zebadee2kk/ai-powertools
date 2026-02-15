import asyncio
import os
from dotenv import load_dotenv
from powertools.core.llm_router.router import LLMRouter
from powertools.integrations.llm.ollama import OllamaProvider
from powertools.integrations.llm.openai import OpenAIProvider

load_dotenv()

async def main():
    # 1. Initialize the router
    router = LLMRouter()
    
    # 2. Register providers
    ollama = OllamaProvider()
    openai = OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"))
    
    router.register_provider(ollama)
    router.register_provider(openai)
    
    # 3. Set default models
    router.set_defaults(
        local_model="mistral:7b",
        cloud_model="gpt-3.5-turbo"
    )
    
    print("--- Task 1: Low Complexity (should route to Local) ---")
    try:
        response = await router.route(
            task="Tell me a joke.",
            complexity=0.3
        )
        print(f"Response from {response.provider} ({response.model}):")
        print(f"Content: {response.content}")
        print(f"Latency: {response.latency_ms:.2f}ms")
    except Exception as e:
        print(f"Error Task 1: {e}")

    print("\n--- Task 2: High Complexity (should route to Cloud) ---")
    try:
        response = await router.route(
            task="Explain the quantum physics of black hole evaporation in detail.",
            complexity=0.8
        )
        print(f"Response from {response.provider} ({response.model}):")
        print(f"Content: {response.content[:100]}...")
        print(f"Latency: {response.latency_ms:.2f}ms")
    except Exception as e:
        print(f"Error Task 2: {e}")

if __name__ == "__main__":
    asyncio.run(main())
