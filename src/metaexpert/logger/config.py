from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import List, Optional
import os
from enum import Enum


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogConfiguration(BaseModel):
    """
    Configuration model for the logging system that supports multiple configuration methods
    with priority ordering.
    """
    # Basic configuration
    log_level: str = Field(default="INFO", description="Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
    log_directory: str = Field(default="./logs", description="Directory path for log files")
    expert_log_file: str = Field(default="expert.log", description="Filename for expert logs")
    trades_log_file: str = Field(default="trades.log", description="Filename for trades logs")
    errors_log_file: str = Field(default="errors.log", description="Filename for errors logs")
    
    # Performance configuration
    enable_async: bool = Field(default=False, description="Enable asynchronous logging")
    max_file_size_mb: int = Field(default=10, description="Maximum file size before rotation in MB")
    backup_count: int = Field(default=5, description="Number of backup files to keep")
    
    # Formatting configuration
    enable_structured_logging: bool = Field(default=False, description="Enable RFC 5424 structured JSON format")
    enable_contextual_logging: bool = Field(default=True, description="Enable contextual field inclusion")
    mask_sensitive_data: bool = Field(default=True, description="Enable masking of sensitive information")
    console_log_format: str = Field(default="text", description="Format for console logs (text or json)")
    file_log_format: str = Field(default="json", description="Format for file logs (text or json)")
    
    # Console logging configuration
    log_to_console: bool = Field(default=True, description="Enable console logging")
    
    # Context configuration
    context_fields: List[str] = Field(
        default=["expert_name", "symbol", "trade_id", "order_id", "strategy_id", "account_id"],
        description="List of contextual fields to include"
    )
    
    # Disk space monitoring configuration
    disk_space_check: bool = Field(default=True, description="Enable disk space monitoring and fallback to console when low")
    disk_space_low_threshold_mb: int = Field(default=100, description="Threshold for low disk space in MB")
    
    # Backward compatibility attributes (required by some tests)
    log_file: Optional[str] = Field(default=None, description="Backward compatibility for log_file parameter")
    trade_log_file: Optional[str] = Field(default=None, description="Backward compatibility for trade_log_file parameter")
    error_log_file: Optional[str] = Field(default=None, description="Backward compatibility for error_log_file parameter")
    log_max_file_size: Optional[int] = Field(default=None, description="Backward compatibility for log_max_file_size parameter")
    log_backup_count: Optional[int] = Field(default=None, description="Backward compatibility for log_backup_count parameter")
    async_logging: Optional[bool] = Field(default=None, description="Backward compatibility for async_logging parameter")
    structured_logging: Optional[bool] = Field(default=None, description="Backward compatibility for structured_logging parameter")
    
    @field_validator('log_level')
    def validate_log_level(cls, v):
        # Convert to uppercase for comparison
        upper_v = v.upper()
        # Check if it's a valid log level
        if upper_v not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            raise ValueError('log_level must be one of DEBUG, INFO, WARNING, ERROR, CRITICAL')
        
        # Only allow uppercase in the final value
        if v != upper_v:
            raise ValueError('log_level must be in uppercase: DEBUG, INFO, WARNING, ERROR, CRITICAL')
        
        return v
    
    @field_validator('max_file_size_mb')
    def validate_max_file_size_mb(cls, v):
        if v < 1 or v > 1000:
            raise ValueError('max_file_size_mb must be between 1 and 1000')
        return v
    
    @field_validator('backup_count')
    def validate_backup_count(cls, v):
        if v < 1 or v > 100:
            raise ValueError('backup_count must be between 1 and 100')
        return v
    
    @field_validator('console_log_format', 'file_log_format')
    def validate_format_type(cls, v):
        if v not in ['text', 'json']:
            raise ValueError('Format type must be either "text" or "json"')
        return v
    
    class Config:
        env_prefix = 'LOG_'  # This will allow reading from environment variables like LOG_LEVEL
        case_sensitive = False
        # Allow extra fields from environment variables
        extra = 'ignore'
    
    def __init__(self, **data):
        # Apply environment variables as defaults, but allow explicit parameters to override
        env_data = {}
        
        # Environment variable mappings based on our API contract
        env_mappings = {
            'log_level': 'LOG_LEVEL',
            'log_directory': 'LOG_DIRECTORY',
            'expert_log_file': 'EXPERT_LOG_FILE',
            'trades_log_file': 'TRADES_LOG_FILE',
            'errors_log_file': 'ERRORS_LOG_FILE',
            'enable_async': 'ENABLE_ASYNC',
            'max_file_size_mb': 'MAX_FILE_SIZE_MB',
            'backup_count': 'BACKUP_COUNT',
            'enable_structured_logging': 'ENABLE_STRUCTURED_LOGGING',
            'enable_contextual_logging': 'ENABLE_CONTEXTUAL_LOGGING',
            'mask_sensitive_data': 'MASK_SENSITIVE_DATA',
            'console_log_format': 'CONSOLE_LOG_FORMAT',
            'file_log_format': 'FILE_LOG_FORMAT',
            'disk_space_check': 'DISK_SPACE_CHECK',
            'disk_space_low_threshold_mb': 'DISK_SPACE_LOW_THRESHOLD_MB',
        }
        
        for field, env_var in env_mappings.items():
            env_value = os.getenv(env_var)
            if env_value is not None and field not in data:
                # Convert string values to appropriate types
                if field in ['enable_async', 'enable_structured_logging', 'enable_contextual_logging', 'mask_sensitive_data', 'disk_space_check']:
                    env_data[field] = env_value.lower() in ['true', '1', 'yes', 'on']
                elif field in ['max_file_size_mb', 'backup_count', 'disk_space_low_threshold_mb']:
                    try:
                        env_data[field] = int(env_value)
                    except ValueError:
                        raise ValueError(f"Environment variable {env_var} must be an integer")
                else:
                    env_data[field] = env_value
        
        # Handle backward compatibility parameters
        # Map old parameter names to new ones
        backward_compat_mapping = {
            'log_file': 'expert_log_file',
            'trade_log_file': 'trades_log_file',
            'error_log_file': 'errors_log_file',
            'log_max_file_size': 'max_file_size_mb',
            'log_backup_count': 'backup_count',
            'async_logging': 'enable_async',
            'structured_logging': 'enable_structured_logging',
        }
        
        # Apply backward compatibility mapping
        for old_param, new_param in backward_compat_mapping.items():
            if old_param in data and new_param not in data:
                data[new_param] = data[old_param]
        
        # Merge environment data with provided data (provided data takes precedence)
        env_data.update(data)
        super().__init__(**env_data)