How to Set It Up
Create a Script Wrapper: Create a small script that can be globally accessible by adding a symlink to your path (on Linux/Mac) or a batch file (on Windows). Alternatively, you can install it using pip as an entry point.

Example Setup Using setup.py: Create a setup.py in the project directory:

python
Copy code
from setuptools import setup, find_packages

setup(
    name='telegram-bot-generator',
    version='1.0',
    py_modules=['bot_generator'],
    install_requires=[
        'aiogram==3.13.0',
        'python-dotenv==1.0.0',
        'SQLAlchemy==2.0.23',
        'alembic==1.13.0',
        'colorama==0.4.6',
        'tqdm==4.66.1',
        'cachetools==5.3.2',
    ],
    entry_points={
        'console_scripts': [
            'at=bot_generator:cli_main',
        ],
    },
)
Install the Package: Run this command to install it as a global command:

bash
Copy code
pip install .
Now You Can Use the Commands:

To create a new bot project: at create
For help: at --help
README File Code
markdown
Copy code
# Telegram Bot Project Generator

This tool helps you to quickly generate the project structure for a Telegram bot using Python's `aiogram` library. You can use this tool to set up a small or large bot project with all necessary files and dependencies automatically generated.

## Features
- Create a modular project structure for your Telegram bot.
- Support for both simple and advanced bots.
- Automatic dependency installation.
- Ready-to-use files for handlers, configuration, and more.
- Option to include middlewares, database setup, and other utilities for larger projects.

## Installation

1. Clone this repository:
   ```bash
   git clone <repository_url>
Navigate to the directory:

bash
Copy code
cd <repository_directory>
Install the tool:

bash
Copy code
pip install .
Usage
After installation, you can use the following command to generate a Telegram bot project:

Create a New Project
bash
Copy code
at create
The tool will ask you for the project name and whether it's a big project (with middlewares, database setup, etc.).

Get Help
bash
Copy code
at --help
This will display help information about the available commands.

Next Steps After Project Generation
Navigate to your project directory:

bash
Copy code
cd <project_name>
Create a virtual environment:

bash
Copy code
python -m venv venv
Activate the virtual environment:

Windows: venv\Scripts\activate
macOS/Linux: source venv/bin/activate
Install any remaining dependencies:

bash
Copy code
pip install -r requirements.txt
Add your bot token in a .env file:

env
Copy code
BOT_TOKEN=your_bot_token_here
Run the bot:

bash
Copy code
python bot.py
License
Feel free to modify and distribute this project under the MIT License.

arduino
Copy code

This setup should allow you to easily generate and run a Telegram bot project by using the `at create` command.
