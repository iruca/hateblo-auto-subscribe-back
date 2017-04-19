#!/usr/bin/python
#-*- coding:utf-8 -*-

import requests

def get_rk( hatena_id, password ):
    """はてなIDとログインパスワードからrkを取得します。
    rkが何なのかはよく分からない。
    Args:
        hatena_id:  はてなID文字列
        password: はてなIDに対応するはてなログイン用のパスワード
    Returns:
        rk文字列
    Raises:
        KeyError: rk文字列が取得できなかったとき。ID/パスワードが間違っているか、rkを取得するためのはてなAPIの仕様が変わった
    """
    target_url = "https://www.hatena.ne.jp/login"
    payload = {'name': hatena_id, 'password': password}
    response = requests.post(target_url, data=payload )

    try:
        rk = response.headers["Set-Cookie"].split("rk=")[1].split(";")[0]
    except IndexError:
        raise KeyError("cannot get rk using hatena_id: %s and password: %s . ID/Password is wrong, or Hatena API spec changed." % (hatena_id, password))
    return rk


def get_rkm_rkc(rk, hatena_id, blog_hostname ):
    """はてなブログを購読する前段階で必要になるrkm, rkcの値を取得します。
    rkm, rkcが何なのかはよく分からない。
    Args:
        rk: get_rk関数で得られるトークン文字列
        hatena_id: 読者になりたいはてなブログの著者のはてなID
        blog_hostname: 読者になりたいはてなブログのホスト名
    Returns:
        (rkm文字列, rkc文字列) のタプル
    Raises:
        KeyError: rkm, rkcが取得できなかった。rkが間違っているか、はてなのwebUIのHTML上でrkm, rkcを書いている位置が変わったか。
    """

    headers = {"Cookie" : "rk="+ str(rk) }
    target_url = "http://blog.hatena.ne.jp/%s/%s/subscribe" % (hatena_id, blog_hostname)
    response = requests.get( target_url, headers=headers ).content

    # responseのhtmlに下記のような部品が含まれるので強引にrkmとrkcの値を切り取る
    #   <input type="hidden" name="rkm" value="XXXXX"/>
    #   <input type="hidden" name="rkc" value="XXXXX"/>
    try:
        rkm = response.split("name=\"rkm\" value=\"")[1].split("\"/>")[0]
        rkc = response.split("name=\"rkc\" value=\"")[1].split("\"/>")[0]
    except IndexError:
        raise KeyError("cannot get rkm and rkc using rk: %s . rk is wrong, or Hatena Web UI changed." % rk )
    return (rkm, rkc)

