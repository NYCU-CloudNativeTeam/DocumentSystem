from controller.app import create_app


# this is example for unittest
# intergration pytest with Flask test client
def test_root_url():
    app = create_app()
    with app.test_client() as test_client:
        response = test_client.get('/api/auth/')
        assert response.status_code == 200