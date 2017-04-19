#!/usr/bin/python
#-*- coding:utf-8 -*-


"""
はてなブログの読者登録返しを行うスクリプトです。

使い方: 
python main.py [hatena_id] [login_password]

はてなIDとログイン用パスワードを実行時引数に使用して、
自分のはてなブログ(メインブログ)を購読してくれているユーザのメインブログを購読します。

現状、「読者登録してくれなくなった人の購読をこちらからも外す」機能はつけていません。
"""
import os
import sys
# 実行スクリプトの絶対パスを使って強引にパスを通す
# どのディレクトリからでもこのファイルを実行できるようにするため
sys.path.append( os.path.abspath(os.path.dirname(__file__)) +'/util')
import auth_util
import get_subscribing_util
import get_subscriber_util
import subscription_util
import subscribe_util
import time
sleep_interval= 5.0 # はてなのサーバに迷惑をかけないために適宜加えるスリープ(秒)

args = sys.argv
if len( args ) != 3:
    print "usage: python main.py [hatena_id] [login_password]"
    sys.exit(-1)

# はてなID
hatena_id = args[1]
# ログイン用パスワード
login_password = args[2]

# 認証情報を取得
rk = auth_util.get_rk( hatena_id, login_password )

time.sleep(sleep_interval)

# 自分が購読しているユーザを取得
subscribings = get_subscribing_util.get_subscribings( rk )

# はてなIDだけ抜き出す
subscribing_hatena_ids = [ subscribing[0] for subscribing in subscribings ]

time.sleep(sleep_interval)

# 自分のメインブログのホスト名を取得
my_blog_hostname = subscription_util.fetch_main_blog_hostname( hatena_id )
# 自分のメインブログを購読してくれているユーザを取得
subscribers = get_subscriber_util.get_subscribers( hatena_id, my_blog_hostname, rk )

time.sleep(sleep_interval)

for subscriber in subscribers:
    # 購読してくれてるのに自分が購読してない人たちの
    if subscriber not in subscribing_hatena_ids:
        # メインブログのホスト名を調べて購読!
        blog_hostname = subscription_util.fetch_main_blog_hostname( subscriber )
        print "subscribing %s 's blog... (hostname=%s)" % ( subscriber, blog_hostname )
        (rkm, rkc) = auth_util.get_rkm_rkc(rk, hatena_id, blog_hostname )
        subscribe_util.subscribe( rk, rkm, rkc, subscriber, blog_hostname )
        time.sleep(sleep_interval)
