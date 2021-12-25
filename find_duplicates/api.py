import os
import shutil
from create_html import create_html
from results import FindDuplicatesResults
from utils import find_image_files, get_image_hash


def find_duplications(path: str) -> FindDuplicatesResults:
    """Finds duplicated images in path recursively

    Args:
        path (str): The path to the directory of images

    Returns:
        FindDuplicatesResults: Duplicated images results
    """
    results = FindDuplicatesResults()

    for file_path in find_image_files(path):
        results.add_file(file_path, get_image_hash(file_path))

    results.duplicated_files_count = 0
    for image_hash, files in results.files.items():
        if len(files) > 1:
            for file_path in files[1:]:
                results.duplicated_files.setdefault(image_hash, []).append(file_path)
                results.duplicated_files_count += 1

    results.total_files_count = len(results.files)
    return results


def move_duplications(
    results: FindDuplicatesResults, root_path: str, output_path: str
) -> int:
    """Moves duplicated files into a separate directory

    Args:
        results (FindDuplicatesResults): Duplicated images results
    Returns:
        int: The amount of moved files
    """
    os.makedirs(output_path, exist_ok=True)
    for _, files in results.duplicated_files.items():
        for file_path in files:
            rel_path = os.path.relpath(file_path, root_path)
            duplicate_output_file_path = os.path.join(output_path, rel_path)
            duplicate_output_dir_path = os.path.dirname(duplicate_output_file_path)

            if duplicate_output_dir_path:
                os.makedirs(duplicate_output_dir_path, exist_ok=True)
            print(file_path, duplicate_output_file_path)

            shutil.move(file_path, duplicate_output_file_path)
            results.moved.append((file_path, duplicate_output_file_path))
    results.moved_files_count = len(results.moved)
    return results.moved


def report_results(output_path: str, results: FindDuplicatesResults):
    """Prints the results in a JSON format

    Args:
        results (FindDuplicatesResults): Duplicated images results
    """
    os.makedirs(output_path, exist_ok=True)
    create_html(os.path.join(output_path, "duplications.html"), results)
    print(results.to_json(indent=4))
