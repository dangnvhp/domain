#!/usr/bin/python3.6

import os,time,subprocess,fileinput


with fileinput.FileInput('/etc/selinux/config', inplace=True,backup='.bak') as  f1:

    for line in f1:
       print(line.replace('SELINUX=enforcing','SELINUX=disabled'),end='')
    f1.close()


print('*'*40)

print('\nInfo Primary Domain Controller')
print('\n'+'*'*40)
ip_dc2 = input('Enter ip Backup DC : ')
print('\nExample Enter Netmask: 8 16 24')
netmask = input('Enter Netmask : ')

#host_n = input('\nEnter hostname Backup DC: ')

print('\nExample domain : domain.local\n')
domain = input('Enter domain :')

print('\n'+'*'*40)

############ tach chuoi

a = domain.split('.')[0]

print('\nInfo Primary Domain Controller')
print('\n'+'*'*40)
ip_dc1 = input('\nEnter ip Primary DC : ')

host_pdc = input('Enter hostname Primary DC: ')


print('*'*40)

host_n = subprocess.check_output('cat /etc/hostname',shell=True,universal_newlines=True)

host = host_n.rstrip('\n')

with open('/etc/hosts','a+') as f:

   f.write('\n' + ip_dc1 +' ' + host_pdc+'.' + domain + ' '+host_pdc)
   f.write('\n' + ip_dc2 + ' ' + host + '.' + domain + ' ' + host)
   f.close()
########### transfer file hosts

print('\nCopy file hosts to Primary DC\n')

time.sleep(3)

os.system('scp /etc/hosts root@'+host_pdc+'.'+domain+':/etc/')



gw = os.popen("ip route |grep default | awk '{print $3}'").read()

################################## config network interface


def eno():
    a = os.path.exists('/sys/class/net/eno1')

    return a
def eth():
    a = os.path.exists('/sys/class/net/eth0')
    return a

def em():
    a = os.path.exists('/sys/class/net/em1')
    return a
def ens():
    a = os.path.exists('/sys/class/net/ens33')
    return a

eno_ = eno()
#print(bool(eno_))

eth_ = eth()
#print(bool(eth_))

em_ = em()
#print(bool(em_))

ens_ = ens()
#print(bool(ens_))

if bool(eth_) == True:

    with fileinput.FileInput('/etc/sysconfig/network-scripts/ifcfg-eth0', inplace=True, backup='.bak') as  f:
        for line in f:
            print(line.replace('BOOTPROTO="dhcp"','BOOTPROTO=static'),end='')
            #print(line.replace('ONBOOT="no"', 'ONBOOT=yes'))
        f.close()
    with open('/etc/sysconfig/network-scripts/ifcfg-eth0', 'a+') as f1:
        f1.write('\nIPADDR=' + ip_dc2)
        f1.write('\nFREFIX=' + netmask)
        f1.write('\nGATEWAY=' + gw)
        f1.write('\nDNS1=127.0.0.1')
        f1.write('\nDNS2=8.8.8.8')
        f1.close()

elif bool(eno_) == True:

    with fileinput.FileInput('/etc/sysconfig/network-scripts/ifcfg-eno1', inplace=True, backup='.bak') as  f:
        for line in f:
            print(line.replace('BOOTPROTO="dhcp"','BOOTPROTO=static'),end='')
            #print(line.replace('ONBOOT="no"', 'ONBOOT=yes'))
        f.close()
    with open('/etc/sysconfig/network-scripts/ifcfg-eno1','a+') as f1:
        f1.write('\nIPADDR='+ip_dc2)
        f1.write('\nFREFIX='+netmask)
        f1.write('\nGATEWAY='+gw)
        f1.write('\nDNS1=127.0.0.1')
        f1.write('\nDNS2=8.8.8.8')
        f1.close()

elif bool(em_ )== True:

    with fileinput.FileInput('/etc/sysconfig/network-scripts/ifcfg-em1', inplace=True, backup='.bak') as  f:
        for line in f:
            print(line.replace('BOOTPROTO="dhcp"','BOOTPROTO=static'),end='')
            #print(line.replace('ONBOOT="no"', 'ONBOOT=yes'))
        f.close()
    with open('/etc/sysconfig/network-scripts/ifcfg-em1', 'a+') as f1:
        f1.write('\nIPADDR=' + ip_dc2)
        f1.write('\nFREFIX=' + netmask)
        f1.write('\nGATEWAY=' + gw)
        f1.write('\nDNS1=127.0.0.1')
        f1.write('\nDNS2=8.8.8.8')
        f1.close()

