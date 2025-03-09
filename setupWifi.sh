
# sudo raspi-config -> WiFi country
iw reg set AT
apt install -y dnsmasq hostapd iptables
printf "interface wlan0\nstatic ip_address=192.168.1.1/24\nnohook wpa_supplicant\n" >> /etc/dhcpcd.conf
systemctl restart dhcpcd
ip l | grep wlan0 >> setupWifi.log
mv /etc/dnsmasq.conf /etc/dnsmasq.conf_alt


printf "interface=wlan0\nno-dhcp-interface=eth0\ndhcp-range=192.168.1.100,192.168.1.200,255.255.255.0,24h\n# DNS  \ndhcp-option=option:dns-server,192.168.1.1\n" >> /etc/dnsmasq.conf
dnsmasq --test -C /etc/dnsmasq.conf >> setupWifi.log

systemctl restart dnsmasq
systemctl status dnsmasq >> setupWifi.log
systemctl enable dnsmasq

printf "# WLAN-Router-Betrieb\n# Schnittstelle und Treiber\ninterface=wlan0\n#driver=nl80211\n# WLAN-Konfiguration\nssid=sockBase0\nchannel=1\nhw_mode=g\nieee80211n=1\nieee80211d=1\ncountry_code=DE\nwmm_enabled=1\n# WLAN-Verschlüsselung\nauth_algs=1\nwpa=2\nwpa_key_mgmt=WPA-PSK\nrsn_pairwise=CCMP\nwpa_passphrase=sockBase\n" >> /etc/hostapd/hostapd.conf
chmod 600 /etc/hostapd/hostapd.conf

# testwise:
# hostapd -dd /etc/hostapd/hostapd.conf

printf "RUN_DAEMON=yes\n" >> /etc/default/hostapd
printf 'DAEMON_CONF="/etc/hostapd/hostapd.conf"\n' >> /etc/default/hostapd

# enable host APD
systemctl unmask hostapd
systemctl start hostapd
systemctl enable hostapd
systemctl status hostapd  >> setupWifi.log


# nano /etc/sysctl.conf
# iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
# sh -c "iptables-save > /etc/iptables.ipv4.nat"
# nano /etc/rc.local
# # reboot
# mv /etc/dnsmasq.conf /etc/dnsmasq.conf_alt
# nano /etc/dnsmasq.conf
# dnsmasq --test -C /etc/dnsmasq.conf
# systemctl restart dnsmasq
# systemctl status dnsmasq
# systemctl enable dnsmasq
# nano /etc/hostapd/hostapd.conf
# chmod 600 /etc/hostapd/hostapd.conf
# nano /etc/hostapd/hostapd.conf
# hostapd -dd /etc/hostapd/hostapd.conf
# # screen
# sudo nano /etc/default/hostapd

