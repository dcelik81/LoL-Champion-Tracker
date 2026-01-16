import subprocess

def run_build():
    print("Build işlemi başlatılıyor...")
    
    command = [
        "pyinstaller",
        "--onefile",
        "--noconsole",
        "--name", "main",
        "--collect-all", "win10toast",
        "main.py"
    ]
    
    try:
        subprocess.run(command, check=True)
        print("\nBuild başarıyla tamamlandı! 'dist' klasörünü kontrol edin.")
    except subprocess.CalledProcessError as e:
        print(f"\nBir hata oluştu: {e}")
    except FileNotFoundError:
        print("\nPyInstaller bulunamadı. 'pip install pyinstaller' yaptığınızdan emin olun.")

if __name__ == "__main__":
    run_build()