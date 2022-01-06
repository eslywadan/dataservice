from flask import Flask

from home import home_bp
from contact import contact_bp

"""https://towardsdatascience.com/creating-restful-apis-using-flask-and-python-655bad51b24"""

"""https://medium.com/analytics-vidhya/swagger-ui-dashboard-with-flask-restplus-api-7461b3a9a2c8"""


app = Flask(__name__)

app.register_blueprint(home_bp, url_prefix='/home')
app.register_blueprint(contact_bp, url_prefix='/contact')


if __name__ == '__main__':
  app.run(debug=True)