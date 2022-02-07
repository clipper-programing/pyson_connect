# pyson_connectの使い方
## プログラムを実行する前に
EpsonConnectのデベロッパーズサイトにてライセンス申請を行うと発行されるクライアントキーとクライアントシークレットキーを用意してください。
[EpsonConnectデベロッパーズサイトはこちら](https://www.epsondevelopers.com/api/epson-connect-j/)

## モジュールのインポート
以下のようにimportしてください。
```
import pyson_connect
```

## インスタンス化
```
ps = pyson_connect.PysonConnect(クライアントID, クライアントシークレット)
```
なお、以下の変数名で環境変数に登録するとソースコードにクライアントIDとクライアントシークレットをソースコード上に記載しなくても利用することができます。
```
export epsonClientID=クライアントID
export epsonClientSecret=クライアントシークレット
```
環境変数登録後は以下のようにしてインスタンス化します。
```
ps = pyson_connect.PysonConnect()
```

## EpsonConnect認証関数
認証を行う関数です。引数にEpsonConnectのメールアドレスを指定します。
```
ps.authentification(EpsonConnectのメールアドレス)
```
戻り値は以下のようになります。
```
{
    "access_token":"アクセストークン",
    "expires_in":"アクセストークン有効時間(sec)",
    "refresh_token":"リフレッシュトークン",
    "subject_id":"プリンタのID"
}
```

## アクセストークン再発行関数 
アクセストークンを再発行する関数です。引数にアクセストークンを指定します。
```
ps.reissue_access_token(リフレッシュトークン)
```
戻り値は以下のようになります。
```
{
    "access_token":"アクセストークン",
    "expires_in":"アクセストークン有効時間(sec)",
    "subject_id":"プリンタのID"
}
```

## 印刷能力取得関数 
直前に認証を行ったプリンタの印刷能力を取得する関数です。引数には印刷モードを指定します。
```
ps.get_device_print_capabilities(print_mode)
```
以下のようにすると、すでに認証を通したデバイスの情報を得ることができるようになります。
```
ps.get_device_print_capabilities(print_mode, access_token=アクセストークン, subject_id=プリンタのID)
```
戻り値は以下のようになります。
```
{
    "color_modes": [
        "color",
        "mono"
    ],
    "media_sizes": [
        {
            "media_size": "印刷可能な用紙サイズ",
            "media_types": [
                {
                    "media_type": "印刷可能な用紙の種類",
                    "borderless": "フチなし印刷サポート可否",
                    "sources": [
                        "指定可能な給紙装置"
                    ],
                    "print_qualities": [
                        "指定可能な印刷品質"
                    ],
                    "2_sided": "両面印刷サポート可否"
                }
            ]
        },
        ...
    ]
}
```

## 印刷設定関数
直前に認証を行ったプリンタに対して印刷設定を行うことができる関数です。
```
ps.print_setting(設定データ)
```
以下のようにすると、すでに認証を通したデバイスに対して印刷設定を行えるようになります。
```
ps.print_setting(印刷データ, access_token=アクセストークン, subject_id=プリンタのID)
```
印刷データの例
```
    data = {
                "job_name":"ジョブを識別するための名前(最大256文字)",
                "print_mode":"印刷モード(document/photo)",
                "print_setting":{
                    "media_size":"用紙サイズ(ex: ms_a4)",
                    "media_type":"印刷する用紙の種別(ex: mt_plainpaper)",
                    "borderless":"印刷時のフチ有無(bool),
                    "print_quality":"印刷品質(normal/high/draft)",
                    "source":"給紙装置(ex: front1)",
                    "color_mode":"カラー設定(mono/color)",
                    "2_sided":"両面印刷(none/long/short)",
                    "reverse_order":逆順印刷の可否(bool),
                    "copies":印刷部数(1~99),
                    "collate":部単位印刷の可否(bool)
                    }
                }
```
*なお、詳しい印刷データの内容はEpson Connect API仕様書の5.2.4. 印刷設定のページをご覧ください*

戻り値は以下のようになります。
```
{
    "job_id":"印刷ジョブID",
    "upload_uri":"ファイルアップロード用URI"
}
```

## ファイルアップロード関数
直前に認証を行い、印刷設定をおこなったプリンタに紐付けられたアップロードURIに対してファイルをアップロードする関数です。
ファイルパスに印刷したい画像やドキュメントファイルのURLを指定するとインターネット上に存在する画像を印刷することができます。
```
ps.upload_print_file(ファイルパス, 印刷モード)
```
以下のようにすると、すでにに印刷設定を行ったプリンタに対してファイルを送信することができるようになる。
```
ps.upload_print_file(file_path, document_type, job_id=印刷ジョブID, upload_uri=ファイルアップロード用URI)
```

## 印刷実行関数
直前に認証、印刷設定及びファイルアップロードを行ったプリンタに対して印刷指示を送れる関数です。
```
ps.excute_print()
```
以下のようにすると、すでに印刷設定、ファイルアップロードを行ったプリンタに対してプリント指示を遅れるようになります。
```
ps.excute_print(access_token=アクセストークン, subject_id=プリンタのID, jobID=印刷ジョブID)
```

## 印刷キャンセル関数
引数に指定したアクセストークン、サブジェクトID、印刷ジョブIDに対して印刷のキャンセル指示を送ることができます。
```
ps.cancel_print(アクセストークン, プリンタのID, 印刷ジョブID)
```

## プリントジョブ取得関数
直前に認証、印刷指示を送ったプリンタに対してプリンタの実行情報を取得することのできる関数です。
```
ps.get_print_job_info()
```
以下のようにすることですでに認証や印刷実行を行ったプリンタの実行情報を取得できるようになります。
```
ps.get_print_job_info(access_token=アクセストークン, subject_id=プリンタのID, jobID=印刷ジョブID)
```
戻り値は以下のようになります。
```
{
    "status":"印刷ステータス",
    "status_reason":"ステータスの内容",
    "start_date":”印刷実行日時",
    "job_name":"印刷ジョブ名",
    "ttl_pages":"印刷ページ数",
    "update_date":"印刷ジョブ状態の更新日時"
}
```

## デバイス情報取得関数
直前に認証を行ったプリンタの情報を取得することができる関数です。
```
ps.get_device_info()
```
以下のようにするとすでに認証などを行っているプリンタの情報を取得することができるようになります。
```
ps.get_device_info(access_token=アクセストークン, subject_id=プリンタのID)
```
戻り値は以下のようになります。
```
{
    "printer_name":"デバイスの製品名",
    "serial_no":"デバイスのシリアルナンバー",
    "ec_connected":"デバイスのEpsonConnect接続状況"
}
```

## 認証取り消し関数
アクセストークンとプリンタのIDを指定することにより、該当の認証情報を取り消すことができます。
```
ps.cancel_authentication(アクセストークン, プリンタのID)
```
    
## 印刷通知設定関数
直前に認証などを行ったプリンタの印刷結果をdataのなかで指定したURLに対して通知を行うかを設定できる関数です。
```
ps.notification_setting(data)
```
以下のようにすることですでに認証などを行っているプリンタの印刷結果などの通知を設定することができるようになります。
```
ps.notification_setting(data, access_token=アクセストークン, subject_id=プリンタのID)
```
通知設定データの例
```
    data = {
            "notification":通知の有無(bool),
            "callback_uri":"通知を受信するURI":
            }
```


## スキャン宛先一覧関数
直前に認証などを行ったプリンタに保存されているスキャン宛先の一覧を取得することができる関数です。
```
ps.get_scan_destination_list()
```
以下のようにすることですでに認証などを行っているプリンタの情報を取得することができます。
```
ps.get_scan_destination_list(access_token=アクセストークン, subject_id=プリンタのID)
```
戻り値は以下のようになります。
```
{
    "destinations": [
        {
            "scan_dest_id":"スキャン宛先ID", 
            "alias_name": "エイリアス名", 
            "dest_type": "スキャン宛先の種類(url/email)", 
            "destination":"スキャン宛先" 
        }
    ]
}
```

## スキャン宛先登録関数
直前に認証などを行ったプリンタに対してスキャン宛先を登録することのできる関数です。
```
ps.register_scan_destination(data)
```
以下のようにすることですでに認証などを行っているプリンタに対してスキャン宛先を登録することができます。
```
ps.register_scan_destination(data, access_token=アクセストークン, subject_id=プリンタのID)
```
宛先登録用データの例
```
    data = {
            "alias_name":"エイリアス名",
            "dest_type":"スキャン宛先の種別(url/mail)",
            "destination":"スキャン宛先"
            }
```

## スキャン宛先更新関数
直前に認証などを行ったプリンタに対して、既に登録されている宛先を変更することのできる関数です。
```
ps.update_scan_destination(data)
```
以下のようにすることで既に認証を行っているプリンタに対しても同様なことが行えます。
```
ps.update_scan_destination(data, access_token=アクセストークン, subject_id=プリンタのID)
```
宛先変更用データの例
```
    data = {
            "scan_dest_id":scan_dest_id,
            "alias_name":"エイリアス名",
            "dest_type":"スキャン宛先の種別(url/mail)",
            "destination":"スキャン宛先"
            }
```

## スキャン宛先削除関数
アクセストークン、プリンタのID、スキャン宛先IDを指定することにより、指定した宛先をプリンタから削除できる関数です。
```
ps.delete_scan_destination(アクセストークン, プリンタのID, スキャン宛先ID)
```
