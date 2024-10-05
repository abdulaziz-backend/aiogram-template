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
git clone https://github.com/abdulaziz-backend/aiogram-template.git
```
## 2. Navigate to the Project Directory
```bash
cd <repository_directory>
```


## Usage
Once installed, you can generate a Telegram bot project using the following commands:

## Create a New Project
```bash
py manage.py
```

- The tool will prompt for the project name and whether you'd like to include middlewares, database setup, and other utilities (for larger projects).



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

