from agents import Agent, Runner, InputGuardrail, OutputGuardrail, GuardrailFunctionOutput
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
import asyncio
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

class ContentOutput(BaseModel):
    is_content_request: bool
    content_type: str
    reasoning: str

content_analyzer = Agent(
    name="Content Analyzer",
    instructions="You analyze content requests to determine the type of content needed",
    model="gpt-4o-mini",
    output_type=ContentOutput
)

blog_writer = Agent(
    name="Blog Writer",
    handoff_description="Specialist agent for writing blog posts",
    instructions="You write engaging blog posts on various topics, following best practices for content creation.",
)

social_media_writer = Agent(
    name="Social Media Writer",
    handoff_description="Specialist agent for social media content",
    instructions="You create engaging social media posts that are optimized for different platforms.",
)

async def content_guardrail(ctx, agent, input_data):
    result = await Runner.run(content_analyzer, input_data, context=ctx.context)
    final_output = result.final_output_as(ContentOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        continue_execution=final_output.is_content_request
    )

triage_agent = Agent(
    name="Content Generation Triage",
    instructions="You determine which content creator to use based on the content type",
    handoffs=[blog_writer, social_media_writer],
    input_guardrails=[
        InputGuardrail(guardrail_function=content_guardrail),
    ],
)

async def main():
    result = await Runner.run(triage_agent, "Write a blog post about AI")
    return result.final_output

if __name__ == "__main__":
    asyncio.run(main()) 