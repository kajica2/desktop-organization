#!/bin/bash
# Desktop consolidation script — moves loose files on ~/Desktop into categorized folders.
# Existing directories (projects) are NOT moved; they're documented as-is in the report.
set -e

cd ~/Desktop
ORG=./_Organized

echo "→ Starting consolidation at $(date)"

# ===== Helper: move by extension =====
move_by_ext() {
    local ext="$1"
    local dest="$2"
    # Use nullglob to handle no matches
    shopt -s nullglob
    for f in *."$ext"; do
        # Skip anything inside _Organized
        [[ "$f" == _Organized* ]] && continue
        # Skip directories
        [[ -d "$f" ]] && continue
        echo "  $f → $dest/"
        mv -n "$f" "$dest/" 2>/dev/null || echo "    (skip - already exists)"
    done
}

# ===== Documents =====
echo "[Documents]"
move_by_ext pdf  "$ORG/Documents"
move_by_ext txt  "$ORG/Documents"
move_by_ext html "$ORG/Documents"
move_by_ext htm  "$ORG/Documents"

# ===== Media: Audio =====
echo "[Media/Audio]"
move_by_ext wav  "$ORG/Media/Audio"
move_by_ext mp3  "$ORG/Media/Audio"
move_by_ext aif  "$ORG/Media/Audio"
move_by_ext aiff "$ORG/Media/Audio"
move_by_ext m4a  "$ORG/Media/Audio"
move_by_ext flac "$ORG/Media/Audio"

# ===== Media: Video =====
echo "[Media/Video]"
move_by_ext mov  "$ORG/Media/Video"
move_by_ext mp4  "$ORG/Media/Video"
move_by_ext avi  "$ORG/Media/Video"
move_by_ext mkv  "$ORG/Media/Video"
move_by_ext webm "$ORG/Media/Video"

# ===== Media: Images (be careful with p1-p10 prefixes and PNG variants) =====
echo "[Media/Images]"
move_by_ext png  "$ORG/Media/Images"
move_by_ext jpg  "$ORG/Media/Images"
move_by_ext jpeg "$ORG/Media/Images"
move_by_ext gif  "$ORG/Media/Images"
move_by_ext svg  "$ORG/Media/Images"
move_by_ext webp "$ORG/Media/Images"
move_by_ext avif "$ORG/Media/Images"
move_by_ext tiff "$ORG/Media/Images"
move_by_ext tif  "$ORG/Media/Images"
move_by_ext heic "$ORG/Media/Images"

# ===== Code =====
echo "[Code]"
move_by_ext js   "$ORG/Code"
move_by_ext ts   "$ORG/Code"
move_by_ext py   "$ORG/Code"
move_by_ext php  "$ORG/Code"
move_by_ext json "$ORG/Code"
move_by_ext css  "$ORG/Code"
move_by_ext sh   "$ORG/Code"
move_by_ext sql  "$ORG/Code"
move_by_ext yaml "$ORG/Code"
move_by_ext yml  "$ORG/Code"
move_by_ext toml "$ORG/Code"
move_by_ext xml  "$ORG/Code"

# ===== Archives =====
echo "[Archives]"
move_by_ext zip  "$ORG/Archives"
move_by_ext dmg  "$ORG/Archives"
move_by_ext tar  "$ORG/Archives"
move_by_ext gz   "$ORG/Archives"
move_by_ext rar  "$ORG/Archives"
move_by_ext "7z" "$ORG/Archives"

# ===== Special: pxd (Pixelmator docs) =====
echo "[Media/Images pxd]"
move_by_ext pxd "$ORG/Media/Images"

