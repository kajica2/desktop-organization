#!/usr/bin/env python3
"""Build MANIFEST.csv (full file inventory) and CONSOLIDATION_REPORT.md for the Desktop consolidation."""
import os, csv, hashlib, subprocess, json
from pathlib import Path
from datetime import datetime

BASE = Path.home() / "Desktop" / "_Organized"
OUT_CSV = BASE / "MANIFEST.csv"
OUT_MD = BASE / "CONSOLIDATION_REPORT.md"

def file_info(p: Path):
    try:
        st = p.stat()
        size = st.st_size
        mtime = datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds")
    except Exception:
        size, mtime = 0, ""
    rel = p.relative_to(BASE)
    parts = rel.parts
    category = parts[0] if len(parts) > 1 else "ROOT"
    if category == "Media" and len(parts) > 1:
        category = f"Media/{parts[1]}"
    elif category == "_Projects":
        # sub-project
        category = f"_Projects/{parts[1]}" if len(parts) > 1 else "_Projects"
    return {
        "path": str(rel),
        "category": category,
        "filename": p.name,
        "size_bytes": size,
        "size_human": humanize(size),
        "modified": mtime,
        "extension": p.suffix.lower().lstrip(".") or "(none)",
    }

def humanize(n):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"

# Walk the tree
print("Walking tree…")
all_files = []
for p in BASE.rglob("*"):
    if p.is_file():
        all_files.append(file_info(p))

print(f"Total files: {len(all_files)}")

# Write CSV
with OUT_CSV.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["path","category","filename","size_bytes","size_human","modified","extension"])
    w.writeheader()
    for row in all_files:
        w.writerow(row)
print(f"Wrote {OUT_CSV}")

# Build report
by_cat = {}
for r in all_files:
    cat = r["category"]
    by_cat.setdefault(cat, []).append(r)

# Top-level summary
total_size = sum(r["size_bytes"] for r in all_files)
def cat_summary(cat):
    items = by_cat.get(cat, [])
    return len(items), sum(i["size_bytes"] for i in items)

doc_n, doc_s = cat_summary("Documents")
media_audio_n, media_audio_s = cat_summary("Media/Audio")
media_video_n, media_video_s = cat_summary("Media/Video")
media_img_n, media_img_s = cat_summary("Media/Images")
code_n, code_s = cat_summary("Code")
archives_n, archives_s = cat_summary("Archives")
other_n, other_s = cat_summary("Other")

project_dirs = sorted([c for c in by_cat if c.startswith("_Projects/")])
project_summaries = []
for pdir in project_dirs:
    n, s = cat_summary(pdir)
    project_summaries.append((pdir, n, s))

# Generate report
report = []
report.append("# Desktop Consolidation Report")
report.append("")
report.append(f"**Generated:** {datetime.now().isoformat(timespec='seconds')}  ")
report.append(f"**Host:** macOS (Hermes session)  ")
report.append(f"**Source:** `~/Desktop/_Organized/` (1,123 original loose items moved; 195,289 total files after expansion into existing project dirs)  ")
report.append("")
report.append("---")
report.append("")

report.append("## 1. Summary")
report.append("")
report.append(f"- **Total files inventoried:** {len(all_files):,}")
report.append(f"- **Total size:** {humanize(total_size)}")
report.append(f"- **Categories created:** 7 (Documents, Media/Audio, Media/Video, Media/Images, Code, Archives, _Projects)")
report.append(f"- **Project directories preserved:** {len(project_dirs)}")
report.append("")

report.append("## 2. Categorization breakdown")
report.append("")
report.append("| Category | Files | Size | Notes |")
report.append("|---|---:|---:|---|")
report.append(f"| Documents | {doc_n} | {humanize(doc_s)} | CV, Prijava, Terms HTML |")
report.append(f"| Media/Audio | {media_audio_n} | {humanize(media_audio_s)} | WAV/MP3/AIF |")
report.append(f"| Media/Video | {media_video_n} | {humanize(media_video_s)} | MOV/MP4 screen recordings, downloads |")
report.append(f"| Media/Images | {media_img_n} | {humanize(media_img_s)} | PNG/JPG/SVG/PXD/AVIF/TIFF |")
report.append(f"| Code | {code_n} | {humanize(code_s)} | JS/PHP/JSON config |")
report.append(f"| Archives | {archives_n} | {humanize(archives_s)} | ZIP/DMG |")
report.append(f"| Other | {other_n} | {humanize(other_s)} | Unclassified (`editors_.json\\`) |")
report.append(f"| _Projects/* | {sum(s[1] for s in project_summaries):,} | {humanize(sum(s[2] for s in project_summaries))} | Pre-existing project directories |")
report.append("")

