# BRANDTONE

BRANDTONE is a tool that helps rewrite marketing text to match specific brand tones while enforcing formatting rules.

## Features

- Transform text to match different tones (formal, casual, playful, technical, etc.)
- Enforce formatting rules to maintain brand consistency
- Quality check for tone accuracy and grammar
- Export results in text or JSON format

## Setup

1. Clone the repository
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Create a `.env` file in the project root with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Running the Application

```
streamlit run app.py
```

## Usage

1. Enter your marketing text in the input field
2. Select your desired tone
3. Click "Convert" to transform the text
4. Review the result and export if desired

## Formatting Rules Enforced

- No all caps text
- Limited use of exclamation points
- Consistent bullet point formatting
- Other customizable formatting rules
