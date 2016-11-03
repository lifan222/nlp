# CaboCha のラッパー
# python 3 用のコード
import xml.etree.ElementTree as ET
import subprocess
import sys
import platform

# コマンドライン引数の解析
class AppSettings:
    def __init__(self, args):
        opt = False
        optstr = ''
        dic = {'file':'','input':'','help':'', 'fromstdin':''}
        for str in args[-(len(args)-1):]:
            if opt == True:
                dic[optstr] = str;
                opt = False
            else:
                if (str[0] == '-' or str[0] == '/' ):
                    str = str[-(len(str)-1):]
                    if str == 'o':
                        opt = True
                        optstr = 'file'
                    elif str == '-help':
                        dic['help'] = 'on'
                    elif str == 'h':
                        dic['help'] = 'on'
                    elif str == '-stdin':
                        dic['fromstdin'] = 'on'
                    elif str == 's':
                        dic['fromstdin'] = 'on'
                else:
                    dic['input'] = str
        self.inputfile = dic['input']
        self.outfile = dic['file']
        if len(dic['help'])>0:
            self.help = True
        else:
            self.help = False;
        if len(dic['fromstdin'])>0:
            self.fromstdin = True
        else:
            self.fromstdin = False;
        if len(self.inputfile) == 0:
            self.help = True

app = AppSettings(sys.argv)

if app.help == True:
    print('usage:');
    print('python cabochawrap.py [--help|-h]')
    print('python cabochawrap.py [-o outputfilename] inputfilename')
    print('\tinputfilename: plain text to input')
    print('\toutputname: xml filename to output')
    exit()

# xmlファイルに記述されてるCaboChaのパスを取得
# 結果は辞書形式で帰ってくる
#
def CaboChaInit ():
    tree = ET.parse('config.xml');
    root = tree.getroot();
    CaboChaPath = "";
    cabochaelem = None
    cabochaencode = 'shift-jis'
    result = 0;
    for modelem in root.findall('module'):
        if modelem.attrib['name'] == 'cabocha':
            cabochaelem = modelem
    if cabochaelem == None:
        print('error: Cabocha モジュールが見つかりません')
        return [0, CaboChaPath]
    CaboChaDirPath = cabochaelem.attrib['path'];
    cabochaencode = cabochaelem.attrib['encode']
    for elem in cabochaelem.findall('directory'):
        if int(elem.attrib['import']) == 1:
            CaboChaPath = CaboChaDirPath + '\\' + elem.attrib['name']
            result = 1
    return [result,CaboChaPath,cabochaencode]
# 指定したコマンドの出力を取得
# バイト列を送ってバイト列を返してもらう
def res_cmd(cmd,input):
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    return process.communicate(input=input)[0];
def res_cmd_stdin(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True)
    return popen.communicate()[0];

# CaboChaの起動
def ShellCaboCha(CaboChaPath,targetPath,cabochaEncode='shift-jis') :
    CaboChaToolPath = CaboCha[1]+"\\CaboCha.exe"
    lookup = ('utf_8', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213',
        'shift_jis', 'shift_jis_2004','shift_jisx0213',
        'iso2022jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_3',
        'iso2022_jp_ext','latin_1', 'ascii')
    # 引用 片っ端からデコード
    encode = None
    inputstr=''
    for encoding in lookup:
        try:
            f = open(targetPath, "r",encoding=encoding)
            inputstr = f.read()
            f.close()
            break
        except:
            pass
    inputbytes = inputstr.encode(cabochaEncode, 'ignore');
    if isinstance(inputstr, str):
        bytes = res_cmd('\"'+CaboChaToolPath+'\" -f3', inputbytes)
    else:
        bytes = res_cmd_stdin('\"'+CaboChaToolPath+'\"')
    return bytes.decode(cabochaEncode, 'ignore')
CaboCha = CaboChaInit()
if CaboCha[0] == 0 :
    exit()
result = ShellCaboCha(CaboCha[1], app.inputfile,CaboCha[2])
xml = ET.fromstring("<document>"+result+"</document>")
xmlTree = ET.ElementTree(element=xml)
if len(app.outfile) > 0:
    xmlTree.write(app.outfile, 'utf-8', True)
else:
    ET.tostring(xml)
