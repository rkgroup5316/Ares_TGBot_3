import os


class Asset:
    """
    Class to represent an asset (image) with attributes for path, binary data, and value.

    Attributes:
        path (str): The file path of the image.
        data (bytes): The binary data of the image in memory.
        value (str, optional): An optional value associated with the asset.
    """

    def __init__(self, path: str, value: str = None) -> None:
        """
        Initializes an Asset object.

        Args:
            path (str): The file path of the image.
            value (str, optional): An optional value associated with the asset.
                Defaults to None.
        """

        self.path = path
        self.data: bytes = None  # Add type hint for clarity
        self.value = value

    def load(self) -> None:
        """
        Loads the image data from the file path into memory.

        Raises:
            FileNotFoundError: If the image file is not found.
            IOError: If there's an error reading the image file.
        """

        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Image file not found: {self.path}")

        try:
            with open(self.path, 'rb') as f:
                self.data = f.read()
                return self.data
        except IOError as e:
            raise IOError(f"Error reading image file: {self.path}") from e

def load_asset(path: str, value: str = None) -> Asset:
    """
    Loads an image into an Asset object.

    Args:
        path (str): The file path of the image.
        value (str, optional): An optional value associated with the asset.
                Defaults to None.

    Returns:
        Asset: The Asset object containing the image data, path, and value.
    """

    asset = Asset(path, value)
    bytesData=asset.load()
    return bytesData


def send_image_via_telegram_bot():
    pass



# Example usage
if __name__ == '__main__':
    image_path = 'path/to/your/image.jpg'
    asset = load_asset(image_path)

    # Send the image using your Telegram bot code (replace with your implementation)
    send_image_via_telegram_bot(asset.data)

    print(f"Image loaded: {asset.path}")
    if asset.value:
        print(f"Value associated with the asset: {asset.value}")
