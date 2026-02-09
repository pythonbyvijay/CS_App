# questions.py

# Categorized initial data bank
initial_questions = [
    {
        "category": "3 Marks Theory",
        "question": "State any three special characteristics of a Friend Function.",
        "answer": "1. Not in the scope of the class. 2. Can be called without an object. 3. Has access to private members."
    },
    {
        "category": "4 Marks Theory",
        "question": "Explain the concept of Virtual Memory in detail.",
        "answer": "Virtual memory is a memory management technique that creates an illusion of a very large main memory by using disk space..."
    },
    {
        "category": "C++ Programs",
        "question": "Write a C++ program to find the largest of three numbers.",
        "answer": """#include <iostream>
using namespace std;
int main() {
    int a, b, c;
    cout << "Enter three numbers: ";
    cin >> a >> b >> c;
    if(a>=b && a>=c) cout << a << " is largest";
    else if(b>=a && b>=c) cout << b << " is largest";
    else cout << c << " is largest";
    return 0;
}"""
    },
    {
        "category": "HTML Programs",
        "question": "Write HTML code to create a link to 'google.com' that opens in a new tab.",
        "answer": '<a href="https://www.google.com" target="_blank">Visit Google</a>'
    }
]

# User database
users = {
    "admin": {"password": "Bhawarth@79", "role": "admin"},
    "student": {"password": "password", "role": "student"}
}