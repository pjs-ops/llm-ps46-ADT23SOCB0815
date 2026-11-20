
# ✨ TaskWise AI — AI-Powered To-Do List Generator

### GenAI Mini Project | Problem Statement 46 | Roll No. 46

TaskWise AI is an AI-powered productivity application that transforms messy, unstructured notes into a clear, organised, and prioritised to-do list with deadlines.

Powered by the **Groq LLM API**, the application automatically identifies actionable tasks, assigns priorities, interprets deadlines, and allows users to track their progress through a beautiful, pastel-themed Streamlit interface.

---

## 🎯 Problem Statement

People often write tasks as scattered thoughts, reminders, or long paragraphs, making it difficult to organise and prioritise their responsibilities.

The objective of this project is to develop an AI-powered application that converts free-text notes into a structured to-do list containing:

- Task descriptions
- Priority levels (High, Medium, Low)
- Deadlines
- Task completion status

The application uses a Large Language Model (LLM) to understand natural language and extract meaningful tasks.

---

## 🌟 Key Features

### 🤖 AI-Powered Task Extraction
- Converts unstructured notes into actionable tasks.
- Uses the Groq LLM API for natural language understanding.
- Handles multiple tasks written in a single paragraph.

### 🚦 Intelligent Task Prioritisation
- Automatically assigns High, Medium, or Low priority.
- Identifies urgent tasks and important deadlines.
- Sorts tasks according to their priority.

### 📅 Smart Deadline Detection
- Understands expressions such as "today", "tomorrow", and "next Friday".
- Converts relative deadlines into calendar dates.
- Handles tasks without specified deadlines.

### ✅ Interactive To-Do List
- Displays individual tasks with checkboxes.
- Allows users to mark tasks as completed.
- Updates completion statistics and progress indicators.

### 📊 Productivity Dashboard
Displays:
- Total tasks
- Completed tasks
- Pending tasks
- High-priority tasks
- Overall completion progress

### 📥 CSV Export
- Downloads the generated to-do list as a CSV file.
- Allows users to save their task data for future reference.

### 🎨 Modern User Interface
- Pastel blue, beige, and soft yellow theme.
- Rounded cards and visually distinct priority badges.
- Sample input buttons for quick testing.
- Sidebar for API configuration and project information.

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| Programming Language | Python |
| Frontend / UI | Streamlit |
| LLM API | Groq API |
| AI Model | openai/gpt-oss-120b |
| API Integration | Groq Python SDK |
| Data Processing | Pandas |
| Environment Variables | python-dotenv |
| Version Control | Git & GitHub |

---

## ⚙️ How the Application Works

The application follows a simple AI-powered workflow:

```text
          USER INPUT
              |
              v
    Unstructured Text Notes
              |
              v
       Streamlit Interface
              |
              v
       Prompt Construction
              |
              v
          Groq LLM API
              |
              v
      Structured JSON Output
              |
              v
     Task Extraction & Validation
              |
              v
      Priority-Based Sorting
              |
              v
       Interactive To-Do List
              |
              v
      Progress Tracking & CSV
```

### Step-by-Step Explanation

1. The user enters messy notes into the Streamlit text area.
2. The application constructs a prompt containing the notes and current date.
3. The prompt is sent to the Groq LLM API.
4. The AI identifies individual tasks, priorities, and deadlines.
5. The model returns structured JSON data.
6. Python processes and validates the response.
7. Tasks are organised by priority.
8. Streamlit displays the generated to-do list.
9. Users can mark tasks as completed and download them as CSV.

---

## 📂 Project Structure

```text
PS46_ToDo_From_Text/
│
├── app.py
│   # Main Streamlit application
│
├── requirements.txt
│   # Python dependencies
│
├── README.md
│   # Project documentation
│
├── TEST_CASES.md
│   # Sample test inputs
│
├── .gitignore
│   # Excludes sensitive files
│
└── .streamlit/
    └── config.toml
        # Streamlit theme configuration
```

**Note:** The `.env` file containing the API key must never be uploaded to GitHub.

---

## 🚀 Installation and Setup

### Prerequisites

Ensure you have:

- Python 3.10 or later
- VS Code or another Python IDE
- Internet connection
- Groq API key

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Replace the placeholders with your GitHub username and repository name.

### Step 2: Install Dependencies

Open the terminal and execute:

```bash
python -m pip install -r requirements.txt
```

### Step 3: Configure Groq API Key

Get your API key from:

https://console.groq.com/keys

Create a `.env` file in the project directory.

Add:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Alternatively, enter the Groq API key through the application's sidebar.

