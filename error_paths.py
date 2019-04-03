# Bottle and Database imports
import bottle
from bottle_utils.flash import message_plugin
from bottle_sqlite import SQLitePlugin
import caribou

# Create Bottle Object
error_app = bottle.Bottle()

# Database Configuration
database_file = 'library_project.db'
migrations_path = 'migrations/'
caribou.upgrade(database_file, migrations_path)

# Install Plugins
error_app.install(message_plugin)
error_app.install(SQLitePlugin(dbfile=database_file, pragma_foreign_keys=True))

# HTML Errors
@error_app.error(404)
def error404(error):
    return bottle.template('page_not_found')

@error_app.error(401)
def error401(error):
    try: 
        bottle.redirect('/', 303)
    except bottle.HTTPResponse as res:
        return res
