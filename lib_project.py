# Bottle and Database imports
import bottle
from bottle_utils.flash import message_plugin
from bottle_sqlite import SQLitePlugin
import caribou

# All Paths
import error_paths
import js_request_paths
import general_paths
import user_paths
import librarian_paths

# Create Bottle Object
app = bottle.Bottle()

# Database Configuration
database_file = 'library_project.db'
migrations_path = 'migrations/'
caribou.upgrade(database_file, migrations_path)

# Install Plugins
app.install(message_plugin)
app.install(SQLitePlugin(dbfile=database_file, pragma_foreign_keys=True))

# App Path Merges
app.merge(error_paths.error_app)
app.merge(js_request_paths.request_app)
app.merge(general_paths.general_app)
app.merge(user_paths.user_app)
app.merge(librarian_paths.librarian_app)


app.run(host='localhost', port=8080, debug=True)
