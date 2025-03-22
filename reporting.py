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

def filter_list_by_endings(A, B):
  """
  Generates a new list C containing entries from list A that do not have 
  an "ends with" match from any string in list B.

  Args:
    A: A list of strings.
    B: A list of strings representing potential endings.

  Returns:
    A new list C containing strings from A that don't end with any string in B.
  """
  C = []
  for a_item in A:
    ends_with_match = False
    for b_item in B:
      if str(a_item).endswith(b_item):
        ends_with_match = True
        break  # No need to check other endings if a match is found
    if not ends_with_match:
      C.append(a_item)
  return C


if __name__ == "__main__":
    dotenv_path = find_dotenv("oo.env")
    config = dotenv_values(dotenv_path)
    vault_root_dir = config["VAULT_PATH"]
    attach_dir = config["ATTACHMENTS_PATH"]
    note_file_type = "*.md"  # Example: Find all MD files
    pattern = r"\[\[(.*?)(\.jpg|\.jpeg|\.png)(.*?)\]\]"  # find [[image_file]] links

# Seek through the Vault, finding all the note files
# and look inside each one for links to image attachments

    found_files = find_files(vault_root_dir, note_file_type)
    linked_images = []
    if found_files:
#        print("Found files:")
         found_matches = find_matches(found_files, pattern)
         # will be a list of lists, with each element containing one or more tuples containing the matched file info 
         # e.g. ('Screenshot 2023-09-06 at 12.55.51', '.png', '|250')
         if found_matches:
            with open(f'linked_images_report.txt', 'w') as linksfile:
                for m in found_matches:
                    for inst in m:
                        linked_images.append(f'{inst[0]}{inst[1]}')
                        linksfile.write(f'{inst[0]}{inst[1]}\n')
                        # print(inst)
    else:
        print("No files of type", note_file_type, "found in", vault_root_dir)

    # print(linked_images)
    # exit()

# Scan through the Attachments folders to find all the .jpg, .jpeg and .png files

    jpg_files = find_files(attach_dir, '*.jpg')
    jpeg_files = find_files(attach_dir, '*.jpeg')
    png_files = find_files(attach_dir, '*.png')
    image_files = jpg_files + jpeg_files + png_files
    # for i in image_files:
    #     print(i)

# So image_files is a list of absolute filenames for all images in the Attachments folder
#   and linked_images is a list of image links in note files
# So if we walk through image_files and remove entries where any linked_images entry is an
#   'ends with' match then we're left with a list of image files in the Attachments folder
#   that ARE NOT linked to in any note file.
# 

    C = filter_list_by_endings(image_files, linked_images)
    with open(f'orphan_images_report.txt', 'w') as orphansfile:
        for i in C:
            orphansfile.write(f'{i}\n')
    print(f'Found {len(C)} orphan image files.')
