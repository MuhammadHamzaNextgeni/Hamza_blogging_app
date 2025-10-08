# Use official Python image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy only requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Expose the default Django port
EXPOSE 8000

# Set environment variables (you can pass your .env separately)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Command to run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
