import os
import json
from datetime import datetime

from dotenv import load_dotenv
from tavily import TavilyClient

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")


# ==========================================
# CHECK API KEYS
# ==========================================

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is missing from .env")

if not OLLAMA_API_KEY:
    raise ValueError("OLLAMA_API_KEY is missing from .env")


# ==========================================
# TAVILY CLIENT
# ==========================================

tavily = TavilyClient(
    api_key=TAVILY_API_KEY
)


# ==========================================
# TAVILY SEARCH TOOL
# ==========================================

@tool
def search_web(query: str) -> str:
    """
    Search the internet for current AI and technology information.
    """

    print(f"\nSearching web for: {query}\n")

    response = tavily.search(
        query=query,
        max_results=5,
        search_depth="advanced"
    )

    results = response.get("results", [])

    if not results:
        return "No search results found."

    output = ""

    for i, result in enumerate(results, start=1):

        title = result.get("title", "")
        url = result.get("url", "")
        content = result.get("content", "")

        output += f"""
SOURCE {i}

Title:
{title}

URL:
{url}

Content:
{content}

--------------------------------
"""

    return output


# ==========================================
# OLLAMA CLOUD LLM
# ==========================================

llm = ChatOpenAI(
    model="gpt-oss:20b-cloud",
    temperature=0.3,
    api_key=OLLAMA_API_KEY,
    base_url="https://ollama.com/v1"
)


# ==========================================
# LANGCHAIN AGENT
# ==========================================

agent = create_agent(
    model=llm,
    tools=[search_web],

    system_prompt="""
You are an autonomous AI technology research and
social media content generation agent.

Your responsibilities are:

1. Research current AI and technology information.
2. Use the search_web tool whenever current,
   latest, or trending information is required.
3. Analyze the information returned by the search tool.
4. Identify the most important and relevant trend.
5. Explain the trend clearly.
6. Explain why the trend is important.
7. Explain the possible business impact.
8. Generate professional social media content.

You must generate content for:

1. LinkedIn
2. Instagram
3. Twitter/X

LinkedIn requirements:

- Professional tone.
- Educational and informative.
- Around 150-250 words.
- Suitable for business and technology audiences.

Instagram requirements:

- Engaging caption.
- Shorter than LinkedIn.
- Include 8-12 relevant hashtags.

Twitter/X requirements:

- Create exactly 5 tweets.
- Each tweet should be concise.
- Tweets should form one logical thread.
- Keep the thread informative and engaging.

SOURCE REQUIREMENTS:

- Use the sources returned by search_web.
- Include the most relevant sources in the final JSON.
- Do not invent source URLs.
- Only include URLs that were returned by search_web.
- Include source title and URL.

IMPORTANT RULES:

- Always use search_web for current or trending information.
- Do not invent facts.
- Base the content on the research results.
- Do not mention that you are an AI.
- Do not include markdown code fences.
- Return ONLY valid JSON.
- Do not write anything before or after the JSON.

The JSON MUST use exactly this structure:

{
    "topic": "The main AI or technology trend",

    "summary": "A concise explanation of the trend and why it matters",

    "sources": [
        {
            "title": "Source title",
            "url": "Source URL"
        }
    ],

    "linkedin": {
        "post": "Professional LinkedIn post"
    },

    "instagram": {
        "caption": "Instagram caption",
        "hashtags": [
            "#AI",
            "#ArtificialIntelligence"
        ]
    },

    "twitter": {
        "thread": [
            "Tweet 1",
            "Tweet 2",
            "Tweet 3",
            "Tweet 4",
            "Tweet 5"
        ]
    }
}

The JSON must contain all of these keys:

topic
summary
sources
linkedin
instagram
instagram.caption
instagram.hashtags
twitter
twitter.thread
"""
)


# ==========================================
# SAVE REPORT
# ==========================================

def save_report(content):

    today = datetime.now().strftime("%Y-%m-%d")

    os.makedirs("reports", exist_ok=True)

    filename = f"reports/{today}.json"

    report = {
        "date": today,
        "generated_by": "LangChain + Ollama",
        "research_source": "Tavily",
        "content": content
    }

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False
        )

    return filename


# ==========================================
# CLEAN JSON RESPONSE
# ==========================================

def clean_json(response):

    response = response.strip()

    if response.startswith("```json"):
        response = response[7:]

    elif response.startswith("```"):
        response = response[3:]

    if response.endswith("```"):
        response = response[:-3]

    return response.strip()


# ==========================================
# GENERATE CONTENT
# ==========================================

def generate_content(user_request):

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_request
                }
            ]
        }
    )

    final_message = result["messages"][-1]

    response = final_message.content

    response = clean_json(response)

    content = json.loads(response)

    return content


# ==========================================
# COMMAND LINE TEST
# ==========================================

def main():

    print("=" * 60)
    print("AI DAILY CONTENT AGENT")
    print("=" * 60)

    request = """
Find the latest and most interesting trending AI
technology topic.

Research current information from the web.

Then generate:

1. A professional LinkedIn post.
2. An Instagram caption with 8-12 hashtags.
3. A Twitter/X thread containing exactly 5 tweets.

Also include the most relevant research sources
with their titles and URLs.

Return only valid JSON using the required structure.
"""

    print("\nAgent is researching and generating content...\n")

    try:

        content = generate_content(request)

        filename = save_report(content)

        print("\nTopic:")
        print(content["topic"])

        print("\nSummary:")
        print(content["summary"])

        # ======================================
        # SOURCES
        # ======================================

        print("\nResearch Sources:")

        for i, source in enumerate(
            content["sources"],
            start=1
        ):

            print(f"\n{i}. {source['title']}")
            print(source["url"])

        # ======================================
        # LINKEDIN
        # ======================================

        print("\nLinkedIn:")
        print(content["linkedin"]["post"])

        # ======================================
        # INSTAGRAM
        # ======================================

        print("\nInstagram:")
        print(content["instagram"]["caption"])

        print("\nHashtags:")
        print(
            " ".join(
                content["instagram"]["hashtags"]
            )
        )

        # ======================================
        # TWITTER/X
        # ======================================

        print("\nTwitter/X Thread:")

        for i, tweet in enumerate(
            content["twitter"]["thread"],
            start=1
        ):

            print(f"{i}. {tweet}")

        # ======================================
        # REPORT
        # ======================================

        print("\nReport saved:")
        print(filename)

        print("\n" + "=" * 60)
        print("DONE")
        print("=" * 60)

    except json.JSONDecodeError:

        print("\nAgent did not return valid JSON.")

    except Exception as e:

        print(f"\nError: {e}")


# ==========================================
# START
# ==========================================

if __name__ == "__main__":
    main()