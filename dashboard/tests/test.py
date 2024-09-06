import unittest
from unittest.mock import patch
import pandas as pd
from data_handler import get_results
from callbacks import filter_results, dynamic_graph_size
import plotly.express as px

class TestDataHandler(unittest.TestCase):

    @patch('data_handler.pd.read_csv')
    def test_get_results(self, mock_read_csv):
        # Mock data for the CSV files
        mock_data_4mp = pd.DataFrame({'resolution': [4], 'model': ['extra_large'], 'detections': [100]})
        mock_data_16mp = pd.DataFrame({'resolution': [16], 'model': ['large'], 'detections': [120]})
        mock_data_64mp = pd.DataFrame({'resolution': [64], 'model': ['small'], 'detections': [130]})
        
        # Mock the return value of pd.read_csv
        mock_read_csv.side_effect = [mock_data_4mp, mock_data_16mp, mock_data_64mp]
        
        # Call get_results() and check if the concatenation is done correctly
        result = get_results()

        # Assert that all the data is concatenated correctly
        self.assertEqual(len(result), 3)
        self.assertIn('resolution', result.columns)
        self.assertIn('model', result.columns)
        self.assertIn('detections', result.columns)

class TestCallbacks(unittest.TestCase):

    def setUp(self):
        # Example mock data for testing
        self.mock_data = pd.DataFrame({
            'resolution': [4, 16, 64],
            'model': ['extra_large', 'large', 'small'],
            'detections': [100, 120, 130]
        })

    def test_filter_results_single_resolution(self):
        # Test filtering by single resolution
        result = filter_results(self.mock_data, '4', ['extra_large'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result['resolution'].iloc[0], 4)
        self.assertEqual(result['model'].iloc[0], 'extra_large')

    def test_filter_results_multiple_resolutions(self):
        # Test filtering by multiple resolutions
        result = filter_results(self.mock_data, ['4', '16'], ['extra_large', 'large'])
        self.assertEqual(len(result), 2)
        self.assertTrue(result['resolution'].isin([4, 16]).all())
        self.assertTrue(result['model'].isin(['extra_large', 'large']).all())

    def test_dynamic_graph_size(self):
        # Test if graph height is updated based on the number of models
        fig = px.box(self.mock_data, x="model", y="detections", color="resolution")
        dynamic_graph_size(['extra_large', 'large', 'small'], fig)

        # Check the updated height
        self.assertEqual(fig.layout.height, 500 * 2)

if __name__ == '__main__':
    unittest.main()