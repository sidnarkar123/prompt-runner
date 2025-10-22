def prompt_to_spec(prompt):
    prompt = prompt.lower()
    if "control room" in prompt:
        return {"scene":"Sci-Fi Control Room","elements":["holographic displays","sliding doors"],"lighting":"neon blue","theme":"futuristic industrial"}
    elif "kitchen" in prompt:
        return {"scene":"Modern Kitchen","elements":["island","stainless steel appliances"],"lighting":"warm white","theme":"contemporary"}
    else:
        return {"scene":"Generic Scene","elements":[],"lighting":"default","theme":"neutral"}
