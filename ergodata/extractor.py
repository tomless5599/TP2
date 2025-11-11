"""High level utilities to extract ergonomics metrics from documents.

The module provides a :class:`ErgonomicDocumentExtractor` class that can extract
text from PDF and raster image files before identifying key metrics used in the
Garg, Kodak and RSST ergonomic assessment methods. The extractor has a focus on
robustness: missing optional dependencies are reported with actionable
messages, and the parsing layer keeps track of the text snippets that triggered
any captured value.
"""

from __future__ import annotations

import argparse
import csv
import json
import importlib
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

_TEXT_CLEAN_RE = re.compile(r"\s+")


def _clean_text(value: str) -> str:
    """Normalise whitespace to simplify pattern matching."""

    return _TEXT_CLEAN_RE.sub(" ", value.strip())


def _normalise_for_match(value: str) -> str:
    """Return a lowercase representation without diacritics for fuzzy matches."""

    normalised = unicodedata.normalize("NFKD", value)
    return "".join(char for char in normalised if not unicodedata.combining(char)).lower()


def _extract_value_from_line(line: str, *, unit: Optional[str] = None) -> Optional[str]:
    """Extract a relevant value from ``line`` using basic heuristics."""

    cleaned_line = line.strip()
    if not cleaned_line:
        return None
    if unit:
        unit_pattern = re.escape(unit.lower())
        pattern = re.compile(
            rf"(?P<value>[0-9]+(?:[\.,][0-9]+)?)(?:(?=\s*{unit_pattern})|(?<=\s*{unit_pattern}))",
            re.IGNORECASE,
        )
        match = pattern.search(cleaned_line)
        if match:
            return match.group("value")
    match = re.search(r"(?P<value>[0-9]+(?:[\.,][0-9]+)?)", cleaned_line)
    if match:
        return match.group("value")
    for separator in (":", "=", "-", "→"):
        if separator in cleaned_line:
            candidate = cleaned_line.split(separator, 1)[1].strip()
            if unit and unit.lower() in candidate.lower():
                candidate = candidate.lower().split(unit.lower(), 1)[0].strip()
            if candidate:
                return candidate
    return None


@dataclass
class MetricPattern:
    """Describe how to extract a metric from free text."""

    name: str
    patterns: Sequence[re.Pattern]
    unit: Optional[str] = None
    normaliser: Optional[callable] = None
    keywords: Sequence[str] = ()

    def search(self, text: str, *, lines: Optional[Sequence[str]] = None) -> Optional[Tuple[str, str]]:
        """Return the first match as a ``(value, snippet)`` tuple."""

        for pattern in self.patterns:
            match = pattern.search(text)
            if match:
                raw_value = match.group("value").replace(",", ".")
                value = raw_value
                if self.normaliser is not None:
                    try:
                        value = self.normaliser(raw_value)
                    except Exception:  # pragma: no cover - defensive
                        continue
                snippet = _clean_text(text[max(0, match.start() - 60) : match.end() + 60])
                return str(value), snippet
        if lines and self.keywords:
            fallback = self._search_with_keywords(lines)
            if fallback:
                value, snippet = fallback
                if self.normaliser is not None:
                    try:
                        value = self.normaliser(value)
                    except Exception:  # pragma: no cover - defensive fallback
                        return None
                return str(value), snippet
        return None

    def _search_with_keywords(self, lines: Sequence[str]) -> Optional[Tuple[str, str]]:
        """Fallback heuristic looking for lines containing ``keywords``."""

        normalised_keywords = tuple(_normalise_for_match(keyword) for keyword in self.keywords)
        best_candidate: Optional[Tuple[str, str, int]] = None
        for line in lines:
            if not line:
                continue
            normalised_line = _normalise_for_match(line)
            score = sum(1 for keyword in normalised_keywords if keyword in normalised_line)
            if not score:
                continue
            candidate_value = _extract_value_from_line(line, unit=self.unit)
            if candidate_value is None:
                continue
            numeric_candidate = candidate_value.replace(",", ".")
            if not re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", numeric_candidate):
                numeric_candidate = candidate_value.strip()
            if best_candidate is None or score > best_candidate[2]:
                best_candidate = (numeric_candidate, line.strip(), score)
        if best_candidate:
            value, snippet, _score = best_candidate
            return value, snippet
        return None


