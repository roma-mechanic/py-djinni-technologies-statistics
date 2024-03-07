import subprocess
import logging

import pandas as pd


def run_scrapy_spider():
    spider_name = "djinni_spy"
    output_file = "djinni_data.csv"

    try:
        # Run the Scrapy spider using subprocess
        subprocess.run(["scrapy", "crawl", spider_name, "-O", output_file])
        logging.info(
            "Scrapy spider '{}' successfully executed. Results written to '{}'".format(
                spider_name, output_file
            )
        )
    except subprocess.CalledProcessError as e:
        logging.error("Error executing Scrapy spider: {}".format(e))
    except Exception as ex:
        logging.error("An unexpected error occurred: {}".format(ex))


def main():
    # run_scrapy_spider()
    df = pd.read_csv("djinni_data.csv")
    print(df.dtypes)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
