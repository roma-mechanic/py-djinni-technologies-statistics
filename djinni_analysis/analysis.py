import subprocess
import logging
import matplotlib.pyplot as plt

import pandas as pd
from djinni_analysis.config import technologies as TECHNOLOGIES


def run_scrapy_spider():
    spider_name = "djinni_spy"
    output_file = "djinni_data.csv"

    try:
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


def extract_technologies(description):
    return [word for word in TECHNOLOGIES if word in description]


def generate_plot(x_data, y_data):
    fig, ax = plt.subplots(figsize=(20, 20))
    ax.bar(x_data, y_data)
    ax.set_title("Sum of all technologies")
    ax.set_xlabel("technologies")
    ax.set_ylabel("The need")
    plt.xticks(rotation=45)
    ax.grid()
    plt.show()


def main():
    run_scrapy_spider()
    df = pd.read_csv("djinni_data.csv")
    df["posted_date"] = pd.to_datetime(
        df["posted_date"], format="%H:%M %d.%m.%Y"
    )
    df["experience"] = (
        pd.to_numeric(df["experience"], errors="coerce").fillna(0).astype(int)
    )
    df["technology"] = df["description"].apply(extract_technologies)
    techno_types = df["technology"].explode()
    df = df.join(pd.crosstab(techno_types.index, techno_types))
    columns = techno_types.drop_duplicates().dropna()
    techno_df = df.loc[:, columns]
    sums = techno_df.sum(axis=0)
    sum_df = pd.DataFrame({"sum_value": sums})
    sum_df.sort_values(by="sum_value", ascending=False, inplace=True)
    generate_plot(sum_df.index, sum_df.sum_value)
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.bar(df.experience, df.applications)
    ax.set_title("applications")
    ax.set_xlabel("year of experience")
    ax.set_ylabel("number of applications")

    ax.grid()
    plt.show()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
