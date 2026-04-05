# 📦 Finance Backend Submission

---

## 🔗 GitHub Repository URL
https://github.com/gitberhandling/finance_banking

Provide the full URL to your public GitHub repository containing the project source code.

---

## 🌐 Live Demo / API Documentation URL
https://your-api.onrender.com/docs

If deployed, this link provides access to the live API documentation (Swagger UI). Alternatively, local docs are available at:
http://localhost:8000/docs

---

## 🛠 Primary Framework or Library Used
**Other: FastAPI (Python)**

---

## ✅ Features Implemented

- [x] User and Role Management  
- [x] Financial Records CRUD  
- [x] Record Filtering (by date, category, type)  
- [x] Dashboard Summary APIs (totals, trends)  
- [x] Role-Based Access Control  
- [x] Input Validation and Error Handling  
- [x] Data Persistence (PostgreSQL)  

---

## 🧠 Technical Decisions and Trade-offs

FastAPI was chosen as the backend framework due to its high performance, built-in support for asynchronous operations, and automatic API documentation via Swagger UI. It allows rapid development while maintaining clean and efficient code.

PostgreSQL was selected as the database because it is reliable, scalable, and well-suited for structured financial data. It also supports complex queries required for analytics and aggregation.

SQLAlchemy was used as the ORM to abstract database interactions and prevent SQL injection while maintaining flexibility and control over queries.

JWT (JSON Web Tokens) was implemented for authentication to ensure a stateless and scalable system. Role-based access control is enforced using FastAPI dependency injection, making the authorization logic clean and reusable.

The application follows a layered architecture:
API Layer → Service Layer → Database Layer

---

## 📝 Additional Notes

### Setup Instructions
1. Clone the repository  
2. Create a virtual environment  
3. Install dependencies:
   pip install -r requirements.txt  
4. Configure PostgreSQL database  
5. Run the server:
   uvicorn app.main:app --reload  
6. Access API docs:
   http://localhost:8000/docs  

---

### Summary
This project demonstrates backend design, API structuring, and role-based access control using FastAPI.
