```bash
# Install the node modules
cd frontend
npm install

# Install other packages
npm install --save vue-router
npm install bootstrap-vue --save
npm install axios --save

# Run the Frontend
npm run serve

# Run the backend
cd backend
python3 -m venv myenv
source myenv/bin/activate
python app.py
