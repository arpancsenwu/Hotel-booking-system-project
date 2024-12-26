from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from datetime import datetime

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = 'your_secret_key_here'

# Database connection
db_config = {
    'host': 'localhost',
    'user': 'root', # Replace with your MySQL username
    'password': '', # Replace with your MySQL password
    'database': 'hotel_management'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Check-In
@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        mobile_no = request.form['mobile_no']
        room_no = request.form['room_no']
        price = request.form['price']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO guests (name, address, mobile_no, room_no, price)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, address, mobile_no, room_no, price))
            conn.commit()
            flash("Guest checked in successfully!", "success")
        except mysql.connector.Error as err:
            flash(f"Error: {err}", "danger")
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('index'))

    return render_template('checkin.html')

# Check-Out
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        room_no = request.form['room_no']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Mark checkout
            query = """
                UPDATE guests
                SET checkout_date = %s
                WHERE room_no = %s AND checkout_date IS NULL
            """
            cursor.execute(query, (datetime.now(), room_no))
            conn.commit()

            if cursor.rowcount == 0:
                flash("No active guest found for this room.", "danger")
            else:
                flash("Guest checked out successfully!", "success")
        except mysql.connector.Error as err:
            flash(f"Error: {err}", "danger")
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('index'))

    return render_template('checkout.html')

# Guest List
@app.route('/guestlist')
def guestlist():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM guests WHERE checkout_date IS NULL")
        guests = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Error: {err}", "danger")
        guests = []
    finally:
        cursor.close()
        conn.close()

    return render_template('guestlist.html', guests=guests)

# Guest Info
@app.route('/guestinfo', methods=['GET', 'POST'])
def guestinfo():
    guest = None
    if request.method == 'POST':
        room_no = request.form['room_no']

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM guests WHERE room_no = %s", (room_no,))
            guest = cursor.fetchone()

            if not guest:
                flash(f"No guest found in room {room_no}.", "danger")
        except mysql.connector.Error as err:
            flash(f"Error: {err}", "danger")
        finally:
            cursor.close()
            conn.close()

    return render_template('guestinfo.html', guest=guest)

if __name__ == '__main__':
    app.run(debug=True)
