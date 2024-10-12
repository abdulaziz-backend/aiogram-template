import os
import sys
import subprocess
import time
from colorama import init, Fore, Style
from tqdm import tqdm

init(autoreset=True)

def create_directory(path):
    os.makedirs(path, exist_ok=True)

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)

def generate_bot_structure(project_name, project_size):
    # Create main directory
    create_directory(project_name)

    # Create subdirectories
    create_directory(f'{project_name}/handlers')
    if project_size in ['middle', 'pro']:
        create_directory(f'{project_name}/keyboards')
        create_directory(f'{project_name}/middlewares')
        create_directory(f'{project_name}/models')
        create_directory(f'{project_name}/services')
        create_directory(f'{project_name}/utils')
    if project_size == 'pro':
        create_directory(f'{project_name}/alembic/versions')
        create_directory(f'{project_name}/tests')
        create_directory(f'{project_name}/config')

    # Write files
    write_file(f'{project_name}/bot.py', get_bot_content(project_size))
    write_file(f'{project_name}/config.py', get_config_content(project_size))
    write_file(f'{project_name}/handlers/__init__.py', '')
    write_file(f'{project_name}/handlers/user.py', get_user_handler_content(project_size))

    if project_size in ['middle', 'pro']:
        write_file(f'{project_name}/database.py', get_database_content())
        write_file(f'{project_name}/keyboards/reply.py', get_keyboard_content())
        write_file(f'{project_name}/models/base.py', get_model_content())
        write_file(f'{project_name}/middlewares/__init__.py', '')
        write_file(f'{project_name}/middlewares/throttling.py', get_throttling_middleware_content())
        write_file(f'{project_name}/utils/__init__.py', '')
        write_file(f'{project_name}/utils/logger.py', get_logger_content())

    if project_size == 'pro':
        write_file(f'{project_name}/alembic.ini', get_alembic_ini_content())
        write_file(f'{project_name}/tests/test_handlers.py', get_test_handlers_content())
        write_file(f'{project_name}/config/production.py', get_production_config_content())
        write_file(f'{project_name}/config/development.py', get_development_config_content())

    write_file(f'{project_name}/requirements.txt', get_requirements_content(project_size))

def get_bot_content(project_size):
    content = '''
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import user

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Register handlers
user.register_handlers(dp)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    print("This bot was created by abdulaziz")
    print("Subscribe to this channel: @pythonnews_uzbekistan")
    asyncio.run(main())
'''
    return content

def get_config_content(project_size):
    content = '''
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bot.db')
'''
    return content

def get_user_handler_content(project_size):
    content = '''
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.reply("Welcome! How can I help you?")

def register_handlers(dp: Dispatcher):
    dp.include_router(router)
'''
    return content

def get_database_content():
    return '''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''

def get_keyboard_content():
    return '''
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Help"))
    return keyboard
'''

def get_model_content():
    return '''
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base
import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
'''

def get_throttling_middleware_content():
    return '''
from aiogram import BaseMiddleware
from aiogram.types import Message
from cachetools import TTLCache

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit=0.5):
        self.cache = TTLCache(maxsize=10000, ttl=rate_limit)

    async def __call__(self, handler, event: Message, data):
        if event.from_user.id in self.cache:
            return
        
        self.cache[event.from_user.id] = None
        return await handler(event, data)
'''

def get_logger_content():
    return '''
