#!/bin/bash

# S3 Setup Script for Network Security ML Project

BUCKET_NAME="aws-networksecurity"
REGION="us-east-1"

echo "======================================"
echo "S3 Setup for Network Security Project"
echo "======================================"
echo ""

# Check if AWS CLI is configured
echo "Checking AWS credentials..."
if ! aws sts get-caller-identity &> /dev/null; then
    echo " AWS credentials not configured. Run 'aws configure' first."
    exit 1
fi
echo " AWS credentials found"
echo ""

# Create bucket
echo "Creating S3 bucket: $BUCKET_NAME"
if aws s3 mb s3://$BUCKET_NAME --region $REGION 2>/dev/null; then
    echo " Bucket created successfully"
else
    echo "  Bucket might already exist or name is taken"
    echo "   Checking if bucket is accessible..."
    if aws s3 ls s3://$BUCKET_NAME &> /dev/null; then
        echo "Bucket is accessible"
    else
        echo "Cannot access bucket. Try a different name."
        exit 1
    fi
fi
echo ""

# Enable versioning
echo "Enabling versioning..."
aws s3api put-bucket-versioning \
    --bucket $BUCKET_NAME \
    --versioning-configuration Status=Enabled
echo " Versioning enabled"
echo ""

# Test upload
echo "Testing bucket access..."
echo "test" > test-file.txt
if aws s3 cp test-file.txt s3://$BUCKET_NAME/test/test-file.txt &> /dev/null; then
    echo " Upload test successful"
    aws s3 rm s3://$BUCKET_NAME/test/test-file.txt &> /dev/null
    rm test-file.txt
else
    echo " Upload test failed. Check permissions."
    rm test-file.txt
    exit 1
fi
echo ""

echo "======================================"
echo " S3 Setup Complete!"
echo "======================================"
echo ""
echo "Bucket name: $BUCKET_NAME"
echo "Region: $REGION"
echo ""
echo "To enable S3 sync in your training:"
echo "  export ENABLE_S3_SYNC=true"
echo "  python main.py"
echo ""
echo "To verify uploads:"
echo "  aws s3 ls s3://$BUCKET_NAME/ --recursive"
echo ""