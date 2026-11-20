# TaskWise AI — To-Do List from Text

**Problem Statement 46 · Roll No. 46**

Convert messy free-text notes into an AI-generated task list containing **task**, **priority**, and **deadline**. Tasks are sorted High → Medium → Low and displayed with interactive checkboxes.

## Tech stack
Python · Streamlit · Groq LLM API (`openai/gpt-oss-120b`) · Groq Python SDK / requests · pandas · python-dotenv

## Setup (Windows / VS Code)
1. Install Python 3.10+ and open this folder in VS Code.
2. Open the terminal and run: `python -m pip install -r requirements.txt`
3. Create a file named `.env` (copy `.env.example`) and replace the placeholder with your Groq key from https://console.groq.com/keys
4. Run: `python -m streamlit run app.py`
5. Open the local URL shown by Streamlit and enter notes.

**Security:** `.env` and any API keys must never be uploaded to GitHub or included in the submission ZIP.

## Example notes
> Submit the AI project report by Thursday. Finish Python homework tomorrow. Buy milk sometime this week. Call the project mentor urgently today.

## Core workflow
Pasted notes → prompt with current date → Groq API → JSON tasks → validated/priority-sorted list → checkboxes + CSV download.

## Test checklist (run and capture screenshots)
1. Several tasks with explicit deadlines
2. Casual notes with relative dates (tomorrow/Friday)
3. Notes without any deadlines
4. Mixed urgent and non-urgent tasks
5. Notes with no actionable tasks

## Limitations
LLMs can misinterpret ambiguous priorities/dates; users should verify important deadlines. API and internet access are required.

## Academic report
Complete the two-page procedure report after running the project and taking output screenshots. Describe your actual testing and challenges; do not claim tests you have not run.
"# llm-ps46-ADT23SOCB0815" 
