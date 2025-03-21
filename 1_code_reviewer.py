from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from pydantic import BaseModel
import asyncio
from dotenv import load_dotenv
from agents import set_default_openai_key
import os

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)

class CodeReviewOutput(BaseModel):
    is_code: bool
    language: str
    reasoning: str

code_analyzer = Agent(
    name="Code Analyzer",
    instructions="You analyze code to determine if it needs review and identify its language",
    output_type=CodeReviewOutput
)

python_reviewer = Agent(
    name="Python Reviewer",
    handoff_description="Specialist agent for Python code review",
    instructions="You review Python code for best practices, potential bugs, and improvements. Provide detailed feedback."
)

javascript_reviewer = Agent(
    name="JavaScript Reviewer",
    handoff_description="Specialist agent for JavaScript code review",
    instructions="You review JavaScript code for best practices, potential bugs, and improvements. Provide detailed feedback."
)

async def code_guardrail(ctx, agent, input_data):
    result = await Runner.run(code_analyzer, input_data, context=ctx.context)
    final_output = result.final_output_as(CodeReviewOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_code
    )

triage_agent = Agent(
    name="Code Review Triage",
    instructions="You determine which code reviewer to use based on the programming language",
    handoffs=[python_reviewer, javascript_reviewer],
    input_guardrails=[
        InputGuardrail(guardrail_function=code_guardrail),
    ]
)

async def main():
    # Example 1: Python code review
    result = await Runner.run(triage_agent, """
def example():
    return 'Hello World'
""")
    print("Python code review result:", result.final_output)
    
    # Example 2: JavaScript code review
    result = await Runner.run(triage_agent, """
function example() {
    return 'Hello World';
}
""")
    print("JavaScript code review result:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main()) 