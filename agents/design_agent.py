def prompt_to_spec(prompt):
    # This function simulates the generation of a structured JSON specification
    # based on the user prompt. In a real implementation, this would involve
    # more complex logic or integration with an AI model.

    # Example of a simple mapping from prompt to JSON spec
    if "control room" in prompt:
        return {
            "scene": "Sci-Fi Control Room",
            "elements": ["holographic displays", "sliding doors"],
            "lighting": "neon blue",
            "theme": "futuristic industrial"
        }
    elif "kitchen" in prompt:
        return {
            "scene": "Modern Kitchen",
            "elements": ["island", "stainless steel appliances"],
            "lighting": "warm white",
            "theme": "contemporary"
        }
    else:
        return {
            "scene": "Generic Scene",
            "elements": [],
            "lighting": "default",
            "theme": "neutral"
        }