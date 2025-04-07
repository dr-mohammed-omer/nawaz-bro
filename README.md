# Hyderabad Property Deals Website

A modern, responsive real estate website for property listings in Hyderabad, featuring user authentication with SQLite database integration.

## Features

- Responsive design that works on mobile, tablet, and desktop devices
- Property listings with detailed property pages
- User authentication system (login/register)
- User dashboard for saved properties and inquiries
- SQLite database integration for user data
- Contact forms and newsletter subscription
- Modern UI with animations and interactive elements

## Project Structure

```
project/
├── index_new.html          # Home page
├── property1_new.html      # Property detail page 1
├── property2.html          # Property detail page 2
├── property3.html          # Property detail page 3
├── property4.html          # Property detail page 4
├── login.html              # Login page
├── register.html           # Registration page
├── dashboard.html          # User dashboard
├── db_setup.py             # Database setup script
├── login.py                # Login handler
├── register.py             # Registration handler
└── db/                     # Database directory
    └── property_deals.db   # SQLite database
```

## Setup Instructions

### Prerequisites

- Python 3.6 or higher
- Web server with CGI support (like Apache with mod_cgi enabled)

### Database Setup

1. Run the database setup script to create the SQLite database and tables:

```bash
python db_setup.py
```

This will create a `db` directory with the SQLite database file and populate it with sample data.

The database will be created in a `db` folder in the same directory as the script. The Python scripts use absolute paths to ensure they can find the database regardless of the current working directory.

### Web Server Configuration

#### For Apache:

1. Copy all files to your web server's document root (e.g., `/var/www/html/`)
2. Make sure Python scripts are executable:

```bash
chmod +x login.py register.py
```

3. Configure Apache to handle CGI scripts:

```apache
<Directory /var/www/html>
    Options +ExecCGI
    AddHandler cgi-script .py
</Directory>
```

4. Restart Apache:

```bash
sudo service apache2 restart
```

#### For Local Testing:

You can use Python's built-in HTTP server for testing:

```bash
python -m http.server
```

Then access the site at `http://localhost:8000/index_new.html`

Note: For the Python CGI scripts to work with the built-in server, you'll need to set up a proper CGI server.

## User Accounts

The database is pre-populated with the following user accounts for testing:

| Username    | Password    |
|-------------|-------------|
| admin       | admin123    |
| john_doe    | password123 |
| jane_smith  | password456 |

## Development Notes

- All CSS and JavaScript are embedded directly in the HTML files for simplicity
- The site uses Font Awesome icons from a CDN
- The login system uses localStorage/sessionStorage for client-side authentication in the demo
- In a production environment, you would implement proper server-side authentication

## Future Enhancements

- Property search functionality
- User profile management
- Property listing submission for agents
- Advanced filtering options
- Map integration for property locations
- Payment gateway integration for premium listings

## License

This project is licensed under the MIT License - see the LICENSE file for details.