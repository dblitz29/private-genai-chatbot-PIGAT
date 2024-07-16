import sys
import os
from datetime import datetime
from transformer import pipeline
# def merge_with_knowledge(message, session_id):
#     knowledge_file = f"knowledge/knowledge_{session_id}.txt"
#     if os.path.exists(knowledge_file):
#         with open(knowledge_file, 'r') as f:
#             first_line = f.readline().strip()
#             if first_line:
#                 return f"{first_line}\n{message}"
#     return message
# message = sys.argv[1]
# session_id = os.environ.get('SESSION_ID')
# now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# merged_message = merge_with_knowledge(message, session_id)
# processed_message = f"{merged_message} (Sent at {now})"
# print(processed_message)


qa_pipeline = pipeline("question-answering", model='Jahanzeb1/BERT_QA_model', tokenizer='Jahanzeb1/BERT_QA_model')

def read_context(session_id):
    """
    Read context from a file based on the session_id.
    
    Args:
    session_id (str): The session ID to determine the file name.
    
    Returns:
    str: The context read from the file.
    """
    file_name = f"context_{session_id}.txt"
    try:
        with open(file_name, 'r') as file:
            context = file.read()
        return context
    except FileNotFoundError:
        return "Context file not found."

def get_answer(session_id, question):
    """
    Get answer to a question using the context from a file based on session_id.
    
    Args:
    session_id (str): The session ID to determine the file name.
    question (str): The question to be answered.
    
    Returns:
    str: The answer to the question.
    """
    context = read_context(session_id)
    if context == "Context file not found.":
        return context
    answer = qa_pipeline(question=question, context=context)
    return answer['answer']

question = sys.argv[1]
session_id = os.environ.get('SESSION_ID')
answer = get_answer(session_id, question)

print(answer)