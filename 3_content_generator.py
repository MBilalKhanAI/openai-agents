from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from pydantic import BaseModel
import asyncio
from dotenv import load_dotenv
from agents import set_default_openai_key
import os

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
set_default_openai_key(openai_api_key)

class ContentRequestOutput(BaseModel):
    is_content_request: bool
    content_type: str
    topic: str
    reasoning: str

request_analyzer = Agent(
    name="Content Request Analyzer",
    instructions="You analyze requests to determine if they need content generation and identify the type",
    output_type=ContentRequestOutput
)

blog_writer = Agent(
    name="Blog Writer",
    handoff_description="Specialist agent for blog post writing",
    instructions="You write engaging and informative blog posts with proper structure and SEO optimization."
)

social_media_writer = Agent(
    name="Social Media Writer",
    handoff_description="Specialist agent for social media content",
    instructions="You write engaging and platform-appropriate social media posts with proper hashtags and formatting."
)

async def content_guardrail(ctx, agent, input_data):
    result = await Runner.run(request_analyzer, input_data, context=ctx.context)
    final_output = result.final_output_as(ContentRequestOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_content_request
    )

triage_agent = Agent(
    name="Content Generation Triage",
    instructions="You determine which content writer to use based on the content type and requirements",
    handoffs=[blog_writer, social_media_writer],
    input_guardrails=[
        InputGuardrail(guardrail_function=content_guardrail),
    ]
)

async def main():
    # Example 1: Blog post request
    result = await Runner.run(triage_agent, "Write a blog post about artificial intelligence trends")
    print("Blog post generation result:", result.final_output)
    
    # Example 2: Social media post request
    result = await Runner.run(triage_agent, "Create a social media post about the benefits of exercise")
    print("Social media post generation result:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main()) 