from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from state import SummaryState


load_dotenv()

def final_summary(state: SummaryState) :
    """ Generate a summary based on the gathered information """
    print("---GENERATING FINAL SUMMARY---")
    sources_gathered = state.sources_gathered
    all_sources = "\n".join(source for source in sources_gathered)
    running_summary = state.running_summary
    running_summary = f"## Summary\n\n{running_summary}\n\n ### Sources:\n{all_sources}"

    return {"running_summary": running_summary}

if __name__ == "__main__":
    final_summary(state={"sources_gathered": ["https://www.example.com/1", "https://www.example.com/2"], "running_summary": "This is a summary of the gathered information."})