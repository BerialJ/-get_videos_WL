import os


def make_path():
    local_path = os.path.abspath(__file__)
    folder_name = os.path.dirname(local_path)
    upper_path = os.path.dirname(folder_name)

    paths = {
        'download_path': upper_path + '\\v-dl',

        'blv_page_cookie': folder_name + '\\self_cookies\\blv\\cookies_get_page.txt',
        'blv_dl_cookie': folder_name + '\\self_cookies\\blv\\cookies.txt',

        'yt_page_cookie': folder_name + '\\self_cookies\\yt\\cookies_get_page.txt',
        'yt_dl_cookie': folder_name + '\\self_cookies\\yt\\cookies.txt',

        'yt_dlp_path': upper_path + '\\yt-dlp',
        'ffmpeg_path': upper_path + '\\ffmpeg\\bin\\ffmpeg.exe',
    }

    return paths


proxies = {
  
}
