from api.views import api_set_value, api_get_value, index

def setup_routes(app):
    app.router.add_get('/', index, name='index')
    app.router.add_get('/api', api_get_value, name='api_get_value')
    app.router.add_post('/api', api_set_value, name='api_set_value')
