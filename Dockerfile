# שימוש בתמונה בסיסית של Python 3.10
FROM python:3.10

# הגדרת תיקיית העבודה בתוך הקונטיינר
WORKDIR /app

# עדכון pip לגרסה האחרונה
RUN pip install --upgrade pip

# העתקת קובץ requirements.txt לקונטיינר
COPY requirements.txt /app/

# התקנת התלויות מתוך requirements.txt
RUN pip install -r requirements.txt

# העתקת תיקיית Catalogs (שכוללת קבצי JSON ו-GeoJSON) לקונטיינר
COPY Catalogs /app/Catalogs

# העתקת ה-Notebook לקונטיינר
COPY main.ipynb /app/

# הפעלת Notebook באמצעות nbconvert
CMD ["jupyter", "nbconvert", "--to", "python", "--execute", "main.ipynb"]
