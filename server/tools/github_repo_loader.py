from langchain_community.document_loaders import GitLoader
import os
from server.exception.exception import CustomException
from server.logging.logger import logging

import shutil
import uuid

def get_codebase_from_github(repo_url: str, branch: str = 'main'):
    """ Helper tool node to retrieve github documents from repository and return codebase as string"""
    try:
        # Using a unique ID ensures parallel audits don't crash each other
        # REPO PAth for storing in local machine
        unique_id = str(uuid.uuid4())[:8]
        repo_path = f'./temp_repo_{unique_id}'
        
        # FIX: If the directory exists, remove it to allow a fresh clone
        if os.path.exists(repo_path):
            logging.info(f"Clearing existing directory: {repo_path}")
            shutil.rmtree(repo_path)
            
        logging.info(f'Cloning {repo_url} into {repo_path}')
        git_loader = GitLoader(
            clone_url=repo_url,
            repo_path=repo_path,
            branch=branch,
            file_filter=lambda file_path: file_path.endswith((".js", ".py", ".cpp", ".ts", ".tsx", ".jsx", ".java"))
        )
        
        docs = git_loader.load()
        full_code = ""
        for doc in docs:
            full_code += f"// FILE: {doc.metadata['file_path']}\n"
            full_code += doc.page_content + "\n\n"
        
        return full_code
    except Exception as e:
        logging.error(f"Error while loading github repository: {str(e)}")
        raise e
    