import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


class DataTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj)
        return super().default(obj)


def main():
    engine = create_engine(os.environ["OLD_DATABASE_URL"])
    meta = MetaData()
    meta.reflect(bind=engine)
    session = sessionmaker(bind=engine)()

    table_names = ["performer", "album", "rating"]
    for table_name in table_names:
        query = session.query(meta.tables[table_name]).all()
        values = [{k: getattr(row, k) for k in row.keys()} for row in query]
        with (Path(__file__).parent / f"{table_name}.json").open("w") as file:
            json.dump(values, file, cls=DataTimeEncoder)

    session.close()


if __name__ == "__main__":
    main()
