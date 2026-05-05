import re

def clean_llm_code(raw_output: str) -> str:
    """
    Removes Markdown code fences and extracts only the raw Python code.
    """
    # Regex to find content inside ```python ... ``` or ``` ... ```
    # It captures the group between the backticks
    pattern = r"```(?:python|py)?\s*(.*?)\s*```"
    
    # Try to find a match
    match = re.search(pattern, raw_output, re.DOTALL | re.IGNORECASE)
    
    if match:
        # Return the inner code block
        return match.group(1).strip()
    
    # If no backticks were found, just return the stripped raw string
    # (Sometimes the LLM actually follows instructions and gives raw text)
    return raw_output.strip()