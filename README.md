# DevTools

A comprehensive Python utility library for development tasks. This package provides common utilities for logging, file operations, data processing, and API interactions that you can use across your Python projects.

## Installation

### Install from GitHub

```bash
pip install git+https://github.com/validvar/dev_tooling.git
```

### Install for development

```bash
git clone https://github.com/validvar/dev_tooling.git
cd dev_tooling
pip install -e .
```

### Install with development dependencies

```bash
pip install git+https://github.com/validvar/dev_tooling.git[dev]
```

## Quick Start

```python
from devtools import get_logger, FileUtils, DataUtils, APIUtils

# Logging
logger = get_logger()
logger.info("Hello from devtools!")

# File operations
FileUtils.write_json({"key": "value"}, "data.json")
data = FileUtils.read_json("data.json")

# Data processing
flat_data = DataUtils.flatten_dict({"a": {"b": {"c": 1}}})
print(flat_data)  # {'a.b.c': 1}

# API requests
api = APIUtils(base_url="https://api.example.com")
response = api.get("/users")
```

## Features

### 🪵 Logging (`devtools.logger`)

- **Colored logging** with customizable formatters
- **File and console** output support
- **Development-friendly** log levels and patterns

```python
from devtools import get_logger, setup_logging, DevLogger

# Simple usage
logger = get_logger("myapp")
logger.info("Application started")

# Advanced setup
setup_logging(level="DEBUG", colored=True, log_file="app.log")

# Development logger with shortcuts
dev_log = DevLogger()
dev_log.success("Operation completed successfully")
dev_log.step("Processing data...")
dev_log.timestamp("Current operation")
```

### 📁 File Operations (`devtools.file_utils`)

- **Safe file operations** with automatic directory creation
- **JSON handling** with error handling
- **File information** and search utilities
- **Backup and archive** functionality

```python
from devtools import FileUtils

# JSON operations
data = {"users": [{"id": 1, "name": "John"}]}
FileUtils.write_json(data, "users.json")
loaded_data = FileUtils.read_json("users.json")

# File operations
FileUtils.copy_file("source.txt", "backup.txt")
info = FileUtils.get_file_info("myfile.txt")
print(f"File size: {info['size_mb']} MB")

# Find files
py_files = FileUtils.find_files(".", "*.py", recursive=True)

# Backup with timestamp
backup_path = FileUtils.backup_file("important.txt")
```

### 🔢 Data Processing (`devtools.data_utils`)

- **Dictionary utilities** (flatten, merge, filter)
- **Data cleaning** and validation
- **CSV operations** with pandas-like interface
- **Grouping and sorting** utilities

```python
from devtools import DataUtils

# Dictionary operations
nested = {"user": {"profile": {"name": "John"}}}
flat = DataUtils.flatten_dict(nested)
print(flat)  # {"user.profile.name": "John"}

# Data cleaning
raw_data = [{"name": "  John  ", "age": None}, {"name": "", "age": 25}]
cleaned = DataUtils.clean_data(raw_data, remove_empty=True, remove_none=True)

# Grouping and filtering
data = [{"type": "A", "value": 1}, {"type": "B", "value": 2}, {"type": "A", "value": 3}]
grouped = DataUtils.group_by(data, "type")
sorted_data = DataUtils.sort_by(data, "value", reverse=True)

# CSV operations
DataUtils.dict_to_csv(data, "output.csv")
loaded_csv = DataUtils.csv_to_dict("output.csv")
```

### 🌐 API Utilities (`devtools.api_utils`)

- **HTTP client** with automatic retries
- **Authentication helpers** (Bearer, API Key, Basic)
- **File upload/download** functionality
- **Response parsing** utilities

```python
from devtools import APIUtils

# Initialize with base URL
api = APIUtils(base_url="https://jsonplaceholder.typicode.com")

# Authentication
api.set_auth('bearer', token='your-token')
api.set_headers({'User-Agent': 'MyApp/1.0'})

# Make requests
response = api.get("/posts")
data = APIUtils.parse_response(response, 'json')

# POST with JSON
new_post = {"title": "Test", "body": "Content", "userId": 1}
response = api.post("/posts", json_data=new_post)

# File operations
api.download_file("https://example.com/file.pdf", "local_file.pdf")
api.upload_file("/upload", "document.pdf")

# URL validation
if APIUtils.is_valid_url("https://example.com"):
    print("Valid URL")
```

## Advanced Usage

### Custom Logger with File Output

```python
from devtools import setup_logging

# Setup with custom format and file output
logger = setup_logging(
    level="DEBUG",
    format_str="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    colored=True,
    log_file="app.log"
)
```

### Data Pipeline Example

```python
from devtools import FileUtils, DataUtils, get_logger

logger = get_logger()

# Read CSV data
data = DataUtils.csv_to_dict("input.csv")
logger.info(f"Loaded {len(data)} records")

# Clean and process
cleaned = DataUtils.clean_data(data)
grouped = DataUtils.group_by(cleaned, "category")

# Save results
for category, items in grouped.items():
    output_file = f"output_{category}.json"
    FileUtils.write_json(items, output_file)
    logger.success(f"Saved {len(items)} items to {output_file}")
```

### API Integration Example

```python
from devtools import APIUtils, get_logger, FileUtils

logger = get_logger()
api = APIUtils(base_url="https://api.github.com")

# Set authentication
api.set_auth('bearer', token='your-github-token')

# Fetch user repositories
response = api.get("/user/repos")
if response.status_code == 200:
    repos = response.json()
    logger.success(f"Found {len(repos)} repositories")
    
    # Save to file
    FileUtils.write_json(repos, "my_repos.json")
else:
    logger.error(f"Failed to fetch repos: {response.status_code}")
```

## Development

### Running Tests

```bash
pip install -e .[dev]
pytest
```

### Code Formatting

```bash
black devtools/
flake8 devtools/
mypy devtools/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### v0.1.0
- Initial release
- Logger utilities with colored output
- File operations with JSON/CSV support
- Data processing utilities
- HTTP/API client with retries and authentication
