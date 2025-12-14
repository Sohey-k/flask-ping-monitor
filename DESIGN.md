# Flask Ping Monitor - アプリケーション設計書

## 1. 概要
ネットワーク機器のPing監視を行うローカルWebアプリケーション。
SQLiteでホスト情報を管理し、簡易的なCRUD操作とPing実行機能を提供。

## 2. 技術スタック
- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML + Tailwind CSS (CDN)
- **起動**: Windowsバッチファイル (.bat)

## 3. データベース設計

### テーブル: hosts
| カラム名 | 型 | 制約 | 説明 |
|---------|-----|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 自動採番ID |
| hostname | TEXT | NOT NULL UNIQUE | ホスト名 |
| ip_address | TEXT | NOT NULL | IPアドレス |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 登録日時 |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 更新日時 |

## 4. 機能一覧

### 4.1 メイン機能（トップページ）
- **URL**: `/`
- **機能**: 
  - ドロップダウンメニューでホスト名を選択
  - 選択したホスト名に紐づくIPアドレスを自動セット
  - Pingボタンクリックで5回Ping実行
  - 結果をリアルタイム表示（成功/失敗、応答時間など）

### 4.2 一覧機能
- **URL**: `/list`
- **機能**:
  - DB内の全ホスト情報を表形式で表示
  - 各行にラジオボタン配置
  - ボタン:
    - 「編集」ボタン → 選択したホストの編集ページへ遷移
    - 「削除」ボタン → 選択したホストの削除確認
    - 「新規登録」ボタン → 新規登録ページへ遷移

### 4.3 編集・削除ページ
- **URL**: `/edit/<id>`
- **機能**:
  - 選択したホストのホスト名・IPアドレスを編集
  - 「更新」ボタン → DB更新 → 「編集されました」メッセージ表示
  - 「削除」ボタン → DB削除 → 「削除されました」メッセージ表示
  - 一覧ページへ戻るボタン

### 4.4 新規登録ページ
- **URL**: `/add`
- **機能**:
  - ホスト名・IPアドレス入力フォーム
  - 「登録」ボタン → DB登録 → 「登録されました」メッセージ表示
  - 一覧ページへ戻るボタン

### 4.5 初期データインポート機能
- **URL**: `/import` (管理用)
- **機能**:
  - CSVファイルアップロード
  - CSV形式: `hostname,ip_address`
  - 既存データとの重複チェック
  - 一括登録実行

## 5. ページ構成・画面遷移図
```
[トップページ / Ping実行]
    │
    ├─→ [一覧ページ]
    │       │
    │       ├─→ [編集・削除ページ] → (更新/削除後) → [一覧ページ]
    │       │
    │       └─→ [新規登録ページ] → (登録後) → [一覧ページ]
    │
    └─→ [インポートページ] (初回セットアップ用)
```

## 6. ディレクトリ構成
```
flask-ping-monitor/
├── app.py                 # メインアプリケーション
├── database.py            # DB操作関数
├── csv_import.py          # CSV→SQLiteインポートスクリプト
├── requirements.txt       # 依存パッケージ
├── start.bat              # Windows起動用バッチファイル
├── hosts.db               # SQLiteデータベース (自動生成)
├── data/
│   └── sample_hosts.csv   # サンプルCSVデータ
├── templates/
│   ├── base.html          # ベーステンプレート
│   ├── index.html         # トップページ (Ping実行)
│   ├── list.html          # 一覧ページ
│   ├── edit.html          # 編集・削除ページ
│   ├── add.html           # 新規登録ページ
│   └── import.html        # インポートページ
└── static/
    └── (必要に応じてCSS/JSファイル)
```

## 7. Ping実行仕様
- **コマンド**: `ping -n 5 {ip_address}` (Windows)
- **タイムアウト**: 10秒
- **結果表示**:
  - 成功: 応答時間、パケットロス率
  - 失敗: エラーメッセージ

## 8. セキュリティ考慮事項
- SQLインジェクション対策: パラメータ化クエリ使用
- コマンドインジェクション対策: IPアドレス・ホスト名のバリデーション
- ローカル環境専用のため、認証機能は実装しない

## 9. Windows起動方法

### start.bat の内容
```batch
@echo off
cd /d %~dp0
python app.py
pause
```

### 使用方法
1. `start.bat` をダブルクリック
2. ブラウザで `http://localhost:5000` を開く

## 10. 開発フェーズ

### Phase 1: 基盤構築
- プロジェクト構成作成
- DB設計・テーブル作成
- CSV インポート機能

### Phase 2: 基本機能実装
- トップページ (Ping実行)
- 一覧ページ

### Phase 3: CRUD機能実装
- 新規登録
- 編集・削除

### Phase 4: 仕上げ
- UI/UX調整 (Tailwind CSS)
- エラーハンドリング
- バッチファイル作成