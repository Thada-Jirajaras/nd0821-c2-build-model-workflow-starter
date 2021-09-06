#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning,
exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd
logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):
    """
    Basic Cleaning
    """
    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)

    ######################
    # YOUR CODE HERE     #
    ######################
    # Drop outliers
    logger.info(
        f"Keep only samples with price betweeen {args.min_price} and {args.max_price}")
    min_price = args.min_price
    max_price = args.max_price
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()
    df.to_csv("clean_sample.csv", index=False)

    # Upload the cleaned samples to W&B
    logger.info("Upload the cleaned samples to W&B")
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="input_artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="output_artifact",
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help="output_type",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="output_description",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="min_price",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="max_price",
        required=True
    )

    data_cleaning_args = parser.parse_args()

    go(data_cleaning_args)
