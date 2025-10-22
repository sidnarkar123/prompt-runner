import trimesh
import os

def json_to_glb(json_path, output_dir="outputs/geometry"):
    os.makedirs(output_dir, exist_ok=True)
    mesh = trimesh.creation.box(extents=(10, 20, 5))  # Example box mesh
    case_id = os.path.splitext(os.path.basename(json_path))[0]
    output_file = os.path.join(output_dir, f"{case_id}.glb")
    mesh.export(output_file)
    return output_file
