import qrcode
import os
from hashlib import sha256


def generate_qr_code(data, output_path):
    """
    Generate a QR code image.
    
    Args:
        data: URL or data to encode in QR code
        output_path: Path to save the QR code image
    """
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )
    
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)
    
    return output_path


def generate_file_hash(file_path):
    """
    Generate SHA-256 hash of a file for integrity verification.
    
    Args:
        file_path: Path to the file
    
    Returns:
        Hexadecimal hash string
    """
    with open(file_path, "rb") as f:
        return sha256(f.read()).hexdigest()


def get_local_ip():
    """
    Get the local IP address of the machine.
    
    Returns:
        Local IP address string
    """
    import socket
    try:
        # Create a socket connection to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"