''' This class will split output of HPE Comware's "display diagnostic-information"
    command into individual files. The origin format is as following:
    ==========================(CRLF)   ... section separator
    =======command name=======(CRLF)   ... command name(use this as the basename of filename)
    content:line-1(CRCRLF)
    content:line-2(CRCRLF)
    ...(CRCRLF)
    (CRLF)(an empty line)
    ==========================(CRLF)   ... next section separator
    ...
'''
import  re

class MyLib(object):

    SECTION_SEPARATOR = re.compile('^==+$')
    COMMAND_NAME = re.compile('.*?===.*?')

    def __init__(self, verbose, verbose2) -> None:
        self.verbose = verbose
        self.verbose2 = verbose2

    def get_name(self):
        return "my_lib"

    def write_file(self, title, content):
        if not title or not content or (len(content) == 1 and content == '\n'):
            return
        title = re.sub(' ', '-', title)     # ' ' -> '-'
        filename = title + '.txt'
        if self.verbose:
            print(f'filename={filename}')
        with open(filename, mode = 'w') as f:
            f.write(content)

    def read_file(self, path):

        title = ''
        content = ''

        with open(path, 'rb') as f:
            while True:
                bline = f.readline()                # read 1 line with eol from file
                if len(bline) == 0:                 # reached EOF
                    break
                if len(bline) == 2:                 # CRLF only
                    content += line
                    continue
                eol1 = bline[-1]
                eol2 = bline[-2]
                eol3 = bline[-3]
                line = bline.decode('utf-8', 'ignore')  # bytes to string
                line = line.replace('\r\n', '\n')       # CRLF => LF
                if self.verbose2:
                    print(line, end="")
                if eol3 == 13:                      # carriage return
                    content += line.replace('\r\n', '\n')
                elif self.SECTION_SEPARATOR.match(line):
                    self.write_file(title, content)
                    title = ''
                    content = ''
                elif self.COMMAND_NAME.match(line):
                    line = re.sub('^ +', '', line)  # remove leading spaces
                    line = re.sub(' +$', '', line)  # remove trailing spaces
                    line = line.replace('\n', '')   # remove LF
                    line = re.sub('[=/]', '', line) # remove all '='s and '/'s
                    line = re.sub('^ +', '', line)  # remove leading spaces
                    line = re.sub(' +$', '', line)  # remove trailing spaces
                    line = re.sub('=', '', line)    # remove all '/'s
                    line = re.sub('-', ' ', line)   # '-' -> ' '
                    title = line
                else:
                    content += line
        self.write_file(title, content)
