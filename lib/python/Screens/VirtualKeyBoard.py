from enigma import eListboxPythonMultiContent, gFont, RT_HALIGN_CENTER, RT_VALIGN_CENTER, getPrevAsciiCode
from Screen import Screen
from Components.Language import language
from Components.ActionMap import NumberActionMap
from Components.Sources.StaticText import StaticText
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN
from Tools.LoadPixmap import LoadPixmap
from Tools.NumericalTextInput import NumericalTextInput

class VirtualKeyBoardList(MenuList):

    def __init__(self, list, enableWrapAround = False):
        MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('Regular', 28))
        self.l.setItemHeight(45)


KEY_IMAGES = {'BACKSPACE': 'skin_default/vkey_backspace.png',
 'CLEAR': 'skin_default/vkey_clr.png',
 'EXIT': 'skin_default/vkey_esc.png',
 'OK': 'skin_default/vkey_ok.png',
 'SHIFT': 'skin_default/vkey_shift.png',
 'SPACE': 'skin_default/vkey_space.png'}
KEY_IMAGES_SHIFT = {'BACKSPACE': 'skin_default/vkey_backspace.png',
 'CLEAR': 'skin_default/vkey_clr.png',
 'EXIT': 'skin_default/vkey_esc.png',
 'OK': 'skin_default/vkey_ok.png',
 'SHIFT': 'skin_default/vkey_shift_sel.png',
 'SPACE': 'skin_default/vkey_space.png'}

def VirtualKeyBoardEntryComponent(keys, selectedKey, shiftMode = False):
    key_bg = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, 'skin_default/vkey_bg.png'))
    key_bg_width = key_bg.size().width()
    if shiftMode:
        key_images = KEY_IMAGES_SHIFT
    else:
        key_images = KEY_IMAGES
    res = [keys]
    x = 0
    count = 0
    for count, key in enumerate(keys):
        width = None
        png = key_images.get(key, None)
        if png:
            pixmap = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, png))
            width = pixmap.size().width()
            res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=pixmap))
        else:
            width = key_bg_width
            res.extend((MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=key_bg), MultiContentEntryText(pos=(x, 0), size=(width, 45), font=0, text=key.encode('utf-8'), flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER)))
        if selectedKey == count:
            key_sel = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, 'skin_default/vkey_sel.png'))
            width = key_sel.size().width()
            res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=key_sel))
        if width is not None:
            x += width
        else:
            x += 45

    return res


