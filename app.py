from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'clave_secreta_insegura_para_demo'

# MODO DEBUG ACTIVO (Vulnerable para la demo)
app.config['DEBUG'] = True

PRODUCTOS = {
    "1": {"nombre": "Laptop Gamer Pro 15", "precio": 15000, "icono": "💻", "desc": "AMD Ryzen 7, 16GB RAM, RTX 3060."},
    "2": {"nombre": "Smartphone X Ultra", "precio": 8500, "icono": "📱", "desc": "Pantalla OLED 6.7\", 128GB de almacenamiento."},
    "3": {"nombre": "Headset Wireless RGB", "precio": 1200, "icono": "🎧", "desc": "Sonido envolvente 7.1 y cancelación de ruido."},
    "4": {"nombre": "Smart TV 55\" 4K UHD", "precio": 7999, "icono": "📺", "desc": "Resolución 4K con asistente de voz integrado."},
    "5": {"nombre": "Consola Next-Gen Station", "precio": 11500, "icono": "🎮", "desc": "Incluye control inalámbrico y 1TB SSD."},
    "6": {"nombre": "Teclado Mecánico RGB", "precio": 950, "icono": "⌨️", "desc": "Switches mecánicos rojos y estructura de aluminio."},
    "7": {"nombre": "Mouse Gamer Ergonómico", "precio": 650, "icono": "🖱️", "desc": "Sensor óptico de alta precisión ajustable."},
    "8": {"nombre": "Smartwatch Deportivo Pro", "precio": 2300, "icono": "⌚", "desc": "Monitoreo de frecuencia cardíaca y GPS integrado."}
}

@app.route('/')
def index():
    if 'carrito' not in session:
        session['carrito'] = []
    # Capturamos si viene un producto recién agregado en la URL
    added_item = request.args.get('added')
    return render_template('index.html', productos=PRODUCTOS, added_item=added_item)

@app.route('/agregar/<id_prod>', methods=['POST'])
def agregar(id_prod):
    if id_prod in PRODUCTOS:
        producto = PRODUCTOS[id_prod]
        carrito = session.get('carrito', [])
        carrito.append(producto)
        session['carrito'] = carrito
        # Redirigimos pasando el nombre del producto en la URL para la notificación
        return redirect(url_for('index', added=producto['nombre']))
    return redirect(url_for('index'))

# NUEVA RUTA: Eliminar producto del carrito por su índice
@app.route('/eliminar/<int:index>', methods=['POST'])
def eliminar(index):
    carrito = session.get('carrito', [])
    if 0 <= index < len(carrito):
        carrito.pop(index)
        session['carrito'] = carrito
    return redirect(url_for('ver_carrito'))

@app.route('/carrito')
def ver_carrito():
    carrito = session.get('carrito', [])
    total = sum(item['precio'] for item in carrito)
    return render_template('cart.html', carrito=carrito, total=total)



@app.route('/checkout', methods=['POST'])
def checkout():
    # Capturamos lo que llega por POST
    monto_str = request.form.get('total')
    print(f"--- DEBUG BURP / CHECKOUT --- Valor recibido en 'total': {monto_str}")
    
    try:
        monto = float(monto_str)
    except (TypeError, ValueError):
        monto = 0.0

    # VULNERABILIDAD: Si el monto es 0 o menor, truena la app (Simulando el ataque)
    if monto <= 0:
        raise RuntimeError(f"Error crítico en pasarela de pagos SQL: Transacción inválida de ${monto}. Conexión rechazada en db.internal.local:5432.")

    session.pop('carrito', None)
    return render_template('checkout.html', monto=monto)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, threaded=True)