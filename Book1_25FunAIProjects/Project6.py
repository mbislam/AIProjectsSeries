print("Welcome to Homework Helper Chatbot!")
print("Ask me about math, science, Python, or study tips.")
print("Type quit to exit.")

while True:
    question = input("\nYou: ").lower()

    if question == "quit":
        print("Chatbot: Goodbye! Keep learning and never stop asking questions.")
        break

    elif "math" in question:
        print("Chatbot: Math tip: Break the problem into smaller steps.")
        print("Chatbot: Write down what you know and what you need to find.")

    elif "fraction" in question:
        print("Chatbot: To add fractions, first find a common denominator.")

    elif "science" in question:
        print("Chatbot: Science tip: Ask what happened, why it happened, and how you can test it.")

    elif "python" in question:
        print("Chatbot: Python tip: Read the error message carefully.")
        print("Chatbot: Use print statements to inspect variable values.")

    elif "loop" in question:
        print("Chatbot: A loop repeats a block of code multiple times.")

    elif "study" in question:
        print("Chatbot: Study tip: Review a little bit every day.")
        print("Chatbot: Practice active recall and teach the concept to someone else.")

    elif "exam" in question or "test" in question:
        print("Chatbot: Start early, solve practice problems, and get enough sleep.")

    elif "hello" in question or "hi" in question:
        print("Chatbot: Hello! What homework question do you have today?")

    else:
        print("Chatbot: I am still learning.")
        print("Chatbot: Try asking about math, fractions, science, Python, loops, study tips, or exams.")