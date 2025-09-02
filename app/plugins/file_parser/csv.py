from docling.document_converter import DocumentConverter
from systems.plugins.index import BaseProvider


class Provider(BaseProvider("file_parser", "csv")):

    def parse_file(self, file_path):
        converter = DocumentConverter()
        result = converter.convert(file_path)
        return result.document.export_to_markdown()
