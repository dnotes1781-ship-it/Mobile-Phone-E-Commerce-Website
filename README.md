**Project Overview**

This repository contains an e-commerce web application built with Django for the backend and server-side rendering, and Bootstrap + vanilla JavaScript for the frontend. The README below explains the high-level architecture, how the chatbot integration works, the primary backend and frontend responsibilities, the tech stack, and important functions to know for maintenance and future development.

**Chatbot Workflow**:
- **Purpose**: The chatbot provides conversational assistance to users (product discovery, support, FAQs, and wire-up actions such as adding to cart or navigating to product pages).
- **Flow**: User interacts via chat widget → frontend captures input and sends to the chatbot backend endpoint → backend chatbot controller processes the message and either (a) responds with text+structured actions or (b) calls internal APIs (search, product details, cart) to fetch data → frontend renders reply and actionable buttons.
- **Key Components**:
  - **Chat UI (frontend)**: captures messages, displays response cards, handles button clicks (e.g., "View product", "Add to cart"). See [store/templates/base.html](store/templates/base.html) for the site-wide layout and where the chat widget is likely mounted.
  - **Chat endpoint (backend)**: a Django view (or DRF endpoint) that accepts chat messages, performs NLP / intent classification (could use a cloud LLM or local rule-based logic), and returns structured JSON responses with optional actions.
  - **Action handlers**: small backend helpers that map chatbot actions to site APIs (e.g., lookup product by id, create cart item). These are thin wrappers around existing store views and models.

**Backend (Django)**
- **Tech stack**: Python, Django, Django ORM, SQLite (db.sqlite3 in repo), server-side templates, management commands.
- **Important directories**:
  - `store/models/` — domain models: `product.py`, `customer.py`, `orders.py`, etc.
  - `store/views/` — page controllers for the web routes (product listing, detail, cart, checkout).
  - `store/templates/` — Django HTML templates (server-rendered). The hero carousel is in `store/templates/index.html`.
  - `store/management/commands/` — one-off scripts to seed/adjust DB objects (e.g., `setup_iphone_bundle.py`).
- **Key functions & responsibilities**:
  - `Product` model: stores name, price, description, images, and relationships like `compatible_accessories`.
  - Views that render product lists and details: fetch products, annotate with `is_in_cart`, and supply template context such as `categories`, `products`, and (previously) `storage_options` / `color_options`.
  - Cart helpers (templatetags / middleware): session-backed cart utilities that track items and quantities.
  - Management commands: scripts to create or update seed data.

**Frontend (Templates + JS)**
- **Tech stack**: Bootstrap 5, vanilla JavaScript (small inline scripts), static assets under `static/` (CSS, JS, images).
- **Key UI areas**:
  - `index.html`: hero carousel (now updated with Unsplash images), categories sidebar, product grid.
  - `detail.html`: product detail page, add-to-cart flow, specifications accordion.
  - `cart.html` / checkout pages: user interactions to add/remove and purchase products.
- **Important JS behaviors**:
  - Range price slider: implemented inline on `index.html` to filter products by price.
  - AJAX cart forms: forms that post to the cart action without leaving the page (look for `.ajax-cart-form` use in templates).
  - Carousel: Bootstrap carousel markup lives in `index.html`. Images are responsive and lazy-loaded.

**How to Extend the Chatbot & Integrations**
- To add new intents that trigger site actions (e.g., "show accessories for iPhone 13") implement a backend intent mapping that returns structured responses with an `action` field. The frontend should interpret actions and call appropriate endpoints (product listing, product detail, add-to-cart).
- Example response shape from chat endpoint:

```json
{
  "text": "Here are compatible accessories for iPhone 13:",
  "cards": [ { "title": "iPhone 13 Cover", "action": { "type": "open_product", "id": 123 } } ],
  "actions": [ {"type":"add_to_cart","product_id":123} ]
}
```

**Deployment & Local Testing**
- Install dependencies: `pip install -r requirements.txt`.
- Apply migrations and create a superuser if needed:
  - `python manage.py migrate`
  - `python manage.py createsuperuser`
- Run dev server: `python manage.py runserver` and open `http://127.0.0.1:8000/`.

**Files I changed**
- Carousel updated: [store/templates/index.html](store/templates/index.html)
- New file: `README.md` (this file)

