from abc import ABC, abstractmethod
from pathlib import Path

from app.parsing.vision.models import OCRResult
from PIL import Image

class BaseVisionProvider(ABC):

    @abstractmethod
    def extract(
        self,
        file: Path,
    ) -> OCRResult:
        ...
 
    @abstractmethod
    def extract_images(
        self,
        images : list[Image.Image],
    ) -> OCRResult:
        """
        Performs OCR on list of images
        """
        raise NotImplementedError
    
