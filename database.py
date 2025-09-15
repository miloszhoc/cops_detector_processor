import logging
from dataclasses import dataclass

import psycopg2
import psycopg2.extras
import json

from env_var import DATABASE_URL


@dataclass
class VehicleDetails:
    car_info: str
    description: str
    img_url: str
    img_local_path: str
    img_s3_path: str
    current_plate_number: str
    old_plate_number: list
    vehicle_color: str
    voivodeship: str
    source: str
    city: str
    roads: str
    llm_extracted: str

    def __post_init__(self):
        self.current_plate_number = self.current_plate_number.replace(' ', '')
        self.roads = json.dumps(self.roads)
        self.llm_extracted = json.dumps(self.llm_extracted, ensure_ascii=False)

    def _get_connection(self):
        return psycopg2.connect(DATABASE_URL)

    def add_item_to_database(self):
        conn = self._get_connection()
        cur = conn.cursor()
        logging.info(f"Adding item to database")
        cur.execute(
            """
            INSERT INTO cars (
                description,
                img_url,
                img_local_path,
                img_s3_path,
                current_plate_number,
                old_plate_number,
                vehicle_color,
                voivodeship,
                city,
                source,
                roads,
                llm_extracted,
                car_info) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
            """, (self.description,
                  self.img_url,
                  self.img_local_path,
                  self.img_s3_path,
                  self.current_plate_number,
                  self.old_plate_number,
                  self.vehicle_color,
                  self.voivodeship,
                  self.city,
                  self.source,
                  self.roads,
                  self.llm_extracted,
                  self.car_info))
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        logging.info(f"Record added successfully! New record ID: {new_id}")
