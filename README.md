# Full-Stack Flask App with SQL Server & MongoDB

A robust full-stack web application built with Python and Flask, demonstrating **Polyglot Persistence** by integrating both a relational database (SQL Server) for core application data and a NoSQL database (MongoDB) for system audit logs.

## 🚀 Features

- **User Management (SQL Server):** Add, view, and delete user records with automatic ID resetting (`TRUNCATE`).
- **Activity Logging (MongoDB):** Automatically tracks and logs user creation events in real-time.
- **Data Cleanup:** Dedicated endpoints to clear user records and wipe logs independently.
- **Robust Error Handling:** Built-in exception management for database connection drops and operational errors.

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Relational Database:** SQL Server (`pyodbc`)
- **NoSQL Database:** MongoDB (`pymongo`)
- **Frontend:** HTML5, Jinja2 Templates

## ⚙️ Prerequisites & Setup

Make sure you have Python 3.10+ and the required database instances running locally.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ronelkayam/flask-fullstack-sql-mongo.git](https://github.com/ronelkayam/flask-fullstack-sql-mongo.git)
   cd flask-fullstack-sql-mongo