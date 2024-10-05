# **Telegram Bot Project Generator**

This tool helps you quickly set up a project structure for a Telegram bot using Python's `aiogram` library. It generates all the necessary files and dependencies, allowing you to focus on your bot's logic rather than its setup.

## **Features**
* Modular project structure for scalable Telegram bots.
* Suitable for both simple and complex bot projects.
* Automatic installation of dependencies.
* Pre-configured files for handlers, configurations, and more.
* Optional middlewares, database setup, and utility integrations for larger bots.

---

## **Installation**

### 1. Clone the Repository
```bash
git clone <repository_url>
```
## 2. Navigate to the Project Directory
```bash
cd <repository_directory>
```

## 3. Install the Tool
```bash
pip install aiotemp
```


## Usage
Once installed, you can generate a Telegram bot project using the following commands:

## Create a New Project
```bash
at create
```

- The tool will prompt for the project name and whether you'd like to include middlewares, database setup, and other utilities (for larger projects).

## Get Help
```bash
at --help
```
 - Displays available commands and usage details.

## Next Steps After Project Generation
1. Navigate to the Project Directory
```bash
cd <project_name>
```

## 2. Set Up a Virtual Environment
```bash
python -m venv venv
```

##3. Activate the Virtual Environment:
Windows:
```bash
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```
## 4. Install Remaining Dependencies:
```bash
pip install -r requirements.txt
```

## 5. Add Your Bot Token
Create a .env file in the project root and add your bot token:
```plaintext
BOT_TOKEN=your_bot_token_here
```
6. Run the Bot
```bash
python bot.py
```
## Development Setup
If you'd like to set this up as a global tool, follow these steps:

## 1. Create a Script Wrapper
Linux/macOS: Create a small script and add a symlink to your $PATH.
Windows: Create a batch file.
Alternatively, use pip to install the tool as a global command.

## 2. Example setup.py Configuration
Here’s an example of the setup.py file for this project:

```python

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
```

## 3. Install the Package
Run the following command to install the package globally:
```bash
pip install aiotemplate
```

## License
This project is licensed under the MIT License. Feel free to modify and distribute the code as per the license terms.


