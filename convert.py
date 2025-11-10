#!/usr/bin/env python3
"""Simple Sigma to Kusto/KQL converter"""

import argparse
import sys
from pathlib import Path

from sigma.plugins import InstalledSigmaPlugins
from sigma.collection import SigmaCollection
from sigma.processing.pipeline import ProcessingPipeline


def convert_single_rule(rule_file, pipeline_name, output_file, plugins, backends, pipeline_resolver):
    """Convert a single Sigma rule to Kusto/KQL format"""

    backend_class = backends['kusto']
    rule_path = Path(rule_file)
    rule_content = rule_path.read_text()

    # Resolve pipeline if specified
    if pipeline_name:
        processing_pipeline = pipeline_resolver.resolve([pipeline_name])
    else:
        processing_pipeline = ProcessingPipeline()

    # Create backend and convert
    backend = backend_class(processing_pipeline=processing_pipeline)
    sigma_rule = SigmaCollection.from_yaml(rule_content)
    result = backend.convert(sigma_rule, "default")

    if isinstance(result, list):
        result = "\n".join(result)

    # Output result
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result)
        print(f"Converted: {rule_file} -> {output_file}")
    else:
        print(result)


def convert_rules(input_path, pipeline_name, output_path=None):
    """Convert Sigma rule(s) to Kusto/KQL format"""

    # Auto-discover installed backends
    plugins = InstalledSigmaPlugins.autodiscover()
    backends = plugins.backends
    pipeline_resolver = plugins.get_pipeline_resolver()

    # Get the Kusto backend
    if 'kusto' not in backends:
        print("Error: Kusto backend not found. Install pySigma-backend-microsoft365defender", file=sys.stderr)
        sys.exit(1)

    input_path = Path(input_path)

    # Check if input exists
    if not input_path.exists():
        print(f"Error: Path '{input_path}' not found", file=sys.stderr)
        sys.exit(1)

    # Handle directory input
    if input_path.is_dir():
        # Find all YAML files in the directory
        rule_files = list(input_path.glob("*.yml")) + list(input_path.glob("*.yaml"))

        if not rule_files:
            print(f"Error: No .yml or .yaml files found in '{input_path}'", file=sys.stderr)
            sys.exit(1)

        print(f"Found {len(rule_files)} rule(s) to convert")

        for rule_file in rule_files:
            try:
                if output_path:
                    # Create output directory if it doesn't exist
                    output_dir = Path(output_path)
                    output_dir.mkdir(parents=True, exist_ok=True)
                    output_file = output_dir / f"{rule_file.stem}.kql"
                else:
                    output_file = None

                convert_single_rule(rule_file, pipeline_name, output_file, plugins, backends, pipeline_resolver)
            except Exception as e:
                print(f"Error converting {rule_file}: {e}", file=sys.stderr)
                continue

    # Handle single file input
    else:
        convert_single_rule(input_path, pipeline_name, output_path, plugins, backends, pipeline_resolver)


def main():
    parser = argparse.ArgumentParser(description="Convert Sigma rules to Kusto/KQL")
    parser.add_argument("input", help="Path to Sigma rule YAML file or directory containing rules")
    parser.add_argument("-p", "--pipeline", default="microsoft_xdr", help="Pipeline to use (default: microsoft_xdr)")
    parser.add_argument("-o", "--output", help="Output file or directory (default: stdout)")

    args = parser.parse_args()

    try:
        convert_rules(args.input, args.pipeline, args.output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
