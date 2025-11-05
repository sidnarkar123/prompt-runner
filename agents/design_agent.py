# agents/design_agent.py
import logging
import re
from typing import Dict
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def extract_numbers(text: str, keyword: str, default: float = None) -> float:
    """Extract number following a keyword from text"""
    pattern = rf"{keyword}\s*[:\-=]?\s*(\d+\.?\d*)"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return float(match.group(1))
    return default

def prompt_to_spec(prompt: str) -> Dict:
    """
    Enhanced prompt -> spec translator supporting both scene-based and urban planning specs.
    Detects building parameters from prompts and generates complete specifications.
    """
    prompt_l = prompt.lower()

    # Check if urban planning / building design prompt
    building_keywords = ["building", "floor", "height", "plot", "residential", "commercial", 
                         "fsi", "far", "setback", "mumbai", "ahmedabad", "pune", "nashik"]
    
    is_building_prompt = any(kw in prompt_l for kw in building_keywords)
    
    if is_building_prompt:
        # Urban planning / building specification
        spec = {
            "type": "building_specification",
            "parameters": {
                "height_m": extract_numbers(prompt, r"height", 20.0),
                "width_m": extract_numbers(prompt, r"width|plot width", 30.0),
                "depth_m": extract_numbers(prompt, r"depth|plot depth", 20.0),
                "setback_m": extract_numbers(prompt, r"setback", 3.0),
                "floor_height_m": extract_numbers(prompt, r"floor height", 3.0),
                "fsi": extract_numbers(prompt, r"fsi|far", 1.5),
            },
            "building_type": "residential" if "residential" in prompt_l else 
                           "commercial" if "commercial" in prompt_l else
                           "mixed" if "mixed" in prompt_l else "residential",
            "city": "Mumbai" if "mumbai" in prompt_l else
                   "Ahmedabad" if "ahmedabad" in prompt_l else
                   "Pune" if "pune" in prompt_l else
                   "Nashik" if "nashik" in prompt_l else "Generic",
            "description": prompt,
            "meta": {
                "generated_by": "design_agent_v2",
                "generated_at": datetime.utcnow().isoformat() + "Z",
                "confidence": 0.8
            }
        }
        
        # Calculate derived parameters
        plot_area = spec["parameters"]["width_m"] * spec["parameters"]["depth_m"]
        fsi = spec["parameters"]["fsi"]
        max_built_up_area = plot_area * fsi
        floor_height = spec["parameters"]["floor_height_m"]
        height = spec["parameters"]["height_m"]
        max_floors = int(height / floor_height)
        
        spec["parameters"]["plot_area_sqm"] = round(plot_area, 2)
        spec["parameters"]["max_built_up_area_sqm"] = round(max_built_up_area, 2)
        spec["parameters"]["max_floors"] = max_floors
        spec["parameters"]["actual_height_m"] = max_floors * floor_height
        
        logging.info(f"Building spec created: {max_floors} floors, {height}m height, {spec['city']}")
        
    else:
        # Scene-based specification (original functionality)
        if "control room" in prompt_l:
            spec = {
                "type": "scene",
                "scene": "Sci-Fi Control Room", 
                "elements": ["holographic displays", "sliding doors"], 
                "lighting": "neon blue", 
                "theme": "futuristic industrial"
            }
        elif "kitchen" in prompt_l:
            spec = {
                "type": "scene",
                "scene": "Modern Kitchen", 
                "elements": ["island", "stainless steel appliances"], 
                "lighting": "warm white", 
                "theme": "contemporary"
            }
        else:
            # Default building spec
            spec = {
                "type": "building_specification",
                "parameters": {
                    "height_m": 20.0,
                    "width_m": 30.0,
                    "depth_m": 20.0,
                    "setback_m": 3.0,
                    "floor_height_m": 3.0,
                    "fsi": 1.5,
                    "plot_area_sqm": 600.0,
                    "max_built_up_area_sqm": 900.0,
                    "max_floors": 6,
                    "actual_height_m": 18.0
                },
                "building_type": "residential",
                "city": "Generic",
                "description": prompt,
                "meta": {
                    "generated_by": "design_agent_v2",
                    "generated_at": datetime.utcnow().isoformat() + "Z",
                    "confidence": 0.5
                }
            }

        spec["meta"] = spec.get("meta", {
            "generated_by": "design_agent_v2", 
            "confidence": 0.5,
            "generated_at": datetime.utcnow().isoformat() + "Z"
        })
        
    logging.info("Spec created for prompt: %s", prompt)
    return spec
