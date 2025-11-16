#!/usr/bin/env python3
"""
myTinyDesk PDF Reader - Automatisches Setup Script
Installiert automatisch alle Dependencies und bereitet die Anwendung vor.
OS-übergreifend: Linux, Windows, macOS
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path


class Colors:
    """ANSI Farben für Terminal-Output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    
    @staticmethod
    def disable_on_windows():
        """Deaktiviere Farben auf Windows falls nicht unterstützt"""
        if platform.system() == "Windows":
            for attr in dir(Colors):
                if not attr.startswith('_') and attr != 'disable_on_windows':
                    setattr(Colors, attr, '')


def print_header(text):
    """Drucke formatierten Header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")


def print_success(text):
    """Drucke Erfolgs-Nachricht"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_info(text):
    """Drucke Info-Nachricht"""
    print(f"{Colors.OKBLUE}ℹ {text}{Colors.ENDC}")


def print_warning(text):
    """Drucke Warnungs-Nachricht"""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")


def print_error(text):
    """Drucke Fehler-Nachricht"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def detect_os():
    """Erkenne Betriebssystem"""
    system = platform.system()
    print_info(f"Erkanntes Betriebssystem: {system}")
    print_info(f"Python Version: {platform.python_version()}")
    return system


def check_python_version():
    """Prüfe Python Version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error(f"Python 3.8+ benötigt, aber {version.major}.{version.minor} gefunden")
        return False
    print_success(f"Python Version {version.major}.{version.minor}.{version.micro} OK")
    return True


def check_tkinter():
    """Prüfe ob Tkinter verfügbar ist"""
    try:
        import tkinter
        print_success("Tkinter ist verfügbar")
        return True
    except ImportError:
        print_warning("Tkinter ist nicht installiert")
        return False


