from pathlib import Path
from app import connexion_app

if __name__ == '__main__':
  connexion_app.run(f"{Path(__file__).stem}:connexion_app")
