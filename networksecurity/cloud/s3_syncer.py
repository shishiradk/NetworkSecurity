import os
import logging

logger = logging.getLogger(__name__)


class S3Sync:
    def __init__(self):
        # Check environment variable to enable/disable S3 sync
        self.enable_sync = os.getenv("ENABLE_S3_SYNC", "false").lower() == "true"
        if not self.enable_sync:
            logger.info("S3 sync is DISABLED. Set ENABLE_S3_SYNC=true to enable remote storage.")
        else:
            logger.info("S3 sync is ENABLED. Artifacts will be synced to S3.")
    
    def sync_folder_to_s3(self, folder, aws_bucket_url):
        if not self.enable_sync:
            logger.info(f"[S3 Sync Disabled] Skipping upload: {folder} -> {aws_bucket_url}")
            return
        
        # Verify folder exists before syncing
        if not os.path.exists(folder):
            logger.warning(f"Folder does not exist, skipping sync: {folder}")
            return
        
        command = f"aws s3 sync {folder} {aws_bucket_url}"
        logger.info(f"Syncing to S3: {folder} -> {aws_bucket_url}")
        result = os.system(command)
        
        if result != 0:
            logger.error(f"S3 sync failed with exit code: {result}")
            raise Exception(f"Failed to sync {folder} to {aws_bucket_url}")
        else:
            logger.info("S3 sync completed successfully")

    def sync_folder_from_s3(self, folder, aws_bucket_url):
        if not self.enable_sync:
            logger.info(f"[S3 Sync Disabled] Skipping download: {aws_bucket_url} -> {folder}")
            return
        
        # Create folder if it doesn't exist
        os.makedirs(folder, exist_ok=True)
        
        command = f"aws s3 sync {aws_bucket_url} {folder}"
        logger.info(f"Syncing from S3: {aws_bucket_url} -> {folder}")
        result = os.system(command)
        
        if result != 0:
            logger.error(f"S3 sync failed with exit code: {result}")
            raise Exception(f"Failed to sync from {aws_bucket_url} to {folder}")
        else:
            logger.info("S3 sync completed successfully")