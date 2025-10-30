"""
Script to generate connector code from configuration files
"""
import yaml
from pathlib import Path
from connector_platform.core.code_generator import CodeGenerator

def main():
    generator = CodeGenerator()
    config_dir = Path("platform/config/connectors")
    
    if not config_dir.exists():
        print("Connector config directory not found!")
        return
    
    for config_file in config_dir.glob("*.yaml"):
        print(f"Processing {config_file.name}...")
        
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        connector_name = config.get("name")
        
        python_code = generator.generate_connector_code(config, language="python")
        python_path = generator.save_generated_code(python_code, connector_name, language="python")
        print(f"  Generated Python connector: {python_path}")
        
        try:
            go_code = generator.generate_connector_code(config, language="go")
            go_path = generator.save_generated_code(go_code, connector_name, language="go")
            print(f"  Generated Go connector: {go_path}")
        except Exception as e:
            print(f"  Warning: Could not generate Go connector: {e}")
    
    print("\nConnector generation complete!")

if __name__ == "__main__":
    main()
