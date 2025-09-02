import os

from django.conf import settings
from docling.datamodel.pipeline_options import PdfPipelineOptions, RapidOcrOptions
from docling.document_converter import (
    ConversionResult,
    DocumentConverter,
    InputFormat,
    PdfFormatOption,
)

from systems.plugins.index import BaseProvider


class Provider(BaseProvider("file_parser", "pdf")):

    def parse_file(self, file_path):
        os.environ["HF_HOME"] = settings.MANAGER.hf_cache

        from huggingface_hub import snapshot_download

        download_path = snapshot_download(repo_id="SWHL/RapidOCR")
        det_model_path = os.path.join(download_path, "PP-OCRv4", "en_PP-OCRv3_det_infer.onnx")
        rec_model_path = os.path.join(download_path, "PP-OCRv4", "ch_PP-OCRv4_rec_server_infer.onnx")
        cls_model_path = os.path.join(download_path, "PP-OCRv3", "ch_ppocr_mobile_v2.0_cls_train.onnx")
        ocr_options = RapidOcrOptions(
            det_model_path=det_model_path,
            rec_model_path=rec_model_path,
            cls_model_path=cls_model_path,
        )

        pipeline_options = PdfPipelineOptions(
            do_ocr=True,
            do_table_structure=True,
            table_structure_options={"do_cell_matching": True},
            ocr_options=ocr_options,
        )
        converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pipeline_options,
                ),
            },
        )
        result = converter.convert(file_path)
        return result.document.export_to_markdown()
