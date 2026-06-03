# Django E‑Store (django-Estore)

A simple **Django 4.2** e-commerce (“E‑Store”) project that demonstrates an MVC-style structure with:
- user registration and authentication,
- product listing (“shop”),
- cart and checkout pages,
- basic order placement,
- media uploads for product images (requires Pillow).

> Repo: `kaggwe-marvin/django-Estore`  
> Main Django project: `cakes24`  
> Main Django app: `bakery24`  
> Default branch: `main`

---

## Tech Stack

- **Python / Django 4.2**
- **SQLite** (development database)
- HTML/CSS/JavaScript (frontend templates/static)
- Media/static handling configured for local development

Language mix (approx.): Python 96.4%, HTML 2%, JS 0.8%, CSS 0.7%.

---

## Project Structure

High-level layout (important parts):

- `cakes24/manage.py` — Django entry point
- `cakes24/cakes24/` — project configuration
  - `settings.py` — Django settings (static/media configured here)
  - `urls.py` — root routes (includes `bakery24.urls`)
- `cakes24/bakery24/` — main application
  - `models.py` — Product, Cart, Order, Review models
  - `views.py` — views for home/signin/shop/checkout/payment/about/cart/comments + cart actions
  - `templates/` — HTML templates
  - `static/` — static assets
- `cakes24/db.sqlite3` — SQLite database file (included in repo)

---

## Features

### Authentication
- **Sign up** is handled on the home page using Django’s `UserCreationForm`.
- **Sign in** uses Django authentication (`authenticate`, `login`).

### Shop / Products
- Products are loaded from the `Product` model and shown on the shop page.

### Cart & Orders (work-in-progress)
There are views for cart operations and order placement, but a few parts may need fixes (see “Known Issues” below).

### Reviews
A simple review flow exists via the `Review` model and a review form in the “About” page.

---

## Data Model (Current)

From `cakes24/bakery24/models.py`:

- **Product**
  - `name`, `description`, `price`, `image`
- **Cart**
  - `user` (FK to Django `User`)
  - `stocks` (Many-to-many to `Product`) *(naming: “stocks”)*
- **Order**
  - `user` (FK)
  - `products` (Many-to-many to `Product`)
  - `total_price`, `date_created`
- **Review**
  - `review` (char field)

---

## Setup & Run (Local Development)

### 1) Clone
```bash
git clone https://github.com/kaggwe-marvin/django-Estore.git
cd django-Estore
```

### 2) Create and activate a virtual environment
```bash
python -m venv .venv
# Windows (PowerShell)
. .venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate
```

### 3) Install dependencies

This repository currently **does not include a `requirements.txt`**, so install at least:

```bash
pip install django==4.2 pillow
```

Why Pillow? The `Product.image` field uses `ImageField`, which requires Pillow.

### 4) Run migrations
From the directory containing `manage.py`:

```bash
cd cakes24
python manage.py migrate
```

### 5) Create an admin user (optional)
```bash
python manage.py createsuperuser
```

### 6) Start the server
```bash
python manage.py runserver
```

Open:
- App: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

---

## Static & Media Files

Configured in `cakes24/cakes24/settings.py`:
- `STATIC_URL = '/static/'`
- `STATICFILES_DIRS` includes `bakery24/static`
- `STATIC_ROOT` is set to a `static` directory at the project base
- Media:
  - `MEDIA_URL = '/media/'`
  - `MEDIA_ROOT` points to a `media` directory at the project base

In development, media is served via `urls.py` when `DEBUG=True`.

---

## Known Issues / TODOs (Recommended Improvements)

These are issues that should be addressed to make the project more robust and production-ready:

1. **Hardcoded Django SECRET_KEY**
   - `SECRET_KEY` is committed in `settings.py`. For production, it should be read from environment variables.

2. **Cart model field naming mismatch**
   - In `models.py`, Cart uses `stocks = ManyToManyField(Product)`, but the views reference `cart.products`.
   - Fix by renaming field to `products` *or* updating the views to use `stocks`.

3. **User-to-cart relation not guaranteed**
   - Views use `request.user.cart`, but the `Cart` model is a `ForeignKey` from `Cart` to `User`.
   - Consider a `OneToOneField(User)` for Cart, or always `get_or_create()` a cart for the user.

4. **`__str__` method indentation/attribute issue**
   - The `__str__` method appears incorrectly placed and references `self.text`, which does not exist (Review uses `review`).
   - Add `__str__` methods inside each model and return valid fields, e.g. `return self.name` for Product.

5. **No `requirements.txt`**
   - Add one to make setup reproducible.

6. **Database committed to repo**
   - `db.sqlite3` is included. Usually you add it to `.gitignore` for real projects.

---

## Contributing

Contributions are welcome:
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Open a pull request

---

## License

No license file is currently specified in this repository. If you intend others to use/modify the code, add a `LICENSE` file (MIT, Apache-2.0, GPL, etc.).

---

## Author / Credits

Maintained by **kaggwe-marvin**.
