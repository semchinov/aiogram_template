# Aiogram Bot Template

A modern, well-structured template for Telegram bots using aiogram 3.x framework.

## Features

- 🚀 **Modern aiogram 3.x** - Built with the latest version of aiogram
- 📦 **Modular Structure** - Organized code with separate modules for handlers, middlewares, filters, and keyboards
- ⚙️ **Environment Configuration** - Easy configuration management using environment variables
- 🔒 **Admin System** - Built-in admin filter for privileged commands
- 🛡️ **Throttling Protection** - Anti-spam middleware to prevent abuse
- 📝 **Logging** - Comprehensive logging system with file and console output
- 🐳 **Docker Support** - Ready-to-use Docker configuration
- 🎨 **Keyboards** - Examples of both reply and inline keyboards
- 📚 **Well Documented** - Clear code documentation and examples

## Project Structure

```
aiogram_template/
├── bot/
│   ├── handlers/          # Message and command handlers
│   │   ├── commands.py    # Command handlers (/start, /help, etc.)
│   │   └── messages.py    # Message handlers (echo, etc.)
│   ├── middlewares/       # Bot middlewares
│   │   ├── logging.py     # Logging middleware
│   │   └── throttling.py  # Anti-spam middleware
│   ├── filters/           # Custom filters
│   │   └── admin.py       # Admin filter
│   ├── keyboards/         # Keyboard layouts
│   │   ├── reply.py       # Reply keyboards
│   │   └── inline.py      # Inline keyboards
│   ├── utils/             # Utility functions
│   │   └── logger.py      # Logging configuration
│   └── database/          # Database models (optional)
├── config.py              # Configuration management
├── main.py                # Bot entry point
├── requirements.txt       # Python dependencies
├── .env.example           # Example environment variables
├── Dockerfile             # Docker configuration
└── docker-compose.yml     # Docker Compose configuration
```

## Quick Start

### Prerequisites

- Python 3.11 or higher
- A Telegram Bot Token (get it from [@BotFather](https://t.me/BotFather))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/semchinov/aiogram_template.git
cd aiogram_template
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file from the example:
```bash
cp .env.example .env
```

5. Edit `.env` and add your bot token:
```env
BOT_TOKEN=your_bot_token_here
ADMINS=your_telegram_id
```

6. Run the bot:
```bash
python main.py
```

## Docker Deployment

1. Create a `.env` file with your configuration:
```bash
cp .env.example .env
# Edit .env with your values
```

2. Build and run with Docker Compose:
```bash
docker-compose up -d
```

3. View logs:
```bash
docker-compose logs -f
```

4. Stop the bot:
```bash
docker-compose down
```

## Configuration

All configuration is done through environment variables in the `.env` file:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `BOT_TOKEN` | Your Telegram Bot Token from @BotFather | - | ✅ Yes |
| `ADMINS` | Comma-separated list of admin user IDs | - | ❌ No |
| `DATABASE_URL` | Database connection URL (if using database) | `sqlite+aiosqlite:///./bot.db` | ❌ No |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | `INFO` | ❌ No |
| `RATE_LIMIT` | Rate limit in seconds between messages | `0.5` | ❌ No |

## Adding New Handlers

### Command Handler

Add new commands in `bot/handlers/commands.py`:

```python
@router.message(Command("mycommand"))
async def cmd_mycommand(message: Message):
    await message.answer("Response to mycommand")
```

### Message Handler

Add new message handlers in `bot/handlers/messages.py`:

```python
@router.message(F.text.contains("keyword"))
async def handle_keyword(message: Message):
    await message.answer("You mentioned the keyword!")
```

## Adding Middlewares

Create a new middleware in `bot/middlewares/`:

```python
from aiogram import BaseMiddleware

class MyMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        # Your middleware logic here
        return await handler(event, data)
```

Register it in `main.py`:

```python
dp.message.middleware(MyMiddleware())
```

## Adding Custom Filters

Create a new filter in `bot/filters/`:

```python
from aiogram.filters import Filter
from aiogram.types import Message

class MyFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        # Your filter logic here
        return True
```

Use it in handlers:

```python
@router.message(MyFilter())
async def handle_filtered(message: Message):
    await message.answer("Filter matched!")
```

## Available Commands

- `/start` - Start the bot and show welcome message
- `/help` - Display help information
- `/about` - Show information about the bot

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest
```

### Code Style

This project follows PEP 8 style guide. You can check your code with:

```bash
# Install flake8
pip install flake8

# Run linter
flake8 bot/ main.py config.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Resources

- [aiogram Documentation](https://docs.aiogram.dev/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Python Telegram Bot Examples](https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples)

## Support

If you have any questions or need help, feel free to:
- Open an issue on GitHub
- Check the [aiogram documentation](https://docs.aiogram.dev/)
- Join the [aiogram community](https://t.me/aiogram_en)

## Acknowledgments

- [aiogram](https://github.com/aiogram/aiogram) - The amazing async Telegram Bot framework
- All contributors who help improve this template
