import json
import logging

import google.generativeai as genai
from env_var import GEMINI_API_KEY, MODEL_NAME, NO_DESCRIPTION_SKIP_MSG


def process_item_data_with_llm(item: dict):
    """Extract car information from description"""
    if item['description'] == NO_DESCRIPTION_SKIP_MSG: # processing of descriptions with this message will be skipped
        return {'voivodeship': '', 'city': '', 'vehicle_color': '', 'car_info': '', 'current_licence_plate_number': '',
                'old_license_plates': [], 'road_numbers': []}

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(MODEL_NAME, generation_config={"response_mime_type": "application/json"})
    logging.info(f"Extracting car information from description")
    prompt = f"""
            {item['description']}

            From the above information presented in Polish, extract the Polish name of the province and city, 
            make and model of car, current Polish vehicle registration number consisting of numbers and letters. 
            If there are, previous registration numbers and Polish numbers of roads on which the vehicle moves. 
            Save the results in json format with the following structure:
            {{voivodeship : province name (string),
            city: city (string),
            vehicle_color: color (string),
            car_info: car make and model (string),
            current_licence_plate_number: current Polish vehicle registration number consisting of numbers and letters. This information is critical, and should not be empty (string)
            old_license_plates: previous registration numbers (list),
            road_numbers: Polish numbers of roads on which the vehicle moves (list),
            }}
            - Registration number may be in description or in hashtags (usually it is in both places)
            - Ignore new line characters (\\n).
            - If data is missing, leave blank. Return only the json dictionary structure and nothing else.
            """
    response = model.generate_content(prompt)
    logging.info(f'prompt: \n{prompt}')
    logging.info(f'response: {response.text}')
    try:
        llm_extracted = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        logging.error(f"Failed to decode JSON response: {response.text}")
        return
    else:
        logging.info("Successfully extracted car information")
        if isinstance(llm_extracted, list):
            return llm_extracted[0]
        return llm_extracted
