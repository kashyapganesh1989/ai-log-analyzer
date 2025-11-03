# AI Log Analyzer
AI Log Analyzer is a smart, Streamlit-based tool that automatically reads and analyzes applications/batch logs using OpenAI’s GPT models.
It identifies issues, probable causes, suggested resolutions, and severity — helping developers troubleshoot faster and more effectively.

Features:
✅ Upload log files or analyze logs from a folder path
✅ AI-powered detection of issues, causes, and resolutions
✅ Auto-classification of severity (Info, Warning, Error, Critical)
✅ Export results to CSV or JSON
✅ Clean and professional web UI (Streamlit)
✅ Secure handling of API keys using environment variables

Project Structure:

ai-log-analyzer/
│
├── app.py                  # Main Streamlit UI
├── .env                    # Your local environment variables (not uploaded)
├── .env.example            # Template for others to create their own .env
├── requirements.txt        # Python dependencies
├── utils/
│   ├── log_reader.py       # Reads and parses log files
│   ├── ai_helper.py        # Handles AI API calls and parsing
└── README.md               # Project documentation

Installation & Setup:
1. clone the project
git clone https://github.com/YOUR_USERNAME/ai-log-analyzer.git
cd ai-log-analyzer
2.  activate the project
Create and activate a virtual environment
3. install the requirements
pip install -r requirements.txt
4.Configure environment variables
OPENAI_API_KEY=your_openai_api_key_here
5. Run the app:
6. streamlit run app.py



