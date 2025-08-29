"""
File and directory utilities for development projects
"""

import os
import json
import shutil
import zipfile
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from datetime import datetime


class FileUtils:
    """Utility class for file and directory operations"""
    
    @staticmethod
    def ensure_dir(path: Union[str, Path]) -> Path:
        """
        Ensure directory exists, create if it doesn't
        
        Args:
            path: Directory path
            
        Returns:
            Path object
        """
        path_obj = Path(path)
        path_obj.mkdir(parents=True, exist_ok=True)
        return path_obj
    
    @staticmethod
    def read_json(file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Read JSON file safely
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Parsed JSON data
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file not found: {file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {file_path}: {e}")
    
    @staticmethod
    def write_json(data: Dict[str, Any], file_path: Union[str, Path], indent: int = 2) -> None:
        """
        Write data to JSON file
        
        Args:
            data: Data to write
            file_path: Output file path
            indent: JSON indentation
        """
        FileUtils.ensure_dir(Path(file_path).parent)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
    
    @staticmethod
    def read_lines(file_path: Union[str, Path], encoding: str = 'utf-8') -> List[str]:
        """
        Read all lines from a text file
        
        Args:
            file_path: Path to file
            encoding: File encoding
            
        Returns:
            List of lines
        """
        with open(file_path, 'r', encoding=encoding) as f:
            return [line.rstrip('\n\r') for line in f]
    
    @staticmethod
    def write_lines(lines: List[str], file_path: Union[str, Path], encoding: str = 'utf-8') -> None:
        """
        Write lines to a text file
        
        Args:
            lines: List of lines to write
            file_path: Output file path
            encoding: File encoding
        """
        FileUtils.ensure_dir(Path(file_path).parent)
        with open(file_path, 'w', encoding=encoding) as f:
            f.write('\n'.join(lines))
    
    @staticmethod
    def copy_file(src: Union[str, Path], dst: Union[str, Path]) -> None:
        """
        Copy file from source to destination
        
        Args:
            src: Source file path
            dst: Destination file path
        """
        FileUtils.ensure_dir(Path(dst).parent)
        shutil.copy2(src, dst)
    
    @staticmethod
    def move_file(src: Union[str, Path], dst: Union[str, Path]) -> None:
        """
        Move file from source to destination
        
        Args:
            src: Source file path
            dst: Destination file path
        """
        FileUtils.ensure_dir(Path(dst).parent)
        shutil.move(src, dst)
    
    @staticmethod
    def delete_file(file_path: Union[str, Path]) -> bool:
        """
        Delete file if it exists
        
        Args:
            file_path: Path to file
            
        Returns:
            True if file was deleted, False if it didn't exist
        """
        path_obj = Path(file_path)
        if path_obj.exists():
            path_obj.unlink()
            return True
        return False
    
    @staticmethod
    def get_file_info(file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Get file information
        
        Args:
            file_path: Path to file
            
        Returns:
            Dictionary with file information
        """
        path_obj = Path(file_path)
        if not path_obj.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        stat = path_obj.stat()
        return {
            'name': path_obj.name,
            'path': str(path_obj.absolute()),
            'size': stat.st_size,
            'size_mb': round(stat.st_size / (1024 * 1024), 2),
            'created': datetime.fromtimestamp(stat.st_ctime),
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'is_file': path_obj.is_file(),
            'is_dir': path_obj.is_dir(),
            'extension': path_obj.suffix,
        }
    
    @staticmethod
    def find_files(directory: Union[str, Path], pattern: str = "*", recursive: bool = True) -> List[Path]:
        """
        Find files matching pattern in directory
        
        Args:
            directory: Directory to search
            pattern: Glob pattern
            recursive: Whether to search recursively
            
        Returns:
            List of matching file paths
        """
        path_obj = Path(directory)
        if recursive:
            return list(path_obj.rglob(pattern))
        else:
            return list(path_obj.glob(pattern))
    
    @staticmethod
    def zip_directory(directory: Union[str, Path], output_file: Union[str, Path]) -> None:
        """
        Create zip file from directory
        
        Args:
            directory: Directory to zip
            output_file: Output zip file path
        """
        FileUtils.ensure_dir(Path(output_file).parent)
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in FileUtils.find_files(directory):
                if file_path.is_file():
                    arcname = file_path.relative_to(directory)
                    zipf.write(file_path, arcname)
    
    @staticmethod
    def backup_file(file_path: Union[str, Path], backup_dir: Optional[Union[str, Path]] = None) -> Path:
        """
        Create a backup of a file with timestamp
        
        Args:
            file_path: File to backup
            backup_dir: Directory for backup (default: same as original file)
            
        Returns:
            Path to backup file
        """
        path_obj = Path(file_path)
        if not path_obj.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if backup_dir is None:
            backup_dir = path_obj.parent
        else:
            backup_dir = Path(backup_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{path_obj.stem}_{timestamp}{path_obj.suffix}"
        backup_path = backup_dir / backup_name
        
        FileUtils.copy_file(file_path, backup_path)
        return backup_path
