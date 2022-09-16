import unittest
import utils
import datetime

class TestUtils(unittest.TestCase):

    def test_verificaConflitoDataReservas(self):
        result = utils.verificaConflitoDataReservas(
            [[datetime.datetime(2022, 9, 15, 17, 0),
             datetime.datetime(2022, 9, 22, 17, 0), 
            datetime.datetime(2022, 9, 15, 12, 0), 
            datetime.datetime(2022, 9, 22, 12, 0), 
            datetime.datetime(2022, 9, 16, 16, 0), 
            datetime.datetime(2022, 9, 23, 16, 0), 
            datetime.datetime(2022, 9, 30, 16, 0)], 
            [datetime.datetime(2022, 9, 15, 18, 0), 
            datetime.datetime(2022, 9, 22, 18, 0), 
            datetime.datetime(2022, 9, 15, 13, 0), 
            datetime.datetime(2022, 9, 22, 13, 0), 
            datetime.datetime(2022, 9, 16, 17, 0), 
            datetime.datetime(2022, 9, 23, 17, 0), 
            datetime.datetime(2022, 9, 30, 20, 0)]],
             
            datetime.datetime(2022, 9, 30, 17, 0),
             datetime.datetime(2022, 9, 30, 18, 0)
        )
        self.assertEqual(result, True)

        result = utils.verificaConflitoDataReservas(
            [[datetime.datetime(2022, 9, 15, 17, 0),
             datetime.datetime(2022, 9, 22, 17, 0), 
            datetime.datetime(2022, 9, 15, 12, 0), 
            datetime.datetime(2022, 9, 22, 12, 0), 
            datetime.datetime(2022, 9, 16, 16, 0), 
            datetime.datetime(2022, 9, 23, 16, 0), 
            datetime.datetime(2022, 9, 30, 16, 0)], 
            [datetime.datetime(2022, 9, 15, 18, 0), 
            datetime.datetime(2022, 9, 22, 18, 0), 
            datetime.datetime(2022, 9, 15, 13, 0), 
            datetime.datetime(2022, 9, 22, 13, 0), 
            datetime.datetime(2022, 9, 16, 17, 0), 
            datetime.datetime(2022, 9, 23, 17, 0), 
            datetime.datetime(2022, 9, 30, 20, 0)]],
             
            datetime.datetime(2022, 9, 30, 15, 0),
             datetime.datetime(2022, 9, 30, 21, 0)
        )
        self.assertEqual(result, True)

        result = utils.verificaConflitoDataReservas(
            [[datetime.datetime(2022, 9, 15, 17, 0),
             datetime.datetime(2022, 9, 22, 17, 0), 
            datetime.datetime(2022, 9, 15, 12, 0), 
            datetime.datetime(2022, 9, 22, 12, 0), 
            datetime.datetime(2022, 9, 16, 16, 0), 
            datetime.datetime(2022, 9, 23, 16, 0), 
            datetime.datetime(2022, 9, 30, 16, 0)], 
            [datetime.datetime(2022, 9, 15, 18, 0), 
            datetime.datetime(2022, 9, 22, 18, 0), 
            datetime.datetime(2022, 9, 15, 13, 0), 
            datetime.datetime(2022, 9, 22, 13, 0), 
            datetime.datetime(2022, 9, 16, 17, 0), 
            datetime.datetime(2022, 9, 23, 17, 0), 
            datetime.datetime(2022, 9, 30, 20, 0)]],
             
            datetime.datetime(2022, 9, 30, 15, 0),
             datetime.datetime(2022, 9, 30, 18, 0)
        )
        self.assertEqual(result, True)

        result = utils.verificaConflitoDataReservas(
            [[datetime.datetime(2022, 9, 15, 17, 0),
             datetime.datetime(2022, 9, 22, 17, 0), 
            datetime.datetime(2022, 9, 15, 12, 0), 
            datetime.datetime(2022, 9, 22, 12, 0), 
            datetime.datetime(2022, 9, 16, 16, 0), 
            datetime.datetime(2022, 9, 23, 16, 0), 
            datetime.datetime(2022, 9, 30, 16, 0)], 
            [datetime.datetime(2022, 9, 15, 18, 0), 
            datetime.datetime(2022, 9, 22, 18, 0), 
            datetime.datetime(2022, 9, 15, 13, 0), 
            datetime.datetime(2022, 9, 22, 13, 0), 
            datetime.datetime(2022, 9, 16, 17, 0), 
            datetime.datetime(2022, 9, 23, 17, 0), 
            datetime.datetime(2022, 9, 30, 20, 0)]],
             
            datetime.datetime(2022, 9, 30, 18, 0),
             datetime.datetime(2022, 9, 30, 22, 0)
        )
        self.assertEqual(result, True)

if __name__== '__main__':
    unittest.main()