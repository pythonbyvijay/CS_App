# questions.py

users = {
    "admin": {"password": "Bhawarth@79", "role": "admin"},
    "student": {"password": "password", "role": "student"}
}

initial_data = [
    {
        "category": "3 Marks Theory", 
        "question": "What is a Friend Function in C++?", 
        "answer": "A friend function is a function that is not a member of a class but has access to its private and protected members."
    },
    {
        "category": "C++ Programs", 
        "question": "C++ Program to find Factorial.", 
        "answer": """#include <iostream>
using namespace std;
int main() {
    int n;
    long fact = 1;
    cout << "Enter number: "; cin >> n;
    for(int i=1; i<=n; i++) fact *= i;
    cout << "Factorial: " << fact;
    return 0;
}"""
    }
]