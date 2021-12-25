import os
from typing import Any, List
from results import FindDuplicatesResults


FILE_TEMPLATE = """
<html>
<body>
<table>
    {rows}
</table>
</body>
</html>
"""

ROW_TEMPLATE = """
<tr>{columns}</td>"""

IMAGE_TEMPLATE = """
<td><img src="{file_path}" width="256"/></td>
"""


def create_html(output_path: str, duplications_results: FindDuplicatesResults):
    """Create html file listing all duplications finding in a table

    Args:
        path (str): Path to the html output file
        duplications_results (FindDuplicatesResults): Duplications results
    """

    def to_string(data: List[Any]) -> str:
        return "".join(data)

    def create_columns(files: List[str]) -> str:
        return to_string(
            [IMAGE_TEMPLATE.format(file_path=file_path) for file_path in files]
        )

    def create_rows() -> str:
        return to_string(
            [
                ROW_TEMPLATE.format(columns=create_columns(files))
                for _, files in duplications_results.files.items()
                if len(files) > 1
            ]
        )

    with open(output_path, "w") as file:
        rows = create_rows()
        html_content = FILE_TEMPLATE.format(rows=rows)
        file.write(html_content)
