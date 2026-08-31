import time
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

from agent import generate_content, save_report


# ==========================================
# DAILY AGENT TASK
# ==========================================

def run_daily_agent():

    print("\n" + "=" * 60)
    print("DAILY CONTENT AGENT STARTED")
    print("=" * 60)

    print(
        f"\nStarted at: "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    request = """
Find the latest and most interesting trending AI
technology topic.

Research current information from the web.

The topic must be related to AI or technology.

Then generate:

1. A professional LinkedIn post.
2. An Instagram caption with 8-12 hashtags.
3. A Twitter/X thread containing exactly 5 tweets.

Also include the most relevant research sources
with their titles and URLs.

Return only valid JSON using the required structure.
"""

    try:

        # ======================================
        # RUN LANGCHAIN AGENT
        # ======================================

        content = generate_content(request)


        # ======================================
        # SAVE DAILY REPORT
        # ======================================

        filename = save_report(content)


        print("\nTopic:")
        print(content["topic"])

        print("\nReport saved:")
        print(filename)

        print("\nDaily agent completed successfully.")

    except Exception as e:

        print("\nAgent failed.")

        print(f"Error: {e}")


# ==========================================
# SCHEDULER
# ==========================================

scheduler = BlockingScheduler()


# ==========================================
# DAILY SCHEDULE
# ==========================================

scheduler.add_job(
    run_daily_agent,
    "interval",
    minutes=1
)

# ==========================================
# START SCHEDULER
# ==========================================

print("=" * 60)
print("DAILY CONTENT SCHEDULER")
print("=" * 60)

print("\nScheduler is running.")

print(
    "The agent will run every day at 09:00."
)

print("\nPress CTRL+C to stop the scheduler.")


try:

    scheduler.start()

except (KeyboardInterrupt, SystemExit):

    print("\nScheduler stopped.")