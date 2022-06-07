# -*- coding: utf-8 -*-
"""
Parse Excel table to replace the corresponding terms.
Usage:
python replacer.py <inputfile.xlsx> <inputText.txt> <outputText.txt>
Dependencies:
pandas
xlrd:  conda install -c anaconda xlrd
for pip: openpyxl
"""

# Importing the libraries
import re
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
# Custom
import trie



def super_quick_replace(workbook, in_text):
    # Helper functions
    def parse_term(sheet, x, y, target_dict, prefix="", suffix=" "):
        cell_text = sheet.iat[y, x]
        # Allow padding to protect trailing whitespace.
        if cell_text.startswith("/") and cell_text.endswith("/"):
            cell_text = cell_text[1:-1]
        replacement_term = cell_text[1:] + suffix
        # Grab jp replacement if available
        if isinstance(sheet.iat[y, x - 1], str):
            original_term = sheet.iat[y, x - 1].replace(r'\+', '+')  # Spreadsheets trigger formula stuff with a +
            if original_term.startswith("/") and original_term.endswith("/"):  # allow padding terms in case they need to start with a reserved character.
                original_term = original_term[1:-1]

            if "ignore" not in original_term:
                # split jp term along & to create multiple pairs
                original_terms = original_term.split("&")
                for original_term in original_terms:
                    target_dict[prefix + original_term] = replacement_term


    def process_line(line_index, count):
        for i in range(line_index, line_index + count):
            line = in_text[i]
            if line != "\n":
                for instance in nok.findall(line):  # kill 万
                    line = line.replace(instance, instance[1:])

                # Use trie structure with the rest of the terms.
                if terms:
                    line = terms_re.sub(lambda match: terms[match.group()], line)

                if honorifics:
                    line = honorifics_re.sub(lambda match: match.group(1) + honorifics[match.group(2)], line)

                for instance in titles_re.findall(line):  # only match if followed by A-Z

                    line = line.replace(instance, titles[instance[:-1]] + instance[-1])

                if no_suffix:
                    line = no_suffix_re.sub(lambda match: no_suffix[match.group()], line)

                # Run unoptimized regex to prevent individual regex from interfering with each other.
                if regex_terms:
                    for term, pattern in regex_terms.items():
                        line = re.sub(term, regex_terms[term], line)

                if post_terms:
                    line = post_terms_re.sub(lambda match: post_terms[match.group()], line)

                out_text[i] = line


    # Create list of named tuples for matching terms for all sheets
    regex_terms = dict()  # unoptimized raw regex allowed
    terms = dict()
    honorifics = dict()  # suffixes that trigger on a space before them
    titles = dict()  # prefixes that trigger on [A-Z] after them
    post_terms = dict()  # terms that have a lower priority than honorifics and titles
    no_suffix = dict()  # terms that don't have the trailing space
    # output_terms = []

    for sheet in workbook.values():
        height, width = sheet.shape

        for y in range(0, height):
            for x in range(1, width):
                # Start one from the left, since the JP term will be to the left.
                # Avoiding out-of-bounds when checking for jp term

                # Detect cells marked with # as the first letter
                cell = sheet.iat[y, x]
                if isinstance(cell, str):
                    if not cell.strip():
                        continue

                    # Allow padding to protect trailing whitespace.
                    if cell.startswith("/") and cell.endswith("/"):
                        cell = cell[1:-1]
                    # Find en terms
                    if cell[0] == '#':
                        parse_term(sheet, x, y, terms)
                    # check if it's an honorific. Must be preceded by a space.
                    elif cell[0] == '$':
                        parse_term(sheet, x, y, honorifics)
                    # check if it's a title. These only match if followed by [A-Z]
                    elif cell[0] == '!':
                        parse_term(sheet, x, y, titles)
                    # check if it's a secondary term, to be matched last
                    elif cell[0] == '~':
                        parse_term(sheet, x, y, post_terms)
                    # check if it's a regex
                    elif cell[0] == ':':
                        parse_term(sheet, x, y, regex_terms, suffix="")
                    # check if it's a suffix-less
                    elif cell[0] == '|':
                        parse_term(sheet, x, y, no_suffix, suffix="")


    print(f"""{len(terms) + len(honorifics) + len(titles) + len(post_terms) + len(regex_terms) + len(no_suffix)} terms found in the dictionary.
Beginning replacement on {len(in_text)} lines:""")

    nok = re.compile(r"万\d{4}")  # remove 10,000 separator symbol when possible
    terms_re = trie.trie_regex_from_words(terms.keys())
    honorifics_re = trie.trie_regex_from_words(honorifics.keys(), prefix=r"([a-z]) (", suffix=")")
    if titles:
        titles_re = re.compile("|".join(titles.keys()) + "[A-Z]")
    else:
        titles_re = re.compile("^\b$")  # Never match
    post_terms_re = trie.trie_regex_from_words(post_terms.keys())
    no_suffix_re = trie.trie_regex_from_words(no_suffix.keys())

    # Print the patterns.
    print(f"terms: {terms_re.pattern}")
    print(f"honorifics: {honorifics_re.pattern}")
    print(f"titles: {titles_re.pattern}")
    print(f"post_terms: {post_terms_re.pattern}")
    print(f"regex_terms: {regex_terms}")
    print(f"no_suffix: {no_suffix}")


    # replace terms that match the jp part for all terms | O(lines+terms) now linear
    out_text = ["\n" for _ in in_text]

    with ThreadPoolExecutor(max_workers=4) as executor:
        avg_size = len(in_text) // 4

        for i in range(3):
            # print(f"let's go {i*avg_size} to {(i+1)*avg_size-1}")
            future = executor.submit(process_line, i * avg_size, avg_size)

        future = executor.submit(process_line, 3 * avg_size, avg_size + len(in_text) % 4)

    return out_text


# if __name__ == "__main__":
#     # Requires filename to read from
#     parser = argparse.ArgumentParser()
#     parser.add_argument("inputxlsx")
#     parser.add_argument("inputtext")
#     parser.add_argument("outputtext")
#     parser.add_argument("-st", "--stats", action="store_true",
#                         help="Write usage stats.")
#     args = parser.parse_args()
#
#     tic = time.perf_counter()
#
#     # Importing the excel data
#     try:
#         workbook = pd.read_excel(args.inputxlsx, sheet_name=None)
#     except OSError:
#         sys.exit("ERROR: Excel spreadsheet could not be read")
#     try:
#         with open(args.inputtext, "r", encoding="utf-8") as f:
#             in_text = f.readlines()
#     except OSError:
#         sys.exit("ERROR: text file could not be read")
#
#     # Run replacement
#     out_text = super_quick_replace(workbook, in_text)
#
#     # Writing
#     print(f"Writing output to {args.outputtext}")
#     try:
#         with open(args.outputtext, 'w', encoding="utf-8") as outfile:
#             outfile.writelines(out_text)
#     except OSError:
#         print("ERROR: Writing the file has failed!")
#     else:
#         print("output written successfully")
#
#     toc = time.perf_counter()
#     print(f"Done in {toc - tic:0.4f} seconds")
