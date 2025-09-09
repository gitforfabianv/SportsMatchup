### Using npm (Without Docker)

```bash
# Move to matchups dir
cd matchups

# Install dependencies
npm install

# Run tests
npm test

# Run the app locally
npm run dev

# Backend Setup (be sure to have Python 3.13 installed)
# Move to backend dir 
cd backend 

# Activate virtual environment 
source venv/bin/activate 

# Install Flask and other requirements 
pip3 install -r requirements.txt 

# Run flask locally 
flask run --host=0.0.0.0 --port=5000"
```