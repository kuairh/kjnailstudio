"""
KJ Nail Studio - Flask Web Application
=======================================
运行方式 / How to run:
  1. pip install flask
  2. python app.py
  3. 打开浏览器访问 http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# ============================================================
# 邮件配置 / Email Configuration
# ============================================================
EMAIL_CONFIG = {
    # 发件邮箱（用于发送通知的邮箱，建议用 Gmail 或其他 SMTP 邮箱）
    "sender_email":    "your-sender@gmail.com",       # TODO: 填入发件邮箱
    # 发件邮箱的授权密码（Gmail 请使用"应用专用密码"，非登录密码）
    "sender_password": "your-app-password",            # TODO: 填入授权密码
    # 收件邮箱（预约通知发到这里）
    "receiver_email":  "",                             # TODO: 填入接收通知的邮箱
    # SMTP 服务器设置（Gmail 默认，如用其他邮箱请修改）
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
}


def send_booking_email(data: dict) -> bool:
    """发送预约通知邮件，成功返回 True，失败返回 False"""
    receiver = EMAIL_CONFIG["receiver_email"]
    if not receiver:
        print("[邮件] 收件邮箱未配置，跳过发送")
        return False

    subject = f"[KJ Nail Studio] 新预约 - {data.get('name', '未知姓名')}"

    body_lines = ["您有一条新的预约请求：\n"]
    field_labels = {
        "name":    "姓名",
        "phone":   "电话",
        "email":   "邮箱",
        "service": "服务项目",
        "date":    "预约日期",
        "time":    "预约时间",
        "notes":   "备注",
    }
    for key, label in field_labels.items():
        if key in data:
            body_lines.append(f"{label}: {data[key]}")

    body_lines.append(f"\n提交时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    msg = MIMEMultipart()
    msg["From"]    = EMAIL_CONFIG["sender_email"]
    msg["To"]      = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText("\n".join(body_lines), "plain", "utf-8"))

    try:
        with smtplib.SMTP(EMAIL_CONFIG["smtp_host"], EMAIL_CONFIG["smtp_port"]) as server:
            server.starttls()
            server.login(EMAIL_CONFIG["sender_email"], EMAIL_CONFIG["sender_password"])
            server.sendmail(EMAIL_CONFIG["sender_email"], receiver, msg.as_string())
        print(f"[邮件] 预约通知已发送至 {receiver}")
        return True
    except Exception as e:
        print(f"[邮件] 发送失败: {e}")
        return False

SITE_CONFIG = {
    "studio_name": "KJ Nail Studio",
    "tagline_zh": "每一片指尖，都是一件艺术品",
    "tagline_en": "Every nail, a work of art",
    "address": "229 Stirling Highway, Claremont, WA 6010",
    "city": "Perth, Western Australia",
    "hours": "Mon - Sun: 10:00 AM - 7:00 PM",
    "hours_zh": "周一至周日 10:00 - 19:00",
    "phone": "+61 4XX XXX XXX",
    "whatsapp": "+61 4XX XXX XXX",
    "email": "info@kjnailstudio.com.au",
    "wechat_id": "你的微信ID",
    "wechat_qr_image": "images/wechat-qr.png",
    "year": datetime.now().year,
}

SERVICES = [
    {
        "icon": "💅",
        "name_zh": "凝胶美甲",
        "name_en": "Gel Nails",
        "featured": False,
        "badge_zh": "",
        "badge_en": "",
        "items": [
            {"name_zh": "基础凝胶 (单色)", "name_en": "Basic Gel (Solid Color)", "price": "$45"},
            {"name_zh": "法式凝胶",        "name_en": "French Gel",             "price": "$55"},
            {"name_zh": "猫眼凝胶",        "name_en": "Cat Eye Gel",            "price": "$60"},
            {"name_zh": "渐变凝胶",        "name_en": "Ombre Gel",              "price": "$65"},
        ],
    },
    {
        "icon": "✨",
        "name_zh": "艺术美甲",
        "name_en": "Nail Art",
        "featured": True,
        "badge_zh": "最受欢迎",
        "badge_en": "Most Popular",
        "items": [
            {"name_zh": "简单图案 (每指)", "name_en": "Simple Art (per nail)", "price": "$5+"},
            {"name_zh": "3D浮雕艺术",     "name_en": "3D Nail Art",           "price": "$80+"},
            {"name_zh": "手绘设计",       "name_en": "Hand-painted Design",   "price": "$75+"},
            {"name_zh": "全套定制设计",   "name_en": "Full Custom Set",       "price": "$90+"},
        ],
    },
    {
        "icon": "💎",
        "name_zh": "延长美甲",
        "name_en": "Nail Extensions",
        "featured": False,
        "badge_zh": "",
        "badge_en": "",
        "items": [
            {"name_zh": "水晶延长", "name_en": "Acrylic Extensions", "price": "$75"},
            {"name_zh": "凝胶延长", "name_en": "Gel Extensions",     "price": "$80"},
            {"name_zh": "甲片延长", "name_en": "Tip Extensions",     "price": "$70"},
            {"name_zh": "补甲",     "name_en": "Infill",             "price": "$50"},
        ],
    },
    {
        "icon": "🌸",
        "name_zh": "美甲护理",
        "name_en": "Nail Care",
        "featured": False,
        "badge_zh": "",
        "badge_en": "",
        "items": [
            {"name_zh": "基础修甲",     "name_en": "Basic Manicure",   "price": "$30"},
            {"name_zh": "豪华手部护理", "name_en": "Luxury Hand Care", "price": "$55"},
            {"name_zh": "卸甲",         "name_en": "Gel Removal",      "price": "$20"},
            {"name_zh": "足部美甲",     "name_en": "Pedicure",         "price": "$50+"},
        ],
    },
]

@app.route("/")
def index():
    return render_template("index.html", config=SITE_CONFIG, services=SERVICES)

@app.route("/submit-booking", methods=["POST"])
def submit_booking():
    data = request.get_json()
    print("=== 新预约 / New Booking ===")
    for key, val in data.items():
        print(f"  {key}: {val}")
    send_booking_email(data)
    return jsonify({"success": True, "message": "预约已提交"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)