# OpenAI Agents Examples

A collection of OpenAI agent implementations demonstrating different use cases and capabilities.

## Examples

1. `1_homework.py` - A homework triage system that routes questions to appropriate subject experts
2. `2_poetry.py` - A poetry writing agent that generates poems in various languages
3. `3_streaming.py` - An example of streaming responses from an agent
4. `4_tools.py` - A demonstration of using tools with agents

## Setup

1. Clone the repository
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
python example_name.py
```

## Requirements

- Python 3.11+
- openai-agents>=0.0.4
- python-dotenv>=1.0.1
