# Dockerfile
FROM public.ecr.aws/lambda/python:3.10

# Install system dependencies for rasterio and geospatial libraries
RUN yum update -y && \
    yum install -y gcc gcc-c++ make && \
    yum clean all

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Copy requirements and install the specified packages
COPY requirements.txt .
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Set the CMD to your handler (optional, but good practice)
CMD [ "lambda_function.lambda_handler" ]
