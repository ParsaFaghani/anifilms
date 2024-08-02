A animelist site for translate and upload animes

# steps for run and using:
step 1:
run: ```pip install -r requirements.txt```
step 2:
### Change the variables in the .env file with your information

> [!NOTE]
> ```LIARA_ACCESS_KEY``` == ```AWS_ACCESS_KEY_ID``` ------and------
> ```LIARA_SECRET_KEY``` == ```AWS_SECRET_ACCESS_KEY``` ------and------
> ```LIARA_BUCKET_NAME``` == ```AWS_STORAGE_BUCKET_NAME``` ------and------
> ```LIARA_ENDPOINT``` == ```AWS_S3_ENDPOINT_URL``` ------and------
> and ```AWS_S3_REGION_NAME``` == ```"us-east-1"``` ***default

> [!NOTE]
> using postgresql for database and set your postger variables in to .env file

### set migrations after set variables in .env file:
run ```python manage.py makemigrations```
and run ```python manage.py migrate```

### upload static files to server:
run ```python manage.py collectstatic```

### create a admin user for add first anime to site:
run ```python manage.py createsuperuser```
and set username, email and password

### run site in localhost:
run ```python manage.py runserver```
and open 127.0.0.1:8000 in browser

well, you see a 404 page in 127.0.0.1:8000
add a anime to site for fix problem
for this you open 127.0.0.1:8000/admin/ and enter username and password to login in django controlpanel
afer login you create a anime
> [!IMPORTANT]
> you can change comment and react settings in controlpanel for better look

thank you
