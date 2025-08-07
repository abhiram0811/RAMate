# Contributing to RAMate

Thank you for your interest in contributing to RAMate! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/RAMate.git
   cd RAMate
   ```
3. **Set up the development environment** following the README instructions

## Development Workflow

### Backend Development
1. Create a virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. Initialize the system:
   ```bash
   python setup.py
   python app.py
   ```

### Frontend Development
1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start development server:
   ```bash
   npm run dev
   ```

## Making Changes

1. **Create a new branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards below

3. **Test your changes** thoroughly:
   ```bash
   # Backend testing
   cd backend
   python test_api.py
   
   # Frontend testing
   cd frontend
   npm run build
   ```

4. **Commit your changes** with clear messages:
   ```bash
   git add .
   git commit -m "Add: feature description"
   ```

5. **Push to your fork** and create a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```

## Coding Standards

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Include docstrings for all functions and classes
- Handle errors gracefully with try-catch blocks
- Use meaningful variable and function names

### TypeScript/JavaScript (Frontend)
- Use TypeScript for type safety
- Follow React best practices
- Use functional components with hooks
- Include proper error handling
- Write responsive, accessible code

## Pull Request Guidelines

### Before Submitting
- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] Documentation is updated if needed
- [ ] No sensitive information (API keys, passwords) in code
- [ ] Branch is up to date with main branch

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Other (please describe)

## Testing
- [ ] Backend tests pass
- [ ] Frontend builds successfully
- [ ] Manual testing completed

## Screenshots (if applicable)
Include screenshots for UI changes
```

## Issue Reporting

When reporting bugs or requesting features, please include:

### For Bugs
- **Environment**: OS, Python version, Node.js version
- **Steps to reproduce**: Clear, numbered steps
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Error messages**: Full error output if any
- **Screenshots**: If applicable

### For Feature Requests
- **Problem description**: What problem does this solve?
- **Proposed solution**: How should it work?
- **Alternatives considered**: Other approaches you've thought of
- **Additional context**: Any other relevant information

## Code Review Process

1. All pull requests require review before merging
2. Reviewers will check for:
   - Code quality and style
   - Functionality and correctness
   - Security considerations
   - Performance implications
   - Documentation completeness

3. Address reviewer feedback promptly
4. Once approved, maintainers will merge the PR

## Development Tips

### Debugging
- Use Flask debug mode for backend development
- Check browser console for frontend errors
- Monitor API responses in Network tab
- Use print statements or logging for troubleshooting

### Performance
- Profile slow queries in the RAG pipeline
- Optimize embedding generation for large documents
- Consider caching for frequently accessed data
- Monitor memory usage during development

### Security
- Never commit API keys or sensitive data
- Validate all user inputs
- Use HTTPS in production
- Follow security best practices for Flask and Next.js

## Getting Help

- **Documentation**: Check the README files in backend/ and frontend/
- **Issues**: Search existing issues before creating new ones
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Contact**: Reach out to maintainers for urgent issues

## License

By contributing to RAMate, you agree that your contributions will be licensed under the same license as the project.

Thank you for contributing to RAMate! 🚀
