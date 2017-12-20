from Screens.Screen import Screen
from Components.Label import Label
from Components.ServiceEventTracker import ServiceEventTracker
from os import system, rename as os_rename
from enigma import eTimer, iServiceInformation, iPlayableService, eDVBFrontendParametersSatellite
import re
import socket
from Tools.Directories import fileExists
from Tools.Transponder import ConvertToHumanReadable

class Nab_ExtraInfobar(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self['cam_info'] = Label()
        self['ecm_info'] = Label()
        self['netcard_info'] = Label()
        self['beta_no'] = Label()
        self['beta_emm'] = Label()
        self['beta_ecm'] = Label()
        self['irdeto_no'] = Label()
        self['irdeto_emm'] = Label()
        self['irdeto_ecm'] = Label()
        self['seca_no'] = Label()
        self['seca_emm'] = Label()
        self['seca_ecm'] = Label()
        self['td_no'] = Label()
        self['td_emm'] = Label()
        self['td_ecm'] = Label()
        self['via_no'] = Label()
        self['via_emm'] = Label()
        self['via_ecm'] = Label()
        self['nagra_no'] = Label()
        self['nagra_emm'] = Label()
        self['nagra_ecm'] = Label()
        self['cw_no'] = Label()
        self['cw_emm'] = Label()
        self['cw_ecm'] = Label()
        self['nds_no'] = Label()
        self['nds_emm'] = Label()
        self['nds_ecm'] = Label()
        self['conax_no'] = Label()
        self['conax_emm'] = Label()
        self['conax_ecm'] = Label()
        self['biss_no'] = Label()
        self['biss_emm'] = Label()
        self['biss_ecm'] = Label()
        self['bul_no'] = Label()
        self['bul_emm'] = Label()
        self['bul_ecm'] = Label()
        self['dre_no'] = Label()
        self['dre_emm'] = Label()
        self['dre_ecm'] = Label()
        self['pv_no'] = Label()
        self['pv_emm'] = Label()
        self['pv_ecm'] = Label()
        self['button_fta'] = Label()
        self['button_card'] = Label()
        self['button_emu'] = Label()
        self['button_cex'] = Label()
        self['button_spider'] = Label()
        self['nfreq_info'] = Label()
        self['orbital_pos'] = Label()
        self['Universe'] = Label()
        self.my_timer = eTimer()
        self.my_timer.timeout.get().append(self.__updateEmuInfo)
        self.my_timer_active = 0
        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evStart: self.__start,
         iPlayableService.evUpdatedInfo: self.__start})
        self.onShow.append(self.__start)
        self.onHide.append(self.__onHide)

    def __onHide(self):
        if self.my_timer_active == 1:
            self.my_timer.stop()
            self.my_timer_active = 0

    def __start(self):
        if self.my_timer_active == 1:
            self.my_timer.stop()
            self.my_timer_active = 0
        self['ecm_info'].setText('')
        self['netcard_info'].setText('')
        self['nfreq_info'].setText('')
        self['orbital_pos'].setText('')
        self['beta_emm'].hide()
        self['beta_ecm'].hide()
        self['irdeto_emm'].hide()
        self['irdeto_ecm'].hide()
        self['seca_emm'].hide()
        self['seca_ecm'].hide()
        self['td_emm'].hide()
        self['td_ecm'].hide()
        self['via_emm'].hide()
        self['via_ecm'].hide()
        self['nagra_emm'].hide()
        self['nagra_ecm'].hide()
        self['cw_emm'].hide()
        self['cw_ecm'].hide()
        self['nds_emm'].hide()
        self['nds_ecm'].hide()
        self['conax_emm'].hide()
        self['conax_ecm'].hide()
        self['biss_emm'].hide()
        self['biss_ecm'].hide()
        self['bul_emm'].hide()
        self['bul_ecm'].hide()
        self['dre_emm'].hide()
        self['dre_ecm'].hide()
        self['pv_emm'].hide()
        self['pv_ecm'].hide()
        self['button_fta'].show()
        self['button_card'].hide()
        self['button_emu'].hide()
        self['button_cex'].hide()
        self['button_spider'].hide()
        self.currentCam = 'Common Interface'
        if fileExists('/etc/CurrentBhCamName'):
            f = open('/etc/CurrentBhCamName', 'r')
            for line in f.readlines():
                line = line.replace('\n', '')
                line = line.strip()
                if len(line) > 3:
                    self.currentCam = line

            f.close()
        self['cam_info'].setText(self.currentCam)
        ret = 'Black Hole'
        all = ['Avalon', 'Chaos', 'Ghost']
        f = open('/proc/mounts', 'r')
        for line in f.readlines():
            if line.find('/usr ') != -1:
                for a in all:
                    if line.find(a) != -1:
                        ret = a

                break

        f.close()
        self['Universe'].setText(_('In %s Universe') % ret)
        self.VideoSize = ' '
        isCrypt = False
        service = self.session.nav.getCurrentService()
        myinfo = service and service.info()
        if myinfo is not None:
            isCrypt = myinfo.getInfo(iServiceInformation.sIsCrypted) == 1
            feinfo = service.frontendInfo()
            frontendData = feinfo and feinfo.getAll(True)
            if frontendData is not None:
                ttype = frontendData.get('tuner_type', 'UNKNOWN')
                if ttype == 'DVB-S':
                    fedata = ConvertToHumanReadable(frontendData)
                    sr = str(int(frontendData.get('symbol_rate', 0) / 1000))
                    freq = str(int(frontendData.get('frequency', 0) / 1000))
                    pol = {0: 'H',
                     1: 'V',
                     2: 'CL',
                     3: 'CR',
                     4: None}[frontendData.get('polarization', 'HORIZONTAL')]
                    fec = fedata.get('fec_inner', ' ')
                    self['nfreq_info'].setText('Freq: ' + freq + ' ' + pol + ' Sr: ' + sr + ' ' + fec)
                    orbital = fedata['orbital_position']
                    self['orbital_pos'].setText(orbital)
                elif ttype == 'DVB-T':
                    fedata = ConvertToHumanReadable(frontendData)
                    freq = str(int(frontendData.get('frequency', 0) / 1000))
                    band = fedata.get('bandwidth', ' ')
                    orbital = fedata.get('tuner_type')
                    self['orbital_pos'].setText(orbital)
                    self['nfreq_info'].setText('Freq: ' + freq + ', Band: ' + band)
                elif ttype == 'DVB-C':
                    fedata = ConvertToHumanReadable(frontendData)
                    sr = str(int(frontendData.get('symbol_rate', 0) / 1000))
                    freq = str(int(frontendData.get('frequency', 0) / 1))
                    qam = fedata.get('modulation')
                    orbital = fedata.get('tuner_type')
                    self['orbital_pos'].setText(orbital)
                    self['nfreq_info'].setText('Freq: ' + freq + ', ' + qam + ', Sr: ' + sr)
        if isCrypt == True:
            self['button_fta'].hide()
            Caids = myinfo.getInfoObject(iServiceInformation.sCAIDs)
            for caid in Caids:
                caidname = self.parse_caid_txt(caid)
                self.show_emm(caidname)
                self.my_timer_count = 0
                self.__updateEmuInfo()

    def parse_caid_txt(self, caid):
        ret = ''
        caidnames = ['0100,01FF,Seca',
         '0500,05FF,Viaccess',
         '0600,06FF,Irdeto',
         '0900,09FF,Videoguard',
         '0B00,0BFF,Conax',
         '0D00,0DFF,Cryptoworks',
         '1000,10FF,Tandberg',
         '1700,17FF,Betacrypt',
         '1800,18FF,Nagravision',
         '2600,26FF,Biss',
         '4AEE,4AEE,Bulcrypt',
         '5500,55FF,Bulcrypt',
         '4A00,4AFF,Dreamcrypt',
         '0E00,0EFF,PowerVu']
        for line in caidnames:
            x = line.split(',', 2)
            if caid == caid & int(x[1], 16):
                ret = x[2]
                break

        return ret

    def show_emm(self, caidname):
        if caidname == 'Betacrypt':
            self['beta_emm'].show()
        elif caidname == 'Irdeto':
            self['irdeto_emm'].show()
        elif caidname == 'Nagravision':
            self['nagra_emm'].show()
        elif caidname == 'Seca':
            self['seca_emm'].show()
        elif caidname == 'Tandberg':
            self['td_emm'].show()
        elif caidname == 'Viaccess':
            self['via_emm'].show()
        elif caidname == 'Biss':
            self['biss_emm'].show()
        elif caidname == 'Bulcrypt':
            self['bul_emm'].show()
        elif caidname == 'Conax':
            self['conax_emm'].show()
        elif caidname == 'Cryptoworks':
            self['cw_emm'].show()
        elif caidname == 'Dre-crypt':
            self['dre_emm'].show()
        elif caidname == 'Videoguard':
            self['nds_emm'].show()
        elif caidname == 'PowerVu':
            self['pv_emm'].show()

    def __updateEmuInfo(self):
        self.my_timer.start(750)
        self.my_timer_active = 1
        self.my_timer_count += 1
        if self.my_timer_count > 50:
            self.my_timer.start(10000)
        nmsg = ''
        netinfo = ''
        provid = 'MEO'
        in_gbox = 0
        mycaid = '0000'
        mycaid_check = False
        try:
            f = open('/tmp/ecm.info', 'r')
            lines = f.readlines()
            f.close()
        except:
            lines = ''

        if lines:
            for line in lines:
                line = line.strip()
                pos = line.find('CaID')
                if pos > 1:
                    x = line[pos + 5:pos + 11]
                    x = x.replace('0x0', '0x')
                    mycaid = x
                    nmsg = 'Caid: ' + mycaid
                    mycaid_check = True
                pos = line.find(':')
                if pos > 1:
                    x = line.split(':', 1)
                    x1 = x[1].strip()
                    if x[0] == 'caid':
                        mycaid = x1
                        nmsg = 'Caid: ' + x1
                        mycaid_check = True
                    elif x[0] == 'prov':
                        provid = x1
                        nmsg += '    Provider: ' + x1
                    elif x[0] == 'provider':
                        nmsg += '    Provider: ' + x1
                    elif x[0] == 'using' or x[0] == 'protocol':
                        if x1 == 'emu':
                            self['button_emu'].show()
                        elif x1 == 'sci' or x1 == 'smartreader+':
                            self['button_card'].show()
                        elif x1 == 'fta':
                            self['button_fta'].show()
                        else:
                            self['button_spider'].show()
                    elif x[0] == 'decode':
                        if x1.find('Internal') != -1:
                            self['button_emu'].show()
                        elif x1.find('slot') != -1:
                            self['button_card'].show()
                        elif x1.find('Network') != -1:
                            in_gbox = 1
                            self['button_spider'].show()
                        else:
                            self['button_fta'].show()
                        nmsg += ' decode: ' + x1
                    elif x[0] == 'address':
                        netinfo += 'Address:' + x1
                    elif x[0] == 'from':
                        netinfo += 'Address:' + x1
                    elif x[0] == 'source':
                        netinfo += 'Address:' + x1
                        pos = x1.find('.')
                        if pos > 1:
                            self['button_spider'].show()
                        elif x1 == 'cache1' or x1 == 'cache2' or x1 == 'cache3':
                            self['button_cex'].show()
                        else:
                            self['button_card'].show()
                    elif x[0] == 'protocol':
                        if x1 == 'constcw' or x1 == 'emu':
                            self['button_spider'].hide()
                            self['button_card'].hide()
                            self['button_emu'].show()
                    elif x[0] == 'hops':
                        netinfo += '   Hops:' + x1
                    elif x[0] == 'ecm time':
                        netinfo += '   Ecm time:' + x1

            if in_gbox == 1:
                if fileExists('/tmp/share.info'):
                    f = open('/tmp/share.info', 'r')
                    for line in f.readlines():
                        if line.find(provid) != -1:
                            pos = line.find('at ') + 3
                            end = line.find('id:')
                            netinfo = line[pos:end]
                            break

                    f.close()
            self['ecm_info'].setText(nmsg)
            self['netcard_info'].setText(netinfo)
            if mycaid_check == True:
                mycaidi = int(re.sub('0x', '', mycaid), 16)
                caidname = self.parse_caid_txt(mycaidi)
                if caidname == 'Betacrypt':
                    self['beta_ecm'].show()
                elif caidname == 'Irdeto':
                    self['irdeto_ecm'].show()
                elif caidname == 'Nagravision':
                    self['nagra_ecm'].show()
                elif caidname == 'Seca':
                    self['seca_ecm'].show()
                elif caidname == 'Tandberg':
                    self['td_ecm'].show()
                elif caidname == 'Viaccess':
                    self['via_ecm'].show()
                elif caidname == 'Biss':
                    self['biss_ecm'].show()
                elif caidname == 'Bulcrypt':
                    self['bul_ecm'].show()
                elif caidname == 'Conax':
                    self['conax_ecm'].show()
                elif caidname == 'Cryptoworks':
                    self['cw_ecm'].show()
                elif caidname == 'Dre-crypt':
                    self['dre_ecm'].show()
                elif caidname == 'Videoguard':
                    self['nds_ecm'].show()
                elif caidname == 'PowerVu':
                    self['pv_ecm'].show()


def nab_Switch_Autocam(current, new):
    camname = 'N/A'
    inme = open('/etc/BhCamConf', 'r')
    out = open('/etc/BhCamConf.tmp', 'w')
    for line in inme.readlines():
        if line.find('delcurrent') == 0:
            line = 'delcurrent|' + new + '\n'
        out.write(line)

    out.close()
    inme.close()
    os_rename('/etc/BhCamConf.tmp', '/etc/BhCamConf')
    f = open(new, 'r')
    for line in f.readlines():
        if line.find('CAMNAME=') != -1:
            line = line.strip()
            camname = line[9:-1]

    f.close()
    out = open('/etc/CurrentBhCamName', 'w')
    out.write(camname)
    out.close()
    cmd = 'cp -f ' + new + ' /usr/bin/StartBhCam'
    system(cmd)
    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client_socket.connect('/tmp/Blackhole.socket')
    mydata = 'STOP_CAMD,' + current
    client_socket.send(mydata)
    client_socket.close()
    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client_socket.connect('/tmp/Blackhole.socket')
    mydata = 'NEW_CAMD,' + new
    client_socket.send(mydata)
    client_socket.close()
    return camname
