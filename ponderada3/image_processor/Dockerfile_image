# Use the official Python image
FROM python 

# Set the working directory in the container
WORKDIR /app

# Install project dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Command to run the application
CMD ["uvicorn", "image_processing:app", "--host", "0.0.0.0", "--port", "8001"]