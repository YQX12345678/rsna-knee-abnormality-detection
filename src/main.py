"""
Entry point.

Usage:
    python -m src.main --inference-only --data-root /path/to/data --weights /path/to/manifest_dir
    python -m src.main --with-rad --parent-submission submission_round0.csv
"""
import argparse

from .ensemble import run_dino_inference, write_benchmark_submission
from .rad_branch import run_rad_branch


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--data-root", required=True)
    p.add_argument("--weights", required=True)
    p.add_argument("--output", default="submission.csv")
    p.add_argument("--inference-only", action="store_true")
    p.add_argument("--with-rad", action="store_true")
    p.add_argument("--parent-submission", default="submission_round0.csv")
    return p.parse_args()


def main():
    args = parse_args()
    write_benchmark_submission(args.data_root, args.output)
    run_dino_inference(
        package_dir=args.weights,
        data_root=args.data_root,
        output_path=args.output,
        inference_only=args.inference_only,
    )
    if args.with_rad:
        run_rad_branch(
            parent_submission_path=args.parent_submission,
            output_path=args.output,
            data_root=args.data_root,
        )


if __name__ == "__main__":
    main()
