import unittest
from unittest.mock import patch, mock_open, MagicMock
import sys
import os
from PIL import Image
import io
import csv
from io import StringIO
from math import floor
from PIL import Image, UnidentifiedImageError
from unittest.mock import patch, mock_open, call
from json_to_yolo import convert_coco_json_to_yolo, convert_bbox_coco_to_yolo
from unittest.mock import patch, mock_open, call

class Test_json_to_yolo_functions(unittest.TestCase):
    def test_convert_bbox_coco_to_yolo(self):
        image_width, image_height = 100, 100
        coco_bbox = [10, 20, 30, 40]
        expected_yolo_bbox = [0.25, 0.4, 0.3, 0.4]
        result = convert_bbox_coco_to_yolo(image_width, image_height, coco_bbox)
        self.assertAlmostEqual(result, expected_yolo_bbox, places=6)

        # Test case 2: Bbox at image corner
        image_width, image_height = 200, 200
        coco_bbox = [0, 0, 50, 50]
        expected_yolo_bbox = [0.125, 0.125, 0.25, 0.25]
        result = convert_bbox_coco_to_yolo(image_width, image_height, coco_bbox)
        self.assertAlmostEqual(result, expected_yolo_bbox, places=6)

        # Test case 3: Bbox covering entire image
        image_width, image_height = 300, 300
        coco_bbox = [0, 0, 300, 300]
        expected_yolo_bbox = [0.5, 0.5, 1.0, 1.0]
        result = convert_bbox_coco_to_yolo(image_width, image_height, coco_bbox)
        self.assertAlmostEqual(result, expected_yolo_bbox, places=6)

        # Test case 4: Non-square image
        image_width, image_height = 400, 200
        coco_bbox = [100, 50, 200, 100]
        expected_yolo_bbox = [0.5, 0.5, 0.5, 0.5]
        result = convert_bbox_coco_to_yolo(image_width, image_height, coco_bbox)
        self.assertAlmostEqual(result, expected_yolo_bbox, places=6)

    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json_to_yolo.convert_bbox_coco_to_yolo')
    def test_convert_coco_json_to_yolo(self, mock_convert_bbox, mock_json_load, mock_file, mock_makedirs, mock_exists):
         # Mock os.path.exists to return False (directory doesn't exist)
        mock_exists.return_value = False

        # Mock JSON data
        mock_json_data = {
            'images': [
                {'id': 1, 'file_name': 'image1.jpg', 'width': 100, 'height': 100},
                {'id': 2, 'file_name': 'image2.jpg', 'width': 200, 'height': 200}
            ],
            'categories': [
                {'id': 1, 'name': 'cat'},
                {'id': 2, 'name': 'dog'}
            ],
            'annotations': [
                {'image_id': 1, 'category_id': 1, 'bbox': [10, 10, 30, 30]},
                {'image_id': 1, 'category_id': 2, 'bbox': [50, 50, 20, 20]},
                {'image_id': 2, 'category_id': 1, 'bbox': [20, 20, 40, 40]}
            ]
        }
        mock_json_load.return_value = mock_json_data

        # Mock convert_bbox_coco_to_yolo to return a fixed value
        mock_convert_bbox.return_value = [0.25, 0.25, 0.3, 0.3]

        # Call the function
        convert_coco_json_to_yolo('dummy_path.json', 'output_dir')

        # Assertions
        mock_exists.assert_called_once_with('output_dir')
        mock_makedirs.assert_called_once_with('output_dir')
        
        # Check if the JSON file was read
        mock_file.assert_any_call('dummy_path.json', 'r')
        mock_json_load.assert_called_once()

        # Check if YOLO annotation files were created
        mock_file.assert_any_call(os.path.join('output_dir', 'image1.txt'), 'a')
        mock_file.assert_any_call(os.path.join('output_dir', 'image2.txt'), 'a')

        # Check the content written to the files
        handle = mock_file()
        write_calls = handle.write.call_args_list
        self.assertEqual(write_calls, [
            call('8 0.250000 0.250000 0.300000 0.300000\n'),
            call('8 0.250000 0.250000 0.300000 0.300000\n'),
            call('8 0.250000 0.250000 0.300000 0.300000\n')
        ])

        # Check if convert_bbox_coco_to_yolo was called correctly
        mock_convert_bbox.assert_has_calls([
            call(100, 100, [10, 10, 30, 30]),
            call(100, 100, [50, 50, 20, 20]),
            call(200, 200, [20, 20, 40, 40])
        ])


    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_empty_annotations(self, mock_json_load, mock_file, mock_makedirs, mock_exists):
        # Mock JSON data with no annotations
        mock_json_data = {
            'images': [{'id': 1, 'file_name': 'image1.jpg', 'width': 100, 'height': 100}],
            'categories': [{'id': 1, 'name': 'cat'}],
            'annotations': []
        }
        mock_json_load.return_value = mock_json_data

        # Call the function
        convert_coco_json_to_yolo('dummy_path.json', 'output_dir')

        # Assert that no annotation files were created
        handle = mock_file()
        handle.write.assert_not_called()
    
if __name__ == '__main__':
    unittest.main()