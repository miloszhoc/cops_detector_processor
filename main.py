import json

import database
from env_var import BUCKET_NAME
from item_fetcher import S3ItemFetcher
from llm_processor import process_item_data_with_llm
from utils.logs import LOGGER


def main():
    day_mark = '2025-11-12'
    s = S3ItemFetcher(BUCKET_NAME, day_mark)
    for data in s.list_files_for_date():
        all_items = json.loads(s.parse_file(data))
        for i, item in enumerate(all_items, start=1):
            LOGGER.info("Processing item %d/%d", i, len(all_items))

            llm_output = process_item_data_with_llm(item)

            LOGGER.info(llm_output)

            car_info = llm_output['car_info']
            description = item['description']
            img_url = item['img_url']
            img_local_path = item['img_path']
            img_s3_path = item['s3_path']
            current_plate_number = llm_output['current_licence_plate_number']
            old_plate_number = llm_output['old_license_plates']
            vehicle_color = llm_output['vehicle_color']
            voivodeship = llm_output['voivodeship']
            source = item['source']
            city = llm_output['city']
            roads = llm_output['road_numbers']
            llm_extracted = llm_output

            database.VehicleDetails(car_info, description, img_url, img_local_path, img_s3_path, current_plate_number,
                                    old_plate_number, vehicle_color, voivodeship, source, city, roads,
                                    llm_extracted).add_item_to_database()
            LOGGER.info("Processed item %d", i)


if __name__ == "__main__":
    main()
