# mock-up: real implementation should talk to local Mistral model
def query_mistral(prompt):
    # Basic mock for testing purposes
    if "Fuel" in prompt:
        return "This document relates to the fuel system of a marine diesel engine."
    return "No clear category found."
