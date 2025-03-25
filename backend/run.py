from src.family_cloud_api import create_app

if __name__ == "__main__":
    family_cloud_app = create_app()
    family_cloud_app.run(debug=True)
