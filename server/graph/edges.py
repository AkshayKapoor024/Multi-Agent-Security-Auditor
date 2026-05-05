from langgraph.types import Send
from server.graph.state import AuditState
import json

# Conditional node function to send to verifier
def continue_to_verification(state: AuditState):
    """
    Fan-out function: 
    Takes the list of vulnerabilities and spawns parallel verifiers.
    """
    # Retrieve the latest list of vulnerabilities from the state
    vulns = state["vulnerabilities_logs"]
    
    # If no vulnerability generate audit report instead
    if len(vulns) <=0:
        return "reporter"

    # Send each vulnerability to a separate verifier node instance
    return [
        Send("verifier", {
            "current_code": state["current_code"],
            "latest_vulnerability": json.dumps(v) # Send 1 vuln as a string
        }) 
        for v in vulns
    ]