import pandas as pd
from typing import List

from src.ingestion.base_ingestor import BaseIngestor
from src.domain.page import Page


class CSVIngestor(BaseIngestor):
    """
    Production-safe CSV ingestor with semantic row filtering.
    """

    def _load(self, file_path: str) -> List[Page]:
        df = pd.read_csv(file_path)

        if df.empty:
            return []

        file_name = file_path.split("/")[-1]
        pages: List[Page] = []

        for i, row in enumerate(df.to_dict(orient="records")):
            row_parts = []

            for col, value in row.items():
                if value is None:
                    continue

                value_str = str(value).strip()
                if not value_str:
                    continue

                row_parts.append(f"{col}: {value_str}")

            row_text = ". ".join(row_parts).strip()

            if not self._is_valid_row(row_text):
                continue

            pages.append(
                Page(
                    file_name=file_name,
                    page_number=i + 1,
                    text=row_text,
                    metadata={
                        "source": "csv",
                        "row_index": i,
                        "columns": list(df.columns),
                        "char_count": len(row_text),
                    },
                )
            )

        return pages

    def _is_valid_row(self, text: str) -> bool:
        if not text or len(text) < 30:
            return False

        lowered = text.lower()

        noise_patterns = ["nan", "none", "null"]
        if sum(p in lowered for p in noise_patterns) > 3:
            return False

        alpha_ratio = sum(c.isalpha() for c in text) / max(len(text), 1)
        if alpha_ratio < 0.35:
            return False

        return True
