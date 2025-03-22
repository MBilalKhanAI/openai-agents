# OpenAI Agents Examples

This repository contains examples of OpenAI agents using the `openai-agents` package. Each example demonstrates a different use case for AI agents with specialized roles and capabilities.

## Examples

### 1. Code Reviewer (`1_code_reviewer.py`)
A specialized agent system for code review that:
- Analyzes code to determine if it needs review
- Identifies the programming language
- Routes code to specialized reviewers (Python/JavaScript)
- Provides detailed feedback on code quality and improvements
- Uses guardrails to ensure proper code analysis
- Implements triage system for language-specific reviews

### 2. Document Translator (`2_document_translator.py`)
A translation system that:
- Analyzes text to determine if it needs translation
- Identifies the source language
- Routes text to specialized translators (English/Spanish)
- Maintains original meaning and style in translations
- Uses guardrails to validate text input
- Implements triage system for language-specific translations

### 3. Content Generator (`3_content_generator.py`)
A content creation system that:
- Analyzes content requests to determine the type needed
- Routes requests to specialized content creators
- Generates blog posts and social media content
- Follows platform-specific best practices
- Uses guardrails to validate content requests
- Implements triage system for content type routing

### 4. Data Analyzer (`4_data_analyzer.py`)
A data analysis system that:
- Analyzes input to determine if it contains data for processing
- Identifies the type of data (text/numeric)
- Routes data to specialized analyzers
- Provides insights and analysis based on data type
- Uses guardrails to validate data input
- Implements triage system for data type routing

## Architecture

Each example follows a consistent architecture:
1. Input validation through guardrails
2. Analysis agent for task classification
3. Specialized agents for specific tasks
4. Triage system for routing tasks
5. Async execution for better performance

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

Each example can be run independently:
```bash
python 1_code_reviewer.py
python 2_document_translator.py
python 3_content_generator.py
python 4_data_analyzer.py
```

## Requirements

- Python 3.7+
- OpenAI API key
- Dependencies listed in `requirements.txt`:
  - openai-agents
  - python-dotenv
  - pydantic
  - asyncio

## Contributing

Feel free to submit issues and enhancement requests! 