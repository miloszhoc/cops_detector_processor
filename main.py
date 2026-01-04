import json

import database
from env_var import BUCKET_NAME
from item_fetcher import S3ItemFetcher
from llm_processor import process_item_data_with_llm
from utils.logs import LOGGER
import argparse

from utils.utils import validate_date


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date",
                        type=str,
                        required=True,
                        help="Current date in YYYY-MM-DD format")
    args = parser.parse_args()
    
    day_mark = args.date
    validate_date(day_mark)

    s = S3ItemFetcher(BUCKET_NAME, day_mark)
    for item in s.list_files_for_date():
        all_items = json.loads(s.parse_file(item))
        LOGGER.info(f"Processing {item}")
        for i, record in enumerate(all_items, start=1):
            LOGGER.info("Found item %d/%d", i, len(all_items))
            LOGGER.info(f"Started processing {record}")

            llm_output = process_item_data_with_llm(record)

            LOGGER.info(llm_output)

            car_info = llm_output['car_info']
            description = record['description']
            img_url = record['img_url']
            img_local_path = record['img_path']
            img_s3_path = record['s3_path']
            current_plate_number = llm_output['current_licence_plate_number']
            old_plate_number = llm_output['old_license_plates']
            vehicle_color = llm_output['vehicle_color']
            voivodeship = llm_output['voivodeship']
            source = record['source']
            city = llm_output['city']
            roads = llm_output['road_numbers']
            llm_extracted = llm_output

            database.VehicleDetails(car_info, description, img_url, img_local_path, img_s3_path, current_plate_number,
                                    old_plate_number, vehicle_color, voivodeship, source, city, roads,
                                    llm_extracted).add_item_to_database()
            LOGGER.info("Processed item %d", i)


if __name__ == "__main__":
    main()
