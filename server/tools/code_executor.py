import uuid 
import subprocess
import os 
from server.logging.logger import logging
import tempfile

# Main tool for running code in the python sandbox isolated container 
def execute_code_in_sandbox(code:str):
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

    