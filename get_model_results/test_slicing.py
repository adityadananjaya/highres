import unittest
from unittest.mock import patch, MagicMock

# Assuming the function is in a module named 'your_module'
from slicing import slice

class TestSliceFunction(unittest.TestCase):

    @patch('slicing.slice_coco')
    def test_slice(self, mock_slice_coco):
        # Set up test parameters
        parent_folder = '/path/to/parent'
        json_file = '/path/to/annotations.json'
        output_folder = '/path/to/output'

        # Call the function
        slice(parent_folder, json_file, output_folder)

        # Assert that slice_coco was called with the correct arguments
        mock_slice_coco.assert_called_once_with(
            coco_annotation_file_path=json_file,
            image_dir=parent_folder,
            output_coco_annotation_file_name="sliced_annotations.json",
            output_dir=output_folder,
            slice_height=640,
            slice_width=640,
            overlap_height_ratio=0.2,
            overlap_width_ratio=0.2
        )

    @patch('slicing.slice_coco')
    def test_slice_with_different_params(self, mock_slice_coco):
        # Test with different parameters
        parent_folder = '/different/parent'
        json_file = '/different/annotations.json'
        output_folder = '/different/output'

        slice(parent_folder, json_file, output_folder)

        mock_slice_coco.assert_called_once_with(
            coco_annotation_file_path='/different/annotations.json',
            image_dir='/different/parent',
            output_coco_annotation_file_name="sliced_annotations.json",
            output_dir='/different/output',
            slice_height=640,
            slice_width=640,
            overlap_height_ratio=0.2,
            overlap_width_ratio=0.2
        )

    @patch('slicing.slice_coco')
    def test_slice_coco_not_called(self, mock_slice_coco):
        # Test that slice_coco is not called if we don't call slice
        mock_slice_coco.assert_not_called()

if __name__ == '__main__':
    unittest.main()