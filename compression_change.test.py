from compression_change import compression_change, change_compression, get_file_size
import unittest
import os
import io
import sys

class TestCompressionChange(unittest.TestCase):
    def test_batch_functionality(self):
        compression_change("./test_resolution_images", [95, 90, 85])
        self.assertEqual(os.path.exists("./test_resolution_images/95percent/test8-64mp.jpg"), True)
        self.assertEqual(os.path.exists("./test_resolution_images/90percent/test8-64mp.jpg"), True)
        self.assertEqual(os.path.exists("./test_resolution_images/85percent/test8-64mp.jpg"), True)

        os.remove("./test_resolution_images/95percent/test8-64mp.jpg")
        os.remove("./test_resolution_images/90percent/test8-64mp.jpg")
        os.remove("./test_resolution_images/85percent/test8-64mp.jpg")
        
        os.rmdir("./test_resolution_images/95percent")
        os.rmdir("./test_resolution_images/90percent")
        os.rmdir("./test_resolution_images/85percent")


    def test_reduced_file_size(self):
        compression_change("./test_resolution_images", [95, 90, 85])

        # Use get_file_size
        original_size = get_file_size("./test_resolution_images/test8-64mp.jpg")
        first_size = get_file_size("./test_resolution_images/95percent/test8-64mp.jpg")
        second_size = get_file_size("./test_resolution_images/90percent/test8-64mp.jpg")
        third_size = get_file_size("./test_resolution_images/85percent/test8-64mp.jpg")

        # Compare file sizes
        self.assertGreater(original_size, first_size)
        self.assertGreater(first_size, second_size)
        self.assertGreater(second_size, third_size)

        # Cleaning up after creation
        os.remove("./test_resolution_images/95percent/test8-64mp.jpg")
        os.remove("./test_resolution_images/90percent/test8-64mp.jpg")
        os.remove("./test_resolution_images/85percent/test8-64mp.jpg")
        
        os.rmdir("./test_resolution_images/95percent")
        os.rmdir("./test_resolution_images/90percent")
        os.rmdir("./test_resolution_images/85percent")
    
    def test_incorrect_percentage(self):
        compression_change("./test_resolution_images", [-1, -500, 101, 400])


        self.assertEqual(os.path.exists("./test_resolution_images/-1percent/test8-64mp.jpg"), False)
        self.assertEqual(os.path.exists("./test_resolution_images/-500percent/test8-64mp.jpg"), False)
        self.assertEqual(os.path.exists("./test_resolution_images/101percent/test8-64mp.jpg"), False)
        self.assertEqual(os.path.exists("./test_resolution_images/400percent/test8-64mp.jpg"), False)
    
    def file_does_not_exist(self):
        error_msg = io.StringIO()
        sys.stdout = error_msg
        change_compression("./test_resolution_images/test.jpg", 95, "./test_resolution_images")

        self.assertEquals(error_msg, "./test_resolution_images/test.jpg does not exist")

if __name__ == "__main__":
    unittest.main()