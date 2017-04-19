#!/usr/bin/python
#-*- coding:utf-8 -*-

import requests
from urlparse import urlparse
import time


"""
自分が購読しているはてなブログの著者とブログURLを取得する
"""

def get_subscribings( rk, interval=1.0 ):
    """ 自分が購読しているブログの情報を取得する。
        http://blog.hatena.ne.jp/-/antenna のページに現れる購読中のブログ情報を利用する。
    Args:
        rk: get_rk関数で得られるトークン文字列
        interval: 購読中のブログを表示する各ページを見てまわる間のスリープ間隔(秒).
                はてなのサーバに負荷をかけないようにするため。
    Returns:
        自分が購読しているブログの情報を以下の形で返却する。
        [(著者のはてなID, ブログのホスト名, 直近のエントリのURL)というタプルの配列]
    """
    subscribings = []

    page=1
    continue_flag = True

    # 次のページが存在する限り取得し続ける
    while( continue_flag ):
        target_url = "http://blog.hatena.ne.jp/-/antenna?page="+ str(page) 

        headers = {"Cookie" : "rk="+ str(rk) }
        response = requests.get( target_url, headers=headers).content

        # 返却されたHTMLから、著者のhatena idと直近のエントリのURLが含まれる部分を無理やり抜きだす.

        # http://blog.hatena.ne.jp/-/antenna ページに現れる購読中のブログごとの情報を含むHTMLを分けて考えるのにちょうどいいHTMLを使う
        author_url_contained_texts = response.split( "\" target=\"_blank\" data-track-name=\"admin-antenna-entry admin-antenna-entry-title\" data-track-once>" )

        # 購読しているユーザ数だけループを回す
        for k in range(0, len( author_url_contained_texts )-1 ):
            # delimiter_htmlの直前には直近のエントリのURLが '<a href="' の後に書いてあるのでそこから直近エントリのURLを取り出す。
            # また、そのちょっと前に
            # https://cdn1.www.st-hatena.com/users/hi/hiro-loglog/profile.gif
            # という著者のはてなIDを含む画像URLがあるのでここから強引にはてなIDを取り出す
            recent_entry_url = author_url_contained_texts[k].split('<a href="')[-1]
            author_hatena_id = author_url_contained_texts[k].split('/profile.gif')[-2].split("/")[-1]
            
            # recent_entry_url は http://www.mako0625.net/entry/2017/04/17/214151 のような文字列なので、そこからホスト名を取り出す
            blog_hostname = urlparse(recent_entry_url).hostname

            subscribings.append( (author_hatena_id, blog_hostname, recent_entry_url) )
    
        # まだ次のページがあるようなら続ける
        if "class=\"btn\">次のページ</a>" in response:
            page += 1
            # はてなサーバにDoSをかけないようにスリープを入れる
            time.sleep( interval )
            continue
        else:
            # whileループから抜け出す
            continue_flag = False

    return subscribings



