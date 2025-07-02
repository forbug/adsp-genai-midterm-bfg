# ADSP 32027 Generative AI Principles SU2025 - Midterm Assignment

## Getting Started

To get a local copy up and running, follow these simple steps.

### Local Environment Configuration

Below are the recommended operating-system-specific instructions for:
* Installing & configuring git
* Setting up Visual Studio Code

**NOTE**: While it is not necessary that you use Visual Studio Code, it is recommended, as it contains useful extensions and add-ins that will assist with development, especially those related to Microsoft tools.

#### Install Necessary Tools

**NOTE**: It is assumed that you have Python 3.x installed. If you need assistance with installing Python, please contact one of the administrators of this repository.

1. Install [VSCode](https://code.visualstudio.com/download)
2. Install [git](https://git-scm.com/downloads)
   * If you have a Mac, git may already be installed on your system. To test this, run `git --version` in your terminal.
   * If you are using a Windows 11 machine, you should now open a Git Bash terminal for the remaining steps.
3. Install [poetry](https://python-poetry.org/docs/#installation)
   * IMPORTANT: You may need to add your `~/.local/bin` folder to your path if you are on a Windows or Mac machine. For Mac, see [this article](https://medium.com/@B-Treftz/macos-adding-a-directory-to-your-path-fe7f19edd2f7).
   * Run `poetry --version` to validate that the installation was successful.
4. (optional) Set up [Ollama](https://ollama.com/)
    * Ollama allows you to run local open-source models locally. You can interact with it either through the UI or through your terminal once you have downloaded it from the link above. 
    * Once you have the UI downloaded, you can download models (see the list of available models [here](https://ollama.com/search)) by running `ollama pull <model-name>` in the UI or in your terminal.
    * Then, you can use a model's name in any Ollama-related function from langchain to use the model that you have downloaded.


#### Configure VSCode

If you decide to use VSCode, these extensions will make your experience much easier.

1. Enable `git` in the settings.
   * Follow the instructions in [this YouTube video](https://youtu.be/3Tsaxxv9sls?si=VsSBTenx6jm_K_tY&t=153)
2. (Windows ONLY) Configure `git bash` as your default terminal.
   * Now that you have git/git bash installed, you should be able to open a git bash terminal in VSCode. Follow the instructions [here](https://csweb.wooster.edu/mionescu/cs232/guides/vs-code-default-terminal/#:~:text=Open%20Visual%20Studio%20Code,the%20menu%20that%20pops%20up.) to configure git bash as your default terminal.
   * Mac users will likely prefer to use Terminal or another shell.

#### Configure Git (Optional)

1. Add your SSH keys to your GitHub account.
   * Follow the instructions [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).
2. Configure your git username and email:
   ```bash
   git config user.name "<your-username>"
   git config user.email "<your-github-email>"
   ```
3. Clone the repository:
   ```bash
   git clone git@github.com:ConvoAI-Capstone-SpSu2025/currensee.git
   ```

#### Configure the Python Environment

1. Create the environment from the existing poetry specs in the repository.
   ```bash
   poetry config virtualenvs.in-project true
   poetry env use 3.11.12
   poetry env activate
   # copy and execute the command that is printed out
   poetry install
   ```
   This will create and activate a virtual environment and install all dependencies.

**NOTE:** If you wish to use another environment manager (e.g., conda, pyenv), ensure you install all dependencies listed in [pyproject.toml](pyproject.toml).

#### Environment Variables

- Copy `.env.example` to `.env` and fill in any required secrets or configuration values.

## Running the Basic Graph

To run the basic graph, use the notebook stored in `notebooks/basic_rag_demo.ipynb`. 

**Important**: Make sure that you are using the `.venv` created from the `poetry env activate` command as your kernel.
