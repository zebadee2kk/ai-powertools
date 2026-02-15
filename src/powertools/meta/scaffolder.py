import os
from pathlib import Path

class Scaffolder:
    """
    The 'Tool that builds the Tools'. 
    Automates the creation of standardized PowerTools modules.
    """
    
    def __init__(self, base_path: str = "src/powertools"):
        self.base_path = Path(base_path)

    def create_component(self, name: str, summary: str):
        """Creates a standardized folder and file structure for a new component."""
        component_path = self.base_path / name
        component_path.mkdir(parents=True, exist_ok=True)
        
        # Create standard files
        (component_path / "__init__.py").touch()
        
        core_code = f"\"\"\"\n{name}\n\n{summary}\n\"\"\"\n\ndef main():\n    pass\n"
        with open(component_path / "core.py", "w") as f:
            f.write(core_code)
            
        print(f"✅ Component '{name}' scaffolded at {component_path}")

if __name__ == "__main__":
    # Example usage
    sf = Scaffolder()
    # sf.create_component("new_tool", "A demonstration tool")
