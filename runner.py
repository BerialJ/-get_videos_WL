import os
from sys import argv
import requests
import file_paths


def get_blv_cookie(file):
    cookie = {}
    file = open(file, 'r', encoding='utf-8')
    text = file.readlines()
    file.close()

    for line in text:
        if line[:6] == 'Cookie':
            cookies = line[7:].split(';')
            for cook in cookies:
                pair = cook.replace(' ', '').replace('\n', '').split('=')
                cookie[pair[0]] = pair[1]
    return cookie


def get_blv_page():
    url = 'https://www.bilibili.com/list/watchlater/'
    cookie = get_blv_cookie(paths.get('blv_page_cookie'))

    request = requests.get(url, cookies=cookie)
    response = request.content.decode('utf-8')

    print('# Page Got!')
    return response


def make_blv_command(page):
    avs = []
    parts = []
    for line in page.split('\n'):
        if '点击打开迷你播放器' in line:
            parts = line.split('"link":"bilibili:')
            parts.pop(0)
            break
    for part in parts:
        part = part.split('"')[0].replace('\\u002F', '\\').split('\\')[-1].split('?')[0]
        if part not in avs:
            avs.append(part)

    yt_dlp_path = paths.get('yt_dlp_path')
    download_path = paths.get('download_path')
    cookie_path = paths.get('blv_dl_cookie')
    ffmpeg_path = paths.get('ffmpeg_path')

    commands_made = []
    for line in avs:
        command_made = yt_dlp_path + ' --cookies "' + cookie_path + '" ' \
                       '--output "' + download_path + '\\%(uploader)s--%(title)s-%(resolution)s.%(ext)s" ' \
                       '--merge-output-format mkv ' \
                       '--ffmpeg-location ' + ffmpeg_path + ' ' \
                       'https://www.bilibili.com/video/av' + line + '\n'
        commands_made.append(command_made)

    print('# Commands Made!')
    return commands_made


def get_yt_cookie(file):
    file = open(file, 'r', encoding='utf-8')
    file_read = file.readlines()
    file.close()

    cookie = {}
    for line in file_read:
        name = line.split(': ')[0][1:-1]
        info = line.split(': ')[1][1:-1]
        cookie[name] = info
    return cookie


def get_yt_page():
    proxies = file_paths.proxies
    url = 'https://www.youtube.com/playlist?list=WL'
    cookie = get_blv_cookie(paths.get('yt_page_cookie'))

    request = requests.get(url, cookies=cookie, proxies=proxies)
    response = request.content.decode('utf-8')

    print('# Page Got!')
    return response


def make_yt_command(page):
    avs = []
    parts = []
    for line in page.split('\n'):
        if '<title>稍后观看' in line:
            parts = line.split('"url":"/watch?')
            parts.pop(0)
            break
    for part in parts:
        part = part.split('"')[0]
        if part not in avs:
            avs.append(part)

    yt_dlp_path = paths.get('yt_dlp_path')
    download_path = paths.get('download_path')
    cookie_path = paths.get('blv_dl_cookie')
    ffmpeg_path = paths.get('ffmpeg_path')

    commands_made = []
    for line in avs:
        command_made = yt_dlp_path + ' --cookies "' + cookie_path + '" ' \
                  '--output "' + download_path + '\\%(uploader)s--%(title)s-%(resolution)s.%(ext)s" ' \
                  '--merge-output-format mkv ' \
                  '-r 500k '\
                  '--ffmpeg-location ' + ffmpeg_path + ' ' \
                  'https://www.youtube.com/watch?' + line + '\n'
        commands_made.append(command_made)

    print('# Commands Made!')
    return commands_made


def get_commands(choice):
    if 'bili' in choice:
        page = get_blv_page()
        commands_make = make_blv_command(page)
        return commands_make

    if 't' in choice:
        page = get_yt_page()
        commands_make = make_yt_command(page)
        return commands_make

    else:
        print_help()
        return ''


def run(command_lines):
    for line in command_lines:
        os.system(line)


def print_help():
    print('# Usage: Put your cookies in the right place \n'
          '# runner.py bilibili/youtube \n'
          '# Download will be automatic started')


if __name__ == '__main__':
    #argv.append('youtube.com')
    # argv.append('blibli.com')
    if len(argv) == 1:
        print_help()
    else:
        paths = file_paths.make_path()
        url_type = argv[1]
        commands = get_commands(url_type)
        run(commands)
