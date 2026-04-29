import requests
import sqlite3
import json
import os
from datetime import datetime

config = json.load(open("config.json"))
TikTok_API_BASE = "https://open-api.tiktok.com"

class TikTokAPI:
    def __init__(self):
        self.client_key = config["tiktok"]["client_key"]
        self.client_secret = config["tiktok"]["client_secret"]
        self.shop_id = config["tiktok"]["shop_id"]
        self.access_token = None
    
    def get_access_token(self):
        url = f"{TikTok_API_BASE}/oauth/access_token/"
        data = {
            "client_key": self.client_key,
            "client_secret": self.client_secret,
            "grant_type": "client_credential"
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            self.access_token = response.json().get("data", {}).get("access_token")
            return self.access_token
        return None
    
    def get_products(self, limit=20):
        if not self.access_token:
            self.get_access_token()
        
        url = f"{TikTok_API_BASE}/product/list/"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        params = {
            "shop_id": self.shop_id,
            "page_size": limit
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get("data", {}).get("products", [])
        return []

class Database:
    def __init__(self, db_name="alajashop.db"):
        self.db_name = db_name
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tiktok_product_id TEXT UNIQUE,
                title TEXT,
                description TEXT,
                price REAL,
                currency TEXT,
                images TEXT,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                video_path TEXT,
                status TEXT DEFAULT 'pending',
                published BOOLEAN DEFAULT 0,
                youtube_url TEXT,
                pinterest_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_product(self, product):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        tiktok_id = product.get("id")
        title = product.get("title", "")
        description = product.get("description", "")
        price = product.get("price", 0)
        currency = product.get("currency", "USD")
        images = ",".join([img.get("url") for img in product.get("images", [])])
        status = product.get("status", "active")
        
        cursor.execute("""
            INSERT OR REPLACE INTO products 
            (tiktok_product_id, title, description, price, currency, images, status, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (tiktok_id, title, description, price, currency, images, status, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_products(self, status=None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        if status:
            cursor.execute("SELECT * FROM products WHERE status=?", (status,))
        else:
            cursor.execute("SELECT * FROM products")
        
        rows = cursor.fetchall()
        conn.close()
        
        products = []
        for row in rows:
            products.append({
                "id": row[0],
                "tiktok_product_id": row[1],
                "title": row[2],
                "description": row[3],
                "price": row[4],
                "currency": row[5],
                "images": row[6].split(","),
                "status": row[7],
                "created_at": row[8],
                "updated_at": row[9]
            })
        return products

def sync_products():
    api = TikTokAPI()
    db = Database()
    
    products = api.get_products()
    
    for product in products:
        db.save_product(product)
    
    return len(products)

if __name__ == "__main__":
    print("Sincronizando productos de TikTok Shop...")
    count = sync_products()
    print(f"{count} productos guardados en la base de datos")