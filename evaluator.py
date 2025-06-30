import os
import openai
import json
from dotenv import load_dotenv

load_dotenv()
#need to obtain OpenAI Key 
openai.api_key = os.getenv("OPENAI_API_KEY")

def format_conversation_for_prompt(conversation):
    """Formats chat history into a readable text block."""
    formatted = ""
    for turn in conversation:
        role = turn["role"].capitalize()
        content = turn["content"]
        formatted += f"{role}: {content}\n\n"
    return formatted.strip()

#evaluate the ChatGPT History using GPT 4 and return score and feedback
def evaluate_conversation(conversation, rubric):
    formatted_chat = format_conversation_for_prompt(conversation)

    system_prompt = f"""
    You are a teaching assistant evaluating student interactions with ChatGPT.
    The following rubric will be used:
    {rubric}
    Evaluate the student's use of ChatGPT based on this rubric. 
    Return your response in **this exact JSON format**:
    {{
  "score": <number between 1 and 5>,
  "feedback": "<brief feedback for the student>"
}}
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": formatted_chat}
            ],
            temperature=0.2,
            max_tokens=300
        )

        response_content = response.choices[0].message.content.strip()

        return json.loads(response_content)

    except Exception as e:
        print(f"❌ Evaluation failed: {e}")
        return {"score": 0, "feedback": "There was an error evaluating your submission."}


# Optional test run
if __name__ == "__main__":
    test_convo = [
        {"role": "user", "content": "What is artificial intelligence?"},
        {"role": "assistant", "content": "AI is a field of computer science that..."},
        {"role": "user", "content": "Can AI be dangerous?"},
        {"role": "assistant", "content": "It can be if not used responsibly..."},
    ]

    test_rubric = """
- Asked at least 3 thoughtful questions
- Followed up on AI-related concepts
- Responses show engagement and curiosity
- Stayed relevant to the topic
"""

    result = evaluate_conversation(test_convo, test_rubric)
    print(result)

    