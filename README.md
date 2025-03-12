# AI GTM Learning hackathon - Agentic LLM Eval with Human-in-the-Loop - Team 8:

Please watch our short pitch video: https://drive.google.com/file/d/1BEWKjQ3v5mEmCnCCLRKDnuOhYiyQ-roX/view?resourcekey=0-V620oEUKe8tg9lPr_Fpy9A

Here is our slide deck including the architecture: https://docs.google.com/presentation/d/1orDK3wMsbQRrjZWPYKeA5DGguNkI071qIvbxmiuoazc/edit?usp=sharing&resourcekey=0-qBCFBrIVMCYZ73mv6ZQIXw


Problem & scenario definition:
Evaluating LLMs for customer service chatbots is crucial due to rapid LLM advancements.
Framework needed for rapid evaluation and comparison of new LLMs as they are released.
Build an evaluation service for a modular and adaptable chatbot platform.
Create an evaluation framework for evaluating different LLMs for a variety of metrics (including performance metrics)
Utilize a dataset of customer service questions and expected answers.
Showcase combination of automated as well as human evaluation as best practice.
A performance tracking dashboard for end user to decide which LLM to use.

Solution:
Create BQ DB to store evaluation metrics and performance logs
Create sample Q&A agent that uses Android 5.0 manual to answer user questions
Leverage Vertex AI rapid eval tools to build generation evaluator
Build context evaluator
Build groundness evaluator
Build function calling evaluator
Aggregate together components to create Agent as judge
