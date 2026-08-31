import streamlit as st
import json
import os
from datetime import datetime

from agent import generate_content, save_report


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Daily Content Agent",
    page_icon="AI",
    layout="wide"
)


# ==========================================
# HEADER
# ==========================================

st.title("AI Daily Content Agent")

st.write(
    "Research current AI and technology trends "
    "and generate platform-specific social media content."
)

st.divider()


# ==========================================
# INPUT SECTION
# ==========================================

st.subheader("Content Settings")

topic = st.text_input(
    "Enter an AI or technology topic",
    placeholder="Example: Agentic AI in 2026"
)

auto_discover = st.checkbox(
    "Automatically discover a trending AI topic",
    value=False
)


# ==========================================
# GENERATE BUTTON
# ==========================================

generate_button = st.button(
    "Generate Content",
    type="primary",
    use_container_width=True
)


# ==========================================
# GENERATE CONTENT
# ==========================================

if generate_button:

    # ======================================
    # VALIDATE INPUT
    # ======================================

    if not auto_discover and not topic.strip():

        st.warning(
            "Please enter a topic or enable automatic topic discovery."
        )

        st.stop()


    # ======================================
    # CREATE USER REQUEST
    # ======================================

    if auto_discover:

        user_request = """
Find the latest and most interesting trending
AI technology topic.

Research current information from the web.

The topic must be related to:

- Artificial Intelligence
- Machine Learning
- Generative AI
- AI Agents
- Agentic AI
- Large Language Models
- AI Automation
- AI Robotics
- AI Infrastructure
- AI Chips
- AI Security
- AI Applications

Do not select unrelated topics.

Then generate:

1. A professional LinkedIn post.
2. An Instagram caption with 8-12 hashtags.
3. A Twitter/X thread containing exactly 5 tweets.

Also include the most relevant research sources
with their titles and URLs.

Return only valid JSON using the required structure.
"""

    else:

        user_request = f"""
Research the following AI or technology topic:

{topic}

Use current information from the web.

The topic must be related to AI or technology.

Analyze the latest information and generate:

1. A professional LinkedIn post.
2. An Instagram caption with 8-12 hashtags.
3. A Twitter/X thread containing exactly 5 tweets.

Also include the most relevant research sources
with their titles and URLs.

Return only valid JSON using the required structure.
"""


    # ======================================
    # RUN AGENT
    # ======================================

    with st.spinner(
        "Agent is researching the web and generating content..."
    ):

        try:

            content = generate_content(
                user_request
            )


            # ==================================
            # SAVE REPORT
            # ==================================

            filename = save_report(
                content
            )


            # ==================================
            # SUCCESS MESSAGE
            # ==================================

            st.success(
                f"Content generated successfully. "
                f"Report saved to {filename}"
            )


            # ==================================
            # TOPIC
            # ==================================

            st.divider()

            st.header("Trending Topic")

            st.subheader(
                content.get(
                    "topic",
                    "No topic returned"
                )
            )


            # ==================================
            # SUMMARY
            # ==================================

            st.subheader("Summary")

            st.write(
                content.get(
                    "summary",
                    "No summary returned."
                )
            )


            # ==================================
            # RESEARCH SOURCES
            # ==================================

            st.subheader("Research Sources")

            sources = content.get(
                "sources",
                []
            )

            if sources:

                for i, source in enumerate(
                    sources,
                    start=1
                ):

                    title = source.get(
                        "title",
                        "Untitled source"
                    )

                    url = source.get(
                        "url",
                        ""
                    )

                    st.markdown(
                        f"**{i}. {title}**"
                    )

                    if url:

                        st.markdown(
                            f"[Open Source]({url})"
                        )

                    st.divider()

            else:

                st.info(
                    "No research sources were returned."
                )


            # ==================================
            # SOCIAL MEDIA TABS
            # ==================================

            st.header("Generated Content")

            tab1, tab2, tab3 = st.tabs(
                [
                    "LinkedIn",
                    "Instagram",
                    "Twitter/X"
                ]
            )


            # ==================================
            # LINKEDIN
            # ==================================

            with tab1:

                st.subheader(
                    "LinkedIn Post"
                )

                linkedin = content.get(
                    "linkedin",
                    {}
                )

                linkedin_post = linkedin.get(
                    "post",
                    "No LinkedIn post generated."
                )

                st.text_area(
                    "LinkedIn Content",
                    linkedin_post,
                    height=400
                )


            # ==================================
            # INSTAGRAM
            # ==================================

            with tab2:

                st.subheader(
                    "Instagram Caption"
                )

                instagram = content.get(
                    "instagram",
                    {}
                )

                caption = instagram.get(
                    "caption",
                    "No Instagram caption generated."
                )

                hashtags = instagram.get(
                    "hashtags",
                    []
                )

                st.text_area(
                    "Instagram Caption",
                    caption,
                    height=300
                )

                st.subheader(
                    "Hashtags"
                )

                if hashtags:

                    st.write(
                        " ".join(hashtags)
                    )

                else:

                    st.write(
                        "No hashtags generated."
                    )


            # ==================================
            # TWITTER/X
            # ==================================

            with tab3:

                st.subheader(
                    "Twitter/X Thread"
                )

                twitter = content.get(
                    "twitter",
                    {}
                )

                thread = twitter.get(
                    "thread",
                    []
                )

                if thread:

                    for i, tweet in enumerate(
                        thread,
                        start=1
                    ):

                        st.text_area(
                            f"Tweet {i}",
                            tweet,
                            height=130
                        )

                else:

                    st.info(
                        "No Twitter/X thread generated."
                    )


            # ==================================
            # DOWNLOAD JSON REPORT
            # ==================================

            st.divider()

            st.header("Report")

            report_data = {
                "date": datetime.now().strftime(
                    "%Y-%m-%d"
                ),
                "generated_by": "LangChain + Ollama",
                "research_source": "Tavily",
                "content": content
            }

            report_json = json.dumps(
                report_data,
                indent=4,
                ensure_ascii=False
            )

            st.download_button(
                label="Download JSON Report",
                data=report_json,
                file_name=(
                    f"ai_content_report_"
                    f"{datetime.now().strftime('%Y-%m-%d')}.json"
                ),
                mime="application/json",
                use_container_width=True
            )


            # ==================================
            # RAW JSON
            # ==================================

            with st.expander(
                "View Raw JSON"
            ):

                st.json(
                    content
                )


        # ======================================
        # JSON ERROR
        # ======================================

        except json.JSONDecodeError:

            st.error(
                "The Agent did not return valid JSON. "
                "Please try again."
            )


        # ======================================
        # GENERAL ERROR
        # ======================================

        except Exception as e:

            st.error(
                f"An error occurred: {str(e)}"
            )