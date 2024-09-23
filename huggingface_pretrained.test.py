from huggingface_pretrained import huggingface_pretrained
import unittest
import os

class TestModelOutputs(unittest.TestCase):
    def test_multiple_datasets(self):
        huggingface_pretrained(["facebook/detr-resnet-50"], ["./testing/64mp", "./testing/16mp","./testing/4mp"], [90, 80])
        
        self.assertEqual(os.path.exists("./testing/4mp/facebook_detr-resnet-50/test.jpg"), True)
        self.assertEqual(os.path.exists("./testing/16mp/facebook_detr-resnet-50/test.jpg"), True)
        self.assertEqual(os.path.exists("./testing/64mp/facebook_detr-resnet-50/test.jpg"), True)

        self.assertEqual(os.path.exists("./testing/4mp/90percent/facebook_detr-resnet-50/test.jpg"), True)
        self.assertEqual(os.path.exists("./testing/16mp/90percent/facebook_detr-resnet-50/test.jpg"), True)
        self.assertEqual(os.path.exists("./testing/64mp/90percent/facebook_detr-resnet-50/test.jpg"), True)
        self.assertEqual(os.path.exists("./testing/4mp/80percent/facebook_detr-resnet-50/test.jpg"), True)
        self.assertEqual(os.path.exists("./testing/16mp/80percent/facebook_detr-resnet-50/test.jpg"), True)
        self.assertEqual(os.path.exists("./testing/64mp/80percent/facebook_detr-resnet-50/test.jpg"), True)

        os.remove("./testing/4mp/facebook_detr-resnet-50/test.jpg")
        os.remove("./testing/16mp/facebook_detr-resnet-50/test.jpg")
        os.remove("./testing/64mp/facebook_detr-resnet-50/test.jpg")

        os.remove("./testing/4mp/90percent/facebook_detr-resnet-50/test.jpg")
        os.remove("./testing/16mp/90percent/facebook_detr-resnet-50/test.jpg")
        os.remove("./testing/64mp/90percent/facebook_detr-resnet-50/test.jpg")
        os.remove("./testing/4mp/80percent/facebook_detr-resnet-50/test.jpg")
        os.remove("./testing/16mp/80percent/facebook_detr-resnet-50/test.jpg")
        os.remove("./testing/64mp/80percent/facebook_detr-resnet-50/test.jpg")
        
        os.rmdir("./testing/4mp/facebook_detr-resnet-50")
        os.rmdir("./testing/16mp/facebook_detr-resnet-50")
        os.rmdir("./testing/64mp/facebook_detr-resnet-50")

        os.rmdir("./testing/4mp/90percent/facebook_detr-resnet-50")
        os.rmdir("./testing/16mp/90percent/facebook_detr-resnet-50")
        os.rmdir("./testing/64mp/90percent/facebook_detr-resnet-50")
        os.rmdir("./testing/4mp/80percent/facebook_detr-resnet-50")
        os.rmdir("./testing/16mp/80percent/facebook_detr-resnet-50")
        os.rmdir("./testing/64mp/80percent/facebook_detr-resnet-50")
        

    def test_multiple_models(self):
        huggingface_pretrained(["facebook/detr-resnet-50", "facebook/detr-resnet-101"], ["./testing/4mp"])
        huggingface_pretrained(["facebook/detr-resnet-50", "facebook/detr-resnet-101"], ["./testing/4mp"], [90])

        self.assertEqual(os.path.exists("./testing/4mp/facebook_detr-resnet-50/test.jpg"), True)
        self.assertEqual(os.path.exists("./testing/4mp/90percent/facebook_detr-resnet-50/test.jpg"), True)
        self.assertEqual(os.path.exists("./testing/4mp/facebook_detr-resnet-101/test.jpg"), True)
        self.assertEqual(os.path.exists("./testing/4mp/90percent/facebook_detr-resnet-101/test.jpg"), True)

        os.remove("./testing/4mp/facebook_detr-resnet-50/test.jpg")
        os.remove("./testing/4mp/90percent/facebook_detr-resnet-101/test.jpg")
        os.remove("./testing/4mp/90percent/facebook_detr-resnet-50/test.jpg")
        os.remove("./testing/4mp/facebook_detr-resnet-101/test.jpg")

        os.rmdir("./testing/4mp/facebook_detr-resnet-50")
        os.rmdir("./testing/4mp/facebook_detr-resnet-101")
        os.rmdir("./testing/4mp/90percent/facebook_detr-resnet-50")
        os.rmdir("./testing/4mp/90percent/facebook_detr-resnet-101")

if __name__ == "__main__":
    unittest.main()