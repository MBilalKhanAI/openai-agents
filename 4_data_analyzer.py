from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from pydantic import BaseModel
import asyncio
from dotenv import load_dotenv
from agents import set_default_openai_key
import os

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)

class DataAnalysisOutput(BaseModel):
    is_data: bool
    data_type: str
    analysis_required: str
    reasoning: str

data_analyzer = Agent(
    name="Data Type Analyzer",
    instructions="You analyze input to determine if it contains data that needs analysis and identify its type",
    output_type=DataAnalysisOutput
)

text_analyzer = Agent(
    name="Text Analyzer",
    handoff_description="Specialist agent for text data analysis",
    instructions="You analyze text data to extract insights, patterns, and key information."
)

numeric_analyzer = Agent(
    name="Numeric Analyzer",
    handoff_description="Specialist agent for numeric data analysis",
    instructions="You analyze numeric data to provide statistical insights and identify trends."
)

async def data_guardrail(ctx, agent, input_data):
    result = await Runner.run(data_analyzer, input_data, context=ctx.context)
    final_output = result.final_output_as(DataAnalysisOutput)
    # Only trigger tripwire if it's not data at all
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=False  # Allow both text and numeric analysis
    )

triage_agent = Agent(
    name="Data Analysis Triage",
    instructions="You determine which analyzer to use based on the data type and analysis requirements",
    handoffs=[text_analyzer, numeric_analyzer],
    input_guardrails=[
        InputGuardrail(guardrail_function=data_guardrail),
    ]
)

async def main():
    # Example 1: Numeric data analysis
    result = await Runner.run(triage_agent, "Analyze this numeric data: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10")
    print("Numeric data analysis result:", result.final_output)
    
    # Example 2: Text data analysis
    result = await Runner.run(triage_agent, "Analyze this text: The quick brown fox jumps over the lazy dog")
    print("Text data analysis result:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main()) 