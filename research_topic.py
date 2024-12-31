import json

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from state import SummaryState

load_dotenv()

query_writer_instructions="""Your goal is to generate targeted web search query.

The query will gather information related to a specific topic.

Topic:
{topic}

Return your query as a JSON object:
{{
    "query": "string",
    "aspect": "string",
    "rationale": "string"
}}

Do not return like this do not include json name in code:
```json
{{
    "query": "string",
    "aspect": "string",
    "rationale": "string"
}}
Please ensure you follow this format and do not include any additional information.
```

"""

query_writer_instructions_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            query_writer_instructions
        ),
        (
            "user",
            "Generate a query for web search on {topic}"
        )
    ]
)


llm = ChatOpenAI(model="gpt-4o")

def research_topic(state: SummaryState) :
    """ Generate a query for web search """
    print("---RESEARCHING TOPIC---")
    research_topic = state.research_topic
    prompt = query_writer_instructions_prompt.format(topic=research_topic)  # Format the prompt with the topic
    result = llm.invoke(prompt)  # Pass the formatted prompt
    query = json.loads(result.content)


    return {"research_query": query["query"]}



if __name__ == "__main__":
    research_topic(state=SummaryState({"research_topic": "Recent AI Advancements"}))