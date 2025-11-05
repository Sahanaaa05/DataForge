from producer import producer
from credentials_config import credentials_config
import time


if __name__ == "__main__":
    print("Starting data forecast\n")
    
    credentials_config()
    time.sleep(5)
    producer()
    time.sleep(5)


    print("\n All steps completed successfully!")
