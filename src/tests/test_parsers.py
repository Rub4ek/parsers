import arrow
import datetime

import pytest

from numbers import Number
from parsers import (DateHelper, 
                     RosstatKEP, CBR_USD, BrentEIA)


class Test_today:
    def test_today(self):
        assert DateHelper.today() == datetime.date.today()

class Test_make_date:
    def test_make_date_on_valid_input(self):
        date = DateHelper.make_date('2007-01-25')
        assert date.day == 25
        assert date.month == 1
        assert date.year == 2007

    def test_make_date_on_valid_input_in_slashed_format(self):
        date = DateHelper.make_date('2007/01/25')
        assert date.day == 25
        assert date.month == 1
        assert date.year == 2007

    def test_make_date_on_valid_input_none(self):
        assert DateHelper.make_date(None) == datetime.date.today()

    def test_make_date_on_invalid_input_out_of_range(self):
        with pytest.raises(ValueError):
            DateHelper.make_date('2007-25-01')

    def test_make_date_on_invalid_input_empty_str_raises_exception(self):
        with pytest.raises(Exception):
            DateHelper.make_date('')

    def test_make_date_on_no_argument_empty_raises_type_error(self):
        with pytest.raises(TypeError):
            DateHelper.make_date()


class Base_Test_Parser:
    
    def setup_method(self):
        #must overload this
        self.parser = None
        self.items = None

    def test_get_data_members_are_length_4(self):
        for item in self.items:
            assert len(item) == 4

    def test_get_produces_data_of_correct_types(self):
        for item in self.items:
            assert isinstance(item['date'], str)
            assert isinstance(item['freq'], str)
            assert isinstance(item['name'], str)
            assert isinstance(item['value'], Number)

    def test_get_data_item_date_in_valid_format(self):
        dates = (item['date'] for item in self.items)
        for date in dates:
            assert arrow.get(date)

    def test_get_data_item_date_in_valid_range(self):
        dates = (item['date'] for item in self.items)
        for date in dates:
            date = arrow.get(date).date()
            # EP: splitting to see what exactly fails
            assert self.parser.start_date <= date
            assert date <= datetime.date.today()

    def test_get_data_item_freq_is_one_letter_and_other_conditions(self):
        for item in self.items:
            freq = item['freq']
            assert freq.isalpha()
            assert len(freq) == 1            
            assert freq in self.parser.freqs

    def test_get_data_produces_valid_varname(self):
        for item in self.items:
            assert item['name'] in self.parser.all_varnames

    # valid code and good idea to check, but iplementation too copmplex 
    # for a base test class
    
    #def test_get_data_produces_values_in_valid_range(self, items, min, max):
    #    for item in items:
    #        assert min < item['value'] < max


class TestRosstatKep(Base_Test_Parser):
    
    def setup_method(self):
        self.parser = RosstatKEP('m')
        self.items = list(self.parser.get_data())

    #def test_get_data_produces_values_in_valid_range(self):
    #    cpi_data = [item for item in self.items
    #                if item['name'] == 'CPI_rog']
    #    eur_data = [item for item in self.items
    #                if item['name'] == 'RUR_EUR_eop']
    #    super(TestRosstatKep, self)\
    #        .test_get_data_produces_values_in_valid_range(cpi_data, 90, 110)
    #   super(TestRosstatKep, self)\
    #        .test_get_data_produces_values_in_valid_range(eur_data, 50, 80)


    def test_freqs_are_correct(self):
        assert self.parser.freqs == 'aqm'

    def test_start_date_is_correct(self):
        assert self.parser.start_date == arrow.get('1999-01-31').date()

    def test_source_url_is_correct(self):
        assert self.parser.source_url  == \
               ("http://www.gks.ru/wps/wcm/connect/"
               "rosstat_main/rosstat/ru/statistics/"
               "publications/catalog/doc_1140080765391")

    def test_all_varnames_are_correct(self):
        assert self.parser.all_varnames == ['CPI_rog', 'RUR_EUR_eop']


class TestCBR_USD(Base_Test_Parser):
    
    def setup_method(self):
        self.parser = CBR_USD('d')
        self.items = list(self.parser.get_data())

#    def test_get_data_produces_values_in_valid_range(self):
#        super(TestCBR_USD, self)\
#            .test_get_data_produces_values_in_valid_range(self.items, 50, 70)


    def test_freqs_are_correct(self):
        assert self.parser.freqs == 'd'

    def test_start_date_is_correct(self):
        assert self.parser.start_date == datetime.date(1991, 7, 1)

    def test_source_url_is_correct(self):
        assert self.parser.source_url  == ("http://www.cbr.ru/"
                                           "scripts/Root.asp?PrtId=SXML")

    def test_all_varnames_are_correct(self):
        assert self.parser.all_varnames == ['USDRUR_CB']


class TestBrentEIA(Base_Test_Parser):

    def setup_method(self):
        self.parser = BrentEIA('d')
        self.items = list(self.parser.get_data())

#    def test_get_data_produces_values_in_valid_range(self):
#        super(TestBrentEIA, self) \
#            .test_get_data_produces_values_in_valid_range(self.items, 20, 120)

    def test_freqs_are_correct(self):
        assert self.parser.freqs == 'd'

    def test_start_date_is_correct(self):
        assert self.parser.start_date == datetime.date(1987, 5, 15)

    def test_source_url_is_correct(self):
        assert self.parser.source_url  == ("https://www.eia.gov/opendata/"
                                           "qb.php?category=241335")

    def test_all_varnames_are_correct(self):
        assert self.parser.all_varnames == ['BRENT']


if __name__ == '__main__':
    pytest.main([__file__])
    