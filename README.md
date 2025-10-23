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

### 6. Test the Function

```bash
aws lambda invoke \
    --function-name TSTifToPngFunction \
    --cli-binary-format raw-in-base64-out \
    --payload '{"bucket": "your-bucket-name", "key": "path/to/file.tif"}' \
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

### Error Response

```json
{
    "statusCode": 400,
    "body": "Error: Missing required key in event: 'bucket'. Event must contain 'bucket' and 'key'."
}
```
