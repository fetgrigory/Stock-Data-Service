'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 09/07/2025
Ending //

'''
# Installing the necessary libraries

import zipfile
import logging
from pathlib import Path
from email_sender import EmailSender


class DataArchiver:
    """AI is creating summary for

    Returns:
        [type]: [description]
    """
    @staticmethod
    # Get folder and archive paths for given date
    def _get_paths(date):
        folder_name = date.strftime("%Y-%m-%d")
        folder_path = Path(f"data/{folder_name}")
        archive_path = Path(f"data/{folder_name}.zip")
        return folder_path, archive_path

    @staticmethod
    # Check if archiving is needed for given date
    def should_archive(date):
        """AI is creating summary for should_archive

        Args:
            date ([type]): [description]

        Returns:
            [type]: [description]
        """
        folder_path, _ = DataArchiver._get_paths(date)
        return folder_path.exists() and any(folder_path.glob("*.csv"))

    @staticmethod
    # Remove all CSV files and the folder
    def _cleanup_files(folder_path):
        for csv_file in folder_path.glob("*.csv"):
            csv_file.unlink()
        folder_path.rmdir()

    @staticmethod
    # Archive all CSV files for given date
    def archive(date):
        """AI is creating summary for archive

        Args:
            date ([type]): [description]

        Returns:
            [type]: [description]
        """
        try:
            folder_path, archive_path = DataArchiver._get_paths(date)

            if archive_path.exists():
                logging.info("Archive exists: %s", archive_path)
                return True

            if not DataArchiver.should_archive(date):
                logging.warning("No files to archive for %s", folder_path.name)
                return False

            # Create archive
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for csv_file in folder_path.glob("*.csv"):
                    zipf.write(csv_file, arcname=csv_file.name)

            if not archive_path.exists():
                logging.error("Archive creation failed for %s", folder_path.name)
                return False
            # Cleanup original files
            DataArchiver._cleanup_files(folder_path)
            logging.info("Archiving complete for %s", folder_path.name)

        # Send archive via email
            email_sender = EmailSender()
            if email_sender.send_email_with_attachment(archive_path):
                logging.info("Email with archive sent successfully: %s", archive_path)
                # Delete archive after successful sending
                archive_path.unlink()
                logging.info("Archive deleted: %s", archive_path)
            else:
                logging.warning("Email sending failed for archive: %s", archive_path)

            return True

        except Exception as e:
            logging.error("Archiving error for %s: %s", date, e)
            return False
