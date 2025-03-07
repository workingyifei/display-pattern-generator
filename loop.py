import cv2
import os
import logging
import sys
from typing import List, Set, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Debug info OpenCV version
logger.info(f"OpenCV version: {cv2.__version__}")

class PatternViewer:
    def __init__(self, pattern_dir: str, specified_patterns: Optional[List[str]] = None):
        self.pattern_dir = pattern_dir
        self.image_paths: List[str] = []
        self.window_name = "test patterns"
        self.valid_extensions: Set[str] = {".bmp", ".jpeg", ".png", ".tif", ".tiff"}
        self.specified_patterns = specified_patterns if specified_patterns else []

    def load_image_paths(self) -> None:
        """Load all valid image paths from the pattern directory."""
        try:
            for file in os.listdir(self.pattern_dir):
                extension = os.path.splitext(file)[1].lower()
                if extension in self.valid_extensions:
                    self.image_paths.append(os.path.join(self.pattern_dir, file))
            logger.info(f"Found {len(self.image_paths)} valid pattern files")
        except FileNotFoundError:
            logger.error(f"Pattern directory {self.pattern_dir} not found")
            raise

    def create_window(self) -> None:
        """Create fullscreen window for pattern display."""
        cv2.namedWindow(self.window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def display_patterns(self) -> None:
        """Display specified patterns in a loop until ESC is pressed."""
        if not self.image_paths:
            logger.error("No valid pattern files found")
            sys.exit(1)

        if self.specified_patterns:
            # Check if specified patterns contain valid files and exit if any do not exist 
            for pattern in self.specified_patterns:
                if not os.path.isfile(os.path.join(self.pattern_dir, pattern)):
                    logger.error(f"Specified pattern file does not exist: {pattern}")
                    sys.exit(1)
            self.image_paths = [path for path in self.image_paths if os.path.basename(path) in self.specified_patterns]

        # Check if each path is valid
        for image_path in self.image_paths:
            if not os.path.isfile(image_path):
                logger.error(f"Invalid pattern file path: {image_path}")
                sys.exit(1)

        self.create_window()
        
        try:
            while True:
                for image_path in self.image_paths:
                    image = cv2.imread(image_path)
                    
                    if image is None:
                        logger.error(f"Error loading: {image_path}")
                        continue
                        
                    cv2.imshow(self.window_name, image)
                    
                    # Wait for 1 second or ESC key
                    if cv2.waitKey(1000) == 27:  # ESC key
                        cv2.destroyWindow(self.window_name)
                        return
                        
        except KeyboardInterrupt:
            logger.info("Pattern display interrupted by user")
        finally:
            cv2.destroyWindow(self.window_name)

def main():
    if len(sys.argv) < 2:
        logger.error("Please specify the pattern directory as a command line argument.")
        sys.exit(1)

    pattern_directory = sys.argv[1]  # Get the pattern directory from command line argument
    specified_patterns = sys.argv[2:] if len(sys.argv) > 2 else None  # Get specified patterns from command line arguments
    viewer = PatternViewer(pattern_dir=pattern_directory, specified_patterns=specified_patterns)
    try:
        viewer.load_image_paths()
        viewer.display_patterns()
    except Exception as e:
        logger.error(f"Error running pattern viewer: {e}")

if __name__ == "__main__":
    main()
