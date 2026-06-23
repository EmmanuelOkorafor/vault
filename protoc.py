#!/usr/bin/env python3
"""
Runs protoc --dart_out=. on every request.proto and response.proto
found inside the directories listed in SEARCH_PATHS.
"""

import os
import subprocess
import sys
import argparse

# ─────────────────────────────────────────────
#  Add or remove paths here as needed.
#  Supports absolute paths and paths relative
#  to the script's working directory.
# ─────────────────────────────────────────────
SEARCH_PATHS = [
    # "C:\\Users\\USER\\Documents\\Projects\\Goyerv\\front_end\\goyerv_android_app\\android_app\\lib",
    # "C:\\Users\\USER\\Documents\\Projects\\Goyerv\\front_end\\goyerv_ios_app\\ios_app\\lib",
    # "C:\\Users\\USER\\Documents\\Projects\\Goyerv\\front_end\\goyerv_web_app\\web_desktop_app\\lib",
   
   
    # "C:\\Users\\USER\\Documents\\Projects\\Goyerv\\front_end\\goyerv_web_app\\web_mobile_app\\lib",
    # "C:\\Users\\USER\\Documents\\Projects\\Goyerv\\front_end\\goyerv_community_app\\community_app\\lib",
    "C:\\Users\\USER\\Documents\\Projects\\Goyerv\\front_end\\goyerv_support_app\\support_app\\lib"

]


def compile_protos_in_path(lib_path: str, dry_run: bool = False) -> bool:
    """Walks a single path and compiles any proto files found. Returns True if any were found."""
    if not os.path.isdir(lib_path):
        print(f"[WARN]  Path not found, skipping: {lib_path}")
        return False

    print(f"[INFO] Scanning: {lib_path}")

    found_any = False

    for root, dirs, files in os.walk(lib_path):
        target_protos = [f for f in files if f in ("request.proto", "response.proto")]

        if not target_protos:
            continue

        found_any = True
        print(f"\n  [FOUND] {root}")

        for proto_file in sorted(target_protos):
            cmd = ["protoc", "--dart_out=.", proto_file]
            print(f"    → Running: {' '.join(cmd)}")

            if dry_run:
                print(f"    ✓ (dry-run, skipped)")
                continue

            result = subprocess.run(
                cmd,
                cwd=root,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                print(f"    ✓ Success")
            else:
                print(f"    ✗ Failed (exit code {result.returncode})")
                if result.stdout:
                    print(f"      stdout: {result.stdout.strip()}")
                if result.stderr:
                    print(f"      stderr: {result.stderr.strip()}")

    return found_any


def main():
    parser = argparse.ArgumentParser(
        description="Run protoc --dart_out=. on request.proto / response.proto files in SEARCH_PATHS."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print commands without executing them",
    )
    args = parser.parse_args()

    if not SEARCH_PATHS:
        print("[ERROR] SEARCH_PATHS is empty. Add at least one path to the script.")
        sys.exit(1)

    print(f"[INFO] {len(SEARCH_PATHS)} path(s) configured.\n")

    total_found = 0
    for path in SEARCH_PATHS:
        found = compile_protos_in_path(path, dry_run=args.dry_run)
        if found:
            total_found += 1
        print()

    if total_found == 0:
        print("[INFO] No request.proto or response.proto files found in any of the configured paths.")
    else:
        print("[INFO] Done.")


if __name__ == "__main__":
    main()