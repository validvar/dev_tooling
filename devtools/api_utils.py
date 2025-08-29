"""
API and HTTP utilities for development projects
"""

import json
import time
from typing import Dict, Any, Optional, Union
from urllib.parse import urljoin, urlparse
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class APIUtils:
    """Utility class for API and HTTP operations"""
    
    def __init__(self, base_url: Optional[str] = None, timeout: int = 30):
        """
        Initialize API utils with base URL and default timeout
        
        Args:
            base_url: Base URL for API requests
            timeout: Default timeout for requests
        """
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        
        # Configure retries
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def set_headers(self, headers: Dict[str, str]) -> None:
        """
        Set default headers for all requests
        
        Args:
            headers: Headers dictionary
        """
        self.session.headers.update(headers)
    
    def set_auth(self, auth_type: str, **kwargs) -> None:
        """
        Set authentication for requests
        
        Args:
            auth_type: Type of authentication ('basic', 'bearer', 'api_key')
            **kwargs: Authentication parameters
        """
        if auth_type == 'basic':
            username = kwargs.get('username')
            password = kwargs.get('password')
            if username and password:
                self.session.auth = (username, password)
        
        elif auth_type == 'bearer':
            token = kwargs.get('token')
            if token:
                self.session.headers['Authorization'] = f'Bearer {token}'
        
        elif auth_type == 'api_key':
            api_key = kwargs.get('api_key')
            header_name = kwargs.get('header_name', 'X-API-Key')
            if api_key:
                self.session.headers[header_name] = api_key
    
    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint"""
        if self.base_url and not endpoint.startswith(('http://', 'https://')):
            return urljoin(self.base_url.rstrip('/') + '/', endpoint.lstrip('/'))
        return endpoint
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """
        Make GET request
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            **kwargs: Additional arguments for requests
            
        Returns:
            Response object
        """
        url = self._build_url(endpoint)
        return self.session.get(url, params=params, timeout=self.timeout, **kwargs)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, 
             json_data: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """
        Make POST request
        
        Args:
            endpoint: API endpoint
            data: Form data
            json_data: JSON data
            **kwargs: Additional arguments for requests
            
        Returns:
            Response object
        """
        url = self._build_url(endpoint)
        return self.session.post(url, data=data, json=json_data, timeout=self.timeout, **kwargs)
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """
        Make PUT request
        
        Args:
            endpoint: API endpoint
            data: Form data
            json_data: JSON data
            **kwargs: Additional arguments for requests
            
        Returns:
            Response object
        """
        url = self._build_url(endpoint)
        return self.session.put(url, data=data, json=json_data, timeout=self.timeout, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Make DELETE request
        
        Args:
            endpoint: API endpoint
            **kwargs: Additional arguments for requests
            
        Returns:
            Response object
        """
        url = self._build_url(endpoint)
        return self.session.delete(url, timeout=self.timeout, **kwargs)
    
    def request_with_retry(self, method: str, endpoint: str, max_retries: int = 3,
                          backoff_factor: float = 1.0, **kwargs) -> Optional[requests.Response]:
        """
        Make request with custom retry logic
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            max_retries: Maximum number of retries
            backoff_factor: Backoff multiplier
            **kwargs: Additional arguments for requests
            
        Returns:
            Response object or None if all retries failed
        """
        for attempt in range(max_retries + 1):
            try:
                response = self.session.request(method, self._build_url(endpoint), 
                                             timeout=self.timeout, **kwargs)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                if attempt == max_retries:
                    raise e
                time.sleep(backoff_factor * (2 ** attempt))
        return None
    
    def download_file(self, url: str, file_path: str, chunk_size: int = 8192) -> bool:
        """
        Download file from URL
        
        Args:
            url: File URL
            file_path: Local file path to save
            chunk_size: Chunk size for streaming download
            
        Returns:
            True if download successful
        """
        try:
            response = self.session.get(url, stream=True, timeout=self.timeout)
            response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
            return True
        except Exception:
            return False
    
    def upload_file(self, endpoint: str, file_path: str, field_name: str = 'file',
                   additional_data: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Upload file to endpoint
        
        Args:
            endpoint: Upload endpoint
            file_path: Path to file to upload
            field_name: Form field name for file
            additional_data: Additional form data
            
        Returns:
            Response object
        """
        url = self._build_url(endpoint)
        files = {field_name: open(file_path, 'rb')}
        data = additional_data or {}
        
        try:
            return self.session.post(url, files=files, data=data, timeout=self.timeout)
        finally:
            files[field_name].close()
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """
        Check if URL is valid
        
        Args:
            url: URL to validate
            
        Returns:
            True if URL is valid
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    @staticmethod
    def parse_response(response: requests.Response, 
                      expected_format: str = 'json') -> Union[Dict[str, Any], str, bytes]:
        """
        Parse response based on expected format
        
        Args:
            response: Response object
            expected_format: Expected format ('json', 'text', 'bytes')
            
        Returns:
            Parsed response data
        """
        if expected_format == 'json':
            try:
                return response.json()
            except json.JSONDecodeError:
                return {'error': 'Invalid JSON response', 'content': response.text}
        elif expected_format == 'text':
            return response.text
        elif expected_format == 'bytes':
            return response.content
        else:
            return response.text
    
    @staticmethod
    def build_query_string(params: Dict[str, Any]) -> str:
        """
        Build query string from parameters
        
        Args:
            params: Parameters dictionary
            
        Returns:
            Query string
        """
        from urllib.parse import urlencode
        return urlencode({k: v for k, v in params.items() if v is not None})
    
    def close(self) -> None:
        """Close session"""
        self.session.close()
