import unittest
from picksource import *
from transtosource import *

class TestResConvert(unittest.TestCase):
    @unittest.skip
    def test_xlsx_save(self):
        convertor = SourceToXlsx('test')
        convertor.save('test\\sources_test.xlsx')

    @unittest.skip
    def test_load_source_xlsx(self):
        source_map = SourceToXlsx.load_source_xlsx('test\\sources_test.xlsx')
        self.assertEqual('Music',
        source_map['music_31ab7049'].value)
        
        self.assertEqual('(SIM PIN required)',
        source_map['emergencyCallsOnly-pinRequired_8beba2ef'].value)

    @unittest.skip
    def test_load_trans_xlsx(self):
        trans_map = XlsxToSource().load_translate_xlsx('test\\translate_test.xlsx')
        self.assertEqual('级别23', trans_map['sk-SK'][0].translation)

    def test_get_feature(self):
        feature = SourcePicker.get_feature(r'D:\yunfeng\nstring\convert\source\en-US\apps\communications\contacts\contacts.properties')

        self.assertEqual('communications', feature)




if __name__ == '__main__':
    unittest.main()