**Important:** Never expose your API key publicly.

### Step 4: Run the Application

Execute:

```bash
python -m streamlit run app.py
```

Open:

http://localhost:8501

The TaskWise AI application should now be accessible in your browser.

---

## 📝 Example Input

```text
I need to submit my GenAI project report by Sunday.
Finish my Python assignment tomorrow.
Call my project guide urgently today.
Buy groceries this weekend.
Clean my study table whenever I have free time.
```

### Expected Output

| Task | Priority | Deadline |
|------|----------|----------|
| Call project guide | High | Today |
| Submit GenAI project report | High | Sunday |
| Finish Python assignment | Medium | Tomorrow |
| Buy groceries | Medium | This weekend |
| Clean study table | Low | Not specified |

The application interprets relative deadlines according to the current date.

---

## 🧠 LLM Integration

TaskWise AI uses the Groq API with the `openai/gpt-oss-120b` model.

The LLM performs three main operations:

**1. Task Extraction**

Identifies actionable tasks from natural-language input.

**2. Priority Classification**

Classifies tasks into:
- High
- Medium
- Low

**3. Deadline Interpretation**

Extracts explicitly mentioned dates and interprets relative deadlines.

### Example JSON Output

```json
{
  "tasks": [
    {
      "task": "Submit project report",
      "priority": "High",
      "deadline": "2026-11-22"
    },
    {
      "task": "Organise study notes",
      "priority": "Low",
      "deadline": "Not specified"
    }
  ]
}
```

Python processes the generated JSON and displays the information in an interactive task list.

---

## 🧪 Testing

The application can be tested using the following scenarios:

| Test Case | Input Type | Expected Result |
|-----------|------------|-----------------|
| TC01 | Simple task list | Individual tasks extracted |
| TC02 | Multiple deadlines | Dates interpreted correctly |
| TC03 | Urgent tasks | High priority assigned |
| TC04 | Tasks without deadlines | No deadline invented |
| TC05 | Mixed college and personal tasks | Tasks organised correctly |
| TC06 | Empty input | Appropriate validation message |
| TC07 | Checkbox interaction | Completion progress updated |
| TC08 | CSV download | Generated tasks exported |

### Sample Test Case

```text
I urgently need to submit my AI mini project by November 22.
Tomorrow I need to revise Python for two hours.
Finish my SQL assignment by Monday.
Email my project mentor today.
Buy groceries sometime this weekend.
Update my resume by November 25.
Watch two machine learning lectures next week.
Clean my room whenever I have time.
```

The AI should identify the individual tasks and organise them according to their priorities and deadlines.

---

## 💡 Advantages

- Saves time spent manually organising tasks.
- Understands everyday natural language.
- Automatically prioritises responsibilities.
- Helps students and professionals manage deadlines.
- Provides an interactive and easy-to-use interface.
- Supports task export for future reference.

---

## ⚠️ Limitations

- Requires an active internet connection.
- Depends on the availability of the Groq API.
- AI-generated priorities may occasionally require manual verification.
- Ambiguous deadlines may be interpreted incorrectly.
- Very long inputs may occasionally cause response-format errors.
- Task progress is stored within the current Streamlit session rather than a permanent database.

---

## 🔮 Future Scope

Future improvements could include:

1. User authentication and personalised dashboards.
2. Permanent task storage using a database.
3. Google Calendar integration.
4. Email and push notifications for deadlines.
5. Multilingual task extraction.
6. AI-powered scheduling recommendations.
7. Task editing and manual priority adjustment.
8. Improved processing of long inputs using chunking and retries.

---

## 🎓 Academic Information

| Field | Details |
|-------|---------|
| Project Title | TaskWise AI |
| Problem Statement No. | 46 |
| Roll Number | 46 |
| Category | Career & Productivity |
| Course | GenAI Mini Project |
| Project Type | LLM-Based Mini Project |

---

## 🔐 Security

The application requires a Groq API key.

For security:

- Store API keys in environment variables.
- Never hardcode API keys in source code.
- Add `.env` to `.gitignore`.
- Never upload credentials to GitHub.
- Revoke and replace any accidentally exposed API keys.

---

## 📌 Conclusion

TaskWise AI demonstrates how Large Language Models can be integrated into everyday productivity applications.

By transforming unstructured notes into prioritised tasks with deadlines, the application simplifies task management and helps users organise their responsibilities efficiently.

The project demonstrates practical applications of **Generative AI, Natural Language Processing, API Integration, JSON Processing, and Streamlit-based Web Development**.

---

### ✨ TaskWise AI
*Turning messy thoughts into organised action.*