@dataclass
class ExtractionResult:
    """Hold the metrics extracted for a given method."""

    method: str
    metrics: MutableMapping[str, str] = field(default_factory=dict)
    snippets: MutableMapping[str, str] = field(default_factory=dict)

    def to_row(self) -> Dict[str, str]:
        row = {"method": self.method}
        row.update(self.metrics)
        return row


class ErgonomicDocumentExtractor:
    """Extract data points relevant for Garg, Kodak and RSST analyses."""

    _METHOD_PATTERNS: Mapping[str, Sequence[MetricPattern]] = {
        "garg": (
            MetricPattern(
                "body_weight_kg",
                (
                    re.compile(r"(?:BW|poids\s+(?:du\s+)?sujet)\s*[:=]\s*(?P<value>[0-9]+(?:[\.,][0-9]+)?)", re.IGNORECASE),
                    re.compile(r"poids\s*:\s*(?P<value>[0-9]+(?:[\.,][0-9]+)?)\s*kg", re.IGNORECASE),
                ),
                keywords=("poids", "bw", "poids du sujet"),
            ),
            MetricPattern(
                "vo2max_ml_per_kg_min",
                (
                    re.compile(r"vo2\s*max\s*[:=]\s*(?P<value>[0-9]+(?:[\.,][0-9]+)?)", re.IGNORECASE),
                ),
                keywords=("vo2max", "vo2 max", "ml o2"),
            ),
            MetricPattern(
                "task_duration_min",
                (
                    re.compile(r"dur(?:ée|ee)\s*(?:totale\s*)?[:=]\s*(?P<value>[0-9]+(?:[\.,][0-9]+)?)\s*(?:min|minutes)", re.IGNORECASE),
                    re.compile(r"t\s*=\s*(?P<value>[0-9]+(?:[\.,][0-9]+)?)\s*min", re.IGNORECASE),
                ),
                keywords=("duree", "durée", "temps", "minutes"),
            ),
            MetricPattern(
                "sitting_time_percent",
                (
                    re.compile(r"assis\s*[:=]\s*(?P<value>[0-9]+(?:[\.,][0-9]+)?)\s*%", re.IGNORECASE),
                ),
                unit="%",
                keywords=("assis", "% assis", "position assis"),
            ),
            MetricPattern(
                "standing_time_percent",
                (
                    re.compile(r"debout\s*[:=]\s*(?P<value>[0-9]+(?:[\.,][0-9]+)?)\s*%", re.IGNORECASE),
                ),
                unit="%",
                keywords=("debout", "% debout", "position debout"),
            ),
            MetricPattern(
                "stooped_time_percent",
                (
                    re.compile(r"pench[ée]" r"\s*[:=]\s*(?P<value>[0-9]+(?:[\.,][0-9]+)?)\s*%", re.IGNORECASE),
                ),
                unit="%",
                keywords=("penche", "penché", "% penche"),
            ),
            MetricPattern(
                "total_energy_kcal_min",
                (
                    re.compile(r"d[ée]pense\s+energetique.*?(?P<value>[0-9]+(?:[\.,][0-9]+)?)\s*kcal/min", re.IGNORECASE),
                ),
                unit="kcal/min",
                keywords=(
                    "depense energetique totale",
                    "dépense énergétique totale",
                    "kcal/min",
                    "depense totale",
                ),
            ),
            MetricPattern(
                "total_energy_l_o2_min",
                (
                    re.compile(r"(?P<value>[0-9]+(?:[\.,][0-9]+)?)\s*l\s*o2/min", re.IGNORECASE),
                ),
                unit="l o2/min",
                keywords=("o2/min", "l o2", "litre o2"),
            ),
        ),
        "kodak": (
            MetricPattern(
                "total_points",
                (
                    re.compile(r"total\s+des\s+points\s*[:=]\s*(?P<value>[0-9]+(?:[\.,][0-9]+)?)", re.IGNORECASE),
                ),
                keywords=("total des points", "score total", "points"),
            ),
            MetricPattern(
                "vo2_l_min",
                (
                    re.compile(r"vo2\s*[:=]\s*(?P<value>[0-9]+(?:[\.,][0-9]+)?)\s*l\s*o2/min", re.IGNORECASE),
                ),
                unit="l o2/min",
                keywords=("vo2", "o2/min", "litres"),
            ),
            MetricPattern(
                "main_effort_type",
                (
                    re.compile(r"effort\s+principal\s*[:=]\s*(?P<value>[a-zàéèù\-\s]+)", re.IGNORECASE),
                    re.compile(r"type\s+d['e]effort\s*[:=]\s*(?P<value>[a-zàéèù\-\s]+)", re.IGNORECASE),
                ),
                keywords=("effort principal", "type effort", "effort"),
            ),
            MetricPattern(
                "effort_duration_percent",
                (
                    re.compile(r"%\s+du\s+temps\s*[:=]\s*(?P<value>[0-9]+(?:[\.,][0-9]+)?)", re.IGNORECASE),
                ),
                unit="%",
                keywords=("% du temps", "temps", "pourcentage"),
            ),
        ),
        "rsst": (
            MetricPattern(
                "weighted_sum_kcal_min",
                (
                    re.compile(r"sommation\s+pond[ée]r[ée]e.*?(?P<value>[0-9]+(?:[\.,][0-9]+)?)\s*kcal/min", re.IGNORECASE),
                ),
                unit="kcal/min",
                keywords=("sommation ponderee", "pondérée", "kcal/min"),
            ),
            MetricPattern(
                "task_duration_min",
                (
                    re.compile(r"dur[ée]e\s+totale\s*[:=]\s*(?P<value>[0-9]+(?:[\.,][0-9]+)?)\s*min", re.IGNORECASE),
                ),
                keywords=("duree", "durée", "temps", "minutes"),
            ),
            MetricPattern(
                "average_work_kcal_min",
                (
                    re.compile(r"travail\s+moyen\s*[:=]\s*(?P<value>[0-9]+(?:[\.,][0-9]+)?)\s*kcal/min", re.IGNORECASE),
                ),
                unit="kcal/min",
                keywords=("travail moyen", "kcal/min", "travail"),
            ),
            MetricPattern(
                "rsst_classification",
                (
                    re.compile(r"classification\s+rsst\s*[:=]\s*(?P<value>[a-zàéèù\-\s]+)", re.IGNORECASE),
                ),
                keywords=("classification rsst", "rsst", "classement"),
            ),
            MetricPattern(
                "aiha_classification",
                (
                    re.compile(r"classification\s+aiha\s*[:=]\s*(?P<value>[a-zàéèù\-\s]+)", re.IGNORECASE),
                ),
                keywords=("classification aiha", "aiha", "classement"),
            ),
        ),
    }

    def __init__(self) -> None:
        self._pdf_loader = self._try_import_pdf()
        self._image_loader = self._try_import_image_stack()

    @staticmethod
    def _try_import_pdf():
        spec = importlib.util.find_spec("pdfplumber")
        if spec is None:
            return None
        return importlib.import_module("pdfplumber")  # type: ignore

    @staticmethod
    def _try_import_image_stack():
        image_spec = importlib.util.find_spec("PIL.Image")
        Image = importlib.import_module("PIL.Image") if image_spec is not None else None  # type: ignore
        pytesseract_spec = importlib.util.find_spec("pytesseract")
        pytesseract = (
            importlib.import_module("pytesseract") if pytesseract_spec is not None else None  # type: ignore
        )
        return Image, pytesseract

    def extract_text(self, path: Path) -> str:
        """Extract raw text from ``path``."""

        suffix = path.suffix.lower()
        if suffix == ".pdf":
            if self._pdf_loader is None:
                raise RuntimeError("pdfplumber is required to read PDF files. Install it with `pip install pdfplumber`.")
            with self._pdf_loader.open(path) as pdf:
                parts: List[str] = []
                for page in pdf.pages:
                    parts.append(page.extract_text() or "")
            return "\n".join(parts)
        if suffix in {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}:
            image_lib, tesseract = self._image_loader
            if image_lib is None or tesseract is None:
                raise RuntimeError(
                    "Reading raster images requires Pillow and pytesseract with the Tesseract OCR engine installed."
                )
            image = image_lib.open(path)
            return tesseract.image_to_string(image, lang="fra+eng")
        raise ValueError(f"Unsupported file extension: {suffix}")

    def extract_metrics(self, text: str) -> List[ExtractionResult]:
        """Parse ``text`` and return structured metrics."""

        cleaned_text = _clean_text(text)
        lines = [_clean_text(line) for line in text.splitlines()]
        results: List[ExtractionResult] = []
        for method, patterns in self._METHOD_PATTERNS.items():
            result = ExtractionResult(method=method)
            for pattern in patterns:
                match = pattern.search(cleaned_text, lines=lines)
                if match:
                    value, snippet = match
                    result.metrics[pattern.name] = value
                    result.snippets[pattern.name] = snippet
            if result.metrics:
                results.append(result)
        return results

    def extract_from_path(self, path: Path) -> List[ExtractionResult]:
        return self.extract_metrics(self.extract_text(path))


