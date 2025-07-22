#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################

    logger.info("Start of run")
    artifact = run.use_artifact(args.input_artifact)
    artifact_path = artifact.file()

    df = pd.read_parquet(artifact_path)

    logger.info("Cleaning of data")
    df = df[df['price'].between(args.min_price, args.max_price)]

    logger.info("Exporting of clean data")
    df.to_csv = ('clean_sample.csv', index=False)
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
        help='Fully-qualified name of input artifact for cleaning',
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help='Fully-qualified name of output artifact for cleaned data',
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help='Type of output dataset',
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help='Description of output dataset',
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="Minimum price for rental",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help='Maximum price for rental',
        required=True
    )


    args = parser.parse_args()

    go(args)
