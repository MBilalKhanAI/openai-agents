from agents import Agent, Runner, InputGuardrail, OutputGuardrail, GuardrailFunctionOutput
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
import asyncio
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

class TranslationOutput(BaseModel):
    is_text: bool
    language: str
    reasoning: str

text_analyzer = Agent(
    name="Text Analyzer",
    instructions="You analyze text to determine if it needs translation and identify its language",
    model="gpt-4o-mini",
    output_type=TranslationOutput
)

english_translator = Agent(
    name="English Translator",
    handoff_description="Specialist agent for English translations",
    instructions="You translate text to and from English, maintaining the original meaning and style.",
)

spanish_translator = Agent(
    name="Spanish Translator",
    handoff_description="Specialist agent for Spanish translations",
    instructions="You translate text to and from Spanish, maintaining the original meaning and style.",
)

async def translation_guardrail(ctx, agent, input_data):
    result = await Runner.run(text_analyzer, input_data, context=ctx.context)
    final_output = result.final_output_as(TranslationOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        continue_execution=final_output.is_text
    )

triage_agent = Agent(
    name="Translation Triage",
    instructions="You determine which translator to use based on the language",
    handoffs=[english_translator, spanish_translator],
    input_guardrails=[
        InputGuardrail(guardrail_function=translation_guardrail),
    ],
)

async def main():
    result = await Runner.run(triage_agent, "Hello, how are you today?")
    return result.final_output

if __name__ == "__main__":
    asyncio.run(main()) 