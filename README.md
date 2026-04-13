# Secure Code Final Project

This project demonstrates various security vulnerabilities in a web application. It includes examples of:
- SQL Injection
- Cross-Site Scripting (XSS)
- Broken Access Control
- OS Command Injection
- Insecure Deserialization

references: OWASP to 10

## Peer review

A peer will be invited into the repository to review the code 
and provide feedback on the vulnerabilities and their mitigations. 
The peer will also check for any additional security issues that may have been overlooked.

## Mitigation
Each vulnerability will be mitigated with appropriate security measures, such as:
- Using parameterized queries to prevent SQL injection
- Properly encoding user input to prevent XSS
- Implementing proper access control checks
- Validating and sanitizing user input to prevent OS command injection
- Using secure serialization formats and validating deserialized data

## Actions and workflow
- super-linter will be used to analyze the code for security issues and provide feedback on potential vulnerabilities.

- CodeQL will be used to perform static analysis and identify security vulnerabilities in the codebase.

- Bandit will be used to scan for security issues in Python code, 
such as hardcoded passwords and insecure function calls.

# Author

Ralph Vitug
