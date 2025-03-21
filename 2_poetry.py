from agents import Agent, Runner
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables
load_dotenv()

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

agent = Agent(
    name="Poem Writer",
    instructions="You are a poet. you are responsible for writing poems in all languages",
    model="gpt-4o-mini"
)

result = Runner.run_sync(agent, "Write an arabic poem about patriotism")

print(result.final_output)



