from unittest import TestCase
import data_processor


class TestDataProcessor(TestCase):
    def test_remove_project_gutenberg_text(self):
        text = ("Information\n"
                "*** START OF THIS PROJECT GUTENBERG EBOOK FINDING WORTH WHILE SOUTHWEST ***\n"
                "Such a nice sentence.\n"
                "*** END OF THIS PROJECT GUTENBERG EBOOK TWO WORDS ***\n"
                "License")
        result = data_processor.remove_project_gutenberg_text(text).strip()
        self.assertEqual("Such a nice sentence.", result)
