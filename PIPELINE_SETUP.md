# Azure DevOps Pipeline Setup

## Pipeline Permissions

For the pipeline to automatically create branches and pull requests, you need to grant the build service the following permissions:

### 1. Repository Permissions

Navigate to: **Project Settings** > **Repositories** > Select your repository > **Security**

Find the build service user (usually named like `[Project Name] Build Service ([Organization Name])`) and grant:

- ✅ **Contribute**: Allow
- ✅ **Create branch**: Allow
- ✅ **Contribute to pull requests**: Allow

### 2. Enable System.AccessToken

The pipeline uses `$(System.AccessToken)` which is automatically available. No additional configuration needed.

## How the Pipeline Works

1. **Build Stage**: Tests the conversion with example rule
2. **ConvertRules Stage**:
   - Converts Sigma rules (from `rules/` folder or current directory) to KQL
   - Creates a new branch: `automated-kql-conversion-YYYYMMDD-HHMMSS`
   - Commits converted rules to the new branch
   - Pushes the branch to the repository
   - Creates a pull request targeting the source branch

## Pipeline Triggers

The pipeline triggers on commits to:
- `main` branch
- `develop` branch

## Output

- **Artifacts**: Converted KQL files are published as build artifacts
- **Pull Request**: Automatically created with converted rules
- **Branch**: New branch with timestamped name containing the converted files

## Customization

### Change the rules directory

Edit line 59 in `azure-pipelines.yml`:
```yaml
python convert.py your-rules-folder/ -o converted_rules/
```

### Change the pipeline name

Edit line 123:
```yaml
title = "Your Custom PR Title - $(Build.BuildNumber)"
```

### Change target branch

The PR targets the branch that triggered the build. To change this, edit line 122:
```yaml
targetRefName = "refs/heads/main"  # or your preferred branch
```
