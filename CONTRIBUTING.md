# Contributing to Aiogram Bot Template

Thank you for considering contributing to this project! Here are some guidelines to help you get started.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/aiogram_template.git
   cd aiogram_template
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env with your test bot token
   ```

## Code Style

- Follow PEP 8 style guide
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions small and focused
- Use meaningful variable names

## Making Changes

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes
3. Test your changes thoroughly
4. Commit your changes:
   ```bash
   git commit -m "Add your descriptive commit message"
   ```

5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Create a Pull Request

## Pull Request Guidelines

- Describe what your PR does
- Link any related issues
- Make sure your code follows the existing style
- Test your changes
- Update documentation if needed

## Reporting Issues

When reporting issues, please include:
- A clear description of the problem
- Steps to reproduce
- Expected behavior
- Actual behavior
- Your environment (OS, Python version, aiogram version)

## Questions?

Feel free to open an issue for any questions or clarifications!
