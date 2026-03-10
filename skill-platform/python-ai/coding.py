# -*- coding: utf-8 -*-
import random

# -----------------------------
# CODING CHALLENGE BANK
# -----------------------------
CODING_BANK = {
    "Python": [
        {
            "title": "Sum of Even Numbers",
            "description": "Write a function that takes a list of integers and returns the sum of all even numbers in the list.",
            "starter_code": "def sum_even_numbers(numbers):\n    # Your code here\n    pass",
            "test_cases": [
                {"input": "[1, 2, 3, 4, 5]", "expected": "6"},
                {"input": "[2, 4, 6, 8]", "expected": "20"},
                {"input": "[1, 3, 5]", "expected": "0"}
            ],
            "solution": "def sum_even_numbers(numbers):\n    return sum(num for num in numbers if num % 2 == 0)"
        },
        {
            "title": "String Reversal",
            "description": "Write a function that takes a string and returns it reversed.",
            "starter_code": "def reverse_string(text):\n    # Your code here\n    pass",
            "test_cases": [
                {"input": "'hello'", "expected": "'olleh'"},
                {"input": "'python'", "expected": "'nohtyp'"},
                {"input": "''", "expected": "''"}
            ],
            "solution": "def reverse_string(text):\n    return text[::-1]"
        },
        {
            "title": "Factorial Calculator",
            "description": "Write a function that calculates the factorial of a given non-negative integer.",
            "starter_code": "def factorial(n):\n    # Your code here\n    pass",
            "test_cases": [
                {"input": "5", "expected": "120"},
                {"input": "0", "expected": "1"},
                {"input": "3", "expected": "6"}
            ],
            "solution": "def factorial(n):\n    if n < 0:\n        return None\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)"
        }
    ],

    "JavaScript": [
        {
            "title": "Array Sum",
            "description": "Write a function that takes an array of numbers and returns their sum.",
            "starter_code": "function sumArray(numbers) {\n    // Your code here\n}",
            "test_cases": [
                {"input": "[1, 2, 3, 4]", "expected": "10"},
                {"input": "[5, 10, 15]", "expected": "30"},
                {"input": "[]", "expected": "0"}
            ],
            "solution": "function sumArray(numbers) {\n    return numbers.reduce((sum, num) => sum + num, 0);\n}"
        },
        {
            "title": "Check Palindrome",
            "description": "Write a function that checks if a string is a palindrome (reads the same forwards and backwards).",
            "starter_code": "function isPalindrome(str) {\n    // Your code here\n}",
            "test_cases": [
                {"input": "'racecar'", "expected": "true"},
                {"input": "'hello'", "expected": "false"},
                {"input": "'A man a plan a canal Panama'.toLowerCase().replace(/[^a-z]/g, '')", "expected": "true"}
            ],
            "solution": "function isPalindrome(str) {\n    const cleanStr = str.toLowerCase().replace(/[^a-z0-9]/g, '');\n    return cleanStr === cleanStr.split('').reverse().join('');\n}"
        },
        {
            "title": "Find Maximum",
            "description": "Write a function that finds the maximum value in an array of numbers.",
            "starter_code": "function findMax(numbers) {\n    // Your code here\n}",
            "test_cases": [
                {"input": "[1, 5, 3, 9, 2]", "expected": "9"},
                {"input": "[10, 20, 5]", "expected": "20"},
                {"input": "[-1, -5, -3]", "expected": "-1"}
            ],
            "solution": "function findMax(numbers) {\n    return Math.max(...numbers);\n}"
        }
    ],

    "Java": [
        {
            "title": "Factorial Calculator",
            "description": "Write a method that calculates the factorial of a given number.",
            "starter_code": "public static int factorial(int n) {\n    // Your code here\n}",
            "test_cases": [
                {"input": "5", "expected": "120"},
                {"input": "0", "expected": "1"},
                {"input": "3", "expected": "6"}
            ],
            "solution": "public static int factorial(int n) {\n    if (n <= 1) return 1;\n    return n * factorial(n - 1);\n}"
        },
        {
            "title": "String Reversal",
            "description": "Write a method that reverses a given string.",
            "starter_code": "public static String reverseString(String str) {\n    // Your code here\n}",
            "test_cases": [
                {"input": "\"hello\"", "expected": "\"olleh\""},
                {"input": "\"java\"", "expected": "\"avaj\""},
                {"input": "\"\"", "expected": "\"\""}
            ],
            "solution": "public static String reverseString(String str) {\n    return new StringBuilder(str).reverse().toString();\n}"
        }
    ],

    "C": [
        {
            "title": "Maximum in Array",
            "description": "Write a function that finds the maximum value in an array of integers.",
            "starter_code": "int findMax(int arr[], int size) {\n    // Your code here\n}",
            "test_cases": [
                {"input": "{1, 5, 3, 9, 2}, 5", "expected": "9"},
                {"input": "{10, 20, 5}, 3", "expected": "20"},
                {"input": "{-1, -5, -3}, 3", "expected": "-1"}
            ],
            "solution": "int findMax(int arr[], int size) {\n    int max = arr[0];\n    for (int i = 1; i < size; i++) {\n        if (arr[i] > max) max = arr[i];\n    }\n    return max;\n}"
        },
        {
            "title": "Sum of Array",
            "description": "Write a function that calculates the sum of all elements in an integer array.",
            "starter_code": "int sumArray(int arr[], int size) {\n    // Your code here\n}",
            "test_cases": [
                {"input": "{1, 2, 3, 4}, 4", "expected": "10"},
                {"input": "{5, 10, 15}, 3", "expected": "30"},
                {"input": "{}, 0", "expected": "0"}
            ],
            "solution": "int sumArray(int arr[], int size) {\n    int sum = 0;\n    for (int i = 0; i < size; i++) {\n        sum += arr[i];\n    }\n    return sum;\n}"
        }
    ],

    "SQL": [
        {
            "title": "Select Active Users",
            "description": "Write a SQL query to select all users where status is 'active'.",
            "starter_code": "SELECT * FROM users\nWHERE -- Your condition here",
            "test_cases": [
                {"input": "users table with columns: id, name, email, status", "expected": "SELECT * FROM users WHERE status = 'active'"}
            ],
            "solution": "SELECT * FROM users WHERE status = 'active'"
        },
        {
            "title": "Count Products by Category",
            "description": "Write a SQL query to count the number of products in each category.",
            "starter_code": "SELECT category, COUNT(*)\nFROM products\n-- Your code here\nGROUP BY category;",
            "test_cases": [
                {"input": "products table with columns: id, name, category, price", "expected": "SELECT category, COUNT(*) FROM products GROUP BY category"}
            ],
            "solution": "SELECT category, COUNT(*)\nFROM products\nGROUP BY category;"
        }
    ],

    "React": [
        {
            "title": "Simple Counter Component",
            "description": "Write a React component that displays a counter with increment and decrement buttons.",
            "starter_code": "import React, { useState } from 'react';\n\nfunction Counter() {\n    // Your code here\n    return (\n        <div>\n            {/* Your JSX here */}\n        </div>\n    );\n}\n\nexport default Counter;",
            "test_cases": [
                {"input": "Initial count should be 0", "expected": "Counter starts at 0"},
                {"input": "Click increment button", "expected": "Count increases by 1"},
                {"input": "Click decrement button", "expected": "Count decreases by 1"}
            ],
            "solution": "import React, { useState } from 'react';\n\nfunction Counter() {\n    const [count, setCount] = useState(0);\n\n    return (\n        <div>\n            <h2>Counter: {count}</h2>\n            <button onClick={() => setCount(count + 1)}>Increment</button>\n            <button onClick={() => setCount(count - 1)}>Decrement</button>\n        </div>\n    );\n}\n\nexport default Counter;"
        }
    ],

    "Node.js": [
        {
            "title": "Simple HTTP Server",
            "description": "Write a Node.js script that creates a simple HTTP server listening on port 3000.",
            "starter_code": "const http = require('http');\n\n// Your code here",
            "test_cases": [
                {"input": "Server should listen on port 3000", "expected": "Server starts successfully"},
                {"input": "GET request to /", "expected": "Returns 'Hello World'"}
            ],
            "solution": "const http = require('http');\n\nconst server = http.createServer((req, res) => {\n    res.writeHead(200, { 'Content-Type': 'text/plain' });\n    res.end('Hello World');\n});\n\nserver.listen(3000, () => {\n    console.log('Server running on port 3000');\n});"
        }
    ]
}

def generate_coding_challenges(skills):
    """
    Generate coding challenges based on detected skills.

    Args:
        skills (list): List of detected skills

    Returns:
        list: List of coding challenges
    """
    challenges = []

    for skill in skills:
        if skill in CODING_BANK:
            challenges.extend(CODING_BANK[skill])
        else:
            # Try case-insensitive matching
            for key in CODING_BANK.keys():
                if key.lower() == skill.lower():
                    challenges.extend(CODING_BANK[key])
                    break

    # Limit to 3 challenges max
    if len(challenges) > 3:
        challenges = random.sample(challenges, 3)
    else:
        random.shuffle(challenges)

    # If no challenges found, add a default one
    if not challenges:
        challenges = [{
            "title": "Basic Programming Challenge",
            "description": "Write a function that returns 'Hello, World!'",
            "starter_code": "def hello_world():\n    # Your code here\n    pass",
            "test_cases": [
                {"input": "", "expected": "'Hello, World!'"}
            ],
            "solution": "def hello_world():\n    return 'Hello, World!'"
        }]

    print(f"Coding Challenges Generated: {len(challenges)} challenges")
    return challenges