from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Transaction

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def dashboard():
    transactions = Transaction.query.order_by(Transaction.transaction_date.desc(), Transaction.id.desc()).all()
    income = sum(x.amount for x in transactions if x.kind == "income")
    expense = sum(x.amount for x in transactions if x.kind == "expense")
    balance = income - expense

    categories = {}
    for x in transactions:
        if x.kind == "expense":
            categories[x.category] = categories.get(x.category, 0) + x.amount

    return render_template("index.html", transactions=transactions, income=income,
                           expense=expense, balance=balance, categories=categories)

@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        try:
            amount = float(request.form["amount"])
            if amount <= 0:
                raise ValueError
        except (ValueError, KeyError):
            flash("Enter a valid positive amount.", "error")
            return render_template("form.html")

        kind = request.form.get("kind")
        if kind not in {"income", "expense"}:
            flash("Invalid transaction type.", "error")
            return render_template("form.html")

        item = Transaction(
            title=request.form.get("title", "").strip(),
            amount=amount,
            kind=kind,
            category=request.form.get("category", "Other"),
            transaction_date=date.fromisoformat(request.form.get("transaction_date"))
        )
        if not item.title:
            flash("Title is required.", "error")
            return render_template("form.html")

        db.session.add(item)
        db.session.commit()
        return redirect(url_for("dashboard"))

    return render_template("form.html")

@app.post("/delete/<int:item_id>")
def delete_transaction(item_id):
    item = Transaction.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)
