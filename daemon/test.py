import unittest
import time
from diff import diff_energy
import os


class Test_Diff(unittest.TestCase):

    def setUp(self):
        import logging
        logging.basicConfig(level=logging.INFO)
        self.d = diff_energy(logging)    

    def test_convert(self):
        self.assertEqual(self.d.energy_to_div(3000),4)
        self.assertEqual(self.d.energy_to_div(300),1)

    def test_convert_limits(self):
        self.assertEqual(self.d.energy_to_div(-10000),1)
        self.assertEqual(self.d.energy_to_div(10000),4)

    def test_no_history(self):
        self.assertEqual(self.d.diff(1),1)

    def test_time_too_long(self):
        now = time.time()
        self.d.hist = {"t": now - 10000, "e": 100}
        self.assertEqual(self.d.diff(1),1)

    def test_large_change_up(self):
        now = time.time()
        self.d.hist = {"t": now - 20, "e": 100}
        self.assertEqual(self.d.diff(1500),100)

    def test_large_change_down(self):
        now = time.time()
        self.d.hist = {"t": now - 20, "e": 2000}
        self.assertEqual(self.d.diff(100),2000)

    def test_ignore_large_slow_change(self):
        self.assertEqual(self.d.diff(200),200)
        time.sleep(2)
        self.assertEqual(self.d.diff(500),500)
        time.sleep(2)
        self.assertEqual(self.d.diff(800),800)
        time.sleep(2)
        self.assertEqual(self.d.diff(1000),1000)


    def test_ignore_small_change(self):
        self.assertEqual(self.d.diff(200),200)
        time.sleep(2)
        self.assertEqual(self.d.diff(250),250)
        time.sleep(2)
        self.assertEqual(self.d.diff(300),300)
        time.sleep(2)
        self.assertEqual(self.d.diff(350),350)

    def test_small_change_over_boundary(self):
        boundary = diff_energy.energy_per_div
        now = time.time()
        self.d.hist = {"t": now - 10, "e": boundary - 10}
        time.sleep(2)
        self.assertEqual(self.d.diff(boundary + 10),boundary + 10)

    def test_no_repetition(self):
        self.assertEqual(self.d.diff(200),200)
        time.sleep(2)
        self.assertEqual(self.d.diff(250),250)
        time.sleep(2)
        self.assertEqual(self.d.diff(3000),250)
        time.sleep(2)
        self.assertEqual(self.d.diff(2800),3000)

if __name__ == '__main__':
    unittest.main()
