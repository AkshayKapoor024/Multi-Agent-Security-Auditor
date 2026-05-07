from langchain_community.document_loaders import GitLoader
import os
from server.exception.exception import CustomException
from server.logger.logger import logging

import os
import shutil
import stat
import uuid
import sys

def remove_readonly(func, path, excinfo):
    """Clear the readonly bit and reattempt the removal."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def get_codebase_from_github(repo_url: str, branch: str = 'main'):
    repo_path = "" # Initialize to avoid UnboundLocalError
    try:
        unique_id = str(uuid.uuid4())[:8]
        repo_path = os.path.abspath(f'./temp_repo_{unique_id}')
        
        # Fresh start
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path, onerror=remove_readonly)
            
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
        logging.info('Successfuly fetched codebase from github and sent to mapper')
        # Explicitly delete the loader reference to release file handles
        del git_loader
        return full_code

    except Exception as e:
        logging.error(f"Error while loading github repository: {str(e)}")
        raise CustomException(e,sys)
    finally:
        if repo_path and os.path.exists(repo_path):
            try:
                # Use onerror to handle permission/read-only issues in .git folders
                shutil.rmtree(repo_path, onerror=remove_readonly)
                logging.info(f"Successfully deleted temporary directory: {repo_path}")
            except Exception as cleanup_error:
                logging.warning(f"Failed to clean up {repo_path}: {str(cleanup_error)}")