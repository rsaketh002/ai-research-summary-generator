import json
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from state import SummaryState
from langchain_openai import ChatOpenAI


load_dotenv()

reflection_instructions = """You are an expert research assistant analyzing a summary about {research_topic}.

Your tasks:
1. Identify knowledge gaps or areas that need deeper exploration
2. Generate a follow-up question that would help expand your understanding
3. Focus on technical details, implementation specifics, or emerging trends that weren't fully covered

Ensure the follow-up question is self-contained and includes necessary context for web search.

Return your analysis as a JSON object:
{{ 
    "knowledge_gap": "string",
    "follow_up_query": "string"
}}

Do not return like this do not include json name in code:
```json
{{
    "knowledge_gap": "string",
    "follow_up_query": "string"
}}
```

Please ensure you follow this format and do not include any additional information.
"""

reflection_instructions_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            reflection_instructions
        ),
        (
            "user",
            "Identify a knowledge gap and generate a follow-up web search query based on our existing knowledge: {running_summary}"
        )
    ]
)

llm = ChatOpenAI(model="gpt-4o")

def reflect_on_summary(state: SummaryState) :
    """ Generate a follow-up question based on the summary """
    print("---REFLECTING ON SUMMARY---")
    running_summary = state.running_summary
    research_topic = state.research_topic
    prompt = reflection_instructions_prompt.format(research_topic=research_topic, running_summary=running_summary)
    result = llm.invoke(prompt)
    analysis = json.loads(result.content)

    return {"follow_up_query": analysis["follow_up_query"]}

if __name__ == "__main__":
    reflect_on_summary(state={"running_summary": """In 2024, significant advancements and controversies in AI have reshaped the technological landscape, with key developments spanning various domains. Apple made a notable entry into the generative AI market, enhancing consumer interactions with AI technology. Meanwhile, quantum computing has made strides, offering new possibilities for solving complex problems. The year also saw the emergence of specialized AI agents, marking a shift from general AI models to more targeted, practical applications that improve productivity and creativity.

One of the most noteworthy advancements was OpenAI's release of the o1 model in September 2024, which introduced a novel approach to AI reasoning, setting a new standard for AI capabilities. As companies like Google and Apple concentrated on consumer-oriented AI solutions, Nvidia provided the essential hardware infrastructure to support these innovations. A significant theme of the year was the transition towards specialized AI implementations, moving away from generic applications to more thoughtful and specific uses.

Regulatory developments also played a crucial role, particularly in the European Union, where new regulations categorize AI use cases by risk, impacting how organizations can implement AI technologies. These developments highlight the ongoing balance between technological innovation and regulatory frameworks, which will continue to influence AI's growth and integration into various sectors.""", "research_topic": "Artificial Intelligence"})