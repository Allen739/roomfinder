
# 🏫 Room Finder

**Room Finder** is a plug-and-play Django app that helps students and lecturers instantly find free classrooms across campus. Upload your timetables and room lists, and instantly get free classrooms across campus✌️.

---

## 🚀 Key Features

- 🔼 **Excel Upload**  
  Upload room and schedule data via Excel (`rooms.xlsx`, `timetable.xlsx`) from `/upload/`.

- 🔍 **Search Engine for Classrooms**  
  Filter by building, day, time, and duration at `/`. Find the perfect free room — fast.

- 🛠️ **Admin Panel Tools**  
  Update schedules, cancel lectures, and reassign classrooms at `/admin/`.

- 🌍 **Universally Compatible**  
  Works with any institution’s naming conventions and time formats (12h/24h).

---

## 📦 Tech Stack

- **Backend**: Django 5.x
- **Database**: PostgreSQL / SQLite
- **File Upload**: pandas + openpyxl (for Excel parsing)

---

## 🧰 Prerequisites

- Python 3.8+
- pip
- Git
- virtualenv (recommended)

---

## ⚙️ Local Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Allen739/roomfinder.git
   cd room_finder
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv my-venv
   source my-venv/bin/activate  # or `my-venv\Scripts\activate` on Windows
   ```

3. **Install Requirements**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   Create a `.env` file in the project root:

   ```env
   SECRET_KEY=your-django-secret-key
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3  # or PostgreSQL URL for prod
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Apply Migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

Access:
Search: http://localhost:8000/

Upload: http://localhost:8000/upload/ (login required)

Admin: http://localhost:8000/admin/



---

## 📁 File Upload Format

- `rooms.xlsx`: Room and Building  (e.g., "Lab-1", "Engineering Block").

- `timetable.xlsx`: Course, Subject, Day/Time (e.g., "Mon 08:00-09:30"), Room, Building, Lecturer

> Full sample files are available in the `sample_data/` folder (optional).

---

## 💡 Future Additions

- 🔗 Google Calendar + Outlook sync
- 🧠 AI-based room recommendation
- 📱 Mobile-friendly frontend
- 🔒 User login + role-based permissions

---

Deployment
Deploy to Heroku for public use:
Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli.

Create a Heroku app:
bash

heroku create your-app-name

Set environment variables:
bash

heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app.herokuapp.com

Push to Heroku:
bash

git push heroku main

Run migrations:
bash

heroku run python manage.py migrate

Create superuser:
bash

heroku run python manage.py createsuperuser

Access: https://your-app.herokuapp.com/

Contributing
See CONTRIBUTING.md for how to contribute.
License
MIT License (see LICENSE).
Demo
(TBD: Add link after hosting, e.g., https://room-finder-demo.herokuapp.com/)
Star this repo if you find it useful! 

**Action 2**: Create `LICENSE`.
```bash
touch LICENSE

Content (LICENSE):

MIT License

Copyright (c) 2025 Allen West

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



**Built for modern campuses. Built with ❤️ in Django.**
```

