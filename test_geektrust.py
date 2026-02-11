import unittest
import io
import sys
from geektrust import process_commands

class TestGeekTrustSamples(unittest.TestCase):
    def capture_output(self, input_lines):
        old_stdout = sys.stdout
        try:
            buffer = io.StringIO()
            sys.stdout = buffer
            process_commands(input_lines)
            return buffer.getvalue().strip()
        finally:
            sys.stdout = old_stdout

    def test_sample_input_output_1(self):
        inp = [
            "ALLOCATE 6000 3000 1000\n",
            "SIP 2000 1000 500\n",
            "CHANGE 4.00% 10.00% 2.00% JANUARY\n",
            "CHANGE -10.00% 40.00% 0.00% FEBRUARY\n",
            "CHANGE 12.50% 12.50% 12.50% MARCH\n",
            "CHANGE 8.00% -3.00% 7.00% APRIL\n",
            "CHANGE 13.00% 21.00% 10.50% MAY\n",
            "CHANGE 10.00% 8.00% -5.00% JUNE\n",
            "BALANCE MARCH\n",
            "REBALANCE\n"
        ]
        out = self.capture_output(inp).splitlines()
        # expected lines in sample 1:
        expected = ["10593 7897 2272", "23619 11809 3936"]
        self.assertEqual(out, expected)

    def test_sample_input_output_2(self):
        inp = [
            "ALLOCATE 8000 6000 3500\n",
            "SIP 3000 2000 1000\n",
            "CHANGE 11.00% 9.00% 4.00% JANUARY\n",
            "CHANGE -6.00% 21.00% -3.00% FEBRUARY\n",
            "CHANGE 12.50% 18.00% 12.50% MARCH\n",
            "CHANGE 23.00% -3.00% 7.00% APRIL\n",
            "BALANCE MARCH\n",
            "BALANCE APRIL\n",
            "REBALANCE\n"
        ]
        out = self.capture_output(inp).splitlines()
        expected = ["15937 14552 6187", "23292 16055 7690", "CANNOT_REBALANCE"]
        self.assertEqual(out, expected)

if __name__ == "__main__":
    unittest.main()
