class InvalidFileException(Exception):
    def __init__(self, message="Invalid file type or size."):
        self.message = message
        super().__init__(self.message)

class S3UploadException(Exception):
    def __init__(self, message="Failed to upload file to S3."):
        self.message = message
        super().__init__(self.message)

class CVParseException(Exception):
    def __init__(self, message="Failed to parse CV."):
        self.message = message
        super().__init__(self.message)
