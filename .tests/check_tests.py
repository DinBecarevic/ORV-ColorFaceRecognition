import os
import sys

def check_test_files():
    """Preveri, ali obstajajo testne datoteke v direktoriju skripte"""
    # Get the directory this script is in
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # List test files in the script directory
    test_files = [f for f in os.listdir(script_dir) if f.startswith('test_') and f.endswith('.py')]
    
    if not test_files:
        print("NAPAKA: Ne najdem testnih datotek s predpono 'test_'", file=sys.stderr)
        return False
    
    print(f"Najdene testne datoteke: {', '.join(test_files)}")
    return True

if __name__ == "__main__":
    if not check_test_files():
        sys.exit(1)  # Vrni napako, če ni testnih datotek
    sys.exit(0)  # Vrni uspeh, če so testne datoteke najdene