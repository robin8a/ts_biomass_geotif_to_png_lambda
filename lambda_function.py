import json
import os
import io
import boto3
import rasterio
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for Lambda
import matplotlib.pyplot as plt

# Initialize boto3 client
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    AWS Lambda function handler to convert GeoTIF files to PNG heatmaps.
    
    Expected event format:
    {
        "bucket": "bucket-name",
        "key": "path/to/file.tif"
    }
    
    Returns:
        dict: Response with status code and message
    """
    try:
        # Parse the event to get bucket and key
        bucket_name = event['bucket']
        object_key = event['key']
        
        print(f"Processing file: {object_key} from bucket: {bucket_name}")
        
        # Validate that the file is a TIF file
        if not object_key.lower().endswith(('.tif', '.tiff')):
            return {
                'statusCode': 400,
                'body': json.dumps(f'Error: File {object_key} is not a TIF file')
            }
        
        # Download the TIF file from S3
        try:
            input_object = s3_client.get_object(Bucket=bucket_name, Key=object_key)
            input_tif_bytes = io.BytesIO(input_object['Body'].read())
            print(f"Downloaded {object_key} from S3")
        except Exception as e:
            print(f"Error downloading file: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps(f'Error downloading {object_key}: {str(e)}')
            }
        
        # Read the GeoTIF file
        try:
            with rasterio.open(input_tif_bytes) as src:
                # Read the first band
                data = src.read(1)
                nodata_value = src.nodata
                
                # Mask out nodata values if they exist
                if nodata_value is not None:
                    data_masked = np.ma.masked_equal(data, nodata_value)
                else:
                    data_masked = data
                
                print(f"Successfully read TIF data with shape: {data.shape}")
                
        except Exception as e:
            print(f"Error reading TIF file: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps(f'Error reading TIF file: {str(e)}')
            }
        
        # Create the PNG heatmap
        try:
            # Create figure with appropriate size
            fig, ax = plt.subplots(figsize=(10, 10))
            
            # Create the heatmap using viridis colormap
            im = ax.imshow(data_masked, cmap='viridis')
            
            # Add colorbar
            cbar = plt.colorbar(im, ax=ax, label='Value')
            
            # Set title and labels
            ax.set_title('GeoTIF Heatmap')
            ax.set_xlabel('Column #')
            ax.set_ylabel('Row #')
            
            # Save to BytesIO buffer
            png_buffer = io.BytesIO()
            plt.savefig(png_buffer, format='png', dpi=150, bbox_inches='tight')
            png_buffer.seek(0)
            
            # Close the figure to free memory
            plt.close(fig)
            
            print("Successfully created PNG heatmap")
            
        except Exception as e:
            print(f"Error creating PNG: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps(f'Error creating PNG: {str(e)}')
            }
        
        # Upload the PNG to S3
        try:
            # Create output key with png_ prefix
            base_name = os.path.splitext(os.path.basename(object_key))[0]
            output_key = f"png_{base_name}.png"
            
            s3_client.put_object(
                Bucket=bucket_name,
                Key=output_key,
                Body=png_buffer.getvalue(),
                ContentType='image/png'
            )
            
            print(f"Successfully uploaded PNG to s3://{bucket_name}/{output_key}")
            
        except Exception as e:
            print(f"Error uploading PNG: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps(f'Error uploading PNG: {str(e)}')
            }
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Successfully converted {object_key} to PNG',
                'input_location': f's3://{bucket_name}/{object_key}',
                'output_location': f's3://{bucket_name}/{output_key}'
            })
        }
        
    except KeyError as e:
        print(f"Error: Missing key in event: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps(f'Error: Missing required key in event: {str(e)}. Event must contain "bucket" and "key".')
        }
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Unexpected error: {str(e)}')
        }


