from dataclasses import dataclass

@dataclass
class File:
    id: int
    name: str
    categories: list[str]
    parent: int
    size: int


"""
Task 1
"""
def leafFiles(files: list[File]) -> list[str]:
    # Dict for parents of all files. We wanna check if any of the files' id are parents of
    # any other files. If not they are leaves.
    file_parent = {}
    leaves = []
    for file in files:
        file_parent[file.parent] = file.name
    
    for file in files:
        if file.id not in file_parent:
            leaves.append(file.name)

    return leaves


"""
Task 2
"""
def kLargestCategories(files: list[File], k: int) -> list[str]:
    # First count how many of each category is there.
    categories_dict = {}
    for file in files:
        for category in file.categories:
            if category not in categories_dict:
                categories_dict[category] = 1
            else:
                categories_dict[category] += 1
    
    # We sort based on descending number then if same alphabetically of the names.
    sorted_categories = sorted(categories_dict.items(), key=lambda x: (-x[1], x[0]))
    sorted_category_names = [category[0] for category in sorted_categories]    
    
    # If there are less categories then k return all else, return largest k categories.
    if len(sorted_category_names) < k:
        return sorted_category_names
    else:
        return sorted_category_names[:k]

"""
Task 3
"""
def largestFileSize(files: list[File]) -> int:
    # If no files largest size is zero.
    if len(files) == 0:
        return 0

    # Create a dict of all file's parent id and record files of such parent ids.
    # This allows for the prevention of unneccessarily looking at all files when seeing which belongs
    # to such parent.
    parent_file_dict = {}
    for file in files:
        if file.parent not in parent_file_dict:
            parent_file_dict[file.parent] = [file]
        else:
            parent_file_dict[file.parent].append(file)

    # Function to find size of a given file including children, grandchildren etc through recursion
    # using the previously created dict for fast lookup.
    def findSize(parent_file_dict: dict[list[File]], file: File) -> int:
        if file.id not in parent_file_dict:
            return file.size
        
        current_size = file.size
        for f in parent_file_dict[file.id]:
            current_size += findSize(parent_file_dict, f)
        return current_size

    # Return the max file size.
    max_size = 0
    for file in files:
        max_size = max(max_size, findSize(parent_file_dict, file))
        
    return max_size

    


if __name__ == '__main__':
    testFiles = [
        File(1, "Document.txt", ["Documents"], 3, 1024),
        File(2, "Image.jpg", ["Media", "Photos"], 34, 2048),
        File(3, "Folder", ["Folder"], -1, 0),
        File(5, "Spreadsheet.xlsx", ["Documents", "Excel"], 3, 4096),
        File(8, "Backup.zip", ["Backup"], 233, 8192),
        File(13, "Presentation.pptx", ["Documents", "Presentation"], 3, 3072),
        File(21, "Video.mp4", ["Media", "Videos"], 34, 6144),
        File(34, "Folder2", ["Folder"], 3, 0),
        File(55, "Code.py", ["Programming"], -1, 1536),
        File(89, "Audio.mp3", ["Media", "Audio"], 34, 2560),
        File(144, "Spreadsheet2.xlsx", ["Documents", "Excel"], 3, 2048),
        File(233, "Folder3", ["Folder"], -1, 4096),
    ]

    assert sorted(leafFiles(testFiles)) == [
        "Audio.mp3",
        "Backup.zip",
        "Code.py",
        "Document.txt",
        "Image.jpg",
        "Presentation.pptx",
        "Spreadsheet.xlsx",
        "Spreadsheet2.xlsx",
        "Video.mp4"
    ]

    assert kLargestCategories(testFiles, 3) == [
        "Documents", "Folder", "Media"
    ]

    assert largestFileSize(testFiles) == 20992