# ===== Special-case files with weird/no extension =====
echo "[Special: files with odd names]"
# .png (hidden) — move to images
[[ -f ".png" ]] && mv -n .png "$ORG/Media/Images/dotfile.png" 2>/dev/null
[[ -f " .png" ]] && mv -n " .png" "$ORG/Media/Images/spaced-dotfile.png" 2>/dev/null
# Files that look like extension-less downloads
for f in "LUCYGREEN-gigapixel-high compression-1x.jpg" "eth.png" "eth.svg" "m1.png" "m2.png" "logo-e1727225110523.png" "replicate-prediction-kvhneazth5rmc0ct6v2a3rcgew.png" "Untitled 86.jpg" "Untitled 108_vectorized.png" "Untitled 121.png" "Untitled 123.pxd" "Untitled 119.pxd" "Untitled 106_vectorized 2.pxd" "Untitled 106_vectorized 3.pxd" "Untitled 106_vectorized 5.pxd" "Untitled 106_vectorized 55.pxd" "Untitled.mov" "Untitled 25.mp3" "Untitled 33_1 #04.wav" "sn.jpg" "oar2.avif" "p10-25s.png" "p10-53s.png" "p10-8s.png" "p3-15s.png" "p3-3s.png" "p3-8s.png" "p4-30s.png" "p5-12s.png" "p5-22s.png" "p5-check.png" "p6-20s.png" "p6-check.png" "p7-12s.png" "p7-28s.png" "p7-30s.png" "p7-32s.png" "p7-36s.png" "p7-4s.png" "p7-60s.png" "p7-check.png" "p8-35s.png" "p8-check.png" "p9-50s.png" "p9-5s.png"; do
    [[ -f "$f" ]] && mv -n "$f" "$ORG/Media/Images/" 2>/dev/null
done

# Untitled audio/mov → Video/Audio
for f in "insta.mov" "vidd.mov" "tai_chi.mov" "tens-torrent.mov" "sovereign_signal_reel.mp4"; do
    [[ -f "$f" ]] && mv -n "$f" "$ORG/Media/Video/" 2>/dev/null
done

for f in "caric_ner_giant.mp3" "caric_ner_giant.wav" "caric_ner_giant_2#02.wav" "caric_ner_giantg.mp3" "caric_ner_giantg.wav" "feilo.mp3" "feilo.wav" "ff.mp3" "ff.wav" "ff_1.mp3" "ff_1.wav" "ghgf.mp3" "Output 1-2.mp3" "Output 1-2.wav" "Desktop.wav" "Project 8.mp3" "Project 8.wav" "Flug First test.wav" "Surround.wav" "dd.wav" "wild_freestyle.mp3" "water_gnosis_hypnosis_am_fenrir_2026-06-14-18-10-47.wav" "90666f5b8c7e4af194a43bde47b52d3c_1_chf3_prob4.mp4" "90666f5b8c7e4af194a43bde47b52d3c_3_apo8.mp4" "video_2025-09-26_08-32-30_2_apo8.mp4" "Movie on 12.08.25 at 20.41.aif" "Movie on 12.08.25 at 20.41_1_chf3_prob4.mp4" "Movie on 12.08.25 at 20.41_840545749.mp4" "Screen Recording 2025-06-23 at 21.38.42.mov" "Screen Recording 2025-06-23 at 21.39.33.mov" "Screen Recording 2025-06-23 at 22.42.39.mov" "Screen Recording 2025-08-21 at 04.33.44.mov" "Screen Recording 2025-08-21 at 11.53.56.mov" "Screen Recording 2025-09-11 at 00.22.09.mov" "Screen Recording 2025-09-11 at 00.23.53.mov" "Screen Recording 2025-09-11 at 14.03.28.mov" "Screen Recording 2025-09-30 at 17.47.18.mov" "Screen Recording 2025-10-07 at 19.45.10-1.mov" "Screen Recording 2025-10-07 at 19.45.10.mov" "Screen Recording 2025-10-07 at 19.46.06.mov" "Screen Recording 2025-10-10 at 11.59.52.mov" "Screen Recording 2025-10-10 at 17.36.25.mov" "Screen Recording 2025-10-10 at 17.37.24.mov" "Screen Recording 2025-10-11 at 16.23.14.mov" "Screen Recording 2025-11-09 at 04.27.33.mov" "Screen Recording 2025-11-11 at 18.43.01.mov" "Screen Recording 2025-11-22 at 20.51.39.mov" "Screen Recording 2025-11-22 at 22.14.20.mov" "Screen Recording 2025-11-22 at 23.08.27.mov" "Screen Recording 2025-11-24 at 00.23.00.mov" "Screen Recording 2025-11-24 at 00.28.33.mov" "Screen Recording 2025-11-24 at 02.37.49.mov" "Screen Recording 2025-11-24 at 21.55.40.mov" "Screen Recording 2026-03-17 at 00.05.46.mov" "Screen Recording 2026-03-19 at 15.07.40.mov" "111.mov"; do
    if [[ -f "$f" ]]; then
        case "$f" in
            *.wav|*.mp3|*.aif|*.aiff) mv -n "$f" "$ORG/Media/Audio/" 2>/dev/null ;;
            *.mov|*.mp4)              mv -n "$f" "$ORG/Media/Video/" 2>/dev/null ;;
        esac
    fi
