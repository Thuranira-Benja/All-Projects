FROM python:3.9-slim-buster
WORKDIR /ml_app
COPY ./ml_services/requirements.txt /ml_app/
RUN pip install --no-cache-dir -r requirements.txt
COPY ./ml_services/ /ml_app/
# You would also copy your model files (.pkl, .h5) here
# COPY ./ml_services/models/ /ml_app/models/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]