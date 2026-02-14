# app/error_handlers.py
from flask import render_template

def register_error_handlers(app):
    @app.errorhandler(401)
    def e401(error):
        return render_template("erro.html"), 401

    @app.errorhandler(403)
    def e403(error):
        return render_template("erro.html"), 403

    @app.errorhandler(404)
    def e404(error):
        return render_template("erro.html"), 404

    @app.errorhandler(408)
    def e408(error):
        return render_template("erro.html"), 408

    @app.errorhandler(429)
    def e429(error):
        return render_template("erro.html"), 429

    @app.errorhandler(500)
    def e500(error):
        return render_template("erro.html"), 500

    @app.errorhandler(503)
    def e503(error):
        return render_template("erro.html"), 503
