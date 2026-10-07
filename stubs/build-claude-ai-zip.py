"""Build the claude.ai upload zip for a loader-stub skill.

Bundles stubs/claude-ai/<skill>/SKILL.md plus a dated snapshot.md of the
canonical <skill>/SKILL.md (the loader's offline fallback).

Usage: python stubs/build-claude-ai-zip.py [skill] [out_dir]
Defaults: breakdance-style-conventions, ~/Desktop
Re-run and re-upload only when the stub changes or the snapshot is too stale.
"""
import datetime
import pathlib
import subprocess
import sys
import zipfile

repo = pathlib.Path(__file__).resolve().parent.parent
skill = sys.argv[1] if len(sys.argv) > 1 else "breakdance-style-conventions"
out_dir = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else pathlib.Path.home() / "Desktop"

stub = (repo / "stubs" / "claude-ai" / skill / "SKILL.md").read_text(encoding="utf-8")
canonical = (repo / skill / "SKILL.md").read_text(encoding="utf-8")
commit = subprocess.run(
    ["git", "-C", str(repo), "log", "-1", "--format=%h", "--", f"{skill}/SKILL.md"],
    capture_output=True, text=True,
).stdout.strip()
today = datetime.date.today().isoformat()
snapshot = f"<!-- snapshot {today}, commit {commit}; canonical copy may be newer -->\n{canonical}"

out = out_dir / f"{skill}-claude-ai.zip"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr(f"{skill}/SKILL.md", stub)
    z.writestr(f"{skill}/snapshot.md", snapshot)
print(out)
