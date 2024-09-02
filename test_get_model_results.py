import unittest
from unittest.mock import patch, mock_open
import sys
import os
from PIL import Image
import csv
import io
import shutil

# Add the directory containing get_model_results.py to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import get_model_results

class TestGetModelResults(unittest.TestCase):

    def setUp(self):
        # Create a temporary test directory
        self.test_dir = os.path.join(os.path.dirname(__file__), 'test_directory')
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Create some dummy image files
        open(os.path.join(self.test_dir, 'image1.jpg'), 'w').close()
        open(os.path.join(self.test_dir, 'image2.jpg'), 'w').close()

        print(f"Test directory created: {self.test_dir}")

    

    @patch('get_model_results.YOLO')
    @patch('get_model_results.Image.open')
    @patch('get_model_results.csv.DictWriter')
    def test_script_execution(self, mock_csv_writer, mock_image_open, mock_yolo):
        # Mock command line argument
        sys.argv = ['get_model_results.py', self.test_dir]

        # Mock Image.open to return a mock image with size
        mock_img = unittest.mock.MagicMock()
        mock_img.size = (1000, 1000)
        mock_image_open.return_value.__enter__.return_value = mock_img

        # Mock YOLO model and predictions
        mock_model = unittest.mock.MagicMock()
        mock_boxes = unittest.mock.MagicMock()
        mock_boxes.conf.mean.return_value.item.return_value = 0.8
        mock_pred = [unittest.mock.MagicMock(boxes=mock_boxes)]
        mock_model.predict.return_value = mock_pred
        mock_yolo.return_value = mock_model

        # Capture CSV output
        csv_output = io.StringIO()
        mock_csv_writer.return_value = csv.DictWriter(csv_output, fieldnames=['model', 'image', 'resolution', 'detections', 'average confidence'])

        # Run the script
        get_model_results.main()

        # Assertions
        self.assertEqual(mock_image_open.call_count, 2)  # Called for each image
        self.assertEqual(mock_model.predict.call_count, 10)  # 5 models * 2 images

        # Check CSV output
        csv_output.seek(0)
        csv_content = csv_output.getvalue().splitlines()
        self.assertEqual(len(csv_content), 11)  # Header + 10 data rows
        self.assertEqual(csv_content[0], 'model,image,resolution,detections,average confidence')

    def test_invalid_directory(self):
        # Test with invalid directory
        invalid_dir = '/invalid/directory'
        sys.argv = ['get_model_results.py', invalid_dir]
        with self.assertRaises(SystemExit):
            get_model_results.main()

    def tearDown(self):
        # Remove the temporary test directory and its contents
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        print(f"Test directory removed: {self.test_dir}")
if __name__ == '__main__':
    unittest.main()