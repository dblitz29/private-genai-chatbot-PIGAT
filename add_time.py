import sys
import os
from datetime import datetime

def merge_with_knowledge(message, session_id):
    knowledge_file = f"knowledge/knowledge_{session_id}.txt"
    if os.path.exists(knowledge_file):
        with open(knowledge_file, 'r') as f:
            first_line = f.readline().strip()
            if first_line:
                return f"{first_line}\n{message}"
    return message

message = sys.argv[1]
session_id = os.environ.get('SESSION_ID')
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

merged_message = merge_with_knowledge(message, session_id)
processed_message = f"{merged_message} (Sent at {now})"

print(processed_message)