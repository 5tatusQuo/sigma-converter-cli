# Sigma CLI - Sigma Rule Converter

A standalone command-line tool for converting Sigma rules to various SIEM and security platform formats.

## Installation

### From source

```bash
cd cli
pip install -e .
```

Or install directly from requirements:

```bash
cd cli
pip install -r requirements.txt
pip install -e .
```

## Usage

### Basic Conversion

Convert a Sigma rule to Microsoft XDR (Kusto/KQL) format:

```bash
sigma convert -p microsoft_xdr -t kusto -f default rule.yml
```

### Command Structure

```bash
sigma convert [OPTIONS] RULE_FILE
```

### Options

- `-p, --pipeline`: Processing pipeline to apply (can be specified multiple times)
- `-t, --target`: Target platform (required for conversion)
- `-f, --format`: Output format (required for conversion)
- `-o, --output`: Output file path (default: stdout)
- `--list-targets`: List all available target platforms
- `--list-formats`: List all available output formats
- `--list-pipelines`: List all available processing pipelines

### Examples

#### List available targets

```bash
sigma convert --list-targets
```

Output:
```
Available targets:
  - splunk: Splunk
  - elasticsearch: Elasticsearch
  - microsoft_xdr: Microsoft XDR
  - qradar: IBM QRadar
  ...
```

#### List formats for a specific target

```bash
sigma convert --list-formats --target microsoft_xdr
```

#### List available pipelines

```bash
sigma convert --list-pipelines
```

Or filter by target:

```bash
sigma convert --list-pipelines --target splunk
```

#### Convert with pipeline

```bash
sigma convert -p microsoft_365_defender -t kusto -f default rule.yml
```

#### Convert with multiple pipelines

```bash
sigma convert -p windows -p sysmon -t splunk -f default rule.yml
```

#### Save output to a file

```bash
sigma convert -p microsoft_xdr -t kusto -f default rule.yml -o output.kql
```

## Common Targets and Pipelines

### Microsoft XDR / Defender

```bash
sigma convert -p microsoft_365_defender -t kusto -f default rule.yml
```

or

```bash
sigma convert -p microsoft_xdr -t kusto -f default rule.yml
```

### Splunk

```bash
sigma convert -p splunk_windows -t splunk -f default rule.yml
```

### Elasticsearch

```bash
sigma convert -p ecs_windows -t elasticsearch -f default rule.yml
```

### QRadar

```bash
sigma convert -p qradar -t qradar -f default rule.yml
```

## Creating Test Rules

Here's a simple example Sigma rule to test with:

```yaml
title: Suspicious PowerShell Execution
status: experimental
description: Detects suspicious PowerShell command line patterns
logsource:
    category: process_creation
    product: windows
detection:
    selection:
        Image|endswith: '\powershell.exe'
        CommandLine|contains:
            - '-enc'
            - '-encodedcommand'
    condition: selection
falsepositives:
    - Administrative scripts
level: medium
```

Save this as `test_rule.yml` and convert it:

```bash
sigma convert -p microsoft_365_defender -t kusto -f default test_rule.yml
```

## Troubleshooting

### Import Errors

If you encounter import errors, ensure all required backends are installed:

```bash
pip install -r requirements.txt
```

### Unknown Target or Format

Use the list commands to see available options:

```bash
sigma convert --list-targets
sigma convert --list-formats --target your_target
```

### Pipeline Not Found

Check available pipelines:

```bash
sigma convert --list-pipelines
```

## Development

To contribute or modify the CLI:

1. Clone the repository
2. Navigate to the `cli` directory
3. Install in development mode: `pip install -e .`
4. Make your changes
5. Test with various Sigma rules

## License

See the main project LICENSE file.
