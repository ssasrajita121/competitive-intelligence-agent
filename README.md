\# 🔍 Competitive Intelligence + LinkedIn Content Generator



AI-powered tool for researching topics and generating LinkedIn posts.



\## Features



\- 🔍 \*\*Multi-source Research\*\*: Automatically gathers news and web data

\- 📊 \*\*AI Analysis\*\*: Summarizes findings and extracts insights

\- ✍️ \*\*Content Generation\*\*: Creates LinkedIn posts in 5 different styles

\- 🎯 \*\*User-Controlled\*\*: You decide what to research and post

\- 🔄 \*\*Regeneration\*\*: Improve and refine posts with one click



\## Tech Stack



\- \*\*Python 3.11\*\*

\- \*\*Streamlit\*\* - Web interface

\- \*\*OpenAI GPT\*\* - AI generation

\- \*\*Multi-agent Architecture\*\* - Research + Content agents

\- \*\*RAG\*\* - Coming in v2.0!



\## Installation



1\. Clone the repository:

```bash

git clone https://github.com/YOUR-USERNAME/competitive-intelligence-agent.git

cd competitive-intelligence-agent

```



2\. Create virtual environment:

```bash

py -3.11 -m venv venv

venv\\Scripts\\activate  # Windows

```



3\. Install dependencies:

```bash

pip install -r requirements.txt

```



4\. Create `.env` file with your API keys:

```

OPENAI\_API\_KEY=your-key-here

NEWS\_API\_KEY=your-key-here (optional)

```



5\. Run the app:

```bash

streamlit run app.py

```



\## Usage



1\. \*\*Research\*\*: Enter a topic and click "Start Research"

2\. \*\*Choose Angle\*\*: Select what aspect to write about

3\. \*\*Generate Post\*\*: Pick a style and generate LinkedIn content

4\. \*\*Review \& Edit\*\*: Refine the post before posting manually



\## Project Structure

```

competitive-intelligence-agent/

├── agents/           # AI agents (research, content)

├── config/          # Configuration settings

├── utils/           # Helper functions and prompts

├── app.py           # Main Streamlit app

└── requirements.txt

```





