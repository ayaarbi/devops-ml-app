# DevOps Assignment Report

This report details the steps taken to build a complete Continuous Integration (CI) pipeline for the Iris Classifier ML project. The process includes setting up the project, writing unit tests, adding a linter, containerizing the application with Docker, and automating the entire workflow with GitHub Actions.

## Task 1: Project Setup

**Description of Work:**

The project was initialized from the provided ZIP file. A new, empty repository was created on GitHub. The unzipped project files were then added to a local Git repository, and an initial commit was made. This local repository was linked to the GitHub remote, and the initial project structure was pushed to the `master` branch.

**Screenshot(s):**
![Project's structure](<Screenshot 2025-11-07 212523.png>)

![Initialising a repository](<Screenshot 2025-11-08 140239.png>)

![Result](<Screenshot 2025-11-08 140250.png>)
## Task 2: Running Locally

**Description of Work:**

To verify the project's functionality, it was run on the local machine. This involved:

1. Creating a Python virtual environment using `python -m venv .venv`.

2. Activating the environment (using `.venv\Scripts\activate.bat` on Windows PowerShell).

![virtual environnement](<Screenshot 2025-11-08 141401.png>)

3. Installing all required dependencies from `requirements.txt` using `pip install -r requirements.txt`.
![Installing requirements](<Screenshot 2025-11-08 141436.png>)

4. Executing the main training script using `python src/train.py`.
![Executing training script](<Screenshot 2025-11-08 142340.png>) 

The script ran successfully, created the `models/` directory, and saved the trained model and output plots, confirming the baseline functionality.


## Task 3: Unit Tests (pytest)

**Description of Work:**

A `tests/` directory was created to hold unit tests. The `pytest` framework was chosen for this task and added to `requirements.txt`.

A test file `tests/test_model.py` was created with three meaningful unit tests:

1. `test_load_iris_data`: Verifies that the `load_iris_data` function returns four non-empty NumPy arrays for the train/test splits.

2. `test_model_creation`: Ensures that an `IrisClassifier` object can be instantiated successfully.

3. `test_model_training`: Confirms that the `train()` method runs without errors and correctly sets the internal `is_trained` flag to `True`.

Tests were executed locally using `python -m pytest`, which correctly discovered and passed.

![Passing tests](<Screenshot 2025-11-08 152016.png>)

## Task 4: Linting (flake8)

**Description of Work:**

To enforce code quality and style consistency, `flake8` was added to the project.

1. `flake8` was installed via `pip` and added to `requirements.txt`.

2. A `.flake8` configuration file was created at the project root to define custom rules.

3. **Choices Made:** The `max-line-length` was set to `120` (from the restrictive default of 79) for better readability. The `.venv`, `models/`, and `__pycache__` directories were added to the `exclude` list to prevent linting of non-project code.

The linter was run locally with `flake8 .`, which passed with no output, indicating all styling issues were resolved.

**Screenshot(s):**
![Running flake for the first time](<Screenshot 2025-11-08 152450.png>) 
![Running flake after changes](<Screenshot 2025-11-08 153033.png>) 
![git commit](<Screenshot 2025-11-08 153345.png>)

## Task 5: GitHub Actions CI Workflow

**Description of Work:**

A full CI workflow was created at `.github/workflows/ci.yml`.

**How CI Behaves:**
This workflow is configured to run automatically on every `push` to the `master` branch and on every `pull_request` targeting `master`. This ensures that no code can be merged unless it passes all quality checks.

The workflow consists of a single `build` job that runs on an `ubuntu-latest` runner and performs these steps:

1. **Checkout Code:** Fetches the repository's code.

2. **Set up Python:** Installs Python 3.10, matching our development environment.

3. **Install Dependencies:** Caches and installs all packages from `requirements.txt`.

4. **Lint with flake8:** Runs the linter to check for any styling errors.

5. **Test with pytest:** Runs the full test suite.

6. **Build Docker Image:** Builds the Docker image as a final validation step to ensure the `Dockerfile` is correct and the application is buildable.

**Screenshot(s):**
![Adding new file](<Screenshot 2025-11-08 193934.png>)


## Task 6: Containerize the App (Docker)

**Description of Work:**

The application was containerized to ensure a consistent and reproducible runtime environment.

1. **Dockerfile:** A `Dockerfile` was created in the project root.

   * **Choice Made:** The `python:3.10-slim` image was chosen as a base. This provides a minimal, lightweight environment while matching our Python version, resulting in a smaller final image.

   * The `WORKDIR` was set to `/app`.

   * Dependencies were installed *before* copying the source code to leverage Docker's build cache.

   * The final `CMD` was set to `python src/train.py` to run the training script.

![Dockerfile](<Screenshot 2025-11-08 154900.png>)

2. **.dockerignore:** A `.dockerignore` file was added to prevent large, unnecessary files (like `.venv`, `.git`, `models/`, `tests/`) from being copied into the build context. 

3. **Build & Run:** The image was built locally (`docker build -t iris-app .`) and then run using `docker run --rm -v ${PWD}:/app iris-app` to save the output artifacts to the local directory.

![Building an image](<Screenshot 2025-11-08 160256.png>)

![Running the conterazed app](<Screenshot 2025-11-08 162326.png>)

## In the end
After finishing all the tasks including writing this report, I pushed all the changes to the `master` branch. The GitHub Actions workflow ran automatically and successfully, confirming that the CI pipeline is fully functional.

## How to Run This Project

There are two primary methods to run this project:

### Method 1: Local Virtual Environment

1. Clone the repository: `git clone [your-repo-url]`

2. Navigate to the directory: `cd ml-app`

3. Create a virtual environment: `python -m venv .venv`

4. Activate it: `.\.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Mac/Linux)

5. Install dependencies: `pip install -r requirements.txt`

6. Run training: `python src/train.py`

### Method 2: Docker (Recommended)

1. Ensure Docker Desktop is installed and running.

2. Clone the repository.

3. Navigate to the directory.

4. **Build the image:**

   ```bash
   docker build -t iris-app .
5. **Run the container:**
   ```bash
   docker run iris-app