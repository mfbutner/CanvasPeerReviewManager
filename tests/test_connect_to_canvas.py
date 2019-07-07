import canvasapi
import unittest
import sys

class CanvasConnect(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.url = 'https://canvas.ucdavis.edu'
        cls.password = ''  # put your authorization token here
    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()


    def test_connect(self):
        canvas = canvasapi.Canvas(self.url, self.password)
        course = canvas.get_course(1599)
        self.assertEqual(course.name, 'Matthew Butner Sandbox')


if __name__ == '__main__':
    unittest.main()
