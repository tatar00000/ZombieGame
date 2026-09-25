[app]

title = Zombie Game
package.name = zombiegame
package.domain = org.zombiegame

source.dir = ./projectX
source.include_exts = py,png,jpg,jpeg,mp3,wav,ttf

version = 1.0

requirements = python3,pygame

orientation = landscape
fullscreen = 1

android.archs = arm64-v8a

android.permissions = VIBRATE

[buildozer]

log_level = 2
warn_on_root = 1
