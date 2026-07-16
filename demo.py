from ollama import chat

print("=" * 50)
print("Enterprise Banking AI Assistant")
print("=" * 50)

while True:
    question = input("\nAsk your question (type 'exit' to quit): ")

    if question.lower() == "exit":
        break

    response = chat(
        model="llama3.1",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI Banking Assistant. "
                    "Answer professionally and briefly."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    print("\nAI:")
    print(response["message"]["content"])