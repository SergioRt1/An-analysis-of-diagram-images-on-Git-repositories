from PIL import Image


class ImageExtractor:
    valid_extensions = {".jpg", ".png", ".jpeg"}

    @staticmethod
    def is_valid(image_path):
        try:
            img = Image.open(image_path)
            w, h = img.size

            return w > 100 and h > 100
        except Exception:
            return False
