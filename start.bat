start "Vue App" cmd /c "cd frontend_vue3 && npm run dev"

start "FastAPI App" cmd /c "cd backend_fastapi & .\venv\Scripts\activate & uvicorn app.main:app --reload"

echo Both servers are starting...