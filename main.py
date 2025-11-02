from utils.log_reader import read_log_file
from utils.ai_helper import analyze_log_with_gpt

def main():
    print("=== AI Log Analyzer (OpenAI Version) ===")
    filepath = input("Enter log file path or folder: ").strip()

    print("\nReading logs...")
    log_data = read_log_file(filepath)

    print("\nAnalyzing logs with OpenAI GPT (may take a few seconds)...")
    analysis = analyze_log_with_gpt(log_data)

    print("\n=== Analysis Report ===")
    print(analysis)

if __name__ == "__main__":
    main()
