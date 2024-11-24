# בסיס לתמונה, משתמש בגרסה עדכנית של Python
FROM python:3.9-slim

# יצירת תיקייה עבור האפליקציה
WORKDIR /app

# העתקת הקבצים הנדרשים
COPY . /app

# התקנת ספריות התלויות
RUN pip install --no-cache-dir -r requirements.txt

# פקודת הפעלה ברירת מחדל
CMD ["python", "main.py"]