**Notes & Next Steps**
- I added 7 Unsplash HD images directly via CDN URLs in the carousel; if you prefer local assets, I can download and place them under `static/images/` and update the template to use local paths.
- If you'd like the chatbot endpoint scaffolded (Django view + minimal frontend integration), I can add a simple chat view and a tiny widget to start handling requests and demonstrating actions.

---

If you'd like I can now (pick one):
- run the dev server and verify the carousel visually,
- download the Unsplash images to `static/images/` and update paths,
- scaffold a minimal chatbot endpoint and UI integration.# E-Commerce Application

## Project Overview
This is a Django-based e-commerce web application for selling cameras, lenses, and photography accessories.

## Current Implementation

### Technology Stack
- **Framework**: Django 3.0.6
- **Database**: SQLite3
- **PDF Generation**: ReportLab
- **Frontend**: HTML templates with Django template engine
- **Static Files**: CSS, JavaScript, Images

### Features Implemented

#### 1. **User Management**
- User registration and signup (`store/views/signup.py`)
- User login with password hashing (`store/views/login.py`)
- User profile management (`store/views/userprofile.py`)
- Password validation using Django's built-in validators
- Session-based authentication

#### 2. **Product Catalog**
- Product listing and display (`store/views/home.py`, `store/views/product.py`)
- Category-based product organization (`store/models/category.py`)
- Product search functionality (`store/views/search.py`, `store/views/search_api.py`)
- Product filtering by price range (Min/Max)
- Lens-specific product views (`store/views/lenses.py`)

#### 3. **Shopping & Orders**
- Shopping cart functionality
- Order placement and management (`store/views/orders.py`)
- Order history viewing for customers
- Payment processing interface (`store/views/payment.py`)
- Order success confirmation (`store/views/order_success.py`)

#### 4. **Invoice & PDF Generation**
- PDF invoice generation using ReportLab (`store/views/orders.py`)
- Invoice viewing functionality (`store/views/invoice.py`)
- Downloadable order receipts in PDF format

#### 5. **Media Management**
- Product image uploads and storage
- Media files served from `/image/download/` URL
- Static files organized in `static/` directory

#### 6. **Email Configuration**
- Console backend for development (emails print to terminal)
- Email infrastructure ready for production deployment

### Project Structure
```
Ecommerce/
├── Eshop/                  # Main Django project configuration
│   ├── settings.py         # Project settings
│   ├── urls.py             # URL routing
│   ├── wsgi.py             # WSGI configuration
│   └── asgi.py             # ASGI configuration
├── store/                  # Main application
│   ├── models/             # Data models (Customer, Product, Category, Order)
│   ├── views/              # View handlers
│   ├── templates/          # HTML templates
│   ├── middlewares/        # Custom middleware (auth)
│   ├── templatetags/       # Custom template tags
│   ├── migrations/         # Database migrations
│   └── static/             # App-specific static files
├── static/                 # Global static files (CSS, JS, images)
├── uploads/                # User-uploaded media files
├── db.sqlite3              # SQLite database
└── manage.py               # Django management script
```

### Models
1. **Customer** - User/customer information
2. **Product** - Product details (name, price, description, images)
3. **Category** - Product categories
4. **Order** - Order information and order history

### Key Django Apps & Middleware
- `django.contrib.admin` - Admin panel
- `django.contrib.auth` - Authentication system
- `django.contrib.sessions` - Session management
- `django.contrib.messages` - Messaging framework
- Custom auth middleware for protected views

### Security Features
- CSRF protection enabled
- Password hashing with Django's built-in hashers
- Session-based authentication
- Secure password validators (length, similarity, common passwords, numeric)

## Setup & Installation

### Prerequisites
- Python 3.6+
- pip package manager

### Installation Steps
1. Open the project in IDE
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser (admin):
   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```
7. Access the application at `http://127.0.0.1:8000/`

## Development Notes
- **DEBUG mode**: Currently set to `True` (should be `False` in production)
- **SECRET_KEY**: Should be changed and kept secure in production
- **ALLOWED_HOSTS**: Empty list (needs to be configured for production)
- **Database**: Using SQLite for development (consider PostgreSQL/MySQL for production)

## Future Enhancements
- Payment gateway integration (Stripe, PayPal, etc.)
- Email notifications for orders
- Advanced product filtering and sorting
- Product reviews and ratings
- Wishlist functionality
- Coupon/discount system
- Admin dashboard for inventory management
