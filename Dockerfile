FROM streamlit/streamlit:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install -r requirements.txt

# Copy the entire current directory into the container
COPY . .

# Expose port 8501 to the outside world
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py"]