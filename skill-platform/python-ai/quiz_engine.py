# -*- coding: utf-8 -*-
import random

QUESTION_BANK = {
    "Python": [
        {
            "q": "What is Python?",
            "options": ["Snake", "Programming Language", "Game", "Browser"],
            "answer": "Programming Language"
        },
        {
            "q": "Which keyword is used to define a function in Python?",
            "options": ["func", "def", "define", "function"],
            "answer": "def"
        },
        {
            "q": "What is the output of: print(2 ** 3)?",
            "options": ["6", "8", "9", "5"],
            "answer": "8"
        }
    ],

    "Java": [
        {
            "q": "Java is a ____ language.",
            "options": ["Procedural", "Object-Oriented", "Markup", "Scripting"],
            "answer": "Object-Oriented"
        },
        {
            "q": "Which keyword is used for inheritance in Java?",
            "options": ["extends", "inherits", "implements", "super"],
            "answer": "extends"
        }
    ],

    "Machine Learning": [
        {
            "q": "Which algorithm is used for classification?",
            "options": ["Linear Regression", "KNN", "K-Means", "Apriori"],
            "answer": "KNN"
        },
        {
            "q": "What does 'ML' stand for?",
            "options": ["Machine Learning", "Markup Language", "Memory Location", "Multi-Layer"],
            "answer": "Machine Learning"
        }
    ],

    "C": [
        {
            "q": "Who developed C language?",
            "options": ["Dennis Ritchie", "James Gosling", "Guido van Rossum", "Elon Musk"],
            "answer": "Dennis Ritchie"
        }
    ],

    "JavaScript": [
        {
            "q": "Which keyword is used to declare a variable in modern JavaScript?",
            "options": ["var", "let", "const", "All of the above"],
            "answer": "All of the above"
        },
        {
            "q": "What is the result of: typeof null?",
            "options": ["null", "object", "undefined", "string"],
            "answer": "object"
        }
    ],

    "React": [
        {
            "q": "What is React?",
            "options": ["Database", "JavaScript Library", "Programming Language", "Operating System"],
            "answer": "JavaScript Library"
        },
        {
            "q": "Which hook is used for state management in React?",
            "options": ["useEffect", "useState", "useContext", "useReducer"],
            "answer": "useState"
        }
    ],

    "Node.js": [
        {
            "q": "What is Node.js?",
            "options": ["Frontend Framework", "JavaScript Runtime", "Database", "CSS Framework"],
            "answer": "JavaScript Runtime"
        }
    ],

    "SQL": [
        {
            "q": "What does SQL stand for?",
            "options": ["Structured Query Language", "Simple Query Language", "Standard Query Language", "System Query Language"],
            "answer": "Structured Query Language"
        },
        {
            "q": "Which clause is used to filter rows in SQL?",
            "options": ["SELECT", "WHERE", "FROM", "GROUP BY"],
            "answer": "WHERE"
        }
    ],

    "MongoDB": [
        {
            "q": "What type of database is MongoDB?",
            "options": ["Relational", "NoSQL", "Graph", "Key-Value"],
            "answer": "NoSQL"
        }
    ],

    "AWS": [
        {
            "q": "What does AWS stand for?",
            "options": ["Amazon Web Services", "Advanced Web System", "Application Web Server", "Automated Web Service"],
            "answer": "Amazon Web Services"
        }
    ],

    "Docker": [
        {
            "q": "What is Docker used for?",
            "options": ["Version Control", "Containerization", "Database Management", "Web Development"],
            "answer": "Containerization"
        }
    ],

    "Git": [
        {
            "q": "What is Git?",
            "options": ["Programming Language", "Version Control System", "Database", "Web Framework"],
            "answer": "Version Control System"
        },
        {
            "q": "Which command is used to commit changes in Git?",
            "options": ["git push", "git commit", "git add", "git pull"],
            "answer": "git commit"
        }
    ]
}

def generate_quiz(skills):
    quiz = []

    for skill in skills:
        if skill in QUESTION_BANK:
            quiz.extend(QUESTION_BANK[skill])
        else:
            # Try case-insensitive matching
            for key in QUESTION_BANK.keys():
                if key.lower() == skill.lower():
                    quiz.extend(QUESTION_BANK[key])
                    break

    # Limit to 10 questions max
    if len(quiz) > 10:
        quiz = random.sample(quiz, 10)
    else:
        random.shuffle(quiz)
    
    print(f"Quiz Generated: {len(quiz)} questions")
    return quiz
