# Anki Carder

A Python tool to automatically load word pairs from YAML files into Anki using AnkiConnect.

## Features

- Load word pairs from YAML files into Anki
- Automatic deck creation
- Progress tracking and error handling
- Support for custom deck names
- Tagging cards for easy identification

## Prerequisites

1. **Anki** - Download and install from [ankisrs.net](https://apps.ankiweb.net/)
2. **AnkiConnect** - Install the AnkiConnect add-on in Anki:
   - Open Anki
   - Go to Tools → Add-ons
   - Click "Browse & Install"
   - Enter code: `2055492159`
   - Restart Anki

## Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure Anki is running with AnkiConnect enabled

## Usage

1. Prepare your word pairs in `input.yaml`:
   ```yaml
   Front:
     - Russian word 1
     - Russian word 2
   Back:
     - Ukrainian translation 1
     - Ukrainian translation 2

   ```

2. Run the script:
   ```bash
   python main.py
   ```

3. Follow the prompts to:
   - Confirm you want to proceed
   - Enter a deck name (or use default)

## File Structure

- `main.py` - Main script for loading cards into Anki
- `input.yaml` - Source file with word pairs
- `Pairs.json` - Generated JSON file with pairs
- `requirements.txt` - Python dependencies

## Troubleshooting

- **AnkiConnect not available**: Make sure Anki is running and AnkiConnect is installed and enabled
- **Connection errors**: Check that Anki is running and AnkiConnect is working
- **Card creation fails**: Check the card content for special characters or formatting issues

## Notes

- Cards are tagged with "anki_carder" for easy identification
- The script uses the "Basic" note type by default
- A small delay is added between card additions to avoid overwhelming Anki 