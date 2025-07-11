import pymysql
from app.core.config import settings

def reset_database():
    # 解析数据库URL
    db_url = settings.DATABASE_URL
    user = db_url.split('://')[1].split(':')[0]
    password = db_url.split(':')[2].split('@')[0]
    host = db_url.split('@')[1].split('/')[0]
    database = db_url.split('/')[-1]

    # 连接到MySQL
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password
    )
    
    try:
        with conn.cursor() as cursor:
            # 删除数据库（如果存在）
            cursor.execute(f"DROP DATABASE IF EXISTS {database}")
            # 创建新数据库
            cursor.execute(f"CREATE DATABASE {database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"数据库 {database} 已重置")
    except Exception as e:
        print(f"重置数据库时出错：{str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    reset_database() 