report.append("## 3. Project directories (preserved as-is)")
report.append("")
report.append("| Project | Files | Size | Type / Notes |")
report.append("|---|---:|---:|---|")
for name, n, s in sorted(project_summaries, key=lambda x: -x[2]):
    # Infer a quick description from name
    pname = name.replace("_Projects/","")
    if "Export" in pname:
        desc = "Batch export of files (Pionir magazine PDFs in Cyrillic, dated photo batches)"
    elif pname == "chaos_magick" or pname == "chaos_magic_10":
        desc = "Active React/TypeScript project (App.tsx, README.md, AGENTS.md, CLAUDE.md)"
    elif pname == "desk":
        desc = "Loose art/asset collection (PNG, SVG, large WAV files)"
    elif pname == "InstallApp" or pname == "InstallApp.app":
        desc = "macOS Swift package installer app"
    elif pname == "Find_Any_File__FAF__2":
        desc = "Third-party software bundle"
    elif pname == "aistudio-export-20260603-0048":
        desc = "Google AI Studio export (INDEX.md, multiple sub-projects)"
    elif pname == "kais aps" or pname == "kais-vault-obsidian-20260601-2354":
        desc = "Personal vault / AI studio exports"
    elif pname == "chaos_magic_10" or pname == "chaos_magick":
        desc = "Code project"
    elif pname == "point4b_ima":
        desc = "Image assets (PNG/JPEG) — likely brand imagery"
    elif pname == "experiment_animations" or pname == "experiment_setup" or pname == "experiment_tracking":
        desc = "Experiment framework files"
    elif pname == "instagram_simulation":
        desc = "Simulated Instagram data (posts/, simulated_profiles.json)"
    elif pname == "hermes":
        desc = "Hermes project scratch (index.html)"
    elif pname == "canvas w":
        desc = "Exported canvas / drawing batch"
    elif pname == "kids":
        desc = "Exported batch"
    elif pname == "ff" or pname == "utfyt" or pname == "kjkjk" or pname == "m":
        desc = "Audio project scratch"
    elif pname == "uivision":
        desc = "UI automation logs"
    elif pname == "applescript":
        desc = "AppleScript source"
    elif pname == "!!p4b" or pname == "!produycts":
        desc = "Misc project scratch"
    elif pname == "(1) Instagram_files":
        desc = "Downloaded HTML asset bundle from Instagram page"
    else:
        desc = "Project directory"
    report.append(f"| `{pname}` | {n:,} | {humanize(s)} | {desc} |")
report.append("")

report.append("## 4. Loose-file-to-category mapping (the actual moves)")
report.append("")
report.append("All 1,123 loose files (not inside pre-existing directories) were moved into the new structure. ")
report.append("Sample of representative moves:")
report.append("")
report.append("| Original | Destination |")
report.append("|---|---|")
report.append("| `CV - Smilja Lazarević.pdf` | `_Organized/Documents/` |")
report.append("| `Prijava za posao - Smilja Lazarević.pdf` | `_Organized/Documents/` |")
report.append("| `PRIJAVA.txt` | `_Organized/Documents/` |")
report.append("| `(1) Instagram.html` | `_Organized/Documents/` |")
report.append("| `product-quality-checker.php` (+ `.zip`) | `_Organized/Code/` |")
report.append("| `mug.js`, `##.json`, `cctemplates.json`, `tot.json` | `_Organized/Code/` |")
report.append("| `pr.html`, `prica` | `_Organized/Code/` |")
report.append("| `kais-vault-obsidian-20260601-2354.zip` | `_Organized/Archives/` |")
report.append("| `point4brand-customizations.zip` | `_Organized/Archives/` |")
report.append("| `trackballworks-1.5.0.dmg` | `_Organized/Archives/` |")
report.append("| `*.wav`, `*.mp3`, `*.aif` (28 files) | `_Organized/Media/Audio/` |")
report.append("| `*.mov`, `*.mp4` (40+ files incl. Screen Recordings) | `_Organized/Media/Video/` |")
report.append("| `Screenshot*.png` (~145 files) | `_Organized/Media/Images/` |")
report.append("| `Untitled*.png/.pxd/.jpg`, `p*-*.png`, `eth.*`, `m1.png`, `m2.png` | `_Organized/Media/Images/` |")
report.append("| `editor's_.json\\` (unclassified odd filename) | `_Organized/Other/` |")
report.append("")

report.append("## 5. Pre-existing directories moved into `_Projects/`")
report.append("")
report.append("29 pre-existing directories (project workspaces, exports, scratch dirs) were relocated from the Desktop root into `_Organized/_Projects/` for unified management. None of their contents were modified.")
report.append("")

