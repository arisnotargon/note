1.
触摸板在gdm桌面管理器中可能存在无法点击问题
解决：
https://unix.stackexchange.com/questions/266586/gdm-how-to-enable-touchpad-tap-to-click
switch to a VT (e.g. Ctrl+Alt+F3), login as root and run:
su - gdm -s /bin/sh
to switch user to gdm.

then run:

export $(dbus-launch)
and:

GSETTINGS_BACKEND=dconf gsettings set org.gnome.desktop.peripherals.touchpad tap-to-click true
run exit or hit Ctrl+D to return to root account.

restart the display manager:

systemctl restart gdm


2.
输入法
先安装fcitx，然后google pinyin和mozc

3.
resolvconf的问题
用apt把resolvconf重新安装一次
