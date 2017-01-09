#coding=utf-8
from docx import Document
import data
class Generator:

    def __init__(self):
        self.document = Document()

    def generate(self):
        self.write_head()
        self.write_app_info()
        self.write_binary_info()
        self.write_transport_info()
        self.write_storage_info()

        self.document.save('./temp/{}/report/{}.docx'.format(data.start_time, data.app_bundleID))

        #write app info

    def write_head(self):
        self.document.add_heading(u"iOS应用漏洞检测报告", level=0)


    def write_app_info(self):
        self.document.add_heading(u"应用详情",level=1)

        self.document.add_paragraph(u'检测时间：', style='ListBullet')
        self.document.add_paragraph(data.start_time)
        self.document.add_paragraph(u'应用ID：', style='ListBullet')
        self.document.add_paragraph(data.app_bundleID)
        self.document.add_paragraph(u'应用名称：', style='ListBullet')
        self.document.add_paragraph(data.metadata['name'])
        self.document.add_paragraph(u'应用版本：', style='ListBullet')
        self.document.add_paragraph(data.metadata['app_version'])
        self.document.add_paragraph(u'Bundle路径：', style='ListBullet')
        self.document.add_paragraph(data.metadata['bundle_directory'])
        self.document.add_paragraph(u'Data路径：', style='ListBullet')
        self.document.add_paragraph(data.metadata['data_directory'])

    def write_binary_info(self):
        self.document.add_heading(u"二进制检测结果：", level=1)

        self.document.add_heading(u"二进制保护措施检测", level=2)
        table = self.document.add_table(rows=1, cols=5)
        table.style = 'TableGrid'
        head_cell = table.rows[0].cells
        head_cell[0].text = u'架构'
        head_cell[1].text = 'Encrypted'
        head_cell[2].text = 'Stack Canaries'
        head_cell[3].text = 'ARC'
        head_cell[4].text = 'PIE'
        for arch in data.protection_check_lables.keys():
            row_cells = table.add_row().cells
            row_cells[0].text = arch
            row_cells[1].text = str(data.protection_check_lables[arch]['Encrypted'])
            row_cells[2].text = str(data.protection_check_lables[arch]['Stack Canaries'])
            row_cells[3].text = str(data.protection_check_lables[arch]['ARC'])
            row_cells[4].text = str(data.protection_check_lables[arch]['PIE'])

        self.document.add_heading(u"依赖库检测", level=2)
        table_share_lib = self.document.add_table(rows=1, cols=1)
        table_share_lib.style = 'TableGrid'
        head_cell_lib = table_share_lib.rows[0].cells
        head_cell_lib[0].text = 'Shared Library'
        for lib in data.shared_lib:
            print 'lib:',lib
            row_lib_cells = table_share_lib.add_row().cells
            row_lib_cells[0].text = lib

        self.document.add_heading(u"硬编码", level=2)
        table_hard_code = self.document.add_table(rows=1, cols=1)
        table_hard_code.style = 'TableGrid'
        head_hard_code = table_hard_code.rows[0].cells
        head_hard_code[0].text = 'HardCode:'
        if len(data.hardcode) == 0:
            row_lib_cells = table_hard_code.add_row().cells
            row_lib_cells[0].text = u'无'
        for code in data.hardcode:
            row_lib_cells = table_hard_code.add_row().cells
            row_lib_cells[0].text = code

    def write_transport_info(self):
        self.document.add_heading(u"传输层检测结果", level=1)
        self.document.add_heading(u"中间人攻击检测", level=2)
        self.document.add_heading(u"不安全协议使用", level=2)
        self.document.add_heading(u"敏感信息传输", level=2)

    def write_storage_info(self):
        self.document.add_heading(u"存储层检测结果", level=1)

        self.document.add_heading(u"动态检测结果", level=2)
        self.document.add_heading(u"KeyChain", level=3)
        self.document.add_heading(u"UserDefaults", level=3)
        self.document.add_heading(u"Plist", level=3)


        self.document.add_heading(u"本地审计检测结果", level=2)
        self.document.add_heading(u"KeyChain", level=3)
        self.document.add_heading(u"数据库文件", level=3)
        self.document.add_heading(u"Plist文件", level=3)
if __name__=='__main__':
    data = dict()
    Generator().generate()