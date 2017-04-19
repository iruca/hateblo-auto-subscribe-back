#!/usr/bin/python
#-*- coding:utf-8 -*-

import requests

"""
自分のはてなブログの読者一覧を取得する
"""

def get_subscribers( hatena_id, blog_url, rk ):
    """ 自分のはてなブログの読者一覧を取得します。
    Args:
        hatena_id: 自分のはてなID
        blog_url: 自分のブログのURL
        rk: get_rk関数で得られるトークン文字列
    Returns:
        読者のはてなID文字列のリスト
    """
    subscribers = []

    target_url = "http://blog.hatena.ne.jp/%s/%s/subscribers" % (hatena_id, blog_url )
    
    headers = {"Cookie" : "rk="+ str(rk) }
    response = requests.get( target_url, headers=headers)
    
    # 返却されたHTMLから、読者のhatena idが含まれる部分を無理やりsplitで抜き出す
    hatenaid_contained_text_list = response.content.split('data-user-name="')
    del hatenaid_contained_text_list[0] # 最初は "<HTML ..." みたいな文字列が入っちゃうので取り除く

    for hatenaid_contained_text in hatenaid_contained_text_list:
        hatena_id = hatenaid_contained_text.split('"')[0]
        subscribers.append( hatena_id )

    return subscribers


