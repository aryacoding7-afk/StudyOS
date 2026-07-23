from dataclasses import dataclass
from pathlib import Path

import fitz


@dataclass
class PDFPage:
    page_number: int
    text: str


def extract_text(pdf_path: str | Path) -> tuple[list[PDFPage], int]:
    """
    Extract text page by page from a PDF.
    """

    pdf_path = Path(pdf_path)

    document = fitz.open(pdf_path)

    pages: list[PDFPage] = []

    try:
        page_count = len(document)

        for index, page in enumerate(document):
            page_text = page.get_text().strip()

            if page_text:
                pages.append(
                    PDFPage(
                        page_number=index + 1,
                        text=page_text,
                    )
                )

    finally:
        document.close()

    return pages, page_count