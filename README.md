# OpenAI Agents Collection

A collection of specialized AI agents built using OpenAI's API for various tasks.

## Agents

1. **Code Reviewer** (`1_code_reviewer.py`)
   - Reviews Python and JavaScript code
   - Provides detailed feedback on code quality, style, and potential improvements
   - Includes security and best practices recommendations

2. **Document Translator** (`2_document_translator.py`)
   - Translates documents between English and Spanish
   - Maintains document formatting and structure
   - Preserves technical terminology

3. **Content Generator** (`3_content_generator.py`)
   - Generates blog posts and social media content
   - Adapts tone and style based on target audience
   - Includes SEO optimization suggestions

4. **Data Analyzer** (`4_data_analyzer.py`)
   - Analyzes both text and numeric data
   - Provides statistical insights and patterns
   - Includes trend analysis and key information extraction

5. **Calendar Event Extractor** (`5_calendar_extractor.py`)
   - Extracts calendar events from text
   - Supports multiple date formats
   - Identifies event details including:
     - Event name
     - Date (in YYYY-MM-DD format)
     - Participants
     - Location
     - Description
   - Includes date validation and formatting

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Each agent can be run independently:
```bash
python 1_code_reviewer.py
python 2_document_translator.py
python 3_content_generator.py
python 4_data_analyzer.py
python 5_calendar_extractor.py
```

## Requirements

- Python 3.7+
- OpenAI API key
- Dependencies listed in requirements.txt

## License

MIT License 
