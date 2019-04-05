# Bottle and Database imports
import bottle
from bottle_utils.flash import message_plugin
from bottle_sqlite import SQLitePlugin
import caribou

# All Paths
import paths.api_paths as js_request_paths
import paths.general_paths as general_paths
import paths.user_paths as user_paths
import paths.librarian_paths as librarian_paths

from config import database_file, HOST

# Create Bottle Object
app = bottle.Bottle()

# Database Configuration
migrations_path = 'migrations/'
caribou.upgrade(database_file, migrations_path)

# Install Plugins
app.install(message_plugin)
app.install(SQLitePlugin(dbfile=database_file, pragma_foreign_keys=True))

# HTML Errors
@app.error(404)
def error404(error):
    return bottle.template('visitor_pages/page_not_found')

@app.error(401)
def error401(error):
    print ("ERROR")
    try: 
        bottle.redirect('/', 303)
    except bottle.HTTPResponse as res:
        return res



# App Path Merges
app.merge(js_request_paths.request_app)
app.merge(general_paths.general_app)
app.merge(user_paths.user_app)
app.merge(librarian_paths.librarian_app)


app.run(host=HOST, port=8080, debug=True)
