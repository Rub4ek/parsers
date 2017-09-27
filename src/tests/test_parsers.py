import pytest

import datetime

from parsers import (RosstatKEP_Monthly, 
                     RosstatKEP_Quarterly, 
                     RosstatKEP_Annual,
                     CBR_USD, 
                     BrentEIA)

PARSER_CLASSES = (RosstatKEP_Monthly, 
                  RosstatKEP_Quarterly, 
                  RosstatKEP_Annual,
                  CBR_USD, 
                  BrentEIA)

# attributes
# can be parametrized
def test_parser_class_atributes():
    for cls in PARSER_CLASSES:
        assert cls.freq.isalpha()
        assert len(cls.freq) == 1
        assert isinstance(cls.observation_start_date, datetime.date)
        assert isinstance(cls.source_url, str)
        assert cls.source_url.startswith('http')
        assert isinstance(cls.all_varnames, list)
        assert isinstance(cls.all_varnames[0], str)


# usual calls - no date
def test_parser_instance_created_without_date():
    for cls in PARSER_CLASSES:
        assert cls()
        

# usual calls - no date
def test_parser_instance_created_with_date():
    for cls in PARSER_CLASSES:
        assert cls('2017-09-15')        
  
      
def validate_datapoint(datapoint):
    # Suggestions: 
    #1. timestamp is recent 
    #2. number of fields is expected 
    #3. fields have correct type (value is float and timestamp is valid etc) 
    #4. names are correct. 
    #5. lists are non-empty or exception

    # dict has 4 elements
    assert isinstance(datapoint, dict)
    assert len(datapoint) == 4    
    # date
    assert isinstance(datapoint['date'], str)
    # frequency
    freq = datapoint['freq']
    assert isinstance(datapoint['freq'], str)
    assert freq in "aqmwd"
    # name
    assert isinstance(datapoint['name'], str)
    # value
    assert isinstance(datapoint['value'], float)

        
# .sample() method returns stream of dicts
def test_sample_method_returns_stream_of_dicts():
    for cls in PARSER_CLASSES:
        for datapoint in cls().sample():
            validate_datapoint(datapoint)           

def test_CBR_USD_will_not_work_before_1992():
    gen=CBR_USD('1992-01-01').yield_dicts()
    next(gen)    

def test_yield_dicts_method_is_callable():
    for cls in PARSER_CLASSES:
        gen = cls().yield_dicts()
        a = next(gen)
        validate_datapoint(a)  
      
        
#TODO: use parts of code belwo if needed for validate_datapoint()         
            
#class Base_Test_Parser:
#    
#    def setup_method(self):
#        #must overload this
#        self.parser = None
#        self.items = None
#
#    def test_get_data_members_are_length_4(self):
#        for item in self.items:
#            assert len(item) == 4
#
#    def test_get_produces_data_of_correct_types(self):
#        for item in self.items:
#            assert isinstance(item['date'], str)
#            assert isinstance(item['freq'], str)
#            assert isinstance(item['name'], str)
#            assert isinstance(item['value'], Number)
#
#    def test_get_data_item_date_in_valid_format(self):
#        dates = (item['date'] for item in self.items)
#        for date in dates:
#            assert arrow.get(date)
#
#    def test_get_data_item_date_in_valid_range(self):
#        dates = (item['date'] for item in self.items)
#        for date in dates:
#            date = arrow.get(date).date()
#            # EP: splitting to see what exactly fails
#            assert self.parser.start_date <= date
#            assert date <= datetime.date.today()
#
#    def test_get_data_item_freq_is_one_letter_and_other_conditions(self):
#        for item in self.items:
#            freq = item['freq']
#            assert freq.isalpha()
#            assert len(freq) == 1            
#            assert freq in self.parser.freqs
#
#    def test_get_data_produces_valid_varname(self):
#        for item in self.items:
#            assert item['name'] in self.parser.all_varnames
#
#    # valid code and good idea to check, but iplementation too copmplex 
#    # for a base test class
#    
#    #def test_get_data_produces_values_in_valid_range(self, items, min, max):
#    #    for item in items:
#    #        assert min < item['value'] < max

