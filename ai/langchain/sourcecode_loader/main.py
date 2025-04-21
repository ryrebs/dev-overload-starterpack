import warnings

warnings.filterwarnings("ignore")
from pprint import pprint

from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)


def parse_py():
    loader = GenericLoader.from_filesystem(
        "./example_source_code/samp.py",
        glob="*",
        suffixes=[".py", ".js"],
        ## Enable document parsing within parser_threshold
        ## Document characters <= 1000 will be parsed.
        ## Pargins means labeling the parts of source code, according to
        ## the language's syntax. E.g. def a(), a() is Function name, and so on..
        ## else if parser is disabled, then read source code as text, best for large size source code.
        parser=LanguageParser(language=Language.PYTHON, parser_threshold=1000),
    )
    for doc in loader.load():
        print(doc)


def parse_py_and_split():
    loader = GenericLoader.from_filesystem(
        "./example_source_code/samp.py",
        glob="*",
        suffixes=[".py", ".js"],
        parser=LanguageParser(parser_threshold=1000),
    )
    docs = loader.load()

    ## Chunk size is soft limit
    ## split the docs at chunk size, without losing semantics
    py_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=60, chunk_overlap=0
    )
    result = py_splitter.split_documents(docs)

    for res in result:
        print("content:: ", res.page_content, len(res.page_content))


if __name__ == "__main__":
    parse_py()
    parse_py_and_split()
