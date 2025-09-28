#!/usr/bin/env python3
"""
Validate Python syntax for all agent files.
"""

import ast
import os
import sys

def validate_file(file_path):
    """Validate Python syntax for a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the AST to check for syntax errors
        ast.parse(content)
        return True, None
    except SyntaxError as e:
        return False, f"Syntax error in {file_path}: {e}"
    except Exception as e:
        return False, f"Error reading {file_path}: {e}"

def main():
    """Main validation function."""
    print("Python LangGraph Agents - Syntax Validation")
    print("=" * 50)
    
    # List of files to validate
    files_to_check = [
        "agents/types.py",
        "agents/chat_agent.py",
        "agents/stockbroker/__init__.py",
        "agents/stockbroker/types.py", 
        "agents/stockbroker/tools.py",
        "agents/trip_planner/__init__.py",
        "agents/trip_planner/types.py",
        "agents/trip_planner/nodes/classify.py",
        "agents/trip_planner/nodes/extraction.py",
        "agents/trip_planner/nodes/tools.py",
        "agents/supervisor/__init__.py",
        "agents/supervisor/types.py",
        "agents/supervisor/nodes/router.py",
        "agents/supervisor/nodes/general_input.py",
        "agents/email_agent/__init__.py",
        "agents/email_agent/types.py",
        "agents/email_agent/nodes/write_email.py",
        "agents/email_agent/nodes/interrupt.py",
        "agents/email_agent/nodes/send_email.py",
        "agents/email_agent/nodes/rewrite_email.py",
        "agents/open_code/__init__.py",
        "agents/open_code/types.py",
        "agents/open_code/nodes/planner.py",
        "agents/open_code/nodes/executor.py",
        "agents/pizza_orderer.py",
        "agents/writer_agent.py",
        "main.py",
        "run.py",
        "test_agents.py"
    ]
    
    all_valid = True
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            is_valid, error = validate_file(file_path)
            if is_valid:
                print(f"✓ {file_path}")
            else:
                print(f"❌ {file_path}: {error}")
                all_valid = False
        else:
            print(f"⚠️  {file_path}: File not found")
    
    print("\n" + "=" * 50)
    if all_valid:
        print("🎉 All files have valid Python syntax!")
    else:
        print("❌ Some files have syntax errors.")
        sys.exit(1)

if __name__ == "__main__":
    main()
