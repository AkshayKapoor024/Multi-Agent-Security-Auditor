import uuid 
import subprocess
import os 
from server.logger.logger import logging
import tempfile
import ast
import sys
import importlib.util

# Modules to ignore from downloading in sandbox container
IGNORE_MODULES = {
    "os",
    "sys",
    "json",
    "subprocess",
    "pathlib",
    "re",
    "time",
    "typing",
    "datetime",
    "collections",
    "asyncio",
    "math",
    "random",
    "tempfile",
    "uuid",
    "logging",
    "numpy",
    "pandas",
    "sklearn",
    "torch",
    "tensorflow"
}

# Helper function to extract imports from the codebase
def extract_imports(code: str):
    tree = ast.parse(code)

    modules = set()

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):

            for alias in node.names:
                modules.add(alias.name.split(".")[0])

        elif isinstance(node, ast.ImportFrom):

            if node.module:
                modules.add(node.module.split(".")[0])

    return list(modules)


# Main tool for running code in the python sandbox isolated container 
def execute_code_in_sandbox(code:str):
    """Tool that executes a possible buggy code in a docker sandbox container and returns error or output as per execution"""
    logging.info('Started Building File paths!')
    # Creating temporary file id 
    file_id = str(uuid.uuid4())
    
    # Creating local file path
    local_file = os.path.join(tempfile.gettempdir(), f"{file_id}.py")
    
    # Creating file path for sandbox where we need to copy this file 
    sandbox_file = f'/app/{file_id}.py'
    
    try:
        
        # Writing code in the local file
        with open(local_file,'w') as f:
            f.write(code)
        logging.info('File written in local system')
            
        # Copying local file into the sandbox
        subprocess.run(
            ['docker','cp', local_file , f'sandbox:{sandbox_file}'],
            check=True
        )
        logging.info('File written in sandbox container')
        
        
        # Extracting imported modules from generated code
        imported_modules = extract_imports(code)

        # Filtering stdlib modules
        required_modules = [
            module for module in imported_modules
            if module not in IGNORE_MODULES
        ]

        logging.info(f'Required external modules: {required_modules}')

        for module in required_modules:

            check_module = subprocess.run(
            [
                'docker',
                'exec',
                'sandbox',
                'python3',
                '-c',
                f'import {module}'
            ],
            capture_output=True,
            text=True
        )

        # Install only if missing
        if check_module.returncode != 0:

            logging.info(f'Installing missing module: {module}')

            install_result = subprocess.run(
                [
                    'docker',
                    'exec',
                    'sandbox',
                    'python3',
                    '-m',
                    'pip',
                    'install',
                    '--user',
                    module
                ],
                capture_output=True,
                text=True
            )

            logging.info(f"INSTALL STDOUT: {install_result.stdout}")
            logging.info(f"INSTALL STDERR: {install_result.stderr}")

            if install_result.returncode != 0:
                raise Exception(install_result.stderr)

            logging.info(f'Successfully installed: {module}')
        
        # Executing the temporary file in sandbox environment
        result = subprocess.run(
            ['docker' , 'exec' , 'sandbox' , 'python3' , sandbox_file],
            capture_output=True,
            text=True,
            timeout=5
        )
        logging.info('Code executed in sandbox')
        
        # Returning sandbox error or result
        logging.info('Returned result')
        return {
            'stdout':result.stdout,
            'stderr':result.stderr,
            'exit_code':result.returncode
        }
        
    except subprocess.TimeoutExpired:
        logging.info('error')
        return{
            'error':'Execution Timed out'
        }
    finally :
         # Removing temp file from local device
        if os.path.exists(local_file):
            os.remove(local_file)
        
        # Removing temp file from docker container
        subprocess.run(
            ['docker','exec','sandbox','rm',sandbox_file]
        )

    