class VirtualKeyBoard(Screen):

    def __init__(self, session, title = '', text = ''):
        Screen.__init__(self, session)
        self.keys_list = []
        self.shiftkeys_list = []
        self.lang = language.getLanguage()
        self.nextLang = None
        self.shiftMode = False
        self.text = text
        self.selectedKey = 0
        self.smsChar = None
        self.sms = NumericalTextInput(self.smsOK)
        self['country'] = StaticText('')
        self['header'] = Label(title)
        self['text'] = Label(self.text)
        self['list'] = VirtualKeyBoardList([])
        self['actions'] = NumberActionMap(['OkCancelActions',
         'WizardActions',
         'ColorActions',
         'KeyboardInputActions',
         'InputBoxActions',
         'InputAsciiActions'], {'gotAsciiCode': self.keyGotAscii,
         'ok': self.okClicked,
         'cancel': self.exit,
         'left': self.left,
         'right': self.right,
         'up': self.up,
         'down': self.down,
         'red': self.backClicked,
         'green': self.ok,
         'yellow': self.switchLang,
         'blue': self.shiftClicked,
         'deleteBackward': self.backClicked,
         'back': self.exit,
         '1': self.keyNumberGlobal,
         '2': self.keyNumberGlobal,
         '3': self.keyNumberGlobal,
         '4': self.keyNumberGlobal,
         '5': self.keyNumberGlobal,
         '6': self.keyNumberGlobal,
         '7': self.keyNumberGlobal,
         '8': self.keyNumberGlobal,
         '9': self.keyNumberGlobal,
         '0': self.keyNumberGlobal}, -2)
        self.setLang()
        self.onExecBegin.append(self.setKeyboardModeAscii)
        self.onLayoutFinish.append(self.buildVirtualKeyBoard)

    def switchLang(self):
        self.lang = self.nextLang
        self.setLang()
        self.buildVirtualKeyBoard()

    def setLang(self):
        if self.lang == 'de_DE':
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'q',
              u'w',
              u'e',
              u'r',
              u't',
              u'z',
              u'u',
              u'i',
              u'o',
              u'p',
              u'\xfc',
              u'+'],
             [u'a',
              u's',
              u'd',
              u'f',
              u'g',
              u'h',
              u'j',
              u'k',
              u'l',
              u'\xf6',
              u'\xe4',
              u'#'],
             [u'<',
              u'y',
              u'x',
              u'c',
              u'v',
              u'b',
              u'n',
              u'm',
              u',',
              '.',
              u'-',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'@',
              u'\xdf',
              u'OK']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'"',
              u'\xa7',
              u'$',
              u'%',
              u'&',
              u'/',
              u'(',
              u')',
              u'=',
              u'BACKSPACE'],
             [u'Q',
              u'W',
              u'E',
              u'R',
              u'T',
              u'Z',
              u'U',
              u'I',
              u'O',
              u'P',
              u'\xdc',
              u'*'],
             [u'A',
              u'S',
              u'D',
              u'F',
              u'G',
              u'H',
              u'J',
              u'K',
              u'L',
              u'\xd6',
              u'\xc4',
              u"'"],
             [u'>',
              u'Y',
              u'X',
              u'C',
              u'V',
              u'B',
              u'N',
              u'M',
              u';',
              u':',
              u'_',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'?',
              u'\\',
              u'OK']]
            self.nextLang = 'ar_AE'
        elif self.lang == 'ar_AE':
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'\u0636',
              u'\u0635',
              u'\u062b',
              u'\u0642',
              u'\u0641',
              u'\u063a',
              u'\u0639',
              u'\u0647',
              u'\u062e',
              u'\u062d',
              u'\u062c',
              u'\u062f'],
             [u'\u0634',
              u'\u0633',
              u'\u064a',
              u'\u0628',
              u'\u0644',
              u'\u0627',
              u'\u062a',
              u'\u0646',
              u'\u0645',
              u'\u0643',
              u'\u0637',
              u'\u0630'],
             [u'\u0626',
              u'\u0621',
              u'\u0624',
              u'\u0631',
              u'\u0644\u0627',
              u'\u0649',
              u'\u0629',
              u'\u0648',
              u'\u0632',
              '\xd8\xb8',
              u'#',
              u'ALL'],
             [u'SHIFT',
              u'SPACE',
              u'-',
              u'@',
              u'.',
              u'\u0644\u0622',
              u'\u0622',
              u'\u0644\u0623',
              u'\u0644\u0625',
              u'\u0625',
              u'\u0623',
              u'OK',
              u'LEFT',
              u'RIGHT']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'"',
              u'\xa7',
              u'$',
              u'^',
              u'<',
              u'>',
              u'(',
              u')',
              u'=',
              u'BACKSPACE'],
             [u'\u064e',
              u'\u064b',
              u'\u064f',
              u'\u064c',
              u'%',
              u'\u060c',
              u'\u2018',
              u'\xf7',
              u'\xd7',
              u'\u061b',
              u'<',
              u'>'],
             [u'\u0650',
              u'\u064d',
              u']',
              u'[',
              u'*',
              u'+',
              u'\u0640',
              u'\u060c',
              u'/',
              u':',
              u'~',
              u"'"],
             [u'\u0652',
              u'}',
              u'{',
              u'-',
              u'/',
              u'\u2019',
              u',',
              u'.',
              u'\u061f',
              u':',
              u'_',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'?',
              u'\\',
              u'=',
              u'\u0651',
              u'~',
              u'OK',
              u'LEFT',
              u'RIGHT']]
            self.nextLang = 'es_ES'
        elif self.lang == 'es_ES':
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'q',
              u'w',
              u'e',
              u'r',
              u't',
              u'z',
              u'u',
              u'i',
              u'o',
              u'p',
              u'\xfa',
              u'+'],
             [u'a',
              u's',
              u'd',
              u'f',
              u'g',
              u'h',
              u'j',
              u'k',
              u'l',
              u'\xf3',
              u'\xe1',
              u'#'],
             [u'<',
              u'y',
              u'x',
              u'c',
              u'v',
              u'b',
              u'n',
              u'm',
              u',',
              '.',
              u'-',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'@',
              u'\u0141',
              u'\u0155',
              u'\xe9',
              u'\u010d',
              u'\xed',
              u'\u011b',
              u'\u0144',
              u'\u0148',
              u'OK']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'"',
              u'\xa7',
              u'$',
              u'%',
              u'&',
              u'/',
              u'(',
              u')',
              u'=',
              u'BACKSPACE'],
             [u'Q',
              u'W',
              u'E',
              u'R',
              u'T',
              u'Z',
              u'U',
              u'I',
              u'O',
              u'P',
              u'\xda',
              u'*'],
             [u'A',
              u'S',
              u'D',
              u'F',
              u'G',
              u'H',
              u'J',
              u'K',
              u'L',
              u'\xd3',
              u'\xc1',
              u"'"],
             [u'>',
              u'Y',
              u'X',
              u'C',
              u'V',
              u'B',
              u'N',
              u'M',
              u';',
              u':',
              u'_',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'?',
              u'\\',
              u'\u0154',
              u'\xc9',
              u'\u010c',
              u'\xcd',
              u'\u011a',
              u'\u0143',
              u'\u0147',
              u'OK']]
            self.nextLang = 'fi_FI'
        elif self.lang == 'fi_FI':
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'q',
              u'w',
              u'e',
              u'r',
              u't',
              u'z',
              u'u',
              u'i',
              u'o',
              u'p',
              u'\xe9',
              u'+'],
             [u'a',
              u's',
              u'd',
              u'f',
              u'g',
              u'h',
              u'j',
              u'k',
              u'l',
              u'\xf6',
              u'\xe4',
              u'#'],
             [u'<',
              u'y',
              u'x',
              u'c',
              u'v',
              u'b',
              u'n',
              u'm',
              u',',
              '.',
              u'-',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'@',
              u'\xdf',
              u'\u013a',
              u'OK']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'"',
              u'\xa7',
              u'$',
              u'%',
              u'&',
              u'/',
              u'(',
              u')',
              u'=',
              u'BACKSPACE'],
             [u'Q',
              u'W',
              u'E',
              u'R',
              u'T',
              u'Z',
              u'U',
              u'I',
              u'O',
              u'P',
              u'\xc9',
              u'*'],
             [u'A',
              u'S',
              u'D',
              u'F',
              u'G',
              u'H',
              u'J',
              u'K',
              u'L',
              u'\xd6',
              u'\xc4',
              u"'"],
             [u'>',
              u'Y',
              u'X',
              u'C',
              u'V',
              u'B',
              u'N',
              u'M',
              u';',
              u':',
              u'_',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'?',
              u'\\',
              u'\u0139',
              u'OK']]
            self.nextLang = 'ru_RU'
        elif self.lang == 'ru_RU':
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'\u0439',
              u'\u0446',
              u'\u0443',
              u'\u043a',
              u'\u0435',
              u'\u043d',
              u'\u0433',
              u'\u0448',
              u'\u0449',
              u'\u0437',
              u'\u0445',
              u'+'],
             [u'\u0444',
              u'\u044b',
              u'\u0432',
              u'\u0430',
              u'\u0431',
              u'\u043f',
              u'\u0440',
              u'\u043e',
              u'\u043b',
              u'\u0434',
              u'\u0436',
              u'#'],
             [u'<',
              u'\u044d',
              u'\u044f',
              u'\u0447',
              u'\u0441',
              u'\u043c',
              u'\u0438',
              u'\u0442',
              u',',
              '.',
              u'-',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'@',
              u'\u044c',
              u'\u044e',
              u'\u044a',
              u'OK']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'"',
              u'\xa7',
              u'$',
              u'%',
              u'&',
              u'/',
              u'(',
              u')',
              u'=',
              u'BACKSPACE'],
             [u'\u0419',
              u'\u0426',
              u'\u0423',
              u'\u041a',
              u'\u0415',
              u'\u041d',
              u'\u0413',
              u'\u0428',
              u'\u0429',
              u'\u0417',
              u'I',
              u'\u0425',
              u'*'],
             [u'\u0424',
              u'\u042b',
              u'\u0412',
              u'\u0410',
              u'\u041f',
              u'\u0420',
              u'\u041e',
              u'\u041e',
              u'\u041b',
              u'\u0414',
              u'\u0416',
              u"'"],
             [u'>',
              u'\u042d',
              u'\u042f',
              u'\u0427',
              u'\u0421',
              u'\u041c',
              u'\u0418',
              u'\u0422',
              u';',
              u':',
              u'_',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'?',
              u'\\',
              u'\u042c',
              u'\u0411',
              u'\u042e',
              u'\u042a',
              u'OK']]
            self.nextLang = 'sv_SE'
        elif self.lang == 'sv_SE':
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'q',
              u'w',
              u'e',
              u'r',
              u't',
              u'z',
              u'u',
              u'i',
              u'o',
              u'p',
              u'\xe9',
              u'+'],
             [u'a',
              u's',
              u'd',
              u'f',
              u'g',
              u'h',
              u'j',
              u'k',
              u'l',
              u'\xf6',
              u'\xe4',
              u'#'],
             [u'<',
              u'y',
              u'x',
              u'c',
              u'v',
              u'b',
              u'n',
              u'm',
              u',',
              '.',
              u'-',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'@',
              u'\xdf',
              u'\u013a',
              u'OK']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'"',
              u'\xa7',
              u'$',
              u'%',
              u'&',
              u'/',
              u'(',
              u')',
              u'=',
              u'BACKSPACE'],
             [u'Q',
              u'W',
              u'E',
              u'R',
              u'T',
              u'Z',
              u'U',
              u'I',
              u'O',
              u'P',
              u'\xc9',
              u'*'],
             [u'A',
              u'S',
              u'D',
              u'F',
              u'G',
              u'H',
              u'J',
              u'K',
              u'L',
              u'\xd6',
              u'\xc4',
              u"'"],
             [u'>',
              u'Y',
              u'X',
              u'C',
              u'V',
              u'B',
              u'N',
              u'M',
              u';',
              u':',
              u'_',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'?',
              u'\\',
              u'\u0139',
              u'OK']]
            self.nextLang = 'sk_SK'
        elif self.lang == 'sk_SK':
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'q',
              u'w',
              u'e',
              u'r',
              u't',
              u'z',
              u'u',
              u'i',
              u'o',
              u'p',
              u'\xfa',
              u'+'],
             [u'a',
              u's',
              u'd',
              u'f',
              u'g',
              u'h',
              u'j',
              u'k',
              u'l',
              u'\u013e',
              u'@',
              u'#'],
             [u'<',
              u'y',
              u'x',
              u'c',
              u'v',
              u'b',
              u'n',
              u'm',
              u',',
              '.',
              u'-',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'\u0161',
              u'\u010d',
              u'\u017e',
              u'\xfd',
              u'\xe1',
              u'\xed',
              u'\xe9',
              u'OK']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'"',
              u'\xa7',
              u'$',
              u'%',
              u'&',
              u'/',
              u'(',
              u')',
              u'=',
              u'BACKSPACE'],
             [u'Q',
              u'W',
              u'E',
              u'R',
              u'T',
              u'Z',
              u'U',
              u'I',
              u'O',
              u'P',
              u'\u0165',
              u'*'],
             [u'A',
              u'S',
              u'D',
              u'F',
              u'G',
              u'H',
              u'J',
              u'K',
              u'L',
              u'\u0148',
              u'\u010f',
              u"'"],
             [u'\xc1',
              u'\xc9',
              u'\u010e',
              u'\xcd',
              u'\xdd',
              u'\xd3',
              u'\xda',
              u'\u017d',
              u'\u0160',
              u'\u010c',
              u'\u0164',
              u'\u0147'],
             [u'>',
              u'Y',
              u'X',
              u'C',
              u'V',
              u'B',
              u'N',
              u'M',
              u';',
              u':',
              u'_',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'?',
              u'\\',
              u'\xe4',
              u'\xf6',
              u'\xfc',
              u'\xf4',
              u'\u0155',
              u'\u013a',
              u'OK']]
            self.nextLang = 'cs_CZ'
        elif self.lang == 'cs_CZ':
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'q',
              u'w',
              u'e',
              u'r',
              u't',
              u'z',
              u'u',
              u'i',
              u'o',
              u'p',
              u'\xfa',
              u'+'],
             [u'a',
              u's',
              u'd',
              u'f',
              u'g',
              u'h',
              u'j',
              u'k',
              u'l',
              u'\u016f',
              u'@',
              u'#'],
             [u'<',
              u'y',
              u'x',
              u'c',
              u'v',
              u'b',
              u'n',
              u'm',
              u',',
              '.',
              u'-',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'\u011b',
              u'\u0161',
              u'\u010d',
              u'\u0159',
              u'\u017e',
              u'\xfd',
              u'\xe1',
              u'\xed',
              u'\xe9',
              u'OK']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'"',
              u'\xa7',
              u'$',
              u'%',
              u'&',
              u'/',
              u'(',
              u')',
              u'=',
              u'BACKSPACE'],
             [u'Q',
              u'W',
              u'E',
              u'R',
              u'T',
              u'Z',
              u'U',
              u'I',
              u'O',
              u'P',
              u'\u0165',
              u'*'],
             [u'A',
              u'S',
              u'D',
              u'F',
              u'G',
              u'H',
              u'J',
              u'K',
              u'L',
              u'\u0148',
              u'\u010f',
              u"'"],
             [u'>',
              u'Y',
              u'X',
              u'C',
              u'V',
              u'B',
              u'N',
              u'M',
              u';',
              u':',
              u'_',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'?',
              u'\\',
              u'\u010c',
              u'\u0158',
              u'\u0160',
              u'\u017d',
              u'\xda',
              u'\xc1',
              u'\xc9',
              u'OK']]
            self.nextLang = 'en_EN'
        else:
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'q',
              u'w',
              u'e',
              u'r',
              u't',
              u'y',
              u'u',
              u'i',
              u'o',
              u'p',
              u'-',
              u'['],
             [u'a',
              u's',
              u'd',
              u'f',
              u'g',
              u'h',
              u'j',
              u'k',
              u'l',
              u';',
              u"'",
              u'\\'],
             [u'<',
              u'z',
              u'x',
              u'c',
              u'v',
              u'b',
              u'n',
              u'm',
              u',',
              '.',
              u'/',
              u'CLEAR'],
             [u'SHIFT', u'SPACE', u'OK']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'@',
              u'#',
              u'$',
              u'%',
              u'^',
              u'&',
              u'(',
              u')',
              u'=',
              u'BACKSPACE'],
             [u'Q',
              u'W',
              u'E',
              u'R',
              u'T',
              u'Y',
              u'U',
              u'I',
              u'O',
              u'P',
              u'*',
              u']'],
             [u'A',
              u'S',
              u'D',
              u'F',
              u'G',
              u'H',
              u'J',
              u'K',
              u'L',
              u'?',
              u'"',
              u'|'],
             [u'>',
              u'Z',
              u'X',
              u'C',
              u'V',
              u'B',
              u'N',
              u'M',
              u';',
              u':',
              u'_',
              u'CLEAR'],
             [u'SHIFT', u'SPACE', u'OK']]
            self.lang = 'en_EN'
            self.nextLang = 'de_DE'
        self['country'].setText(self.lang)
        self.max_key = 47 + len(self.keys_list[4])

    def buildVirtualKeyBoard(self, selectedKey = 0):
        list = []
        if self.shiftMode:
            self.k_list = self.shiftkeys_list
            for keys in self.k_list:
                if selectedKey < 12 and selectedKey > -1:
                    list.append(VirtualKeyBoardEntryComponent(keys, selectedKey, True))
                else:
                    list.append(VirtualKeyBoardEntryComponent(keys, -1, True))
                selectedKey -= 12

        else:
            self.k_list = self.keys_list
            for keys in self.k_list:
                if selectedKey < 12 and selectedKey > -1:
                    list.append(VirtualKeyBoardEntryComponent(keys, selectedKey))
                else:
                    list.append(VirtualKeyBoardEntryComponent(keys, -1))
                selectedKey -= 12

        self['list'].setList(list)

    def backClicked(self):
        self.smsChar = None
        self.text = self.text[:-1]
        self['text'].setText(self.text.encode('utf-8'))

    def shiftClicked(self):
        self.smsChar = None
        self.shiftMode = not self.shiftMode
        self.buildVirtualKeyBoard(self.selectedKey)

    def okClicked(self):
        self.smsChar = None
        if self.shiftMode:
            list = self.shiftkeys_list
        else:
            list = self.keys_list
        selectedKey = self.selectedKey
        text = None
        for x in list:
            if selectedKey < 12:
                if selectedKey < len(x):
                    text = x[selectedKey]
                break
            else:
                selectedKey -= 12

        if text is None:
            return
        text = text.encode('UTF-8')
        if text == 'EXIT':
            self.close(None)
        elif text == 'BACKSPACE':
            ss = unicode(self['text'].getText(), 'utf-8')
            ss = ss[:-1]
            self.text = str(ss.encode('utf-8'))
            self['text'].setText(self.text)
        elif text == 'CLEAR':
            self.text = ''
            self['text'].setText(self.text.encode('utf-8'))
        elif text == 'SHIFT':
            self.shiftClicked()
        elif text == 'SPACE':
            self.text += ' '
            self['text'].setText(self.text.encode('utf-8'))
        elif text == 'OK':
            self.close(self.text.encode('utf-8'))
        else:
            self.text += text
            self['text'].setText(self.text.encode('utf-8'))

    def ok(self):
        self.close(self.text.encode('utf-8'))

    def exit(self):
        self.close(None)

    def left(self):
        self.smsChar = None
        self.selectedKey -= 1
        if self.selectedKey == -1:
            self.selectedKey = 11
        elif self.selectedKey == 11:
            self.selectedKey = 23
        elif self.selectedKey == 23:
            self.selectedKey = 35
        elif self.selectedKey == 35:
            self.selectedKey = 47
        elif self.selectedKey == 47:
            self.selectedKey = self.max_key
        self.showActiveKey()

    def right(self):
        self.smsChar = None
        self.selectedKey += 1
        if self.selectedKey == 12:
            self.selectedKey = 0
        elif self.selectedKey == 24:
            self.selectedKey = 12
        elif self.selectedKey == 36:
            self.selectedKey = 24
        elif self.selectedKey == 48:
            self.selectedKey = 36
        elif self.selectedKey > self.max_key:
            self.selectedKey = 48
        self.showActiveKey()

    def up(self):
        self.smsChar = None
        self.selectedKey -= 12
        if self.selectedKey < 0 and self.selectedKey > self.max_key - 60:
            self.selectedKey += 48
        elif self.selectedKey < 0:
            self.selectedKey += 60
        self.showActiveKey()

    def down(self):
        self.smsChar = None
        self.selectedKey += 12
        if self.selectedKey > self.max_key and self.selectedKey > 59:
            self.selectedKey -= 60
        elif self.selectedKey > self.max_key:
            self.selectedKey -= 48
        self.showActiveKey()

    def showActiveKey(self):
        self.buildVirtualKeyBoard(self.selectedKey)

    def keyNumberGlobal(self, number):
        self.smsChar = self.sms.getKey(number)
        print 'SMS', number, self.smsChar
        self.selectAsciiKey(self.smsChar)

    def smsOK(self):
        print 'SMS ok', self.smsChar
        if self.smsChar and self.selectAsciiKey(self.smsChar):
            print 'pressing ok now'
            self.okClicked()

    def keyGotAscii(self):
        self.smsChar = None
        if self.selectAsciiKey(str(unichr(getPrevAsciiCode()).encode('utf-8'))):
            self.okClicked()

    def selectAsciiKey(self, char):
        if char == ' ':
            char = 'SPACE'
        for keyslist in (self.shiftkeys_list, self.keys_list):
            selkey = 0
            for keys in keyslist:
                for key in keys:
                    if key == char:
                        self.shiftMode = keyslist is self.shiftkeys_list
                        self.selectedKey = selkey
                        self.showActiveKey()
                        return True
                    selkey += 1

        return False
