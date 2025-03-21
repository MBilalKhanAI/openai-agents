# OpenAI Agents Examples

A collection of OpenAI agent implementations demonstrating different use cases and capabilities. Each example showcases specialized agents working together through a triage system.

## Examples

1. `1_code_reviewer.py` - A code review system that analyzes and provides feedback for Python and JavaScript code
2. `2_document_translator.py` - A translation system that handles English and Spanish translations
3. `3_content_generator.py` - A content creation system for blog posts and social media content
4. `4_data_analyzer.py` - A data analysis system that processes text and numeric data

## Architecture

Each example implements:
- Input validation through guardrails
- Analysis agent for task classification
- Specialized agents for specific tasks
- Triage system for routing tasks
- Async execution for better performance

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/MBilalKhanAI/openai-agents.git
   cd openai-agents
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key in a `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run any example using:
```bash
python 1_code_reviewer.py      # For code review
python 2_document_translator.py # For translations
python 3_content_generator.py   # For content generation
python 4_data_analyzer.py      # For data analysis
```

## Requirements

- Python 3.7+
- openai-agents>=0.0.4
- python-dotenv>=1.0.1
- pydantic
- asyncio

## Contributing

Feel free to submit issues and enhancement requests! 
