# KJ Nail Studio 网站

## 📁 项目结构

```
kjnailstudio/
├── app.py                  ← Python主程序（在这里修改网站信息）
├── requirements.txt        ← Python依赖包
├── templates/
│   └── index.html          ← 网站HTML模板
├── static/
│   ├── css/
│   │   └── style.css       ← 网站样式（黑金风格）
│   ├── js/
│   │   └── script.js       ← 网站功能
│   └── images/             ← 放你的图片在这里
│       └── wechat-qr.png   ← 微信二维码（放这里）
```

---

## 🚀 本地运行方法

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动网站
python app.py

# 3. 用浏览器打开
http://localhost:5000
```

---

## ✏️ 需要你修改的内容（打开 app.py）

在 `SITE_CONFIG` 字典里修改：

| 字段 | 说明 |
|------|------|
| `phone` | 你的电话号码 |
| `whatsapp` | 你的WhatsApp号码 |
| `email` | 你的邮箱地址 |
| `wechat_id` | 你的微信ID |

---

## 📸 添加图片

### 微信二维码
1. 把你的微信二维码图片重命名为 `wechat-qr.png`
2. 放入 `static/images/` 文件夹

### 作品照片
在 `templates/index.html` 里找到 gallery-placeholder，替换为：
```html
<img src="{{ url_for('static', filename='images/你的图片名.jpg') }}" 
     alt="作品" class="gallery-img">
```

---

## 🌐 部署到 GitHub Pages（静态版）

GitHub Pages 不支持 Python，需要先把网站转为静态文件：

```bash
pip install flask-frozen
python freeze.py
```

然后把 `build/` 文件夹的内容上传到 GitHub。

---

## 📞 联系方式位置

网站"联系我们"板块包含：
- 📍 地址（229 Stirling Highway, Claremont）
- 🕐 营业时间
- 📞 电话（可点击直接拨打）
- 💬 WhatsApp（点击直接打开对话）
- 🟢 微信（显示二维码扫描）
- ✉️ 邮件
