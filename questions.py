# questions.py

users = {
    "admin": {"password": "Bhawarth@79", "role": "admin"},
    "student1": {"password": "1234", "role": "student"},
    "student2": {"password": "2345", "role": "student"},
    "student3": {"password": "3456", "role": "student"},
    "student4": {"password": "4567", "role": "student"},
    "student5": {"password": "5678", "role": "student"}
}

initial_data = [
    {
        "category": "1 Mark MCQ", 
        "question": "Which of the following is the extraction operator in C++?", 
        "options": [">>", "<<", "::", "->"],
        "answer": ">>"
    },
    {
        "category": "3 Marks Theory", 
        "question": "What is a Friend Function?", 
        "answer": "A function that can access private members of a class..."
    }
]