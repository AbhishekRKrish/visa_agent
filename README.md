Visa agent

## Setup and Installation

Follow these steps to get the Visa AI Agent running on your machine (instructions tailored for macOS).

### 1. Prerequisites

- **Install Ollama:**
  - Download and install Ollama for macOS from the [official website](https://ollama.com/).
  - After installation, run the Ollama application. You should see its icon in your top menu bar.
- **Pull the LLM Model:**
  - Open your terminal and run the following command to download the Llama 3 model:
    ```bash
    ollama pull llama3
    ```

### 2. Project Setup

1.  **Create Project Directory:**
    Open your terminal and create a folder for the project.

    ```bash
    mkdir visa_agent
    cd visa_agent
    ```

2.  **Create Virtual Environment:**
    It's highly recommended to use a virtual environment to manage project dependencies.

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    Your terminal prompt should now start with `(venv)`.

3.  **Create Project Files:**
    - Create the main application file: `touch app.py`
    - Create a directory for your visa information files: `mkdir data`
    - Create a `requirements.txt` file to list all dependencies: `touch requirements.txt`

4.  **Add Dependencies to `requirements.txt`:**
    Open the `requirements.txt` file and add the following lines:
    ```
    streamlit
    langchain
    langchain-community
    faiss-cpu
    ollama
    unstructured[md]
    nltk
    ```

5.  **Install Dependencies:**
    Install all the required packages from your `requirements.txt` file.

    ```bash
    pip install -r requirements.txt