def _write_csv(path: Path, results: Iterable[ExtractionResult]) -> None:
    rows = [result.to_row() for result in results]
    if not rows:
        rows.append({"method": "", "info": "Aucune donnée trouvée"})
    fieldnames: List[str] = sorted({key for row in rows for key in row.keys()})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, results: Iterable[ExtractionResult]) -> None:
    payload = []
    for result in results:
        payload.append(
            {
                "method": result.method,
                "metrics": result.metrics,
                "snippets": result.snippets,
            }
        )
    if not payload:
        payload = [
            {
                "method": None,
                "metrics": {},
                "snippets": {},
                "message": "Aucune donnée pertinente n'a été détectée",
            }
        ]
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extraction de données ergonomiques dans des documents.")
    parser.add_argument("input", type=Path, nargs="+", help="Fichiers PDF ou images à analyser")
    parser.add_argument("--output", "-o", type=Path, required=True, help="Chemin du fichier de sortie")
    parser.add_argument(
        "--format",
        "-f",
        choices=("csv", "json"),
        default="csv",
        help="Format de sortie (csv ou json)",
    )
    parser.add_argument(
        "--merge",
        action="store_true",
        help="Fusionner les résultats de plusieurs fichiers en une seule table",
    )
    return parser


def _run_cli(args: Optional[Sequence[str]]) -> int:
    parser = _build_argument_parser()
    namespace = parser.parse_args(args)

    extractor = ErgonomicDocumentExtractor()

    all_results: List[Tuple[Path, List[ExtractionResult]]] = []
    for input_path in namespace.input:
        try:
            results = extractor.extract_from_path(input_path)
        except Exception as exc:  # pragma: no cover - user feedback path
            parser.error(f"Impossible de traiter {input_path}: {exc}")
        all_results.append((input_path, results))

    if namespace.merge:
        merged: List[ExtractionResult] = []
        combined: MutableMapping[str, ExtractionResult] = {}
        for _path, results in all_results:
            for result in results:
                key = result.method
                combined.setdefault(key, ExtractionResult(method=key))
                combined[key].metrics.update(result.metrics)
                combined[key].snippets.update(result.snippets)
        merged.extend(combined.values())
        results_to_export = merged
    else:
        results_to_export = []
        for path, results in all_results:
            if not results:
                results_to_export.append(
                    ExtractionResult(
                        method=path.name,
                        metrics={"info": "Aucune donnée pertinente n'a été détectée"},
                        snippets={},
                    )
                )
            else:
                for result in results:
                    labelled = ExtractionResult(method=f"{path.name}:{result.method}")
                    labelled.metrics.update(result.metrics)
                    labelled.snippets.update(result.snippets)
                    results_to_export.append(labelled)

    if namespace.format == "csv":
        _write_csv(namespace.output, results_to_export)
    else:
        _write_json(namespace.output, results_to_export)

    return 0


def main() -> None:
    raise SystemExit(_run_cli(None))


if __name__ == "__main__":  # pragma: no cover
    main()
