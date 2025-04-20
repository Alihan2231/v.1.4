#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Hata ayıklama yardımcıları
"""

import traceback
import sys
import os
import time

# Log dosyasının yolu
LOG_FILE = os.path.join(os.path.dirname(__file__), "debug_log.txt")

# Global exception hook
def global_exception_hook(exctype, value, tb):
    """Global exception hook"""
    try:
        # Orijinal hata işlemeyi çağır
        sys.__excepthook__(exctype, value, tb)
        
        # Hata bilgilerini dosyaya yaz
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n\n=== UNCAUGHT EXCEPTION {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n")
            f.write(f"Type: {exctype.__name__}\n")
            f.write(f"Value: {value}\n")
            f.write("Traceback:\n")
            traceback_str = "".join(traceback.format_tb(tb))
            f.write(traceback_str)
            f.write("\n=== END OF UNCAUGHT EXCEPTION ===\n\n")
    except Exception as e:
        print(f"Exception hook hatası: {e}")

# Tkinter için callback exception handler
def tkinter_exception_handler(func):
    """Tkinter fonksiyonlarını exception handler ile sarar"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Hata bilgilerini log dosyasına yaz
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"\n\n=== TKINTER EXCEPTION {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n")
                f.write(f"Function: {func.__name__}\n")
                f.write(f"Args: {args}\n")
                f.write(f"Kwargs: {kwargs}\n")
                f.write(f"Exception: {e}\n")
                f.write("Traceback:\n")
                traceback_str = traceback.format_exc()
                f.write(traceback_str)
                f.write("\n=== END OF TKINTER EXCEPTION ===\n\n")
            
            # Konsola da yazdır
            print(f"TKINTER EXCEPTION in {func.__name__}: {e}")
            traceback.print_exc()
            
            # Kullanıcıya bildir (tkinter messagebox kullanmak döngüsel referans oluşturur)
            print("HATA: Bu işlem sırasında beklenmeyen bir hata oluştu. Debug log'a bakınız.")
    
    return wrapper

# Log dosyasını temizle ve başlat
def init_debug_logging():
    """Log dosyasını temizle ve başlat"""
    try:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(f"=== DEBUG LOG STARTED {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n\n")
        
        # Global exception hook'u ayarla
        sys.excepthook = global_exception_hook
        
        print(f"Debug logging başlatıldı: {LOG_FILE}")
        return True
    except Exception as e:
        print(f"Debug logging başlatılamadı: {e}")
        return False

# Log mesajı yaz
def log(message, level="INFO"):
    """Log mesajı yaz"""
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] [{level}] {message}\n")
        return True
    except Exception as e:
        print(f"Log yazılamadı: {e}")
        return False

# Exception'ı logla
def log_exception(e, context=""):
    """Exception'ı logla"""
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] [ERROR] Exception in {context}: {e}\n")
            f.write(traceback.format_exc())
            f.write("\n")
        return True
    except Exception as e2:
        print(f"Exception log yazılamadı: {e2}, Orijinal hata: {e}")
        return False
