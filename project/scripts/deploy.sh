#!/bin/bash

# scripts/deploy.sh

# Update and upgrade the system
sudo apt update && sudo apt upgrade -y

# Install Python 3.9 and pip
sudo apt install -y python3.9 python3.9-venv python3-pip

# Install Git
sudo apt install -y git

# Clone the repository (replace with your repository URL)
git clone https://github.com/yourusername/your-repo.git
cd your-repo

# Set up virtual environment
python3.9 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Set up environment variables
# It's recommended to use a .env file or export variables securely
echo "Setting up environment variables..."
export DATABASE_URL="postgresql://user:password@localhost:5432/chatbot_db"
export AWS_ACCESS_KEY_ID="your_aws_access_key"
export AWS_SECRET_ACCESS_KEY="your_aws_secret_key"
export AWS_S3_BUCKET_NAME="your_s3_bucket"
export AWS_REGION="your_aws_region"
export GROQ_API_KEY="your_groq_api_key"
export GROQ_API_URL="https://api.groq.com/v1/query"
export SECRET_KEY="your_secret_key"

# Run database migrations
# Assuming you have alembic or similar setup
# Example with SQLAlchemy's Base metadata
python
```

```python
# Run the following in Python shell to create tables
from app.database import engine
from app.models import user, chatbot, document, conversation

user.Base.metadata.create_all(bind=engine)
chatbot.Base.metadata.create_all(bind=engine)
document.Base.metadata.create_all(bind=engine)
conversation.Base.metadata.create_all(bind=engine)
exit()
```

**Continue `deploy.sh`:**

```bash
# Continue deploy.sh

# Start the FastAPI application using gunicorn and uvicorn workers
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 &