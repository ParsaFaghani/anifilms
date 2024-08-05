# A animelist site for translate and upload animes
<p align="center"><img alt="anifilms Demo" src="https://github.com/ParsaFaghani/anifilms/raw/master/screenshot1.jpg"/></p>

## 6 steps for run and using:
### **step 1:** install requirements:
run: ```pip install -r requirements.txt```
### **step 2:** Change the variables in the .env file with your information

> [!NOTE]
> can using postgresql for database and set your postger variables in to .env file(If you use postgresql, you must change the database in the settings)

### **step 3:** set migrations:
run ```python manage.py makemigrations```
and run ```python manage.py migrate```

### **step 4:** upload static files to server:
run ```python manage.py collectstatic```

### **step 5:** create a admin user for add first anime to site:
run ```python manage.py createsuperuser```
and set username, email and password

### **step 6:** run site in localhost:
run ```python manage.py runserver```
and open 127.0.0.1:8000 in browser

well, you see a 404 page in 127.0.0.1:8000
add a anime to site for fix problem
for this you open 127.0.0.1:8000/admin/ and enter username and password to login in django controlpanel
afer login you create a anime
> [!IMPORTANT]
> you can change comment and react settings in controlpanel for better look


## ToDo
- [X] control panel
- [X] favorits
- [X] translators profile
- [X] follow and unfollow system
- [X] comment and rating system
- [X] multilanguage(Farsi and English)
- [ ] drf api
- [ ] payment system
- [ ] and your idea


thank you
