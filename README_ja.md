# Camera Info SQL

[English](README.md) | [日本語](README_ja.md)

ROS2のcamera_info topicをDatabaseにjson形式で保存するサンプルです。

## 事前インストールが必要なもの

---

- Docker
- Docker Compose
- Python 3.6.x かそれ以上のバージョン
    - mysql-connector-python (pip)
- ROS2 (テストではhumbleを利用しました)
  - v4l2_camera (Webカメラ情報のPublisher)

## 構成

---

```
camera_info_sql
├── docs
│   └── figures/
├── db
│   ├── migration/
│   ├── Dockerfile
│   └── docker-compose.yml
├── resource/
│   └── jsons/
└── camera_info_sql
    ├── sql_operations/
    ├── ${SQLの操作を行うためのPythonファイル}
    └── camera_info_sql_node.py
```

## 導入設定

---

以下のコマンドを実行:

このリポジトリの取得

```shell
cd ~/ros2_ws/src
git clone git@github.com:koukemo/camera_info_sql.git
```

Packageのビルド

```shell
cd ~/ros2_ws
colcon build --packages-select camera_info_sql
```


## テスト

---

以下のコマンドを実行:

端末1 (DBコンテナと自動マイグレーション)

```shell
cd camera_info_sql/db
docker-compose up
```

端末2 (Webカメラ情報のPublish)

```shell
ros2 run v4l2_camera v4l2_camera_node
```

端末3 (camera_info_sqlの実行)

```shell
cd ~/ros2_ws
. ./install/setup.bash
ros2 run camera_info_sql camera_info_sub
```

## その他のデータベース操作

### MySQLに入る

DBコンテナを起動した状態で以下コマンドを実行: <br>
(接続用パスワードはデフォルトで"test"に設定しています)

```shell
mysql -h 127.0.0.1 -P 3306 -u test -p
```

### テーブル, 挿入データの閲覧

**テーブル名の閲覧** <br>

```shell
python3 ~/ros2_ws/src/camera_info_sql/camera_info_sql/show_tables.py
```

**挿入データの閲覧** <br>
閲覧するデータのデフォルト設定 | table : 'json_tables', column : '*' <br>
(もし閲覧情報を変更したい場合は, [camera_info_sql/camera_info_sql/show_columns.py](camera_info_sql/show_columns.py)を編集)

```shell
python3 ~/ros2_ws/src/camera_info_sql/camera_info_sql/show_columns.py
```

<br>

### 挿入データの削除

> **Warning** <br>
> このコマンドを実行すると, 全テーブルに挿入されたすべてのデータが空になるので注意してください！

**全テーブルのデータを削除** <br>

```shell
python3 ~/ros2_ws/src/camera_info_sql/camera_info_sql/delete_columns.py
```

## 結果

---

SQLに挿入されたデータを確認 : 

![SQL_content](docs/figures/camera_info_sql.png)

<br>

書き出したJsonファイルを確認 : 

![Json_content](docs/figures/camera_info_json_from_msg.png)