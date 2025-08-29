"""
Data processing utilities for development projects
"""

import csv
import json
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from pathlib import Path


class DataUtils:
    """Utility class for data processing operations"""
    
    @staticmethod
    def flatten_dict(nested_dict: Dict[str, Any], separator: str = '.') -> Dict[str, Any]:
        """
        Flatten nested dictionary
        
        Args:
            nested_dict: Nested dictionary to flatten
            separator: Separator for nested keys
            
        Returns:
            Flattened dictionary
        """
        def _flatten(obj, parent_key='', sep=separator):
            items = []
            if isinstance(obj, dict):
                for k, v in obj.items():
                    new_key = f"{parent_key}{sep}{k}" if parent_key else k
                    items.extend(_flatten(v, new_key, sep).items())
            else:
                return {parent_key: obj}
            return dict(items)
        
        return _flatten(nested_dict)
    
    @staticmethod
    def unflatten_dict(flat_dict: Dict[str, Any], separator: str = '.') -> Dict[str, Any]:
        """
        Unflatten dictionary back to nested structure
        
        Args:
            flat_dict: Flattened dictionary
            separator: Separator used in keys
            
        Returns:
            Nested dictionary
        """
        result = {}
        for key, value in flat_dict.items():
            keys = key.split(separator)
            d = result
            for k in keys[:-1]:
                if k not in d:
                    d[k] = {}
                d = d[k]
            d[keys[-1]] = value
        return result
    
    @staticmethod
    def merge_dicts(*dicts: Dict[str, Any], deep: bool = True) -> Dict[str, Any]:
        """
        Merge multiple dictionaries
        
        Args:
            *dicts: Dictionaries to merge
            deep: Whether to perform deep merge
            
        Returns:
            Merged dictionary
        """
        if not dicts:
            return {}
        
        result = {}
        for d in dicts:
            if deep:
                for key, value in d.items():
                    if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                        result[key] = DataUtils.merge_dicts(result[key], value, deep=True)
                    else:
                        result[key] = value
            else:
                result.update(d)
        return result
    
    @staticmethod
    def filter_dict(data: Dict[str, Any], keys: List[str], include: bool = True) -> Dict[str, Any]:
        """
        Filter dictionary keys
        
        Args:
            data: Dictionary to filter
            keys: Keys to include or exclude
            include: If True, include only specified keys; if False, exclude them
            
        Returns:
            Filtered dictionary
        """
        if include:
            return {k: v for k, v in data.items() if k in keys}
        else:
            return {k: v for k, v in data.items() if k not in keys}
    
    @staticmethod
    def clean_data(data: List[Dict[str, Any]], 
                   remove_empty: bool = True,
                   remove_none: bool = True,
                   strip_strings: bool = True) -> List[Dict[str, Any]]:
        """
        Clean data by removing empty/none values and stripping strings
        
        Args:
            data: List of dictionaries to clean
            remove_empty: Remove empty strings
            remove_none: Remove None values
            strip_strings: Strip whitespace from strings
            
        Returns:
            Cleaned data
        """
        cleaned = []
        for item in data:
            cleaned_item = {}
            for key, value in item.items():
                # Strip strings
                if strip_strings and isinstance(value, str):
                    value = value.strip()
                
                # Skip empty or None values if requested
                if remove_empty and value == '':
                    continue
                if remove_none and value is None:
                    continue
                
                cleaned_item[key] = value
            cleaned.append(cleaned_item)
        return cleaned
    
    @staticmethod
    def group_by(data: List[Dict[str, Any]], key: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Group list of dictionaries by a key
        
        Args:
            data: List of dictionaries
            key: Key to group by
            
        Returns:
            Dictionary with grouped data
        """
        grouped = {}
        for item in data:
            group_key = item.get(key)
            if group_key not in grouped:
                grouped[group_key] = []
            grouped[group_key].append(item)
        return grouped
    
    @staticmethod
    def sort_by(data: List[Dict[str, Any]], key: str, reverse: bool = False) -> List[Dict[str, Any]]:
        """
        Sort list of dictionaries by a key
        
        Args:
            data: List of dictionaries
            key: Key to sort by
            reverse: Sort in descending order
            
        Returns:
            Sorted list
        """
        return sorted(data, key=lambda x: x.get(key, ''), reverse=reverse)
    
    @staticmethod
    def csv_to_dict(file_path: Union[str, Path], encoding: str = 'utf-8') -> List[Dict[str, Any]]:
        """
        Read CSV file and convert to list of dictionaries
        
        Args:
            file_path: Path to CSV file
            encoding: File encoding
            
        Returns:
            List of dictionaries
        """
        data = []
        with open(file_path, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(dict(row))
        return data
    
    @staticmethod
    def dict_to_csv(data: List[Dict[str, Any]], 
                    file_path: Union[str, Path], 
                    encoding: str = 'utf-8') -> None:
        """
        Write list of dictionaries to CSV file
        
        Args:
            data: List of dictionaries
            file_path: Output CSV file path
            encoding: File encoding
        """
        if not data:
            return
        
        # Ensure parent directory exists
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        fieldnames = data[0].keys()
        with open(file_path, 'w', newline='', encoding=encoding) as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    
    @staticmethod
    def paginate(data: List[Any], page_size: int = 10, page: int = 1) -> Dict[str, Any]:
        """
        Paginate list data
        
        Args:
            data: List to paginate
            page_size: Items per page
            page: Page number (1-indexed)
            
        Returns:
            Dictionary with pagination info and data
        """
        total_items = len(data)
        total_pages = (total_items + page_size - 1) // page_size
        
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        return {
            'data': data[start_idx:end_idx],
            'pagination': {
                'current_page': page,
                'total_pages': total_pages,
                'page_size': page_size,
                'total_items': total_items,
                'has_next': page < total_pages,
                'has_prev': page > 1,
            }
        }
    
    @staticmethod
    def unique_by_key(data: List[Dict[str, Any]], key: str) -> List[Dict[str, Any]]:
        """
        Get unique items from list based on a key
        
        Args:
            data: List of dictionaries
            key: Key to check for uniqueness
            
        Returns:
            List with unique items
        """
        seen = set()
        unique_data = []
        for item in data:
            value = item.get(key)
            if value not in seen:
                seen.add(value)
                unique_data.append(item)
        return unique_data
    
    @staticmethod
    def validate_required_keys(data: Dict[str, Any], required_keys: List[str]) -> List[str]:
        """
        Validate that dictionary contains required keys
        
        Args:
            data: Dictionary to validate
            required_keys: List of required keys
            
        Returns:
            List of missing keys
        """
        return [key for key in required_keys if key not in data]
    
    @staticmethod
    def extract_values(data: List[Dict[str, Any]], key: str) -> List[Any]:
        """
        Extract values for a specific key from list of dictionaries
        
        Args:
            data: List of dictionaries
            key: Key to extract values for
            
        Returns:
            List of extracted values
        """
        return [item.get(key) for item in data if key in item]
