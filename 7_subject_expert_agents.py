from agents import Agent, Runner, OpenAIChatCompletionsModel, GuardrailFunctionOutput
from agents.run import RunConfig
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import AsyncOpenAI
import asyncio
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)



class first_model(BaseModel):
    is_astronomy:bool
    is_quantum_computing:bool
    is_artifical_intelligence:bool
    is_medicine:bool
    is_other:bool
    reason:str


astronomy_agent = Agent(
    name="Astronomy Agent",
    handoff_description="you are responsible for respone to a user's question about astronomy.",
    instructions="""You have to respond on astronomy related questions. your answer should be based on
    the facts and refrences. you should also provide the source of the information.""",
    )

quantum_computing_agent = Agent(
    name="Quantum Computing Agent",
    handoff_description="you are are responsible to responed to users question related to quantum computing",
    instructions="You are an expert in quantum computing. you answer should be based on latest and upcoming research and development in quantum computing",

)

artificial_intelligence_agent = Agent(
    name="Artificial Intelligence Agent",
    handoff_description="you are responsible for response to users question related to artificial intelligence",
    instructions="you an AI expert, you answer should be inovative"
)

medicine_agent = Agent(
    name="Medicine Agent",
    handoff_description="you are responsible for response to users question related to medicine",
    instructions="You are like a doctor, reply very carefully with great concern for the useer's health"
)

other_agent = Agent(
    name="Other Agent",
    handoff_description="you are responsible for response to users question related to other topics",  
    instructions="you are a generalist, you answer should be based on your knowledge and information from the internet"
)

guardrail_agent = Agent(
    name="Guardrail Agent",
    instructions="""
    you are responsible for checking the answer provided by the agents.
    """
)  

triage_agent = Agent(
    name="Triage Agent",
    instructions="You are a helpful assistant that can triage the user's question to the appropriate agent",
    handoffs=[astronomy_agent, quantum_computing_agent, artificial_intelligence_agent, medicine_agent, other_agent, guardrail_agent]
)

async def guardrail_function(input_data, ctx, agent):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(first_model)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggerd=not final_output.is_other
    )

async def main():
    result = await Runner.run(triage_agent, "What is quantum computing?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())




