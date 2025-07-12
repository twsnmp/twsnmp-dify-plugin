# twsnmp-dify-plugin

このツールは、DifyからTWSNMP FCを利用するためのプラグインです。
基本的にDifyをローカル環境で起動している

![](https://assets.st-note.com/img/1751835568-ZiXUPxl7Wj9h5eMKRAnrHBgs.png?width=1200)

のような環境で起動時の環境変数に

```
FORCE_VERIFYING_SIGNATURE=false
```

を設定していることを想定しています。
サービスで利用している場合にはたぶん使えないと思います。


Difyについては、

https://docs.dify.ai/ja-jp/introduction

TWSNMP FCは、

https://note.com/twsnmp/n/nc6e49c284afb

を参照してください。

## インストール


Difyの画面の「プラグインをインストールする」ボタンからGitHUBを選択します。

![](https://assets.st-note.com/img/1752267158-jnPmE5NpoRsFA3l7JUCwXH94.png?width=4000&height=4000&fit=bounds&format=jpg&quality=90)

twsnmp-dify-pluginのGitHUBのリポジトリのURL

https://github.com/twsnmp/twsnmp-dify-plugin

を入力します。

![](https://assets.st-note.com/img/1752267201-59kDFvSRcMxmfYO7oNV8lPAH.png?width=2000&height=2000&fit=bounds&quality=85)

＜次＞をクリックします。

![](https://assets.st-note.com/img/1752267285-yFYRtIXeWv5KxuaTpnf9iSgD.png?width=1200)

バージョンとパッケージファイルを選択します。
＜次＞をクリックします。

![](https://assets.st-note.com/img/1752267552-rnDjMZH1vOcLfxtPo6K9umBz.png)

のように表示されれば、インストール成功です。

## 認証の設定

プラグインのリストのTWSNMPをクリックして認証の設定をおこいます。

![](https://assets.st-note.com/img/1752267597-LSYh4JA3UlrRBvQsXG1aPuk6.png)

TWSNMP FCのURLとユーザー名、パスワードを入力して＜保存＞をクリックしてください。
エラーがなければ、プラグインが利用可能になります。


### ツールの内容

以下のツールが利用可能です。応答はJSONで出力されます。


| ツール名 | 説明 | パラメータ |
| :--- | :--- | :--- |
| `do_ping` | TWSNMP FCからPINGを実行します。 | `target_ip` (対象IPアドレス), `size` (パケットサイズ), `ttl` (TTL) |
| `get_cert_list` | TWSNMP FCからサーバー証明書のリストを取得します。 | (なし) |
| `get_env_sensor_list` | TWSNMP FCから環境センサーのリストを取得します。 | (なし) |
| `get_ip_address_list` | TWSNMP FCからIPアドレスリストを取得します。 | `name_filter` (名前フィルター), `ip_filter` (IPフィルター), `vendor_filter` (ベンダーフィルター) |
| `get_mac_address_list` | TWSNMP FCからMACアドレスリストを取得します。 | `name_filter` (名前フィルター), `ip_filter` (IPフィルター), `vendor_filter` (ベンダーフィルター) |
| `get_network_list` | TWSNMP FCからネットワークリストを取得します。 | `name_filter` (名前フィルター), `ip_filter` (IPフィルター) |
| `get_node_list` | TWSNMP FCからノードリストを取得します。 | `name_filter` (名前フィルター), `ip_filter` (IPフィルター), `state_filter` (状態フィルター) |
| `get_polling_list` | TWSNMP FCからポーリングリストを取得します。 | `type_filter` (種別フィルター), `name_filter` (名前フィルター), `node_name_filter` (ノード名フィルター), `state_filter` (状態フィルター) |
| `get_sensor_list` | TWSNMP FCからセンサーリストを取得します。 | (なし) |
| `get_wifi_ap_list` | TWSNMP FCからWifiのアクセスポイントのリストを取得します。 | (なし) |
| `snmpwalk` | TWSNMP FCからsnmpwalkを実行します。 | `target` (対象ノード), `mib` (MIBのオブジェクト名) |


## 利用例

AIエージェントのツールにsnmpwalkを

![](https://assets.st-note.com/img/1752308706-VTNO803ZtrHmjhUdyD6EfFnQ.png?width=1200)

のように設定でしてから、snmpwalkを実行するように指示すると

![](https://assets.st-note.com/img/1752268002-cxaPnt5lOhmFWueD17SUGzCM.png?width=1200)

のようにツールを使って実行します。

## プライバシーポリシー

[プライバシーポリシー](PRIVACY.md)

## ライセンス

[ライセンス](LICENSE)
