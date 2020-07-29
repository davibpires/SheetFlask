from flask import Flask


app = Flask(__name__)
app.config.from_object('config.BaseConfig')


from sheet import excel, image


app.register_blueprint(excel.bp)
app.register_blueprint(image.bp)
