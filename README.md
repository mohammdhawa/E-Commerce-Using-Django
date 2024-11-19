# Django E-Commerce Platform

Welcome to the Django E-Commerce Platform! This project is a comprehensive e-commerce solution designed for scalability and ease of use. Built with Django, it includes all essential features needed for a robust online store such as product management, user authentication, a shopping cart, and order processing.

## Key Features

### User Authentication
- **Secure Login and Registration**: Built-in Django authentication with added security features like password hashing.
- **Profile Management**: Users can manage their profiles, view their order history, and save payment and shipping information.

### Product Management
- **Admin Interface**: A powerful, intuitive admin panel for managing inventory. Admins can add, update, and remove products, set prices, and manage stock levels.
- **Product Variations**: Supports multiple variations per product (such as size or color).

### Shopping Cart
- **Session-Based Cart System**: Temporary storage for users' shopping carts using Django's session framework, ensuring data persists even when the browser is closed.
- **Product Quantity Adjustment**: Users can adjust the quantities of items in their cart and see updates to their totals instantly.

### Order Processing
- **Checkout Process**: Integration of a checkout process that handles personal information securely, calculates costs, and processes payments.
- **Order Status Tracking**: After an order is placed, users can track the status of their orders through their user dashboard.

### Search Functionality
- **Product Search**: Allows users to search for products by keywords or categories.
- **Advanced Filtering**: Filter products by various parameters like price, brand, or rating.

## Technology Stack

- **Django**: Serves as the backbone, providing the necessary MVC structure for this application.
- **PostgreSQL**: A robust and scalable database solution suited for handling the demands of a high-traffic online store.
- **Bootstrap**: For styling and responsive design, making the website accessible on various devices.
- **JavaScript**: Enhances frontend interactions for a smoother user experience.
- **Redis**: Acts as a message broker for Celery and stores session data for enhanced performance.
- **Celery**: Handles asynchronous task queue/job queue based on distributed message passing.

## Getting Started

### Prerequisites

Ensure you have Python and pip installed on your machine:

- Python (3.6 or higher)
- pip (latest version)

### Installation

Follow these steps to get your development environment set up:

1. **Clone the repository**:
   ```bash
    1. Step:
    git clone https://github.com/mohammdhawa/E-Commerce-Using-Django.git
    
    2. Step:
    cd E-Commerce-Using-Django
    
    3. Step:
    python -m venv venv
    
    4. Step:
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    
    5. Step:
    pip install -r requirements.txt
    
    6. Step: Configure the PostgreSQL and Redis:
    Ensure PostgreSQL is running and create a new database.
    Ensure Redis is running on its default port.
    Update settings.py with the correct database and Redis configurations.
    
    7. Step Run migrations:
    python manage.py migrate
   
    8. Step: Set up Celery:
    Make sure Redis is configured as the Celery broker in settings.py.
    Run Celery worker: celery -A proj worker -l info
    
    9. Step: Create a superuser:
    python manage.py createsuperuser
    
    10. Step: Start the development server
    python manage.py runserver

