from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import subprocess
import re
from database import (
    init_db, get_all_hosts, get_host_by_id, 
    add_host, update_host, delete_host
)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# アプリ起動時にDB初期化
init_db()

def is_valid_ip(ip_address):
    """IPアドレスのバリデーション"""
    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    return bool(re.match(ipv4_pattern, ip_address))

def ping_host(ip_address, count=5):
    """Ping実行（Windows / Linux / WSL 対応）"""
    if not is_valid_ip(ip_address):
        return {"success": False, "error": "無効なIPアドレスです"}
    
    try:
        # Linux/WSL: -c, Windows: -n
        system = platform.system().lower()

        if system == "windows":
            cmd = ['ping', '-n', str(count), ip_address]
        else:
            cmd = ['ping', '-c', str(count), ip_address]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=15
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "タイムアウトしました"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ========== ルーティング ==========

@app.route('/')
def index():
    """トップページ - Ping実行"""
    hosts = get_all_hosts()
    return render_template('index.html', hosts=hosts)

@app.route('/ping', methods=['POST'])
def ping():
    """Ping実行API"""
    data = request.get_json()
    ip_address = data.get('ip_address', '').strip()
    
    if not ip_address:
        return jsonify({"success": False, "error": "IPアドレスを選択してください"})
    
    result = ping_host(ip_address)
    return jsonify(result)

@app.route('/list')
def list_hosts():
    """一覧ページ"""
    hosts = get_all_hosts()
    return render_template('list.html', hosts=hosts)

@app.route('/add', methods=['GET', 'POST'])
def add_new_host():
    """新規登録ページ"""
    if request.method == 'POST':
        hostname = request.form['hostname'].strip()
        ip_address = request.form['ip_address'].strip()
        
        if not hostname or not ip_address:
            flash('ホスト名とIPアドレスを入力してください', 'error')
            return render_template('add.html')
        
        if not is_valid_ip(ip_address):
            flash('有効なIPアドレスを入力してください', 'error')
            return render_template('add.html')
        
        if add_host(hostname, ip_address):
            flash('登録されました', 'success')
            return redirect(url_for('list_hosts'))
        else:
            flash('既に登録されているホスト名です', 'error')
            return render_template('add.html')
    
    return render_template('add.html')

@app.route('/edit/<int:host_id>', methods=['GET', 'POST'])
def edit_host(host_id):
    """編集・削除ページ"""
    host = get_host_by_id(host_id)
    
    if not host:
        flash('ホストが見つかりません', 'error')
        return redirect(url_for('list_hosts'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'update':
            hostname = request.form['hostname'].strip()
            ip_address = request.form['ip_address'].strip()
            
            if not hostname or not ip_address:
                flash('ホスト名とIPアドレスを入力してください', 'error')
                return render_template('edit.html', host=host)
            
            if not is_valid_ip(ip_address):
                flash('有効なIPアドレスを入力してください', 'error')
                return render_template('edit.html', host=host)
            
            update_host(host_id, hostname, ip_address)
            flash('編集されました', 'success')
            return redirect(url_for('list_hosts'))
        
        elif action == 'delete':
            delete_host(host_id)
            flash('削除されました', 'success')
            return redirect(url_for('list_hosts'))
    
    return render_template('edit.html', host=host)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)