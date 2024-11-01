# E-Commerce Using Django

## Overview
This repository hosts an e-commerce platform built using the Django framework. The platform allows users to browse products, add them to their cart, and make purchases online. It aims to provide a robust solution for small to medium-sized businesses looking to establish an online presence.

## Features
- **User Authentication**: Allows users to register, log in, and manage their accounts.
- **Product Management**: Admins can add, update, and delete products.
- **Cart Functionality**: Users can add items to their cart and view them before checkout.
- **Order Processing**: Supports order creation, payment processing, and order history.
- **Search and Filtering**: Users can search for products and filter results by various criteria like price, category, and brand.
- **Responsive Design**: The site is mobile-friendly and adapts to various screen sizes.

## Tech Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Django, Python
- **Database**: SQLite (default for development), PostgreSQL (recommended for production)
- **Payment Processing**: Stripe API

## Installation

### Prerequisites
- Python 3.x
- pip
- Virtualenv (optional)

### Setting Up a Virtual Environment
```bash
virtualenv venv
source venv/bin/activate  # On Windows use `.\venv\Scripts\activate`
