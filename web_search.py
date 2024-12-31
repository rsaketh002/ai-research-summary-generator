# web_search.py

from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from state import SummaryState

load_dotenv()

def web_search(state: SummaryState):
    """Perform a web search and only pick the first new URL from the results."""
    print("---SEARCHING WEB---")

    research_query = state.research_query
    web_search_tool = TavilySearchResults(max_results=3)
    tavily_results = web_search_tool.invoke({"query": research_query})

    existing_urls = set(state.sources_gathered)
    new_result = None
    new_url = None

    # Iterate over each URL in order and stop when you find the first "new" one.
    for result in tavily_results:
        url = result["url"]
        if url not in existing_urls:
            new_result = result
            new_url = url
            break

    # If no new URL was found, just return the existing state (but increment the loop count).
    if not new_result:
        print("No new URLs found. All results are already in sources_gathered.")
        return {
            "web_research_results": state.web_research_results,
            "sources_gathered": state.sources_gathered,
            "research_loop_count": state.research_loop_count
        }

    # Join the content of the single new result
    joined_tavily_results = [
        new_result["content"]
    ]

    # Append the single new result to the state
    updated_web_research_results = joined_tavily_results
    updated_sources_gathered = [new_url]

    return {
        "web_research_results": updated_web_research_results,
        "sources_gathered": updated_sources_gathered,
        "research_loop_count": state.research_loop_count + 1
    }


if __name__ == "__main__":
    # Example usage:
    test_state = SummaryState(
        research_query="latest breakthroughs in artificial intelligence 2024",
        research_loop_count=0
    )
    new_state = web_search(test_state)
    print(new_state)