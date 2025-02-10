
**Overview**
**MyCurrency** is a Django-based web platform that provides currency exchange rates. It fetches exchange rate data from multiple sources, including **CurrencyBeacon** and a **Mock provider** (for testing). The application follows the **Adapter Design Pattern**, making it flexible to integrate new providers dynamically.

**Features**
- Supports **multiple currency providers**  
- Implements **CRUD operations for Currencies**  
- Fetches **historical exchange rates**  
- Converts amounts between different currencies  
- **Django Rest Framework (DRF)** for a robust API  
- **Database caching** for optimized performance  
- Allows **dynamic provider activation & priority updates**  

**Tech Stack**
- **Backend:** Python 3.11, Django 4+, Django REST Framework
- **External API:** [CurrencyBeacon](https://currencybeacon.com)  
- **Dependencies:** `djangorestframework`, `requests`, `python-decouple`  

---

**Installation & Setup**
**Clone the Repository**
```bash
git clone https://github.com/chaitphani/MyCurrency
cd mycurrency
```

**Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

**Install Dependencies**
```bash
pip install -r requirements.txt
```

**Apply Migrations**
```bash
python manage.py migrate
```

**Create a Superuser**
```bash
python manage.py createsuperuser
```

**Start the Django Server**
```bash
python manage.py runserver
```

---

**API Endpoints**
| **Endpoint**                           | **Method** | **Description** |
|----------------------------------------|-----------|----------------|
| `/currencies/`                         | `GET`     | List all currencies |
| `/currencies/`                         | `POST`    | Create a new currency |
| `/currencies/<currency_code>/`         | `GET`     | Retrieve a specific currency |
| `/currencies/<currency_code>/`         | `PUT`     | Update an existing currency |
| `/currencies/<currency_code>/`         | `DELETE`  | Delete a currency |
| `/currency-rates/`                      | `GET`     | Get currency rates for currency within dates |
| `/convert/`                            | `GET`     | Convert an amount between currencies |

---

**Example API Requests**
**Get All Currencies**
```bash
curl -X GET http://127.0.0.1:8000/currencies/
```
**Response:**
```json
[
    {"id": 1, "code": "USD", "name": "US Dollar", "symbol": "$"},
    {"id": 2, "code": "EUR", "name": "Euro", "symbol": "€"}
]
```

**Convert Currency**
```bash
curl -X GET "http://127.0.0.1:8000/convert/?source_currency=USD&amount=100&exchanged_currency=EUR"
```

**Response:**
```json
{
    "source_currency": "USD",
    "exchanged_currency": "EUR",
    "amount": 100,
    "converted_amount": 91.00,
    "rate": 0.91
}
```

---

**Project Structure**

manage.py
│── mycurrency/                  # Main project directory
|   |── asgi.py
│   │── settings.py
│   │── urls.py
|   |── wsgi.py
exchange/                     # Exchange app
│── migrations/
│── models.py                  # Database models
│── views.py                    # API views
│── urls.py                     # App-specific URLs
│── adapters.py                  # Adapter for API integration
│── services.py                  # Business logic
│── serializers.py               # Serializers
│── admin.py                     # Django admin setup
│── apps.py  
requirements.txt                 # Dependencies
db.sqlite3                       # Default database

