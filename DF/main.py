from credentials_config import credentials_config
from s3_bkt_creation import s3_bkt_creation
from kinesis import kinesis
from kinesis_check import kinesis_check
from glue_job import glue_job
from create_db import create_db
from iam_role import iam_role
from producer import producer
import time


if __name__ == "__main__":
    print("Starting AWS DataForge Pipeline Setup...\n")
    
    credentials_config()
    time.sleep(5)
    iam_role()
    time.sleep(5)
    s3_bkt_creation()
    time.sleep(5)
    kinesis()
    time.sleep(5)
    kinesis_check()
    time.sleep(5)
    create_db()
    time.sleep(5)
    glue_job()
    time.sleep(5)
    producer()

    

    print("\n All steps completed successfully!")
