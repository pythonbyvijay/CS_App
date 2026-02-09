# questions.py
# questions.py

# 1. USER AUTHENTICATION DATABASE
# You can add more students here as needed
users = {
    "admin": {"password": "Bhawarth@79", "role": "admin"},
    "student": {"password": "password", "role": "student"},
    
}

# 2. INITIAL SEED QUESTIONS (Pre-loaded data)
# These will show up as soon as the app starts
initial_data = [
    {
        "category": "3 Marks Theory", 
        "question": "What is a Friend Function in C++?", 
        "answer": "A friend function is a function that is not a member of a class but has access to its private and protected members."
    },
    {
        "category": "4 Marks Theory", 
        "question": "Explain the concept of Virtual Memory.", 
        "answer": "Virtual memory is a memory management technique that provides an idealized abstraction of the storage resources that are actually available on a given machine."
    },
    {
        "category": "C++ Programs", 
        "question": "Write a C++ program to find the factorial of a number.", 
        "answer": """#include <iostream>
using namespace std;
int main() {
    int n;
    long factorial = 1.0;
    cout << "Enter a positive integer: ";
    cin >> n;
    for(int i = 1; i <= n; ++i) {
        factorial *= i;
    }
    cout << "Factorial of " << n << " = " << factorial;    
    return 0;
}"""
    },
    {
        "category": "HTML Programs", 
        "question": "Write HTML code to create a simple 2x2 table.", 
        "answer": """<table border="1">
  <tr>
    <td>Row 1, Col 1</td>
    <td>Row 1, Col 2</td>
  </tr>
  <tr>
    <td>Row 2, Col 1</td>
    <td>Row 2, Col 2</td>
  </tr>
</table>"""
    }
]