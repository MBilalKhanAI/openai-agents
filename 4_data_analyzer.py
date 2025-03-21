from agents import Agent, Runner, InputGuardrail, OutputGuardrail, GuardrailFunctionOutput
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
import asyncio
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    
class DataOutput(BaseModel):
    is_data: bool
    data_type: str
    reasoning: str

data_analyzer = Agent(
    name="Data Analyzer",
    instructions="You analyze input to determine if it contains data that needs processing",
    model="gpt-4o-mini",
    output_type=DataOutput
)

text_analyzer = Agent(
    name="Text Data Analyzer",
    handoff_description="Specialist agent for analyzing text data",
    instructions="You analyze text data to extract insights, sentiment, and key information.",
)

numeric_analyzer = Agent(
    name="Numeric Data Analyzer",
    handoff_description="Specialist agent for analyzing numeric data",
    instructions="You analyze numeric data to calculate statistics, trends, and patterns.",
)

async def data_guardrail(ctx, agent, input_data):
    result = await Runner.run(data_analyzer, input_data, context=ctx.context)
    final_output = result.final_output_as(DataOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        continue_execution=final_output.is_data
    )

triage_agent = Agent(
    name="Data Analysis Triage",
    instructions="You determine which analyzer to use based on the data type",
    handoffs=[text_analyzer, numeric_analyzer],
    input_guardrails=[
        InputGuardrail(guardrail_function=data_guardrail),
    ],
)

async def main():
    result = await Runner.run(triage_agent, "Analyze this data: 1, 2, 3, 4, 5")
    return result.final_output

if __name__ == "__main__":
    asyncio.run(main()) 