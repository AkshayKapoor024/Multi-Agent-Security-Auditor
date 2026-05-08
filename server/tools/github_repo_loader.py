from langchain_community.document_loaders import GitLoader
import os
from server.exception.exception import CustomException
from server.logger.logger import logging

import os
import shutil
import stat
import uuid
import sys

import gc
import time

def remove_readonly(func, path, excinfo):
    """Clear the readonly bit and reattempt the removal."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def get_codebase_from_github(repo_url: str, branch: str = 'main'):
    repo_path = "" 
    try:
        unique_id = str(uuid.uuid4())[:8]
        # Store in a 'temp' subfolder to keep root clean
        repo_path = os.path.abspath(f'./temp/temp_repo_{unique_id}')
        
        # Ensure the temp parent directory exists
        os.makedirs('./temp', exist_ok=True)

        logging.info(f'Cloning {repo_url} into {repo_path}')
        git_loader = GitLoader(
            clone_url=repo_url,
            repo_path=repo_path,
            branch=branch,
            file_filter=lambda f: f.endswith((".js", ".py", ".cpp", ".ts", ".tsx", ".jsx", ".java"))
        )
        
        docs = git_loader.load()
        
        full_code = ""
        for doc in docs:
            full_code += f"// FILE: {doc.metadata['file_path']}\n"
            full_code += doc.page_content + "\n\n"
        
        # --- CRITICAL FIX START ---
        # 1. Manually trigger garbage collection to release GitPython handles
        del git_loader
        gc.collect() 
        # 2. Short sleep to let the OS release file locks
        time.sleep(0.1) 
        # --- CRITICAL FIX END ---

        logging.info('Successfully fetched codebase from github')
        return full_code

    except Exception as e:
        logging.error(f"Error while loading github repository: {str(e)}")
        raise CustomException(e,sys)
    finally:
        if repo_path and os.path.exists(repo_path):
            try:
                # Re-attempting removal with a small delay if it fails
                for i in range(3): # Try 3 times
                    try:
                        shutil.rmtree(repo_path, onerror=remove_readonly)
                        logging.info(f"Successfully deleted temporary directory: {repo_path}")
                        break
                    except Exception:
                        time.sleep(0.2)
            except Exception as cleanup_error:
                logging.warning(f"Failed to clean up {repo_path}: {str(cleanup_error)}")