import unittest
import time
from diff import diff_energy
import os

sens=50
max_energy=3000
max_time=30
class Test_Diff(unittest.TestCase):

    
    def setUp(self):
        import logging
        logging.basicConfig(level=logging.INFO)
        self.d = diff_energy(logging, max_energy=max_energy, sens=sens, max_time=max_time)    

    def test_convert(self):
        self.assertEqual(self.d.energy_to_div(max_energy),4)
        self.assertEqual(self.d.energy_to_div(max_energy/5),1)

    def test_convert_limits(self):
        self.assertEqual(self.d.energy_to_div(-2*max_energy),1)
        self.assertEqual(self.d.energy_to_div(2*max_energy),4)

    def test_no_history(self):
        self.assertEqual(self.d.get_last_valid(1),1)

    def test_time_too_long(self):
        now = time.time()
        self.d.hist = {"t": now - max_time - 1, "e": 100}
        self.assertEqual(self.d.get_last_valid(1),1)

    def test_large_change_up(self):
        now = time.time()
        self.d.hist = {"t": now - max_time / 2, "e": 100}
        self.assertEqual(self.d.get_last_valid(1500),100)

    def test_large_change_down(self):
        now = time.time()
        self.d.hist = {"t": now - max_time / 2, "e": 2000}
        self.assertEqual(self.d.get_last_valid(100),2000)

    def test_ignore_large_slow_change(self):
        e = 200
        self.assertEqual(self.d.get_last_valid(e),e)
        time.sleep(1.0)
        e += sens
        self.assertEqual(self.d.get_last_valid(e),e)
        time.sleep(1.0)
        e += sens
        self.assertEqual(self.d.get_last_valid(e),e)
        time.sleep(1.0)
        e += sens
        self.assertEqual(self.d.get_last_valid(e),e)
        time.sleep(1.0)
        e += sens
        self.assertEqual(self.d.get_last_valid(e),e)


    def test_ignore_small_change(self):
        e = 200
        self.assertEqual(self.d.get_last_valid(e),e)
        time.sleep(0.5)
        e += sens / 4
        self.assertEqual(self.d.get_last_valid(e),e)
        time.sleep(0.5)
        e += sens / 4
        self.assertEqual(self.d.get_last_valid(e),e)
        time.sleep(0.5)
        e += sens / 4
        self.assertEqual(self.d.get_last_valid(e),e)

    def test_small_change_over_boundary(self):
        boundary = self.d.energy_per_div
        now = time.time()
        self.d.hist = {"t": now - 10, "e": boundary - 10}
        time.sleep(1)
        self.assertEqual(self.d.get_last_valid(boundary + 10),boundary + 10)

    def test_no_repetition(self):
        self.assertEqual(self.d.get_last_valid(200),200)
        time.sleep(1)
        self.assertEqual(self.d.get_last_valid(250),250)
        time.sleep(1)
        self.assertEqual(self.d.get_last_valid(3000),250)
        time.sleep(1)
        self.assertEqual(self.d.get_last_valid(2800),3000)

if __name__ == '__main__':
    unittest.main()
