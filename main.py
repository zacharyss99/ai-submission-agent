from scraper import scrape_chatgpt_share_url
from evaluator import evaluate_conversation
from notifier import log_submission
import asyncio

def process_submission(url, student_email, assignment_name):
    print("Starting submission processing...")

    try:
        conversation = asyncio.run(scrape_chatgpt_share_url(url))
    except Exception as e:
        return {
            "student_message": "❌ We couldn't access your ChatGPT link. Please make sure it is publicly shared and try again.",
            "error": str(e)
        }

    #Mom define rubric here
    rubrics = {
        "Lesson 1: Intro to AI": """
        - Asked at least 3 thoughtful questions
        - Responses were on-topic
        - Demonstrated curiosity and engagement
        """,
        "Lesson 2: Prompt Engineering": """
        - Explored different prompt styles
        - Asked follow-up questions
        - Reflected on the model's responses
        """,
    }

    #in general, what model should look for
    #again, can  change if u want
    rubric = rubrics.get(assignment_name, """
    - Asked relevant questions
    - Showed curiosity
    - Stayed on topic
    """)

    #evaluate convo using evaluator.py script
    evaluation = evaluate_conversation(conversation, rubric)

    score = evaluation["score"]
    feedback = evaluation["feedback"]

    # Log submission for your mom
    log_submission(student_email, assignment_name, score, feedback, url)

    # Message for the student
    student_message = f"""
✅ Your submission was received!

📊 **Score**: {score}/5  
📝 **Feedback**: {feedback}
"""

    return {"student_message": student_message}