import os
import sys
import subprocess
import time
from colorama import init, Fore, Style

init(autoreset=True)

def create_directory(path):
    os.makedirs(path, exist_ok=True)

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)

def generate_bot_structure(project_name, is_big_project):
    # Create main directory
    create_directory(project_name)

    # Create subdirectories
    create_directory(f'{project_name}/handlers')
    if is_big_project:
        create_directory(f'{project_name}/keyboards')
        create_directory(f'{project_name}/middlewares')
        create_directory(f'{project_name}/models')
        create_directory(f'{project_name}/services')
        create_directory(f'{project_name}/utils')
        create_directory(f'{project_name}/alembic/versions')

    # Write files
    write_file(f'{project_name}/bot.py', '''
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
    asyncio.run(main())
''')

    write_file(f'{project_name}/config.py', '''
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bot.db')
''')

    write_file(f'{project_name}/handlers/__init__.py', '')

    write_file(f'{project_name}/handlers/user.py', '''
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.reply("Welcome! How can I help you?")

def register_handlers(dp: Dispatcher):
    dp.include_router(router)
''')

    if is_big_project:
        write_file(f'{project_name}/database.py', '''
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
''')

        write_file(f'{project_name}/keyboards/reply.py', '''
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Help"))
    return keyboard
''')

        write_file(f'{project_name}/models/base.py', '''
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base
import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
''')

        write_file(f'{project_name}/middlewares/__init__.py', '')

        write_file(f'{project_name}/middlewares/throttling.py', '''
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
''')

        write_file(f'{project_name}/utils/__init__.py', '')

        write_file(f'{project_name}/utils/logger.py', '''
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
''')

    write_file(f'{project_name}/requirements.txt', '''
aiogram==3.13.0
python-dotenv==1.0.0
SQLAlchemy==2.0.23
alembic==1.13.0
colorama==0.4.6
tqdm==4.66.1
cachetools==5.3.2
''')

def install_requirements(project_name):
    requirements_file = os.path.join(project_name, 'requirements.txt')
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])

def loading_animation(duration):
    for _ in range(int(duration / 0.1)):
        for char in '|/-\\':
            sys.stdout.write(f'\r{Fore.CYAN}Loading {char}')
            sys.stdout.flush()
            time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * 20 + '\r')
    sys.stdout.flush()

def print_welcome():
    print(f"{Fore.CYAN}Welcome to the Telegram Bot Generator!{Style.RESET_ALL}")

def print_project_name_prompt():
    return input(f"{Fore.YELLOW}Enter your project name: {Style.RESET_ALL}")

def print_project_size_prompt():
    while True:
        project_size = input(f"{Fore.YELLOW}Is this a big project? (y/n): {Style.RESET_ALL}").lower()
        if project_size in ['y', 'n']:
            return project_size == 'y'
        else:
            print(f"{Fore.RED}Invalid input. Please enter 'y' or 'n'.{Style.RESET_ALL}")

def print_generating_structure():
    print(f"{Fore.CYAN}Generating project structure...{Style.RESET_ALL}")

def print_structure_generated(project_name):
    print(f"{Fore.GREEN}✅ Telegram bot structure for {project_name} generated successfully!{Style.RESET_ALL}")

def print_installing_libraries():
    print(f"{Fore.CYAN}Installing required libraries...{Style.RESET_ALL}")

def print_libraries_installed():
    print(f"{Fore.GREEN}✅ Required libraries installed successfully!{Style.RESET_ALL}")

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
    is_big_project = print_project_size_prompt()

    print_generating_structure()
    loading_animation(3)
    generate_bot_structure(project_name, is_big_project)
    print_structure_generated(project_name)

    print_installing_libraries()
    loading_animation(5)
    install_requirements(project_name)
    print_libraries_installed()

    print_next_steps(project_name)

if __name__ == '__main__':
    main()