import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, GuardrailFunctionOutput
from agents.run import RunConfig
import asyncio
from pydantic import BaseModel

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

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


class test_model(BaseModel):
    is_math:bool
    is_philosophy:bool
    is_other:bool
    reason:str

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="If the user question about math, you should use this agent",
    instructions="You are a math tutor that can answer about math problems",
)

philosophy_tutor_agent = Agent(
    name="Philosophy Tutor",
    handoff_description="If the use asks about philosopy, you should use this agent",
    instructions="You are a philosphy tutor that can answer about philosophy questions",
)

others_agent = Agent(
    name="Others Tutor",
    handoff_description="If the user question is not about math or philosophy, you should use this agent",
    instructions="""You have to respond the the user in formal way that this model can't
      respond to questions other then math and philosophy. you can use other models."""
)

guardrail_agent = Agent(
    name="Guardrail Agent",
    instructions="You have to check the user question and assign the user to appropriate agent",
    output_type=test_model
)

async def guardrail_agent_process(ctx, input_data, agent):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_outputas(test_model)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggerd=not final_output.is_other
    )


triage_agent = Agent(
    name="Triage Agent",
    instructions="You are a helpful assistant that can triage the user's question to the appropriate agent",
    handoffs=[math_tutor_agent, philosophy_tutor_agent, others_agent]
)


async def main():
    result = await Runner.run(triage_agent, "explain ch4 bonds.")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())