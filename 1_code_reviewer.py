from agents import Agent, Runner, InputGuardrail, OutputGuardrail, GuardrailFunctionOutput
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
import asyncio
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

class CodeReviewOutput(BaseModel):
    is_code: bool
    language: str
    reasoning: str

code_analyzer = Agent(
    name="Code Analyzer",
    instructions="You analyze code to determine if it needs review and identify its language",
    model="gpt-4o-mini",
    output_type=CodeReviewOutput
)

python_reviewer = Agent(
    name="Python Reviewer",
    handoff_description="Specialist agent for Python code review",
    instructions="You review Python code for best practices, potential bugs, and improvements. Provide detailed feedback.",
)

javascript_reviewer = Agent(
    name="JavaScript Reviewer",
    handoff_description="Specialist agent for JavaScript code review",
    instructions="You review JavaScript code for best practices, potential bugs, and improvements. Provide detailed feedback.",
)

async def code_guardrail(ctx, agent, input_data):
    result = await Runner.run(code_analyzer, input_data, context=ctx.context)
    final_output = result.final_output_as(CodeReviewOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        continue_execution=final_output.is_code
    )

triage_agent = Agent(
    name="Code Review Triage",
    instructions="You determine which code reviewer to use based on the programming language",
    handoffs=[python_reviewer, javascript_reviewer],
    input_guardrails=[
        InputGuardrail(guardrail_function=code_guardrail),
    ],
)

async def main():
    result = await Runner.run(triage_agent, "def example(): return 'Hello World'")
    return result.final_output

if __name__ == "__main__":
    asyncio.run(main()) 