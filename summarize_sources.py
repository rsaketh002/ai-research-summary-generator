from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from state import SummaryState


load_dotenv()

summarizer_instructions="""Your goal is to generate a high-quality summary of the web search results.

When EXTENDING an existing summary:
1. Seamlessly integrate new information without repeating what's already covered
2. Maintain consistency with the existing content's style and depth
3. Only add new, non-redundant information
4. Ensure smooth transitions between existing and new content

When creating a NEW summary:
1. Highlight the most relevant information from each source
2. Provide a concise overview of the key points related to the report topic
3. Emphasize significant findings or insights
4. Ensure a coherent flow of information

In both cases:
- Focus on factual, objective information
- Maintain a consistent technical depth
- Avoid redundancy and repetition
- DO NOT use phrases like "based on the new results" or "according to additional sources"
- DO NOT add a preamble like "Here is an extended summary ..." Just directly output the summary.
- DO NOT add a References or Works Cited section.
"""

summarizer_instructions_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            summarizer_instructions
        ),
        (
            "user",
            "{instructions}"
        )
    ]
)

llm = ChatOpenAI(model="gpt-4o")

def summarize_sources(state: SummaryState) :
    """ Generate a summary of the web search results """
    print("---SUMMARIZING SOURCES---")
    web_search_results = state.web_research_results[-1]
    existing_summary = state.running_summary
    research_topic = state.research_topic

    if existing_summary is not None:
        instructions = (
            f"Extend the existing summary: {existing_summary}\n\n"
            f"Include new search results: {web_search_results} "
            f"That addresses the following topic: {research_topic}"
        )
        prompt = summarizer_instructions_prompt.format(instructions=instructions)
    else:
        instructions = (
            f"Generate a summary of these search results: {web_search_results} "
            f"That addresses the following topic: {research_topic}"
        )
        prompt = summarizer_instructions_prompt.format(instructions=instructions)

    result = llm.invoke(prompt)  # Pass the formatted prompt
    running_summary = result.content

    return {"running_summary": running_summary}

if __name__ == "__main__":
    summarize_sources(state={"research_topic": "Recent AI Advancements", "web_search_results": ["Top 10 AI Breakthroughs & Controversies of 2024 - Techopedia From Apple’s groundbreaking entry into generative AI to quantum computing breakthroughs, from specialized AI agents to landmark regulations, the year marked the transition from theoretical possibilities to practical realities that changed how we work, create, and solve problems. “The impact of organizations operating in the EU will likely depend on how the company is using an AI model and what risk category that use case falls under, as identified by the Act. When OpenAI launched the o1 model in September 2024, it introduced a fundamentally new approach to AI reasoning. While Apple and Google focused on consumer AI, and Nvidia offered the hardware that powers it all, the real story was the shift from generic AI to specialized, thoughtful implementations."], "running_summary": None})

