import csv
from database import add_host, get_all_hosts

def import_from_csv(csv_file_path):
    """CSVファイルからホスト情報をインポート"""
    success_count = 0
    error_count = 0
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                hostname = row['hostname'].strip()
                ip_address = row['ip_address'].strip()
                
                if add_host(hostname, ip_address):
                    print(f"✓ Added: {hostname} ({ip_address})")
                    success_count += 1
                else:
                    print(f"✗ Skipped (duplicate): {hostname} ({ip_address})")
                    error_count += 1
        
        print(f"\n=== Import Summary ===")
        print(f"Successfully imported: {success_count}")
        print(f"Skipped (duplicates): {error_count}")
        print(f"Total: {success_count + error_count}")
        
    except FileNotFoundError:
        print(f"Error: File '{csv_file_path}' not found!")
    except Exception as e:
        print(f"Error: {e}")

def show_all_hosts():
    """現在のDB内容を表示"""
    hosts = get_all_hosts()
    
    if not hosts:
        print("No hosts in database.")
        return
    
    print("\n=== Current Hosts in Database ===")
    print(f"{'ID':<5} {'Hostname':<20} {'IP Address':<15}")
    print("-" * 45)
    for host in hosts:
        print(f"{host['id']:<5} {host['hostname']:<20} {host['ip_address']:<15}")

if __name__ == '__main__':
    # CSVからインポート
    import_from_csv('data/sample_hosts.csv')
    
    # DB内容を表示
    show_all_hosts()