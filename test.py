import unittest
from picksource import *
from transtosource import *

class TestResConvert(unittest.TestCase):
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

    def test_res_pattern(self):
        pattern = SourcePicker('').get_res_pattern()
        str1 = '# abc = 123'
        str2 = ' ab = 12 '
        str3 = 'dfsldsfj '

        match1 = pattern.match(str1)
        self.assertFalse( match1)
        match2 = pattern.match(str2)
        self.assertTrue( match2)
        self.assertEqual('ab', match2.groups()[0])
        self.assertEqual('12', match2.groups()[1].strip())
        match3 = pattern.match(str3)
        self.assertFalse(match3)


    def test_update_file(self):
        picker = SourcePicker('')
        res_list = picker.pick_file(r'test\music_c1.properties', '')
        updater = SourceUpdate()
        updater.update_file(r'test\music.properties', res_list)

    def test_pick_source(self):
        picker = SourceToXlsx(r'test\en-US')
        picker.save('source.xlsx')
        
    
    def test_trans_to_source(self):
        convertor = XlsxToSource()
        convertor.trans_to_source(r'test\transtosource\en-US',
        r'test\transtosource\source.xlsx',
        r'test\transtosource\trans.xlsx',)



if __name__ == '__main__':
    unittest.main()