import logging

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler('bot.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
'''

def get_alembic_ini_content():
    return '''
# A generic, single database configuration.

[alembic]
# path to migration scripts
script_location = alembic

# template used to generate migration files
# file_template = %%(rev)s_%%(slug)s

# timezone to use when rendering the date
# within the migration file as well as the filename.
# string value is passed to dateutil.tz.gettz()
# leave blank for localtime
# timezone =

# max length of characters to apply to the
# "slug" field
# truncate_slug_length = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
# sourceless = false

# version location specification; this defaults
# to alembic/versions.  When using multiple version
# directories, initial revisions must be specified with --version-path
# version_locations = %(here)s/bar %(here)s/bat alembic/versions

# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8

sqlalchemy.url = driver://user:pass@localhost/dbname


[post_write_hooks]
# post_write_hooks defines scripts or Python functions that are run
# on newly generated revision scripts.  See the documentation for further
# detail and examples

# format using "black" - use the console_scripts runner, against the "black" entrypoint
# hooks=black
# black.type=console_scripts
# black.entrypoint=black
# black.options=-l 79

# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
'''

def get_test_handlers_content():
    return '''
import pytest
from aiogram.types import Message
from handlers.user import cmd_start

@pytest.mark.asyncio
async def test_cmd_start():
    message = Message(text="/start")
    result = await cmd_start(message)
    assert "Welcome" in result.text
'''

def get_production_config_content():
    return '''
import os

BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
DEBUG = False
'''

def get_development_config_content():
    return '''
BOT_TOKEN = 'your_bot_token_here'
DATABASE_URL = 'sqlite:///bot.db'
DEBUG = True
'''

def get_requirements_content(project_size):
    content = '''
aiogram==3.13.0
python-dotenv==1.0.0
colorama==0.4.6
tqdm==4.66.1
'''
    if project_size in ['middle', 'pro']:
        content += '''
SQLAlchemy==2.0.23
alembic==1.13.0
cachetools==5.3.2
'''
    if project_size == 'pro':
        content += '''
pytest==7.4.3
pytest-asyncio==0.21.1
'''
    return content

def install_requirements(project_name):
    requirements_file = os.path.join(project_name, 'requirements.txt')
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])

def loading_animation(duration):
    for _ in tqdm(range(int(duration * 10)), desc="Processing", ncols=70, bar_format="{l_bar}{bar}"):
        time.sleep(0.1)

def print_welcome():
    print(f"{Fore.CYAN}Welcome to the Telegram Bot Generator!{Style.RESET_ALL}")

def print_project_name_prompt():
    return input(f"{Fore.YELLOW}Enter your project name: {Style.RESET_ALL}")

def print_project_size_prompt():
    while True:
        project_size = input(f"{Fore.YELLOW}Choose project size (small/middle/pro): {Style.RESET_ALL}").lower()
        if project_size in ['small', 'middle', 'pro']:
            return project_size
        else:
            print(f"{Fore.RED}Invalid input. Please enter 'small', 'middle', or 'pro'.{Style.RESET_ALL}")

def print_generating_structure():
    print(f"{Fore.CYAN}Generating project structure...{Style.RESET_ALL}")

def print_structure_generated(project_name):
    print(f"{Fore.GREEN} Telegram bot structure for {project_name} generated successfully!{Style.RESET_ALL}")

def print_installing_libraries():
    print(f"{Fore.CYAN}Installing required libraries...{Style.RESET_ALL}")

def print_libraries_installed():
    print(f"{Fore.GREEN} Required libraries installed successfully!{Style.RESET_ALL}")

def print_next_steps(project_name):
    print(f"\n{Fore.CYAN}Next steps:{Style.RESET_ALL}")
    print(f"1. cd {project_name}")
    print("2. Create a virtual environment:")
    print("   python -m venv venv")
    print("3. Activate your virtual environment:")
    print("   - On Windows: venv\\Scripts\\activate")
    print("   - On macOS and Linux: source venv/bin/activate")
    print("4. Create a .env file and add your BOT_TOKEN")
    print("5. Run the bot: python bot.py")

def main():
    print_welcome()
    
    project_name = print_project_name_prompt()
    project_size = print_project_size_prompt()

    print_generating_structure()
    loading_animation(3)
    generate_bot_structure(project_name, project_size)
    print_structure_generated(project_name)

    print_installing_libraries()
    loading_animation(5)
    install_requirements(project_name)
    print_libraries_installed()

    print_next_steps(project_name)

if __name__ == '__main__':
    main()
