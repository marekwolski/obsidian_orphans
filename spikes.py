from dotenv import find_dotenv, dotenv_values
from pathlib import Path
import re

def find_files(root_dir, file_type="*"):
    """
    Recursively finds all files of a particular type within a directory structure.

    Args:
        root_dir (str): Path to the root directory to start searching from.
        file_type (str, optional): Glob pattern to match file types. Defaults to "*".

    Returns:
        list: List of Path objects representing the found files.
    """
    all_files = []
    for path in Path(root_dir).rglob(file_type):
        if path.is_file():  # Filter out directories
            all_files.append(path)
    return all_files

def search_text_file(filepath, pattern):
    """
    Searches a text file for lines containing strings matching a regular expression.

    Args:
        filepath (str): Path to the text file.
        pattern (str): Regular expression pattern to match.

    Returns:
        list: List of lines containing matches.
    """

    matches = []
    with open(filepath, 'r') as file:
        for line in file:
            found = re.findall(pattern, line)
            if found:
                for inst in found:
                    matches.append(inst)
    return matches # a List of Tuples containing any markdown links to image attachments

def find_matches(filelist, pattern):
    matches = []
    for file in filelist:
        match = search_text_file(file, pattern)
        if match:
            #print(f"\nFound {len(match)} matches in {file}:")
            #print(match)
            matches.append(match)
        #else:
            #print("No matches found for the pattern:", pattern)
    return matches


if __name__ == "__main__":
    dotenv_path = find_dotenv("oo.env")
    config = dotenv_values(dotenv_path)
    root_dir = config["VAULT_PATH"]
    file_type = "*.md"  # Example: Find all MD files
    pattern = r"\[\[(.*?)(\.jpg|\.jpeg|\.png)(.*?)\]\]"

# Seek through the Vault, finding all the note files
# and look inside each one for links to image attachments

    found_files = find_files(root_dir, file_type)
    if found_files:
#        print("Found files:")
         found_matches = find_matches(found_files, pattern)
         # will be a list of lists, with each element containing one or more tuples containing the matched file info 
         if found_matches:
            with open(f'links_report.txt', 'w') as linksfile:
                for m in found_matches:
                    for inst in m:
                        linksfile.write(str(inst))
                        linksfile.write('\n\n')
                        #print(inst)
    else:
        print("No files of type", file_type, "found in", root_dir)

