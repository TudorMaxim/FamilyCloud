from src.family_cloud_api import create_app

family_cloud_app = create_app()

from src.family_cloud_api.celery import celery

if __name__ == "__main__":
    family_cloud_app.run(debug=True)
