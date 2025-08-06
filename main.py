import yaml
import json
import requests
import time
from typing import List, Tuple

INPUT_FILE = "input.yaml"
PAIRS_FILE = "Pairs.json"
ANKI_CONNECT_URL = "http://localhost:8765"

def generate_pairs(data: dict) -> List[Tuple[str, str]]:
    with open(INPUT_FILE, "r") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        data["Front"] = [s.strip() for s in data.get("Front", [])]
        data["Back"] = [s.strip() for s in data.get("Back", [])]
    zipped = list(zip(data["Front"], data["Back"]))
    with open(PAIRS_FILE, "w") as file:
        json.dump(zipped, file, ensure_ascii=False, indent=4)
    return zipped

def check_anki_connect() -> bool:
    """Check if AnkiConnect is available"""
    try:
        response = requests.post(ANKI_CONNECT_URL, json={
            "action": "version",
            "version": 6
        }, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def create_deck(deck_name: str) -> bool:
    """Create a new deck if it doesn't exist"""
    response = requests.post(ANKI_CONNECT_URL, json={
        "action": "createDeck",
        "version": 6,
        "params": {
            "deck": deck_name
        }
    })
    return response.status_code == 200

def add_note_to_anki(front: str, back: str, deck_name: str) -> Tuple[bool, str]:
    """Add a single note to Anki"""
    note = {
        "deckName": deck_name,
        "modelName": "Basic",
        "fields": {
            "Front": front,
            "Back": back
        },
        "tags": ["anki_carder"]
    }

    response = requests.post(ANKI_CONNECT_URL, json={
        "action": "addNote",
        "version": 6,
        "params": {
            "note": note
        }
    })
    
    if response.status_code == 200:
        result = response.json()
        if "result" in result and result["result"] is not None:
            return True, "Success"
        else:
            error_msg = result.get('error', 'Unknown error')
            return False, error_msg
    else:
        return False, f"HTTP error: {response.status_code}"

def load_pairs_to_anki(pairs: List[Tuple[str, str]], deck_name: str) -> None:
    """Load all pairs into Anki"""
    if not check_anki_connect():
        print("❌ AnkiConnect is not available. Please:")
        print("1. Install AnkiConnect add-on in Anki")
        print("2. Make sure Anki is running")
        print("3. Check that AnkiConnect is enabled")
        return
    
    # Create deck if it doesn't exist
    if not create_deck(deck_name):
        print(f"❌ Failed to create deck '{deck_name}'")
        return
    
    print(f"📚 Adding {len(pairs)} cards to deck '{deck_name}'...")
    
    success_count = 0
    failed_cards = []
    
    for i, (front, back) in enumerate(pairs, 1):
        print(f"Adding card {i}/{len(pairs)}: {front[:30]}...")
        
        success, error_msg = add_note_to_anki(front, back, deck_name)
        if success:
            success_count += 1
        else:
            print(f"❌ Failed to add card: {front}")
            print(f"   Error: {error_msg}")
            failed_cards.append((front, back, error_msg))
        
        # Small delay to avoid overwhelming Anki
        time.sleep(0.1)
    
    print(f"✅ Successfully added {success_count}/{len(pairs)} cards to Anki!")
    
    # Show failed cards if any
    if failed_cards:
        print(f"\n❌ Failed to add {len(failed_cards)} cards:")
        for front, back, error in failed_cards:
            print(f"  • {front} → {back}")
            print(f"    Error: {error}")

def main():
    # Generate pairs from YAML
    pairs = generate_pairs({})
    print(f"📝 Generated {len(pairs)} word pairs")
    print(json.dumps(pairs, ensure_ascii=False, indent=4))
    
    # Check if user wants to proceed
    if input(f"\nProceed to add cards to Anki? (y/n): ").lower() != "y":
        print("❌ Operation cancelled")
        return
    
    # Get deck name from user
    deck_name = input("Enter deck name (default: Українська): ").strip()
    if not deck_name:
        deck_name = "Українська"
    
    # Load pairs to Anki
    load_pairs_to_anki(pairs, deck_name)

if __name__ == "__main__":
    main()