"""Compatibility entry point for the revised A3 portfolio builder.
Optional document tooling requires Python/reportlab/python-docx/Pillow/qrcode and Tahoma.
The PHP app itself has no Python dependency.
"""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('build-final-portfolio.py')),run_name='__main__')