elif bool(ens_ )== True:

    with fileinput.FileInput('/etc/sysconfig/network-scripts/ifcfg-ens33', inplace=True, backup='.bak') as  f:
        for line in f:
            print(line.replace('BOOTPROTO="dhcp"','BOOTPROTO=static'),end='')
            #print(line.replace('ONBOOT="no"', 'ONBOOT=yes'))
        f.close()
    with open('/etc/sysconfig/network-scripts/ifcfg-ens33', 'a+') as f1:
        f1.write('\nIPADDR=' + ip_dc2)
        f1.write('\nFREFIX=' + netmask)
        f1.write('\nGATEWAY=' + gw)
        f1.write('\nDNS1=127.0.0.1')
        f1.write('\nDNS2=8.8.8.8')
        f1.close()

else:
    print("Dont't have interface")

    exit(0)

########### restart network

os.system('systemctl restart network')

print('\nPrepare install.......\n')

time.sleep(5)


os.system('yum  –y  install epel-release && yum –y update')

#### install packet basic

os.system('yum -y install perl gcc libacl-devel libblkid-devel gnutls-devel readline-devel python-devel gdb pkgconfig krb5-workstation zlib-devel setroubleshoot-server libaio-devel setroubleshoot-plugins policycoreutils-python libsemanage-python setools-libs-python setools-libs popt-devel libpcap-devel sqlite-devel libidn-devel libxml2-devel libacl-devel libsepol-devel libattr-devel keyutils-libs-devel cyrus-sasl-devel cups-devel bind-utils libxslt docbook-style-xsl openldap-devel pam-devel bzip2 wget')


print('\nInstall krb5')
time.sleep(3)

os.system('yum -y install authconfig krb5-workstation')


###### dowload samba4

os.system('wget https://download.samba.org/pub/samba/stable/samba-4.6.0.tar.gz')

#### extract

os.system('tar -zxvf samba-4.6.0.tar.gz')

### buil

print('\n Begin compiling')

time.sleep(3)

os.system('cd /root/samba-4.6.0 && ./configure --enable-debug --enable-selftest --with-ads --with-systemd --with-winbind')


############ make and install

os.system('cd samba-4.6.0 && make && make install ')


with open('/etc/resolv.conf','w') as f2:
    f2.write('# Generated by NetworkManager')
    f2.write('\nsearch '+ domain )
    f2.write('\nnameserver ' + ip_dc1)
    f2.close()


## remove file created when install samba

os.system('rm -rf /etc/krb5.conf')
os.system('rm -rf /etc/samba/smb.conf')

##domain = input('Enter domain name : ')

## copy file krb5.conf to etc

os.system('cd domain/ && cp krb5.conf /etc/')

with open('/etc/krb5.conf','a+') as f3:

    f3.write('\n    default_realm = '+domain.upper())
    f3.close()

##### get the kerberos key from PDC

os.system('kinit administrator@'+domain.upper())
os.system('klist')


###add the server to the existing domain
os.system('cp /usr/local/samba/bin/samba-tool /usr/sbin/')

os.system('samba-tool domain join '+domain+'  DC -U"'+a+'\\administrator" --dns-backend=SAMBA_INTERNAL')

### create samba service
os.system('cp domain/samba.service /etc/systemd/system/samba.service')

####################################################################

print('\n2: Switch Primary DC press Enter()')

time.sleep(30)

input('Enter to continue.....')

#################################################################


for line in fileinput.FileInput('/usr/local/samba/etc/smb.conf',inplace=1):
    if "workgroup = "+a.upper() in line:
        line=line.replace(line,line+"\tallow dns updates = nonsecure and secure\n")
    print (line,end='')


os.system('systemctl enable samba &&  systemctl start samba')

##################################################################

print('\nCopy file krb5.conf to Primary DC\n')

time.sleep(3)

os.system('scp /etc/krb5.conf root@'+host_pdc+'.'+domain+':/etc/ ')

###################################################################

print('\nInstall done!!!!!')

time.sleep(2)

print('\n4: Switch Primary DC press Enter')

time.sleep(30)

input('Enter to continue.....\n')

###################################################################

os.system('samba-tool drs showrepl')

###################################################################

print('showrepl done!!!!')

time.sleep(3)

print('\n6: Switch Primary DC press Enter')

time.sleep(30)

input('Enter to continue.....')

###################################################################

print('Install and config done!!!! reboot after 5s')
time.sleep(5)

os.system('reboot now')

