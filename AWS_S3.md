# AWS S3 Download Instructions

This document provides instructions for downloading files from S3 using the AWS CLI.

## Basic AWS S3 Download Command

```bash
aws s3 cp s3://BUCKET_NAME/OBJECT_KEY LOCAL_PATH --profile PROFILE_NAME
```

## Command Parameters

- `BUCKET_NAME`: Your S3 bucket name
- `OBJECT_KEY`: The full path/key of the object in S3
- `LOCAL_PATH`: Where you want to save the file locally (can be a directory or specific filename)
- `PROFILE_NAME`: Your AWS CLI profile name

## Examples

### 1. Download to current directory:
```bash
aws s3 cp s3://tsbiomassmodeldata/biomass_map_img__20251016212350__S2__B4_B3_B2__2023_01_28__2336.tif . --profile suan-blockchain
```

### 2. Download to a specific local directory:
```bash
aws s3 cp s3://tsbiomassmodeldata/biomass_map_img__20251016212350__S2__B4_B3_B2__2023_01_28__2336.tif ./downloads/ --profile suan-blockchain
```

### 3. Download with a different local filename:
```bash
aws s3 cp s3://tsbiomassmodeldata/biomass_map_img__20251016212350__S2__B4_B3_B2__2023_01_28__2336.tif ./my_local_file.tif --profile suan-blockchain
```

### 4. Generic template (replace placeholders):
```bash
aws s3 cp s3://YOUR_BUCKET_NAME/YOUR_OBJECT_KEY ./local_filename --profile YOUR_PROFILE_NAME
```

## Additional Options

### Download with progress bar and timeout settings:
```bash
aws s3 cp s3://BUCKET_NAME/OBJECT_KEY LOCAL_PATH --profile PROFILE_NAME --cli-read-timeout 0 --cli-connect-timeout 60
```

### Download recursively (for directories):
```bash
aws s3 cp s3://BUCKET_NAME/PREFIX/ ./local_directory/ --recursive --profile PROFILE_NAME
```

### Download with specific region:
```bash
aws s3 cp s3://BUCKET_NAME/OBJECT_KEY LOCAL_PATH --profile PROFILE_NAME --region us-east-1
```

### Download multiple files with pattern matching:
```bash
aws s3 cp s3://BUCKET_NAME/ --recursive --exclude "*" --include "*.tif" ./downloads/ --profile PROFILE_NAME
```

## Common Use Cases

### Download a GeoTIF file for processing:
```bash
aws s3 cp s3://tsbiomassmodeldata/path/to/file.tif ./input.tif --profile suan-blockchain
```

### Download processed PNG output:
```bash
aws s3 cp s3://tsbiomassmodeldata/png_filename.png ./output.png --profile suan-blockchain
```

### Download entire directory structure:
```bash
aws s3 cp s3://tsbiomassmodeldata/data/ ./local_data/ --recursive --profile suan-blockchain
```

## Troubleshooting

### Check if AWS CLI is configured:
```bash
aws configure list --profile suan-blockchain
```

### List S3 bucket contents:
```bash
aws s3 ls s3://BUCKET_NAME/ --profile PROFILE_NAME
```

### List specific directory contents:
```bash
aws s3 ls s3://BUCKET_NAME/path/to/directory/ --profile PROFILE_NAME
```

## Notes

- The command will show progress information during download
- Successful downloads will display confirmation with file size and transfer details
- Make sure you have the necessary permissions to access the S3 bucket and objects
- Use `--dryrun` flag to test commands without actually downloading files
