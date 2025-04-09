import argparse

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

###########
# METHODS #
###########

VALID_RATINGS = [1.0, 2.0, 3.0, 4.0, 5.0]
"""(List[str]): The list of valid book review ratings for the input book reviews dataset."""


def count_review_ratings(data_source: str, output_uri: str) -> None:
    """
    Count the number of book review ratings by score.

    This method counts the number of one-star, two-star, three-star,
    four-star, and five-star book review ratings from the input CSV
    specified by the `data_source` parameter via an EMR Spark
    cluster. The results are written to the `output_uri` parameter
    after calculating the results.

    :param data_source: The input CSV that contains the book reviews.
    :param output_uri: The output destination to dump the results.
    :return: None
    """
    with SparkSession.builder.appName("Count Review Ratings").getOrCreate() as spark:
        reviews_df = spark.read.option("header", "true").csv(data_source)
        reviews_df = reviews_df.withColumn(
            "review/score", col("review/score").cast("float")
        )
        reviews_df = reviews_df.filter(col("review/score").isin(VALID_RATINGS))
        score_count = reviews_df.groupBy("review/score").count()
        score_count.write.option("header", "true").mode("overwrite").csv(output_uri)


#######
# CLI #
#######

if __name__ == "__main__":
    # create arg parser and add arguments for count_review_ratings method
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_source",
        help="The S3 URI of the Book Ratings CSV.",
    )
    parser.add_argument(
        "--output_uri",
        help="The S3 URI of the output folder to write the review rating count results.",
    )
    args = parser.parse_args()

    # count review ratings given the args passed in from cli
    count_review_ratings(args.data_source, args.output_uri)
