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
        self.d.wipe_hist()
        past = time.time() - 10000
        self.d.diff(1,past)
        self.assertEqual(self.d.diff(1),1)

    def test_large_change_up(self):
        now = time.time()
        self.d.hist = [
                        {"t": now - 30, "e": 101},
                        {"t": now - 20, "e": 102},
                        {"t": now - 10, "e": 103},
                        ]
        self.assertEqual(self.d.diff(1500,now),102)

    def test_large_change_down(self):
        now = time.time()
        self.d.hist = [
                        {"t": now - 20, "e": 2000},
                        ]
        self.assertEqual(self.d.diff(100,now),2000)

    def test_ignore_large_slow_change(self):
        now = time.time()
        self.d.hist = [
                        {"t": now - 60, "e": 100},
                        {"t": now - 50, "e": 500},
                        {"t": now - 40, "e": 1000},
                        {"t": now - 30, "e": 1500},
                        {"t": now - 20, "e": 2000},
                        {"t": now - 10, "e": 2500},
                        ]
        self.assertEqual(self.d.diff(3000,now),3000)

    def test_history_length(self):
        now = time.time()
        # too young is < min_time 10
        # too old is > max_time 30
        self.d.hist = [
                        {"t": now - 40, "e": 100}, #  too old
                        {"t": now - 30, "e": 101}, #  too old
                        {"t": now - 20, "e": 102}, #  first valid
                        {"t": now - 15, "e": 103}, #  valid
                        {"t": now - 5, "e": 104},  #  too young
                        {"t": now - 3, "e": 105},  #  too young
                        ]

        hist = self.d.get_hist()
        self.assertEqual(hist['e'],102)

        # 2 old ones should be trimmed so = 4
        self.assertEqual(len(self.d.hist),4)

    def test_ignore_small_change(self):
        now = time.time()
        self.d.hist = [
                        {"t": now - 30, "e": 101},
                        {"t": now - 20, "e": 102},
                        {"t": now - 10, "e": 103},
                        ]
        now = time.time()
        self.assertEqual(self.d.diff(200,now),200)
    
    def test_small_change_over_boundary(self):
        boundary = diff_energy.energy_per_div
        now = time.time()
        self.d.hist = [
                        {"t": now - 10, "e": boundary - 10},
                        ]
        self.assertEqual(self.d.diff(boundary + 10,now),boundary + 10)

if __name__ == '__main__':
    unittest.main()
