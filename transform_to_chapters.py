#!/usr/bin/env python3
"""
Script to transform thirukkural.json into a chapter-level JSON structure.
Each chapter contains an array of kurals with only the specified fields.
"""

import json
from collections import defaultdict

def transform_thirukkural_to_chapters(input_file, output_file):
    """
    Transform the thirukkural.json file into a chapter-level structure.
    
    Args:
        input_file (str): Path to the input thirukkural.json file
        output_file (str): Path to the output chapter-level JSON file
    """
    
    # Read the input JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Group kurals by chapter
    chapters = defaultdict(list)
    
    for kural in data:
        # Extract only the required fields
        kural_data = {
            "Number": kural.get("Number"),
            "Translation": kural.get("Translation"),
            "Explanation": kural.get("explanation"),  # Note: lowercase in original
            "Couplet": kural.get("couplet"),
            "Emotions": kural.get("emotions"),
            "EmotionDetail": kural.get("EmotionDetail")
        }
        
        # Get the chapter name
        chapter_name = kural.get("Chapter")
        if chapter_name:
            chapters[chapter_name].append(kural_data)
    
    # Convert to the final structure
    result = []
    for chapter_name, kurals in chapters.items():
        chapter_data = {
            "Chapter": chapter_name,
            "Kurals": kurals
        }
        result.append(chapter_data)
    
    # Sort chapters by the first kural number in each chapter
    result.sort(key=lambda x: x["Kurals"][0]["Number"] if x["Kurals"] else 0)
    
    # Write the output JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Transformation completed!")
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    print(f"Total chapters: {len(result)}")
    
    # Print some statistics
    total_kurals = sum(len(chapter["Kurals"]) for chapter in result)
    print(f"Total kurals: {total_kurals}")
    
    # Print chapter names
    print("\nChapters found:")
    for i, chapter in enumerate(result, 1):
        print(f"{i:2d}. {chapter['Chapter']} ({len(chapter['Kurals'])} kurals)")

if __name__ == "__main__":
    input_file = "src/thirukkural.json"
    output_file = "src/thirukkural_chapters.json"
    
    try:
        transform_thirukkural_to_chapters(input_file, output_file)
    except FileNotFoundError:
        print(f"Error: Could not find input file '{input_file}'")
        print("Please make sure you're running this script from the correct directory.")
    except Exception as e:
        print(f"Error: {e}")
