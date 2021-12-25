from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import List, Dict, Tuple

ImageHash = str
ImageFilePath = List[str]


@dataclass_json
@dataclass
class FindDuplicatesResults:
    total_files_count: int = 0
    files: Dict[ImageHash, ImageFilePath] = field(default_factory=dict)
    duplicated_files_count: int = 0
    duplicated_files: Dict[ImageHash, ImageFilePath] = field(default_factory=dict)
    moved: List[Tuple[ImageFilePath, ImageFilePath]] = field(default_factory=list)
    moved_files_count: int = 0

    def add_file(self, file_path: str, hash: str):
        self.files.setdefault(hash, [])
        self.files[hash].append(file_path)
