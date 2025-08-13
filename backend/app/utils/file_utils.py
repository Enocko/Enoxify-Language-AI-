import os
import tempfile
import shutil
from typing import Optional
import magic
from pathlib import Path

class FileUtils:
    """Utility class for file operations"""
    
    @staticmethod
    def create_temp_directory() -> str:
        """Create a temporary directory for processing files"""
        temp_dir = tempfile.mkdtemp(prefix="accessibility_enhancer_")
        return temp_dir
    
    @staticmethod
    def cleanup_temp_directory(temp_dir: str):
        """Clean up temporary directory and its contents"""
        try:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        except Exception as e:
            print(f"Warning: Could not clean up temp directory {temp_dir}: {e}")
    
    @staticmethod
    def get_file_info(file_path: str) -> dict:
        """Get comprehensive file information"""
        try:
            stat = os.stat(file_path)
            file_type = magic.from_file(file_path, mime=True)
            
            return {
                "name": os.path.basename(file_path),
                "path": file_path,
                "size": stat.st_size,
                "type": file_type,
                "extension": Path(file_path).suffix.lower(),
                "created": stat.st_ctime,
                "modified": stat.st_mtime
            }
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def is_safe_file(file_path: str) -> bool:
        """Check if a file is safe to process"""
        dangerous_extensions = ['.exe', '.bat', '.cmd', '.com', '.pif', '.scr', '.vbs', '.js']
        file_ext = Path(file_path).suffix.lower()
        
        return file_ext not in dangerous_extensions
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe storage"""
        # Remove or replace dangerous characters
        dangerous_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        sanitized = filename
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '_')
        
        # Limit length
        if len(sanitized) > 255:
            name, ext = os.path.splitext(sanitized)
            sanitized = name[:255-len(ext)] + ext
        
        return sanitized
    
    @staticmethod
    def ensure_directory_exists(directory_path: str):
        """Ensure a directory exists, create if it doesn't"""
        os.makedirs(directory_path, exist_ok=True)
    
    @staticmethod
    def get_file_size_mb(file_path: str) -> float:
        """Get file size in megabytes"""
        try:
            size_bytes = os.path.getsize(file_path)
            return size_bytes / (1024 * 1024)
        except Exception:
            return 0.0
    
    @staticmethod
    def copy_file_safe(source: str, destination: str) -> bool:
        """Safely copy a file with error handling"""
        try:
            shutil.copy2(source, destination)
            return True
        except Exception as e:
            print(f"Error copying file: {e}")
            return False
    
    @staticmethod
    def move_file_safe(source: str, destination: str) -> bool:
        """Safely move a file with error handling"""
        try:
            shutil.move(source, destination)
            return True
        except Exception as e:
            print(f"Error moving file: {e}")
            return False
