# Contributing to AES File Encryptor

Thank you for your interest in contributing to the AES File Encryptor project! This document provides guidelines and instructions for contributing.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inclusive environment for all contributors, regardless of experience level, background, or identity.

### Expected Behavior
- Be respectful and considerate
- Use welcoming and inclusive language
- Accept constructive criticism gracefully
- Focus on what's best for the project
- Show empathy towards other contributors

### Unacceptable Behavior
- Harassment or discriminatory language
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information
- Other unprofessional conduct

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/dfizzy247/aes-file-encryptor.git
   cd aes-file-encryptor
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/ORIGINAL-OWNER/aes-file-encryptor.git
   ```

## How to Contribute

### Types of Contributions

1. **Bug Fixes**
   - Fix existing issues
   - Improve error handling
   - Resolve security vulnerabilities

2. **Feature Development**
   - Implement new features from the roadmap
   - Enhance existing functionality
   - Improve user experience

3. **Documentation**
   - Improve README and guides
   - Add code comments
   - Create tutorials or examples

4. **Testing**
   - Write unit tests
   - Perform security testing
   - Test on different platforms

5. **UI/UX Improvements**
   - Enhance visual design
   - Improve accessibility
   - Optimize user workflows

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Git
- Virtual environment tool

### Setup Steps

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

3. **Run the application**:
   ```bash
   python run.py
   ```

4. **Run tests** (when available):
   ```bash
   pytest tests/
   ```

## Coding Standards

### Python Style Guide
Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide:

- **Indentation**: 4 spaces (no tabs)
- **Line Length**: Maximum 100 characters
- **Naming Conventions**:
  - Functions/variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_CASE`

### Code Quality

1. **Type Hints**:
   ```python
   def encrypt_data(data: bytes, password: str) -> bytes:
       """Encrypt data using AES-256-GCM."""
       pass
   ```

2. **Docstrings**:
   ```python
   def function_name(param1: type, param2: type) -> return_type:
       """
       Brief description of function.
       
       Args:
           param1: Description of param1
           param2: Description of param2
           
       Returns:
           Description of return value
           
       Raises:
           ExceptionType: When this exception is raised
       """
       pass
   ```

3. **Error Handling**:
   ```python
   try:
       # Risky operation
       result = encrypt_data(data, password)
   except ValueError as e:
       # Specific exception handling
       logger.error(f"Encryption failed: {e}")
       raise
   except Exception as e:
       # General exception handling
       logger.error(f"Unexpected error: {e}")
       raise
   ```

### Security Guidelines

1. **Never hardcode secrets**:
   ```python
   # ❌ Bad
   API_KEY = "sk_live_123456789"
   
   # ✅ Good
   API_KEY = os.environ.get("API_KEY")
   ```

2. **Validate user input**:
   ```python
   def process_file(file_path: str) -> None:
       if not os.path.exists(file_path):
           raise FileNotFoundError(f"File not found: {file_path}")
       if not os.path.isfile(file_path):
           raise ValueError(f"Not a file: {file_path}")
   ```

3. **Use secure random generation**:
   ```python
   import os
   salt = os.urandom(16)  # Cryptographically secure
   ```

## Testing Guidelines

### Writing Tests

1. **Unit Tests**:
   ```python
   import unittest
   from backend.crypto import encrypt_data, decrypt_data
   
   class TestEncryption(unittest.TestCase):
       def test_encrypt_decrypt_cycle(self):
           """Test that encryption and decryption are reversible."""
           original_data = b"Test data"
           password = "secure_password"
           
           encrypted = encrypt_data(original_data, password)
           decrypted = decrypt_data(encrypted, password)
           
           self.assertEqual(original_data, decrypted)
   ```

2. **Test Coverage**:
   - Aim for at least 80% code coverage
   - Test edge cases and error conditions
   - Test with various file types and sizes

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov=frontend

# Run specific test file
pytest tests/test_crypto.py

# Run with verbose output
pytest -v
```

## Pull Request Process

### Before Submitting

1. **Update your fork**:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**:
   - Write clean, documented code
   - Follow coding standards
   - Add tests for new features

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```
   
   **Commit Message Format**:
   - `Add:` New feature or functionality
   - `Fix:` Bug fix
   - `Update:` Modify existing feature
   - `Remove:` Delete code or feature
   - `Docs:` Documentation changes
   - `Test:` Add or modify tests
   - `Refactor:` Code refactoring

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

### Submitting Pull Request

1. Go to the original repository on GitHub
2. Click "New Pull Request"
3. Select your fork and branch
4. Fill out the PR template:
   - **Title**: Clear, concise description
   - **Description**: Detailed explanation of changes
   - **Related Issues**: Link to related issues
   - **Testing**: Describe how you tested
   - **Screenshots**: If UI changes

### PR Review Process

1. **Automated Checks**:
   - Code style validation
   - Test suite execution
   - Security scanning

2. **Code Review**:
   - At least one maintainer review required
   - Address all review comments
   - Make requested changes

3. **Merge**:
   - Maintainer will merge when approved
   - Your contribution will be credited

## Reporting Bugs

### Before Reporting

1. **Check existing issues**: Search for similar reports
2. **Verify the bug**: Ensure it's reproducible
3. **Gather information**: Collect relevant details

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Windows 10]
- Python Version: [e.g., 3.9.5]
- Application Version: [e.g., 1.0.0]

**Screenshots**
If applicable

**Additional Context**
Any other relevant information
```

## Suggesting Enhancements

### Enhancement Proposal Template

```markdown
**Feature Description**
Clear description of the proposed feature

**Problem Statement**
What problem does this solve?

**Proposed Solution**
How should it work?

**Alternatives Considered**
Other approaches you've thought about

**Additional Context**
Mockups, examples, or references
```

## Development Workflow

### Branch Naming Convention
- `feature/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `docs/documentation-update` - Documentation
- `refactor/code-improvement` - Code refactoring
- `test/test-addition` - Test additions

### Version Control Best Practices

1. **Commit Often**: Make small, logical commits
2. **Write Good Messages**: Clear, descriptive commit messages
3. **Keep History Clean**: Rebase before merging if needed
4. **Don't Commit Secrets**: Never commit passwords or API keys

## Questions?

If you have questions about contributing:

1. **Check Documentation**: Review README and wiki
2. **Search Issues**: Look for similar questions
3. **Ask in Discussions**: Use GitHub Discussions
4. **Contact Maintainers**: Reach out directly if needed

## Recognition

Contributors will be:
- Listed in the project's contributors page
- Credited in release notes
- Acknowledged in the README

Thank you for contributing to AES File Encryptor! 🎉
