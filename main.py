from dotenv import load_dotenv
from state import SummaryState, SummaryStateInput, SummaryStateOutput
from final_summary import final_summary
from reflect import reflect_on_summary
from research_topic import research_topic
from web_search import web_search
from summarize_sources import summarize_sources
from langgraph.graph import StateGraph, START, END
from typing import Literal

load_dotenv()

def route_research(state: SummaryState) -> Literal["finalize_summary", "web_research"]:
    """ Route the research based on the follow-up query """
    if state.research_loop_count <= 3:
        return "web_research"
    else:
        return "finalize_summary"


builder = StateGraph(SummaryState, input=SummaryStateInput, output=SummaryStateOutput)
builder.add_node("generate_query", research_topic)
builder.add_node("web_research", web_search)
builder.add_node("summarize_sources", summarize_sources)
builder.add_node("reflect_on_summary", reflect_on_summary)
builder.add_node("finalize_summary", final_summary)

builder.add_edge(START, "generate_query")
builder.add_edge("generate_query", "web_research")
builder.add_edge("web_research", "summarize_sources")
builder.add_edge("summarize_sources", "reflect_on_summary")
builder.add_conditional_edges("reflect_on_summary", route_research)
builder.add_edge("finalize_summary", END)

graph = builder.compile()
graph.get_graph().draw_mermaid_png(output_file_path="output.png")

if __name__ == "__main__":
        input_data = {"research_topic" : "Deep research report on Hinduism and Vedas"}

        res = graph.invoke(input_data)
        print(res)