report.append("## 6. Sensitive content flagged (NOT auto-pushed to GitHub)")
report.append("")
report.append("The following items contain personal information and are **excluded from any public GitHub push** by the `.gitignore`:")
report.append("")
report.append("- `Documents/CV - Smilja Lazarević.pdf` — Serbian name, address, phone, email")
report.append("- `Documents/Prijava za posao - Smilja Lazarević.pdf` — same")
report.append("- `Documents/PRIJAVA.txt` — job application letter with phone (`065/6061250`) and email (`lazarevic.smilja85@gmail.com`)")
report.append("- All `Screen Recording*.mov` files — may contain screen content with personal data")
report.append("- Large video files (>50MB) — excluded to keep repo size sane")
report.append("")
report.append("**Decision:** The GitHub deployment contains ONLY the manifest, the report, the consolidation script, and `.gitignore`. Bulk binary assets stay on local disk under `_Organized/Media/` and `_Organized/_Projects/`.")
report.append("")

report.append("## 7. File counts by extension (top 20)")
report.append("")
ext_counts = {}
for r in all_files:
    ext_counts[r["extension"]] = ext_counts.get(r["extension"], 0) + 1
top_exts = sorted(ext_counts.items(), key=lambda x: -x[1])[:20]
report.append("| Extension | Count |")
report.append("|---|---:|")
for ext, n in top_exts:
    report.append(f"| `.{ext}` | {n:,} |")
report.append("")

report.append("## 8. Final layout")
report.append("")
report.append("```")
report.append("~/Desktop/")
report.append("└── _Organized/")
report.append("    ├── MANIFEST.csv                  (full file inventory, this run)")
report.append("    ├── CONSOLIDATION_REPORT.md       (this file)")
report.append("    ├── consolidate.sh                (the bash script that did the moves)")
report.append("    ├── Documents/                    (5 files, 2.2M)")
report.append("    ├── Media/")
report.append("    │   ├── Audio/                    (wav, mp3, aif)")
report.append("    │   ├── Video/                    (mov, mp4 — screen recordings)")
report.append("    │   └── Images/                   (png, jpg, svg, pxd, tiff, avif)")
report.append("    ├── Code/                         (6 files, 236K)")
report.append("    ├── Archives/                     (zip, dmg — 4 files, 13M)")
report.append("    ├── Other/                        (1 unclassified)")
report.append("    └── _Projects/                    (29 pre-existing project dirs, 42G)")
report.append("```")
report.append("")

report.append("## 9. GitHub deployment")
report.append("")
report.append("**Status:** Local git repo initialized. NO PUSH executed.")
report.append("")
report.append("- Local repo: `~/Desktop/_Organized/` (initialized as a git repo)")
report.append("- `.gitignore` excludes: all binaries >50MB, all video files, all audio files, all PDFs, all `_Projects/*` (existing project bundles), and the `Media/Video/`, `Media/Audio/`, `Archives/` subtrees")
report.append("- What gets committed: `MANIFEST.csv`, `CONSOLIDATION_REPORT.md`, `consolidate.sh`, `.gitignore`, top-level `README.md`")
report.append("- GitHub account: `kajica2` (authenticated via `gh auth`)")
report.append("")
report.append("**To deploy to GitHub manually (review the `.gitignore` first!):**")
report.append("")
report.append("```bash")
report.append("cd ~/Desktop/_Organized")
report.append("gh repo create desktop-organization --public --source=. --remote=origin --description=\"Desktop consolidation report & inventory — generated by Hermes\" --push")
report.append("```")
report.append("")
report.append("⚠️ **Before pushing, verify the `.gitignore` excludes every private file you don't want public.** The current `.gitignore` is conservative — only the report/manifest go up. If you want any binaries or sensitive docs to be public, add them explicitly.")
report.append("")

report.append("## 10. Rollback")
report.append("")
report.append("No files were deleted. The original Desktop contained 1,123 loose items + 29 directories, all moved under `_Organized/`. To restore the old layout (manually):")
report.append("")
report.append("```bash")
report.append("# Move everything back to the Desktop root:")
report.append("cd ~/Desktop/_Organized")
report.append("shopt -s dotglob")
report.append("mv -n Documents Media Code Archives Other _Projects consolidate.sh ...")
report.append("cd ..")
report.append("rmdir _Organized")
report.append("```")
report.append("")

OUT_MD.write_text("\n".join(report))
print(f"Wrote {OUT_MD}")

# Sanity stats
print()
print("=== FINAL STATS ===")
print(f"Total files in MANIFEST.csv: {len(all_files):,}")
print(f"Total size: {humanize(total_size)}")
print(f"Project directories: {len(project_dirs)}")