def install_tkinter(os_type):
    """Installiere Tkinter basierend auf OS"""
    print_info("Versuche Tkinter zu installieren...")
    
    if os_type == "Linux":
        # Erkenne Linux Distribution
        try:
            with open('/etc/os-release', 'r') as f:
                content = f.read().lower()
                if 'ubuntu' in content or 'debian' in content:
                    cmd = ['sudo', 'apt-get', 'install', '-y', 'python3-tk']
                elif 'fedora' in content or 'rhel' in content or 'centos' in content:
                    cmd = ['sudo', 'dnf', 'install', '-y', 'python3-tkinter']
                elif 'arch' in content:
                    cmd = ['sudo', 'pacman', '-S', '--noconfirm', 'tk']
                else:
                    print_warning("Unbekannte Linux-Distribution. Bitte installiere Tkinter manuell:")
                    print_info("  Debian/Ubuntu: sudo apt-get install python3-tk")
                    print_info("  Fedora/RHEL:   sudo dnf install python3-tkinter")
                    print_info("  Arch:          sudo pacman -S tk")
                    return False
            
            print_info(f"Führe aus: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=False)
            return result.returncode == 0
            
        except Exception as e:
            print_error(f"Fehler beim Installieren von Tkinter: {e}")
            return False
            
    elif os_type == "Darwin":  # macOS
        print_info("Auf macOS ist Tkinter normalerweise vorinstalliert.")
        print_warning("Falls nicht, installiere mit: brew install python-tk")
        return False
        
    elif os_type == "Windows":
        print_info("Auf Windows ist Tkinter normalerweise in Python enthalten.")
        print_warning("Falls nicht, installiere Python neu von python.org mit Tkinter-Option")
        return False
    
    return False


def create_venv():
    """Erstelle virtuelle Umgebung"""
    venv_path = Path('.venv')
    
    if venv_path.exists():
        print_info("Virtuelle Umgebung existiert bereits")
        return True
    
    print_info("Erstelle virtuelle Umgebung...")
    try:
        subprocess.run([sys.executable, '-m', 'venv', '.venv'], check=True)
        print_success("Virtuelle Umgebung erstellt")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Fehler beim Erstellen der virtuellen Umgebung: {e}")
        return False


def get_venv_python():
    """Hole Pfad zum Python in der virtuellen Umgebung"""
    if platform.system() == "Windows":
        return Path('.venv') / 'Scripts' / 'python.exe'
    else:
        return Path('.venv') / 'bin' / 'python'


def install_requirements():
    """Installiere Requirements aus requirements.txt"""
    requirements_file = Path('requirements.txt')
    
    if not requirements_file.exists():
        print_error("requirements.txt nicht gefunden!")
        return False
    
    print_info("Lese requirements.txt...")
    with open(requirements_file, 'r') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    print_info(f"Gefundene Dependencies: {', '.join(requirements)}")
    
    venv_python = get_venv_python()
    
    print_info("Installiere Dependencies...")
    try:
        subprocess.run([
            str(venv_python), '-m', 'pip', 'install', '--upgrade', 'pip'
        ], check=True, capture_output=True)
        
        subprocess.run([
            str(venv_python), '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], check=True)
        
        print_success("Alle Dependencies erfolgreich installiert")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Fehler beim Installieren der Dependencies: {e}")
        return False


def create_launcher(os_type):
    """Erstelle Starter-Script"""
    print_info("Erstelle Starter-Script...")
    
    if os_type == "Windows":
        launcher_path = Path('start_pdfreader.bat')
        content = """@echo off
.venv\\Scripts\\python.exe main.py
pause
"""
    else:  # Linux/macOS
        launcher_path = Path('start_pdfreader.sh')
        content = """#!/bin/bash
.venv/bin/python main.py
"""
    
    try:
        with open(launcher_path, 'w') as f:
            f.write(content)
        
        if os_type != "Windows":
            os.chmod(launcher_path, 0o755)
        
        print_success(f"Starter-Script erstellt: {launcher_path}")
        return True
    except Exception as e:
        print_error(f"Fehler beim Erstellen des Starter-Scripts: {e}")
        return False


def test_installation():
    """Teste die Installation"""
    print_info("Teste Installation...")
    
    venv_python = get_venv_python()
    
    try:
        # Teste ob alle Module importiert werden können
        test_code = """
import tkinter
import fitz
from PIL import Image
print("OK")
"""
        result = subprocess.run(
            [str(venv_python), '-c', test_code],
            capture_output=True,
            text=True,
            check=True
        )
        
        if "OK" in result.stdout:
            print_success("Installation erfolgreich getestet")
            return True
        else:
            print_error("Test fehlgeschlagen")
            return False
            
    except subprocess.CalledProcessError as e:
        print_error(f"Test fehlgeschlagen: {e}")
        print_error(f"Output: {e.stderr}")
        return False


def main():
    """Hauptfunktion"""
    # Deaktiviere Farben auf Windows falls nötig
    if platform.system() == "Windows":
        Colors.disable_on_windows()
    
    print_header("myTinyDesk PDF Reader - Setup")
    
    # 1. OS erkennen
    os_type = detect_os()
    
    # 2. Python Version prüfen
    if not check_python_version():
        print_error("Setup abgebrochen: Python Version zu alt")
        sys.exit(1)
    
    # 3. Tkinter prüfen
    has_tkinter = check_tkinter()
    if not has_tkinter:
        installed = install_tkinter(os_type)
        if installed:
            has_tkinter = check_tkinter()
        
        if not has_tkinter:
            print_warning("\nTkinter konnte nicht automatisch installiert werden.")
            print_warning("Bitte installiere Tkinter manuell und führe setup.py erneut aus.")
            response = input("\nTrotzdem fortfahren? (j/n): ")
            if response.lower() != 'j':
                sys.exit(1)
    
    # 4. Virtuelle Umgebung erstellen
    if not create_venv():
        print_error("Setup abgebrochen: Konnte virtuelle Umgebung nicht erstellen")
        sys.exit(1)
    
    # 5. Requirements installieren
    if not install_requirements():
        print_error("Setup abgebrochen: Konnte Dependencies nicht installieren")
        sys.exit(1)
    
    # 6. Starter-Script erstellen
    create_launcher(os_type)
    
    # 7. Installation testen
    test_installation()
    
    # Fertig!
    print_header("Installation abgeschlossen!")
    
    print(f"\n{Colors.OKGREEN}{Colors.BOLD}myTinyDesk PDF Reader ist bereit!{Colors.ENDC}\n")
    print("Starte die Anwendung mit:")
    if os_type == "Windows":
        print(f"  {Colors.OKCYAN}start_pdfreader.bat{Colors.ENDC}")
        print(f"  oder: {Colors.OKCYAN}.venv\\Scripts\\python.exe main.py{Colors.ENDC}")
    else:
        print(f"  {Colors.OKCYAN}./start_pdfreader.sh{Colors.ENDC}")
        print(f"  oder: {Colors.OKCYAN}.venv/bin/python main.py{Colors.ENDC}")
    
    print(f"\n{Colors.OKBLUE}Viel Spaß mit myTinyDesk! ⭐{Colors.ENDC}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("\n\nSetup abgebrochen durch Benutzer")
        sys.exit(1)
    except Exception as e:
        print_error(f"\n\nUnerwarteter Fehler: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
