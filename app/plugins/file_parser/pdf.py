import os

from django.conf import settings
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import (
    ConversionResult,
    DocumentConverter,
    InputFormat,
    PdfFormatOption,
)
from docling_ocr_onnxtr import OnnxtrOcrOptions

from systems.plugins.index import BaseProvider


class Provider(BaseProvider("file_parser", "pdf")):

    def parse_file(self, file_path):
        ocr_options = OnnxtrOcrOptions(
            det_arch="db_mobilenet_v3_large",
            reco_arch="Felix92/onnxtr-parseq-multilingual-v1",
        )
        pipeline_options = PdfPipelineOptions(
            ocr_options=ocr_options,
        )
        pipeline_options.allow_external_plugins = True
        pipeline_options.do_table_structure = True
        pipeline_options.table_structure_options.do_cell_matching = True

        converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pipeline_options,
                ),
            },
        )
        result = converter.convert(file_path)
        return result.document.export_to_markdown()
