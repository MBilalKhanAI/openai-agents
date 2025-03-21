from agents import Agent, Runner, ModelSettings, function_tool
from dotenv import load_dotenv
from agents import set_default_openai_key
import asyncio
import os

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(api_key)

@function_tool
def weather_tool(city:str) -> str:
    """Get the weather in a given city"""
    return f"The weather in {city} is sunny and 70 degrees"

weather_haiku_agent = Agent(
    name="Weather Haiku Agent",
    instructions="""You are a poet who writes haikus about the weather.
    You are given a city and you need to write a haiku about the weather in that city.
    """,
    tools=[weather_tool],
)
async def main():
    result = await Runner.run(weather_haiku_agent, "what is weather in tokyo?")
    print("weather in tokyo is", result.final_output)

if __name__ == "__main__":
    asyncio.run(main()) 







    
