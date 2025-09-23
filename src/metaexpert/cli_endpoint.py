"""CLI endpoint for parsing command-line arguments."""

import sys
from io import StringIO
from typing import Any, Dict, List

from metaexpert._argument import parse_arguments


def parse_cli_arguments(request: dict[str, Any]) -> Dict[str, Any]:
    """Parse command-line arguments and return the parsed configuration.

    Args:
        request: Dictionary containing arguments and program name
        
    Returns:
        Dictionary with status and parsed arguments or errors
    """
    try:
        # Extract arguments and program name from request
        arguments: List[str] = request.get("arguments", [])
        program_name: str = request.get("program_name", "metaexpert")
        
        # Save original sys.argv and stderr
        original_argv = sys.argv
        original_stderr = sys.stderr
        
        # Capture stderr output
        stderr_capture = StringIO()
        
        # Set sys.argv to simulate command-line arguments
        sys.argv = [program_name] + arguments
        sys.stderr = stderr_capture
        
        try:
            # Parse arguments using the existing parser
            parsed_args = parse_arguments()
            
            # Convert parsed arguments to dictionary
            parsed_dict = vars(parsed_args)
            
            # Restore original sys.argv and stderr
            sys.argv = original_argv
            sys.stderr = original_stderr
            
            return {
                "status": "success",
                "parsed_arguments": parsed_dict,
                "errors": []
            }
        except SystemExit:
            # This happens when argparse encounters an error
            # Get the captured error message
            error_output = stderr_capture.getvalue()

            # Restore original sys.argv and stderr
            sys.argv = original_argv
            sys.stderr = original_stderr
            
            return {
                "status": "error",
                "parsed_arguments": {},
                "errors": [error_output.strip()]
            }
        except Exception as e:
            # Restore original sys.argv and stderr
            sys.argv = original_argv
            sys.stderr = original_stderr
            
            return {
                "status": "error",
                "parsed_arguments": {},
                "errors": [str(e)]
            }
    except Exception as e:
        return {
            "status": "error",
            "parsed_arguments": {},
            "errors": [f"Failed to parse CLI arguments: {str(e)}"]
        }