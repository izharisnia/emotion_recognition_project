# 🎭 Emotion-Based Recipe Recommendation Project

This project is a **mood-driven recipe recommendation system** built with **Flask, SQLite, HTML, CSS, and JavaScript**.
Users can log their mood, and the app suggests recipes accordingly from the database.

---

## 🚀 Features

* User authentication (Sign up / Login).
* Mood-based recipe recommendations.
* Recipe details with ingredients, steps, and calorie info.
* Feedback and history tracking.
* Admin panel for managing recipes and users.

---

## 🗂️ Project Structure

```
emotion_recognition_project/
│── app.py               # Flask main app
│── database/
│   └── app.db           # SQLite database
│── static/              # CSS, JS, images
│── templates/           # HTML templates
│── recipes_seed.sql     # Sample data (recipes with mood tags)
│── requirements.txt     # Dependencies
│── README.md            # Project documentation
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**

```
git clone https://github.com/your-username/emotion_recognition_project.git
cd emotion_recognition_project
```

2. **Create virtual environment & activate**

```
python -m venv venv
# On Windows
venv\Scripts\activate
# On Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**

```
pip install -r requirements.txt
```

4. **Setup the database**

```
sqlite3 database/app.db < recipes_seed.sql
```

5. **Run the app**

```
python app.py
```

6. Open in browser:
   👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🔑 Admin Login Style (Important)

* The **Admin Panel** can be accessed by navigating to:

```
http://127.0.0.1:5000/admin
```

* Default credentials (update later in database):

```
Username: admin
Password: admin123
```

* From the **Admin Panel**, you can:

  * Add / Edit / Delete recipes.
  * Manage user accounts.
  * Review feedback and history.

---

## 📊 Example Recipes in Database

* "Happy Pancakes" 🥞 (Mood: Happy)
* "Comfort Soup" 🍲 (Mood: Sad)
* "Energy Smoothie" 🥤 (Mood: Tired)
* "Celebration Cake" 🍰 (Mood: Excited)

---

## 🛠️ Tech Stack

* **Backend:** Flask (Python)
* **Database:** SQLite
* **Frontend:** HTML, CSS, JS
* **Other:** Bootstrap, Jinja2 Templates

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss.

---

## 📜 License

This project is licensed under the MIT License.
