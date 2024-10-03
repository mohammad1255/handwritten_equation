from PIL import Image, ImageDraw, ImageFont
import random
import os

# إعداد المسار لحفظ الصور
output_dir = 'generated_data'
os.makedirs(output_dir, exist_ok=True)

# إعداد قائمة الأرقام والألوان
numbers = list('0123456789')
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]

# إعداد الخط
font = ImageFont.truetype("arial.ttf", 40)  # استخدم مسار الخط الموجود لديك

# توليد الصور
for i in range(1000):  # توليد 1000 صورة كمثال
    img = Image.new('RGB', (100, 100), color=(255, 255, 255))  # خلفية بيضاء
    d = ImageDraw.Draw(img)
    
    # رسم أرقام عشوائية
    for _ in range(random.randint(3, 10)):
        number = random.choice(numbers)
        color = random.choice(colors)
        x = random.randint(0, 80)
        y = random.randint(0, 80)
        d.text((x, y), number, fill=color, font=font)

    # حفظ الصورة
    img.save(os.path.join(output_dir, f'image_{i}.png'))

print(f"تم توليد الصور في المجلد: {output_dir}")