# ------------------------   end of datapoitn validation    



#
#
#class TestRosstatKep(Base_Test_Parser):
#    
#    def setup_method(self):
#        self.parser = RosstatKEP('m')
#        self.items = list(self.parser.get_data())
#
#    #def test_get_data_produces_values_in_valid_range(self):
#    #    cpi_data = [item for item in self.items
#    #                if item['name'] == 'CPI_rog']
#    #    eur_data = [item for item in self.items
#    #                if item['name'] == 'RUR_EUR_eop']
#    #    super(TestRosstatKep, self)\
#    #        .test_get_data_produces_values_in_valid_range(cpi_data, 90, 110)
#    #   super(TestRosstatKep, self)\
#    #        .test_get_data_produces_values_in_valid_range(eur_data, 50, 80)
#
#
#    def test_freqs_are_correct(self):
#        assert self.parser.freqs == 'aqm'
#
#    def test_start_date_is_correct(self):
#        assert self.parser.start_date == arrow.get('1999-01-31').date()
#
#    def test_source_url_is_correct(self):
#        assert self.parser.source_url  == \
#               ("http://www.gks.ru/wps/wcm/connect/"
#               "rosstat_main/rosstat/ru/statistics/"
#               "publications/catalog/doc_1140080765391")
#
#    def test_all_varnames_are_correct(self):
#        assert self.parser.all_varnames == ['CPI_rog', 'RUR_EUR_eop']
#
#


#    def yield_dicts(self):        
#        return cbr_fx.get_cbr_er(self.start, self.end)
#    
#    def sample(self):
#        """Yields dictionaries with sample datapoints."""
#        return iter([{'date': '2017-09-15', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 57.7706},
# {'date': '2017-09-16', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 57.5336},
# {'date': '2017-09-19', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 57.6242},
# {'date': '2017-09-20', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 58.0993},
# {'date': '2017-09-21', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 58.129},
# {'date': '2017-09-22', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 58.2242},
# {'date': '2017-09-23', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 57.6527},
# {'date': '2017-09-26', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 57.566}])
#
#
#class TestCBR_USD():
#    
#    def setup_method(self):
#        self.parser = CBR_USD('d')
#        self.items = list(self.parser.get_data())
#
##    def test_get_data_produces_values_in_valid_range(self):
##        super(TestCBR_USD, self)\
##            .test_get_data_produces_values_in_valid_range(self.items, 50, 70)
#
#
#    def test_freqs_are_correct(self):
#        assert self.parser.freqs == 'd'
#
#    def test_start_date_is_correct(self):
#        assert self.parser.start_date == datetime.date(1991, 7, 1)
#
#    def test_source_url_is_correct(self):
#        assert self.parser.source_url  == ("http://www.cbr.ru/"
#                                           "scripts/Root.asp?PrtId=SXML")
#
#    def test_all_varnames_are_correct(self):
#        assert self.parser.all_varnames == ['USDRUR_CB']
##
#
#class TestBrentEIA(Base_Test_Parser):
#
#    def setup_method(self):
#        self.parser = BrentEIA('d')
#        self.items = list(self.parser.get_data())
#
##    def test_get_data_produces_values_in_valid_range(self):
##        super(TestBrentEIA, self) \
##            .test_get_data_produces_values_in_valid_range(self.items, 20, 120)
#
#    def test_freqs_are_correct(self):
#        assert self.parser.freqs == 'd'
#
#    def test_start_date_is_correct(self):
#        assert self.parser.start_date == datetime.date(1987, 5, 15)
#
#    def test_source_url_is_correct(self):
#        assert self.parser.source_url  == ("https://www.eia.gov/opendata/"
#                                           "qb.php?category=241335")
#
#    def test_all_varnames_are_correct(self):
#        assert self.parser.all_varnames == ['BRENT']
#
#
if __name__ == '__main__':
    pytest.main([__file__])
