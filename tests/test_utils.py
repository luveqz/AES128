from tests.context import *
import unittest

class TestUtils(unittest.TestCase):

    def test_multiply(self):
        self.assertEqual(2, multiply(1, 2))
        self.assertEqual(32, multiply(16, 2))
        self.assertEqual(27, multiply(9, 3))
        self.assertEqual(9, multiply(9, 1))

    def test_set_offset(self):
        msg = 'Hey, I am here'

        result = set_offset(msg)
        expected = 'Hey, I am here  '

        self.assertEqual(expected, result)

    def test_fill_state(self):
        state = new_matrix(4, 4)
        msg = 'Dear Sheep, Hi.'

        fill_state(state, msg)

        expected = [
        [0x44, 0x20, 0x65, 0x48],
        [0x65, 0x53, 0x70, 0x69],
        [0x61, 0x68, 0x2c, 0x2e],
        [0x72, 0x65, 0x20, 0x20]]

        self.assertEqual(expected, state)

    def test_new_matrix(self):
        result = new_matrix(4, 4)

        self.assertEqual(4, len(result))

        for x in range(4):
            self.assertEqual(4, len(result[x]))

    def test_get_last_4_bytes(self):
        array = [0xec, 0x5f, 0x97, 0x44,
                 0x17, 0xc4, 0xa7, 0x7e,
                 None, None, None, None]

        last_4 = get_last_4_bytes(array)

        self.assertEqual(array[4:8], last_4)

    def test_add_last_4_bytes(self):
        array = [0x63, 0x7c, 0x77, 0x7b,
                 0xf2, 0x6b, 0x6f, 0xc5,
                 0x30, 0x01, 0x67, 0x2b,
                 0xfe, 0xd7, 0xab, 0x76,
                 None, None, None, None,
                 None, None, None, None]

        tmp = [0x97, 0x44, 0x17, 0xc4]

        add_last_4_bytes(array, tmp)

        expected = [0xf4, 0x38, 0x60, 0xbf]

        self.assertEqual(4, array.count(None))
        self.assertEqual(expected, array[16:20])

    def test_rotate_row(self):
        row = [0, 1, 2, 3]

        rotate_row(row, 3)
        self.assertEqual(3, row[2])
        self.assertEqual(0, row[3])

        rotate_row(row, -1)
        self.assertEqual(3, row[1])
        self.assertEqual(0, row[2])

    def test_format_byte(self):
        _hex = format_byte(0x1)
        self.assertEqual('01', _hex)

        _hex = format_byte(0xa5)
        self.assertEqual('A5', _hex)

    def test_state_to_string(self):
        state = [[0, 1, 2, 3],
                 [0, 1, 2, 3],
                 [0, 1, 2, 3],
                 [0, 1, 2, 3]]

        expected = ('00 00 00 00 '
                    '01 01 01 01 '
                    '02 02 02 02 '
                    '03 03 03 03')

        self.assertEqual(expected, state_to_string(state))

if __name__ == '__main__':
    unittest.main()
