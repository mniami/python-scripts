import os
from typing import Optional
from typing_extensions import Required
import click
from api import (
    find_duplications,
    move_duplications,
    report_results,
)


@click.command()
@click.argument("path", required=True)
@click.option("--move", is_flag=True)
@click.option("--output-path", default="")
def find_duplicates(path: str, move: bool, output_path: Optional[str]):
    results = find_duplications(path)
    output_path = output_path if output_path else os.path.join(path, "duplications")

    if move:
        move_duplications(results, path, output_path)

    report_results(output_path, results)


if __name__ == "__main__":
    find_duplicates()
