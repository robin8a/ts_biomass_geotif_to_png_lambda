# GeoTIF to PNG Lambda Function

This Lambda function converts GeoTIF files to PNG heatmaps and uploads them to the same S3 bucket.

## Function Overview

- **Input**: S3 bucket and key for a TIF file
- **Output**: PNG heatmap saved as `png_<original_filename>.png` in the same bucket
- **Processing**: Uses rasterio to read TIF, matplotlib to create heatmap with viridis colormap

## Event Format

```json
{
    "bucket": "your-bucket-name",
    "key": "path/to/your/file.tif"
}
```

## Deployment Instructions

### Prerequisites

- Docker installed
- AWS CLI configured with `suan-blockchain` profile
- Access to ECR repository

### 1. Build Docker Image

```bash
docker build -t ts_biomass_geotif_to_png_lambda .
```

### 2. Login to ECR

```bash
aws ecr get-login-password --region us-east-1 --profile suan-blockchain | docker login --username AWS --password-stdin 036134507423.dkr.ecr.us-east-1.amazonaws.com
```

### 3. Create ECR Repository

```bash
aws ecr create-repository --repository-name ts_biomass_geotif_to_png_lambda --region us-east-1 --profile suan-blockchain
```

```json
{
    "repository": {
        "repositoryArn": "arn:aws:ecr:us-east-1:036134507423:repository/ts_biomass_geotif_to_png_lambda",
        "registryId": "036134507423",
        "repositoryName": "ts_biomass_geotif_to_png_lambda",
        "repositoryUri": "036134507423.dkr.ecr.us-east-1.amazonaws.com/ts_biomass_geotif_to_png_lambda",
        "createdAt": "2025-10-23T10:52:45.077000-05:00",
        "imageTagMutability": "MUTABLE",
        "imageScanningConfiguration": {
            "scanOnPush": false
        },
        "encryptionConfiguration": {
            "encryptionType": "AES256"
        }
    }
}
```

### 4. Tag and Push Image

```bash
docker tag ts_biomass_geotif_to_png_lambda:latest 036134507423.dkr.ecr.us-east-1.amazonaws.com/ts_biomass_geotif_to_png_lambda:latest

docker push 036134507423.dkr.ecr.us-east-1.amazonaws.com/ts_biomass_geotif_to_png_lambda:latest
```

### 5. Create Lambda Function

```bash
aws lambda create-function \
    --function-name TSTifToPngFunction \
    --package-type Image \
    --code ImageUri=036134507423.dkr.ecr.us-east-1.amazonaws.com/ts_biomass_geotif_to_png_lambda:latest \
    --role arn:aws:iam::036134507423:role/ts-lambda-biomass-execution-role \
    --timeout 60 \
    --memory-size 3008 \
    --profile suan-blockchain
```

```json
{
    "FunctionName": "TSTifToPngFunction",
    "FunctionArn": "arn:aws:lambda:us-east-1:036134507423:function:TSTifToPngFunction",
    "Role": "arn:aws:iam::036134507423:role/ts-lambda-biomass-execution-role",
    "CodeSize": 0,
    "Description": "",
    "Timeout": 60,
    "MemorySize": 3008,
    "LastModified": "2025-10-23T16:03:24.297+0000",
    "CodeSha256": "54c80a16b746eca1a4e952086f7e35808dbb7b2e468364d2a01180fbe9676475",
    "Version": "$LATEST",
    "TracingConfig": {
        "Mode": "PassThrough"
    },
    "RevisionId": "b38f8322-765d-41ce-b91b-2f924a06a41a",
    "State": "Pending",
    "StateReason": "The function is being created.",
    "StateReasonCode": "Creating",
    "PackageType": "Image",
    "Architectures": [
        "x86_64"
    ],
    "EphemeralStorage": {
        "Size": 512
    },
    "SnapStart": {
        "ApplyOn": "None",
        "OptimizationStatus": "Off"
    }
}
```

### 6. Test the Function

```bash
aws lambda invoke \
    --function-name TSTifToPngFunction \
    --cli-binary-format raw-in-base64-out \
    --payload '{"bucket": "your-bucket-name", "key": "path/to/file.tif"}' \
    output.json \
    --profile suan-blockchain
```

```bash
aws lambda invoke \
    --function-name TSTifToPngFunction \
    --cli-binary-format raw-in-base64-out \
    --payload '{"bucket": "tsbiomassmodeldata", "key": "biomass_map_img__20251016212350__S2__B4_B3_B2__2023_01_28__2336.tif"}' \
    output.json \
    --profile suan-blockchain
```

## Update Function Code

To update the function with new code:

```bash
aws lambda update-function-code \
    --function-name TSTifToPngFunction \
    --image-uri 036134507423.dkr.ecr.us-east-1.amazonaws.com/ts_biomass_geotif_to_png_lambda:latest \
    --profile suan-blockchain
```

## Response Format

### Success Response

```json
{
    "statusCode": 200,
    "body": {
        "message": "Successfully converted file.tif to PNG",
        "input_location": "s3://bucket/file.tif",
        "output_location": "s3://bucket/png_file.png"
    }
}
```

```sh
aws s3 cp s3://tsbiomassmodeldata/biomass_map_img__20251016212350__S2__B4_B3_B2__2023_01_28__2336.tif . --profile suan-blockchain
```

### Error Response

```json
{
    "statusCode": 400,
    "body": "Error: Missing required key in event: 'bucket'. Event must contain 'bucket' and 'key'."
}
```
