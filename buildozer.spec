[app]
title = Kiro
package.name = kiro
package.domain = org.kiro
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
icon.filename = icon.png
version = 1.0
requirements = python3==3.10.6,hostpython3==3.10.6,kivy==2.2.1,pillow,android,requests,urllib3,certifi,charset-normalizer,idna
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.arch = armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
