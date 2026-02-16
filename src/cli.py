"""CLI interface."""

import argparse
import sys
from typing import Optional

from src.detector import detect_injection


def main(argv: Optional[list[str]] = None) -> int:
    """Main entry point for the CLI.

    Args:
        argv: Command line arguments (defaults to sys.argv).

    Returns:
        Exit code (0 for no detection, 1 for detection, 2 for errors).
    """
    parser = argparse.ArgumentParser(description="Detect prompt injection patterns in text")
    parser.add_argument(
        "text",
        nargs="?",
        help="Text to analyze for prompt injection",
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Read text from file",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show detailed detection results",
    )
    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        help="Output results as JSON",
    )

    args = parser.parse_args(argv)

    text: str

    if args.file:
        try:
            with open(args.file, "r") as f:
                text = f.read()
        except OSError as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            return 2
    elif args.text:
        text = args.text
    else:
        parser.print_help()
        return 0

    result = detect_injection(text)

    if args.json:
        import json

        output = {
            "detected": result.is_detected,
            "category": result.category,
            "matches": result.matches,
            "score": result.score,
        }
        print(json.dumps(output, indent=2))
    elif args.verbose:
        if result.is_detected:
            print("⚠️  Prompt injection detected!")
            print(f"   Category: {result.category}")
            print(f"   Score: {result.score:.2f}")
            print(f"   Matches: {len(result.matches)}")
            for match in result.matches:
                print(f"   - {match}")
        else:
            print("✅ No prompt injection detected")
    else:
        if result.is_detected:
            print(f"Detected: {result.category}")
            return 1
        else:
            print("No injection detected")
            return 0

    return 0 if not result.is_detected else 1


if __name__ == "__main__":
    sys.exit(main())
