def extract_title(markdown):
    split_markdown = markdown.split("\n")
    for line in split_markdown:
        if line.startswith("# "):
            return line[2:].strip(" ")
    raise Exception("no title found")