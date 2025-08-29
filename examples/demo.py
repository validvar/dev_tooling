#!/usr/bin/env python3
"""
Demo script showing devtools functionality
"""

from devtools import get_logger, FileUtils, DataUtils, APIUtils, DevLogger


def main():
    """Demonstrate devtools features"""
    
    # Setup logging
    logger = get_logger("demo")
    dev_log = DevLogger("demo")
    
    dev_log.step("Starting devtools demo")
    
    # File operations demo
    dev_log.step("Demonstrating file operations")
    
    sample_data = {
        "users": [
            {"id": 1, "name": "John Doe", "email": "john@example.com"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
        ],
        "config": {
            "app_name": "Demo App",
            "version": "1.0.0",
            "debug": True
        }
    }
    
    # Write JSON
    FileUtils.write_json(sample_data, "demo_data.json")
    dev_log.success("Created demo_data.json")
    
    # Read it back
    loaded_data = FileUtils.read_json("demo_data.json")
    logger.info(f"Loaded {len(loaded_data['users'])} users")
    
    # Data processing demo
    dev_log.step("Demonstrating data processing")
    
    # Flatten nested data
    flat_config = DataUtils.flatten_dict(sample_data["config"])
    logger.info(f"Flattened config: {flat_config}")
    
    # Process user data
    users = sample_data["users"]
    sorted_users = DataUtils.sort_by(users, "name")
    logger.info(f"Users sorted by name: {[u['name'] for u in sorted_users]}")
    
    # Group by domain
    users_with_domain = []
    for user in users:
        domain = user["email"].split("@")[1]
        users_with_domain.append({**user, "domain": domain})
    
    grouped = DataUtils.group_by(users_with_domain, "domain")
    for domain, domain_users in grouped.items():
        logger.info(f"Domain {domain}: {len(domain_users)} users")
    
    # API demo (using a public API)
    dev_log.step("Demonstrating API operations")
    
    api = APIUtils(base_url="https://jsonplaceholder.typicode.com")
    api.set_headers({"User-Agent": "DevTools-Demo/1.0"})
    
    try:
        response = api.get("/posts", params={"_limit": 3})
        if response.status_code == 200:
            posts = APIUtils.parse_response(response, "json")
            logger.info(f"Fetched {len(posts)} posts from API")
            
            # Save API data
            FileUtils.write_json(posts, "api_posts.json")
            dev_log.success("Saved API posts to api_posts.json")
        else:
            logger.warning(f"API request failed: {response.status_code}")
    except Exception as e:
        logger.error(f"API demo failed: {e}")
    finally:
        api.close()
    
    # Cleanup demo
    dev_log.step("Cleaning up demo files")
    
    demo_files = ["demo_data.json", "api_posts.json"]
    for file_path in demo_files:
        if FileUtils.delete_file(file_path):
            logger.info(f"Deleted {file_path}")
    
    dev_log.success("Demo completed successfully!")


if __name__ == "__main__":
    main()
