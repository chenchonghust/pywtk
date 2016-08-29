import calendar
import csv
import numpy
import pandas
import time
from unittest import TestCase, skip
from zipfile import ZipFile

from wtk_api import get_forecast_data, FORECAST_ATTRS

class TestGetForecastData(TestCase):
    def test_partial_year(self):
        '''Match site data from forecast nc files
        '''
        # UTC
        start = pandas.Timestamp('2007-01-01', tz='utc')
        end = pandas.Timestamp('2007-01-02', tz='utc')
        fcst_data = get_forecast_data("53252", start, end)
        # From ncdump, all values are float32 which do not compare easily to
        # python floats which are float64
        expected = numpy.array([6.2671943, 8.6079865, 6.7353525,
                    6.384234, 0.26309761, 3.6874273, 1.4196928, 0.53551841,
                    10.572015, 13.249797, 10.526829, 10.306773], dtype='float32')
        self.assertEqual(25, len(fcst_data))
        self.assertTrue(numpy.array_equal(expected, list(fcst_data.ix[0])))
        ex_dict = dict(zip(FORECAST_ATTRS, expected))
        # Verify column names are correct
        for k, v in ex_dict.items():
            self.assertEqual(v, fcst_data.ix[0][k])
