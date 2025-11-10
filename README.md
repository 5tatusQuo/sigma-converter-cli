# Sigma to Kusto Converter

Simple Python tool for converting Sigma rules to Kusto Query Language (KQL) for Microsoft Defender/Sentinel.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

**Convert a single rule:**
```bash
python convert.py rule.yml
```

**Convert with output file:**
```bash
python convert.py rule.yml -o output.kql
```

**Convert all rules in a folder:**
```bash
python convert.py rules/ -o converted_rules/
```

**Use a different pipeline:**
```bash
python convert.py rule.yml -p microsoft_365_defender
```

## Azure DevOps Pipeline

The included pipeline automatically:
1. Converts Sigma rules from the `rules/` folder to KQL
2. Creates a new branch with the converted files
3. Opens a pull request

See [PIPELINE_SETUP.md](PIPELINE_SETUP.md) for configuration details.

## Example

Input (`example_rule.yml`):
```yaml
title: Suspicious PowerShell Execution
logsource:
    category: process_creation
    product: windows
detection:
    selection:
        Image|endswith: '\powershell.exe'
        CommandLine|contains: ['-enc', '-encodedcommand']
    condition: selection
```

Output:
```kql
DeviceProcessEvents
| where FolderPath endswith "\\powershell.exe"
  and (ProcessCommandLine contains "-enc"
    or ProcessCommandLine contains "-encodedcommand")
```
