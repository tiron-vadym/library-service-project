# Library Service Project

API service for library management written on DRF

## Installing using GitHub

Install PostgresSQL and create db

```shell
git clone https://github.com/tiron-vadym/library-service-project
cd library_API
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
set DB_HOST=<your db hostname>
set DB_NAME=<your db name>
set DB_USER=<your db username>
set DB_PASSWORD=<your db user password>
set SECRET_KEY=<your secret key>
python manage.py migrate
python manage.py runserver
```

## Run with docker

Docker should be installed

```shell
docker-compose --build
docker-compose up
```

## Getting access(JWT authenticated)

* Used email instead of username
* Create user via /api/customer/register
* Get access token via /api/customer/token

## Endpoints

- Admin Panel: `/admin/`
- Books Service API: `/api/books-service/`
- Customer API: `/api/customer/`
- Borrowing Service API: `/api/borrowing-service/`
- Payments Service API: `/api/payments-service/`

## Debugging and Documentation

- Debug Toolbar: `/__debug__/`
- API Schema: `/api/schema/`
- Swagger Documentation: `/api/doc/swagger/`
- ReDoc Documentation: `/api/doc/redoc/`

#### Notifications Service (Telegram)

- Sending notifications about new borrowing created, borrowings overdue & successful payment
- Scheduled tasks for notifications about overdue borrowings using Сelery
- Telegram API integration

#### Payments Service (Stripe)

- Handling payments for book borrowings through the platform
- Stripe API integration
