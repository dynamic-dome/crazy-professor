#!/usr/bin/env python3
"""Safely load one field-notes Output file for harvest triage.

The field-notes value is editable and therefore untrusted. This helper accepts
only canonical crazy-professor output filenames, resolves them below the target
project's lab directory, rejects symlink escapes, and labels the loaded content
as untrusted data.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath

LAB_RELATIVE_PATH = Path(".agent-memory") / "lab" / "crazy-professor"
OUTPUT_NAME_RE = re.compile(
    r"^(?:(?:chat|duet)/)?\d{4}-\d{2}-\d{2}-\d{4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$"
)


class HarvestPathError(ValueError):
    """Raised when an editable field-notes Output value is unsafe or invalid."""


@dataclass(frozen=True)
class UntrustedHarvestOutput:
    relative_path: str
    trust: str
    content: str


def resolve_output_path(target_project: Path | str, output_file: str) -> Path:
    """Return a canonical in-lab output path or raise before any output read."""
    if not isinstance(output_file, str) or not OUTPUT_NAME_RE.fullmatch(output_file):
        raise HarvestPathError("Output file is not a canonical single/chat/duet markdown filename")
    if PurePosixPath(output_file).is_absolute() or PureWindowsPath(output_file).is_absolute():
        raise HarvestPathError("Absolute Output paths are forbidden")

    try:
        lab_root = (Path(target_project) / LAB_RELATIVE_PATH).resolve(strict=True)
        resolved = (lab_root / output_file).resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise HarvestPathError(f"Output file cannot be resolved: {exc}") from exc

    try:
        resolved.relative_to(lab_root)
    except ValueError as exc:
        raise HarvestPathError("Output file escapes the crazy-professor lab directory") from exc
    if not resolved.is_file():
        raise HarvestPathError("Output path is not a regular file")
    return resolved


def load_untrusted_output(
    target_project: Path | str, output_file: str
) -> UntrustedHarvestOutput:
    """Validate, then load an output with an explicit untrusted-data label."""
    resolved = resolve_output_path(target_project, output_file)
    try:
        content = resolved.read_text(encoding="utf-8")
    except OSError as exc:
        raise HarvestPathError(f"Output file cannot be read: {exc}") from exc
    return UntrustedHarvestOutput(
        relative_path=output_file,
        trust="untrusted",
        content=content,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-project", required=True, type=Path)
    parser.add_argument("--output-file", required=True)
    args = parser.parse_args()

    try:
        loaded = load_untrusted_output(args.target_project, args.output_file)
    except HarvestPathError as exc:
        print(f"harvest output rejected: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(asdict(loaded), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
