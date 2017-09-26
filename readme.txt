执行环境：python3 ， 需要安装openpyxl库（pip3 install openpyxl)

1. 从源文件source 提取string字串
执行  python picksource.py -i [path to en-US],
output: 提取出来的字串将存在与en-US同级的source.xlsx文件当中。


2. 将翻译好的字串导入源文件source中
执行 python transtosource.py -b [path to en-US]
  en-US 的父目录下还需要包含source.xlsx，trans.xlsx。
  source.xlsx 即是执行picksource.py 生成的文件。
  trans.xlsx 是基于source.xlsx 所做的翻译文件，格式是固定的,
  可参考test/transtosource/trans.xlsx文件, 通常由nstring 系统导出。
output:
  根据trans.xlsx的LangCode,拷贝生成相应的与en-US同级的目录,
  根据trans.xlsx和source.xlsx
  TextID匹配更新翻译内容。可参考test/transtosource/下的文件生成。

