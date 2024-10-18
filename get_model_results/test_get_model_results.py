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

# Import the functions from your script
from get_model_results import return_yolo_models, write_csv_files, process_with_models, main

class TestYOLOFunctions(unittest.TestCase):
    def test_return_yolo_models(self):
        models = return_yolo_models()
        self.assertTrue("extra_large" in models)
        self.assertTrue("large" in models)
        self.assertTrue("medium" in models)
        self.assertTrue("small" in models)
        self.assertTrue("nano" in models)
    @patch('get_model_results.Image.open')
    def test_process_with_models(self, mock_image_open):
        # Mock image
        mock_img = MagicMock()
        mock_img.size = (1000, 1000)
        mock_image_open.return_value.__enter__.return_value = mock_img

        # Mock YOLO model
        mock_model = MagicMock()
        mock_pred = MagicMock()
        mock_pred.boxes.conf.mean.return_value.item.return_value = 0.8
        mock_pred.boxes.__len__.return_value = 5
        mock_model.predict.return_value = [mock_pred]

        # Test data
        imgs = ['test_image.jpg']
        all_models = {'model1': mock_model, 'model2': mock_model}

        # Call the function
        result = process_with_models(imgs, all_models)

        # Assertions
        self.assertEqual(len(result), 2)  # Two models, one image
        for row in result:
            self.assertIn(row['model'], ['model1', 'model2'])
            self.assertEqual(row['image'], 'test_image.jpg')
            self.assertEqual(row['resolution'], 1)  # 1000 * 1000 / 1000000 = 1
            self.assertEqual(row['detections'], 5)
            self.assertEqual(row['average confidence'], 0.8)

    @patch('get_model_results.Image.open')
    def test_process_with_models_invalid_image(self, mock_image_open):
        mock_image_open.side_effect = UnidentifiedImageError

        imgs = ['invalid_image.jpg']
        all_models = {'model1': MagicMock()}

        with patch('builtins.print') as mock_print:
            result = process_with_models(imgs, all_models)

        self.assertEqual(len(result), 0)
        mock_print.assert_called_once_with('invalid_image.jpg not an  image')

if __name__ == '__main__':
    unittest.main()



# import unittest

# class TestMyFunction(unittest.TestCase):
#     def test_addition(self):
#         self.assertEqual(1 + 1, 2)

# if __name__ == '__main__':
#     unittest.main()