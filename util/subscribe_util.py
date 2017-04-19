#!/usr/bin/python
#-*- coding:utf-8 -*-

import requests
from urlparse import urlparse
import time


"""
任意のはてなブログの読者になったり、購読を中止したりする
"""
def subscribe( rk, rkm, rkc, hatena_id, blog_hostname ):
    """ 任意のはてなブログの読者になる。
    Args:
        rk: get_rk関数で得られるトークン文字列
        rkm: get_rkm_rkc関数で得られるトークン文字列
        rkc: get_rkm_rkc関数で得られるトークン文字列
        hatena_id: 読者になりたいはてなブログの著者のはてなID
        blog_hostname: 読者になりたいはてなブログのホスト名
    Returns:
        なし
    """
    target_url = "http://blog.hatena.ne.jp/%s/%s/subscribe" % (hatena_id, blog_hostname)
    headers = {"Cookie" : "rk="+ str(rk) }
    payload = {"confirm" : "", "delete" : "", "rkm" : rkm, "rkc" : rkc, "iframe" : "1"}
    
    response = requests.post( target_url, headers=headers, data=payload)
 
    return 
   
def unsubscribe( rk, rkm, rkc, hatena_id, blog_hostname ):
    """ 任意のはてなブログの購読を中止する。
    Args:
        rk: get_rk関数で得られるトークン文字列
        rkm: get_rkm_rkc関数で得られるトークン文字列
        rkc: get_rkm_rkc関数で得られるトークン文字列
        hatena_id: 購読を中止したいはてなブログの著者のはてなID
        blog_hostname: 購読を中止したいはてなブログのホスト名
    Returns:
        なし
    """
    target_url = "http://blog.hatena.ne.jp/%s/%s/subscribe" % (hatena_id, blog_hostname)
    headers = {"Cookie" : "rk="+ str(rk) }
    payload = {"confirm" : "", "delete" : "1", "rkm" : rkm, "rkc" : rkc, "iframe" : "1"}

    response = requests.post( target_url, headers=headers, data=payload)

    return
    
