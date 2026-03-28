"""
freeze.py - 将 Flask 网站转为静态文件，用于部署到 GitHub Pages
============================================================
运行方式：
  pip install flask-frozen
  python freeze.py

生成的静态文件会在 build/ 文件夹里，上传到 GitHub 即可。
"""

from flask_frozen import Freezer
from app import app

app.config['FREEZER_DESTINATION'] = 'build'
app.config['FREEZER_RELATIVE_URLS'] = True

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()
    print("\n✅ 静态文件已生成在 build/ 文件夹！")
    print("   把 build/ 里的所有文件上传到 GitHub 仓库即可。")
