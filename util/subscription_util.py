#!/usr/bin/python
#-*- coding:utf-8 -*-

import requests
from urlparse import urlparse

def fetch_main_blog_hostname( hatena_id ):
    """はてなIDを入力すると、そのユーザのメインブログのホスト名を取得する。
    http://blog.hatena.ne.jp/${hatena_id}/ にアクセスすると、
    301 Moved Permanently というステータスコードとともに
    LocationヘッダにメインブログのURLを入れて返してくれる機能を利用している

    Args:
        hatena_id: ユーザのはてなID文字列

    Returns:
        ユーザのメインブログのホスト名文字列

    Raises:
        KeyError: hatena_idが無効、ブログをやっていないユーザだったなどの理由で>ブログURLが取得できなかった
    """
    forward_page_url = "http://blog.hatena.ne.jp/"+ str(hatena_id) +"/"
    response = requests.get( forward_page_url, allow_redirects=False)

    if response.status_code != 301:
        raise KeyError("cannot fetch any urls from "+ forward_page_url )

    # LocationヘッダにブログのURLが入っている
    url = response.headers["Location"]

    # はてなブログをやっていない人だった場合、ブログのURLではなくプロフィールのURLに飛ばされる
    if "profile.hatena.ne.jp" in url:
        raise KeyError("this user is not using the blog service. hatena_id="+ str(hatena_id) +", forwarded_page_url="+ str(forward_page_url) )

    # ホスト名を返却
    return urlparse( url ).hostname

