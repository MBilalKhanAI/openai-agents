from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from pydantic import BaseModel
import asyncio
from dotenv import load_dotenv
from agents import set_default_openai_key
import os

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)

class TranslationOutput(BaseModel):
    needs_translation: bool
    source_language: str
    target_language: str
    reasoning: str

language_analyzer = Agent(
    name="Language Analyzer",
    instructions="You analyze text to determine if it needs translation and identify its language",
    output_type=TranslationOutput
)

english_translator = Agent(
    name="English Translator",
    handoff_description="Specialist agent for English translation",
    instructions="You translate text to English, maintaining the original meaning and context."
)

spanish_translator = Agent(
    name="Spanish Translator",
    handoff_description="Specialist agent for Spanish translation",
    instructions="You translate text to Spanish, maintaining the original meaning and context."
)

async def translation_guardrail(ctx, agent, input_data):
    result = await Runner.run(language_analyzer, input_data, context=ctx.context)
    final_output = result.final_output_as(TranslationOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.needs_translation
    )

triage_agent = Agent(
    name="Translation Triage",
    instructions="You determine which translator to use based on the source and target languages",
    handoffs=[english_translator, spanish_translator],
    input_guardrails=[
        InputGuardrail(guardrail_function=translation_guardrail),
    ]
)

async def main():
    # Example 1: English to Spanish translation
    result = await Runner.run(triage_agent, "Translate this to Spanish: Hello, how are you today?")
    print("English to Spanish translation result:", result.final_output)
    
    # Example 2: Spanish to English translation
    result = await Runner.run(triage_agent, "Translate this to English: Hola, ¿cómo estás hoy?")
    print("Spanish to English translation result:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main()) 