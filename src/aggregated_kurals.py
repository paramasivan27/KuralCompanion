import json
import os


def load_aggregated_kurals():
    file_path = os.path.join(os.path.dirname(__file__), 'aggregated_thirukkural_with_summary.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading aggregated kurals: {e}")
        return {"chapters": []}


AGGREGATED_KURALS_DATA = load_aggregated_kurals()


def get_aggregated_chapters():
    return AGGREGATED_KURALS_DATA.get("chapters", [])