done

# Screenshot PNGs (bulk pattern)
for f in Screenshot*.png "Screenshot-2025-07-20-at-21.32.36-1-247x296.png"; do
    [[ -f "$f" ]] && mv -n "$f" "$ORG/Media/Images/" 2>/dev/null
done

# JSON code files with weird names
for f in "##.json" "cctemplates.json" "tot.json" "editors_.json\\" "mug.js" "VirtualDesktop.Android-20250916-023232.jpg" "creatorium_chilling_with_the_dogs_surounded_by_nature_--chaos_c5b325e1-a786-415c-bbde-6116c4c0c6cc_3.tiff" "creatorium_httpss.mj.runBFEmQhQU9CM_Amanita_pantherina_--chao_2136d7bc-b880-40a8-a29e-9c35543063a6_3_vectorized 2.pxd" "creatorium_httpss.mj.runwLaS3AYLqhQ_httpss.mj.runZDHvFnVNBys__eea7f997-ff8d-4190-8511-d080cb3736fb_3.pxd"; do
    if [[ -f "$f" ]]; then
        case "$f" in
            *.json|*.js) mv -n "$f" "$ORG/Code/" 2>/dev/null ;;
            *.jpg|*.tiff|*.pxd) mv -n "$f" "$ORG/Media/Images/" 2>/dev/null ;;
        esac
    fi
done

# Point4Brand assets
for f in "point4brand-customizations.zip" "product-quality-checker.php" "product-quality-checker.php.zip" "pr.html" "prica"; do
    [[ -f "$f" ]] && mv -n "$f" "$ORG/Code/" 2>/dev/null
done

# Documents: CV & Prijava (already by ext but ensure)
for f in "CV - Smilja Lazarević.pdf" "Prijava za posao - Smilja Lazarević.pdf" "PRIJAVA.txt" "(1) Instagram.html"; do
    [[ -f "$f" ]] && mv -n "$f" "$ORG/Documents/" 2>/dev/null
done

# Misc archive
[[ -f "trackballworks-1.5.0.dmg" ]] && mv -n "trackballworks-1.5.0.dmg" "$ORG/Archives/" 2>/dev/null
[[ -f "kais-vault-obsidian-20260601-2354.zip" ]] && mv -n "kais-vault-obsidian-20260601-2354.zip" "$ORG/Archives/" 2>/dev/null

# ===== Catch-all: any remaining loose files =====
echo "[Catch-all: remaining loose files]"
shopt -s nullglob
for f in *; do
    [[ "$f" == _Organized ]] && continue
    [[ -d "$f" ]] && continue  # leave dirs in place
    [[ -f "$f" ]] && {
        echo "  unclassified → Other/: $f"
        mv -n "$f" "$ORG/Other/" 2>/dev/null
    }
done

echo "✓ Consolidation complete at $(date)"
echo
echo "--- Result summary ---"
du -sh "$ORG"/* 2>/dev/null | sort -h