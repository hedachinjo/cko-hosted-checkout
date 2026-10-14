#Imporating path Class from pathlib module
from pathlib import Path

#Grabs directory containing main.py
PROJECT_DIR = Path(__file__).resolve().parent

#Main function to test python, and break off rust
def main():
    print("Checkout.com Hosted Checkout Demo")
    print("--------------------------------")
    print("Good to go!")

    env_file = PROJECT_DIR / ".env"

    if env_file.exists():
        print("Environment file: Found")
    else:
        print("Environment file: Missing")

main()
