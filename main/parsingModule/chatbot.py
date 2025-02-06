import google.generativeai as genai
import os

os.environ["API_KEY"] = 'AIzaSyDyU3NhJ7MhfZT0fUWJH8S-xU8ZLqe9r9M'
genai.configure(api_key=os.environ["API_KEY"])
def get_chatbot_response(user_message, chat_history):
    PROMPT_TEMPLATE = """
    You are a career guidance assistant on the JobSync platform.
    Your name is MentorX
    Your job is to provide expert recommendations to job seekers.
    Always refer to the previous conversation history to provide relevant responses.

    Here is the conversation so far:

    {history}

    Now, answer the next user query. Avoid using Bot prefix
    User: {query}
    Bot:
    """
    try:
        model = genai.GenerativeModel("gemini-pro")

        # Format chat history properly
        formatted_history = "\n".join(chat_history)  
        formatted_prompt = PROMPT_TEMPLATE.format(history=formatted_history, query=user_message)

        response = model.generate_content(formatted_prompt)

        return response.text  # Return only the chatbot's response

    except Exception as e:
        return f"Error: {str(e)}"