This assignment was designed to practice python fundamentals for streaming data. The project was executed using a synthetic AITU Campus Shuttle and Mobility Data.

The submission consists of six files:
1. "main.py" - a python file that stores data, processes streaming events, validates chronological order of events, creates JSON file, perform key analysis on data.
2. "api.py" - a python file with FastAPI POST /events web service that accepts one event and returns its data.
3. "tests.py" - a python file that executes 4 testing events and validates the performance.
4. "events.json" - a dataset generated during the project (in "main.py" file).
5. "README.md" - a file with textual explanation of code execution.
6. "report.pdf" - a technical report.

To run the project:
1. Install Python version, Python 3.14 was used to complete this assignment.
2. Install the software to execute the code and work with files. For example, VS Code.
3. Open a terminal and run "py main.py" command to execute the event streaming simulation, JSON generation, and summary analysis.
4. Run "py -m pytest tests.py" to test four even cases.
5. To launch the REST API server, execute "py -m uvicorn api:app --reload".
