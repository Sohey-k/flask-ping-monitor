import sqlite3
from datetime import datetime

DB_NAME = 'hosts.db'

def get_db_connection():
    """データベース接続を取得"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # 辞書形式でアクセス可能にする
    return conn

def init_db():
    """データベースとテーブルを初期化"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS hosts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hostname TEXT NOT NULL UNIQUE,
            ip_address TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def get_all_hosts():
    """全ホスト情報を取得"""
    conn = get_db_connection()
    hosts = conn.execute('SELECT * FROM hosts ORDER BY hostname').fetchall()
    conn.close()
    return hosts

def get_host_by_id(host_id):
    """IDでホスト情報を取得"""
    conn = get_db_connection()
    host = conn.execute('SELECT * FROM hosts WHERE id = ?', (host_id,)).fetchone()
    conn.close()
    return host

def add_host(hostname, ip_address):
    """新規ホストを追加"""
    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO hosts (hostname, ip_address) VALUES (?, ?)',
            (hostname, ip_address)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False  # 重複エラー

def update_host(host_id, hostname, ip_address):
    """ホスト情報を更新"""
    conn = get_db_connection()
    conn.execute(
        'UPDATE hosts SET hostname = ?, ip_address = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
        (hostname, ip_address, host_id)
    )
    conn.commit()
    conn.close()

def delete_host(host_id):
    """ホストを削除"""
    conn = get_db_connection()
    conn.execute('DELETE FROM hosts WHERE id = ?', (host_id,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    # 直接実行した場合はDB初期化
    init_db()