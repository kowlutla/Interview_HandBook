#!/usr/bin/env python3
"""Extract fenced Mermaid diagrams and the embedded OpenAPI 3.1 YAML for CI validation."""
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

MASTERY = Path(__file__).resolve().parents[1]
CHAPTERS = MASTERY / "chapters"
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/system-design-artifacts")
files = sorted(CHAPTERS.glob("*/README.md"))
if len(files) != 20:
    raise SystemExit(f"Expected 20 chapter README files, found {len(files)}")

fence_re = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
mermaid_count = 0
openapi_count = 0
errors = []

for file in files:
    lines = file.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        match = fence_re.match(lines[i])
        if not match:
            i += 1
            continue
        fence, info = match.group(1), match.group(2).strip().lower()
        marker, minimum = fence[0], len(fence)
        start_line = i + 1
        i += 1
        body = []
        while i < len(lines):
            if re.match(r"^\s*" + re.escape(marker) + "{" + str(minimum) + r",}\s*$", lines[i]):
                break
            body.append(lines[i])
            i += 1
        if i == len(lines):
            errors.append(f"{file}:{start_line}: unclosed fenced block")
            break
        i += 1
        text = "\n".join(body) + "\n"
        slug = file.parent.name
        if info.startswith("mermaid"):
            mermaid_count += 1
            first = next((line.strip() for line in body if line.strip() and not line.strip().startswith("%%")), "")
            if not re.match(r"^(flowchart|sequenceDiagram|stateDiagram(?:-v2)?|classDiagram|erDiagram|journey|gantt|pie|mindmap|timeline|gitGraph|quadrantChart|xychart|block|architecture-beta)\b", first):
                errors.append(f"{file}:{start_line}: unrecognized Mermaid declaration {first!r}")
            target = OUT / "mermaid" / f"{slug}-{mermaid_count:02d}.mmd"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
        elif info.startswith(("yaml", "yml")) and re.search(r"(?m)^openapi:\s*3\.1\.\d+\s*$", text):
            openapi_count += 1
            target = OUT / "openapi" / f"{slug}-{openapi_count:02d}.yaml"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")

# Resolve local Markdown links as part of the same artifact check. This is a
# path-existence check only; it does not validate external URL liveness or anchors.
repo_root = MASTERY.parent
markdown_link_re = re.compile(r"!??\[[^\]]*\]\(([^)]+)\)")
for markdown_file in sorted(MASTERY.rglob("*.md")):
    source = markdown_file.read_text(encoding="utf-8")
    for match in markdown_link_re.finditer(source):
        destination = match.group(1).strip()
        if destination.startswith("<") and ">" in destination:
            destination = destination[1:destination.index(">")]
        else:
            destination = destination.split()[0] if destination else ""
        parsed = urlsplit(destination)
        if not destination or parsed.scheme or parsed.netloc or not parsed.path:
            continue
        local_target = (markdown_file.parent / unquote(parsed.path)).resolve()
        try:
            local_target.relative_to(repo_root.resolve())
        except ValueError:
            errors.append(f"{markdown_file}: link escapes repository root: {destination!r}")
            continue
        if not local_target.exists():
            line = source.count("\n", 0, match.start()) + 1
            errors.append(f"{markdown_file}:{line}: broken local Markdown link {destination!r}")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
if mermaid_count != 29:
    raise SystemExit(f"Expected 29 Mermaid blocks, found {mermaid_count}")
if openapi_count != 1:
    raise SystemExit(f"Expected one embedded OpenAPI 3.1 document, found {openapi_count}")
print(f"Extracted {mermaid_count} Mermaid diagrams and {openapi_count} OpenAPI 3.1 document.")
print(f"Output: {OUT}")
