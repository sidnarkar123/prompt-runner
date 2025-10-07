
# Streamlit Prompt Runner

## Overview

The **Streamlit Prompt Runner** is a web application designed to facilitate the interaction between users and automated agents through natural language prompts. The application allows users to input prompts, generate structured JSON specifications, and route these specifications to various agents for further processing. This project serves as a mini "Prompt-to-Agent" pipeline, ensuring transparency and traceability of user interactions.

## Project Structure

```
streamlit-prompt-runner/
├── main.py                # Main entry point for the Streamlit application
├── requirements.txt       # Lists project dependencies
├── streamlit.toml         # Configuration settings for the Streamlit app
├── prompts/               # Stores user prompt text files
├── specs/                 # Stores JSON outputs from the design agent
├── logs/                  # Contains log files for prompts and actions
│   ├── prompt_logs.json   # Tracks all user prompts
│   └── action_logs.json   # Logs all routing actions
├── send_to_evaluator/     # Stores routed specs for the evaluator agent
├── send_to_unreal/        # Stores routed specs for the Unreal Engine team
├── agents/                # Contains agent implementations
│   ├── design_agent.py    # Generates structured JSON from prompts
│   ├── evaluator_agent.py  # Evaluates generated specifications
│   └── unreal_agent.py     # Simulates sending specs to Unreal Engine
├── components/            # Contains UI components
│   └── ui.py              # Defines reusable UI components
├── utils/                 # Contains utility functions
│   └── io_helpers.py      # Helper functions for file I/O
└── README.md              # Documentation for the project
```

## Installation

To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd streamlit-prompt-runner
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure the Streamlit application (if necessary) in `streamlit.toml`.

## Usage

To run the application, execute the following command in your terminal:

```
streamlit run main.py
```

Once the application is running, you can:

1. Enter a natural language prompt in the input field.
2. Submit the prompt to generate a structured JSON specification.
3. View past prompts and their corresponding JSON outputs in the log viewer.
4. Route the generated specifications to the evaluator or Unreal Engine team as needed.

## Features

- User-friendly interface for prompt submission and JSON viewing.
- Integration with automated agents for generating and evaluating specifications.
- Logging of all user interactions for transparency and review.
- Ability to route specifications to different agents for further processing.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

- Thanks to the Streamlit community for their support and resources.
- Special thanks to all contributors who help improve this project.
=======
# prompt-runner
Streamlit Prompt Runner is a lightweight, interactive web app built with Streamlit that allows users to input prompts, automatically generate structured JSON specifications using an integrated Design Agent, and visualize, log, and manage previous prompts with ease. 
>>>>>>> 7114d4a9187792caa3991904e8f2a6a3eb072316
