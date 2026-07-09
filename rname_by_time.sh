#!/bin/bash
# Rename files in every directory recursively with 00_, 01_, 02_... prefix
# based on modification time (oldest = 00).
# Strips any existing NN_ prefix before applying new numbering.

DRY_RUN=false
ROOT_DIR="."

for arg in "$@"; do
  if [ "$arg" = "--dry-run" ]; then
    DRY_RUN=true
  else
    ROOT_DIR="$arg"
  fi
done

ROOT_DIR="${ROOT_DIR%/}"

find "$ROOT_DIR" -type d | while IFS= read -r dir; do
  [[ "$dir" == */.git* || "$dir" == *.git ]] && continue

  counter=0
  while IFS= read -r -d '' file; do
    base=$(basename "$file")
    # Strip existing NN_ prefix if present
    base="${base#[0-9][0-9]_}"
    parent=$(dirname "$file")
    prefix=$(printf "%02d" "$counter")
    newname="${prefix}_${base}"

    if [ "$DRY_RUN" = true ]; then
      echo "[DRY-RUN] $file  ->  $parent/$newname"
    else
      mv -n "$file" "$parent/$newname"
      echo "Renamed: $base -> $newname"
    fi
    ((counter++))
  done < <(find "$dir" -maxdepth 1 -type f \( -name '*.v' -o -name '*.sv' \) -printf '%T@ %p\0' | sort -zn | sed -z 's/^[^ ]* //')
done

if [ "$DRY_RUN" = true ]; then
  echo ""
  echo "--- DRY RUN complete. Run without --dry-run to execute. ---"
fi
