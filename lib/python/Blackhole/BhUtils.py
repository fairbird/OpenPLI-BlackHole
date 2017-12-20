from re import sub
from Tools.Directories import fileExists, resolveFilename, SCOPE_CURRENT_SKIN
import xml.etree.cElementTree
entities = [('&#228;', u'\xe4'),
 ('&auml;', u'\xe4'),
 ('&#252;', u'\xfc'),
 ('&uuml;', u'\xfc'),
 ('&#246;', u'\xf6'),
 ('&ouml;', u'\xf6'),
 ('&#196;', u'\xc4'),
 ('&Auml;', u'\xc4'),
 ('&#220;', u'\xdc'),
 ('&Uuml;', u'\xdc'),
 ('&#214;', u'\xd6'),
 ('&Ouml;', u'\xd6'),
 ('&#223;', u'\xdf'),
 ('&szlig;', u'\xdf'),
 ('&#8230;', u'...'),
 ('&#8211;', u'-'),
 ('&#160;', u' '),
 ('&#34;', u'"'),
 ('&#38;', u'&'),
 ('&#39;', u"'"),
 ('&#60;', u'<'),
 ('&#62;', u'>'),
 ('&lt;', u'<'),
 ('&gt;', u'>'),
 ('&nbsp;', u' '),
 ('&amp;', u'&'),
 ('&quot;', u'"'),
 ('&apos;', u"'")]

def nab_strip_html(html):
    html = html.replace('\n', ' ')
    html = sub('\\s\\s+', ' ', html)
    html = sub('<br(\\s+/)?>', '\n', html)
    html = sub('</?(p|ul|ol)(\\s+.*?)?>', '\n', html)
    html = sub('<li(\\s+.*?)?>', '-', html)
    html = html.replace('</li>', '\n')
    return nab_strip_pass1(html)


def nab_strip_pass1(html):
    html = sub('<(.*?)>', '', html)
    html.replace('&#196;', '\xc3\x84')
    html.replace('&#228;', '\xc3\xa4')
    html.replace('&auml;', '\xc3\xa4')
    html.replace('&#252;', '\xc3\xbc')
    html.replace('&uuml;', '\xc3\xbc')
    html.replace('&#246;', '\xc3\xb6')
    html.replace('&ouml;', '\xc3\xb6')
    html.replace('&#196;', '\xc3\x84')
    html.replace('&Auml;', '\xc3\x84')
    html.replace('&#220;', '\xc3\x9c')
    html.replace('&Uuml;', '\xc3\x9c')
    html.replace('&#214;', '\xc3\x96')
    html.replace('&Ouml;', '\xc3\x96')
    html.replace('&#223;', '\xc3\x9f')
    html.replace('&szlig;', '\xc3\x9f')
    html.replace('&lt;', '<')
    html.replace('&gt;', '>')
    html.replace('&nbsp;', ' ')
    html.replace('&amp;', '&')
    html.replace('&quot;', '"')
    html.replace('&apos;', "'")
    return html


def nab_Read_CCCinfoCfg():
    myhost = '127.0.0.1'
    myuser = mypass = ''
    myport = '16001'
    if fileExists('/etc/delcccaminfo'):
        f = open('/etc/delcccaminfo', 'r')
        for line in f.readlines():
            line = line.strip()
            if line.find('HOST ADDRESS:') != -1:
                myhost = line[13:]
            elif line.find('WEBINFO USERNAME:') != -1:
                myuser = line[17:]
            elif line.find('WEBINFO PASSWORD:') != -1:
                mypass = line[17:]
            elif line.find('WEBINFO LISTEN PORT:') != -1:
                myport = line[20:]

        f.close()
    myurl = 'http://' + myhost + ':' + myport
    if myuser and mypass:
        myurl = 'http://' + myuser + ':' + mypass + '@' + myhost + ':' + myport
    return [myhost,
     myuser,
     mypass,
     myport,
     myurl]


def nab_Write_CCCinfoCfg(mycfg):
    out = open('/etc/delcccaminfo', 'w')
    strview = 'HOST ADDRESS:' + mycfg[0] + '\n'
    out.write(strview)
    strview = 'WEBINFO USERNAME:' + mycfg[1] + '\n'
    out.write(strview)
    strview = 'WEBINFO PASSWORD:' + mycfg[2] + '\n'
    out.write(strview)
    strview = 'WEBINFO LISTEN PORT:' + mycfg[3] + '\n'
    out.write(strview)
    out.close()


def DeliteGetSkinPath():
    myskinpath = resolveFilename(SCOPE_CURRENT_SKIN, '')
    if myskinpath == '/usr/share/enigma2/':
        myskinpath = '/usr/share/enigma2/skin_default/'
    return myskinpath


def nab_Detect_Machine():
    machine = 'dm8000'
    if fileExists('/etc/bhmachine'):
        f = open('/etc/bhmachine', 'r')
        machine = f.readline().strip()
        f.close()
    return machine


def BhU_get_Version():
    ver = '1.0.0'
    if fileExists('/etc/bhversion'):
        f = open('/etc/bhversion', 'r')
        ver = f.readline().strip()
        ver = ver.replace('BlackHole ', '')
        f.close()
    return ver


def BhU_check_proc_version():
    ver = ''
    if fileExists('/proc/blackhole/version'):
        f = open('/proc/blackhole/version', 'r')
        ver = f.readline().strip()
        f.close()
    return ver


def BhU_checkSkinVersion(skinfile):
    version = '2.0.0'
    authors = ['Army', 'Matrix10', 'capa']
    ret = 'Sorry this skin is not compatible with the current Black Hole image version.'
    curversion = int(version.replace('.', ''))
    fullfile = '/usr/share/enigma2/' + skinfile
    checkver = False
    checkauth = False
    if fileExists(fullfile):
        f = open(fullfile)
        for line in f.readlines():
            if line.find('black hole version:') != -1:
                parts = line.strip().split(':')
                ver = int(parts[1].strip().replace('.', ''))
                if ver >= curversion:
                    checkver = True
            elif line.find('skin author:') != -1:
                parts = line.strip().split(':')
                auth = parts[1].strip()
                for a in authors:
                    if a == auth:
                        checkauth = True

        f.close()
    if checkver == True:
        if checkauth == True:
            ret = 'passed'
    return ret


def BhU_find_hdd():
    hdd = ''
    hdds = ['sda',
     'sdb',
     'sdc',
     'sdd',
     'sde',
     'sdf']
    for device in hdds:
        filename = '/sys/block/%s/removable' % device
        if fileExists(filename):
            if file(filename).read().strip() == '0':
                hdd = device
                break

    return hdd
