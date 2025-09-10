from flask import Flask, render_template, request
import math

app = Flask(__name__)

def formatar_com_raiz(valor, casas=2):
    if valor is None:
        return "Não informado"
    n = valor * valor
    arred = round(n)
    if abs(n - arred) < 1e-6:
        k = 1
        m = arred
        i = 2
        while i * i <= m:
            while m % (i * i) == 0:
                k *= i
                m //= i * i
            i += 1
        if m == 1:
            return f"{valor:.{casas}f} (ou {k})"
        else:
            raiz = f"{'' if k == 1 else k}√{m}"
            return f"{valor:.{casas}f} (ou {raiz})"
    return f"{valor:.{casas}f}"

@app.route('/', methods=['GET', 'POST'])
def calcular():
    resultado = {}
    aviso = erro = None

    if request.method == 'POST':
        def to_float(v):
            try:
                return float(v)
            except:
                return None

        a = to_float(request.form.get('lado_a'))
        b = to_float(request.form.get('lado_b'))
        c = to_float(request.form.get('lado_c'))
        angulo_graus = to_float(request.form.get('angulo_x'))

        to_rad = lambda d: d * math.pi / 180

        if c is None and a is not None and b is not None:
            c = math.sqrt(a**2 + b**2)
        if a is None and b is not None and c is not None and c > b:
            a = math.sqrt(c**2 - b**2)
        if b is None and a is not None and c is not None and c > a:
            b = math.sqrt(c**2 - a**2)

        if (angulo_graus is None or angulo_graus == 0) and a is not None and b is not None:
            angulo_graus = math.atan(a / b) * (180 / math.pi)

        if angulo_graus is not None:
            ang = to_rad(angulo_graus)

            if a is None:
                if c is not None:
                    a_by_c = math.sin(ang) * c
                    a = a_by_c
                    if b is not None:
                        a_by_b = math.tan(ang) * b
                        if abs(a_by_c - a_by_b) > 0.1:
                            b_esperado = math.cos(ang) * c
                            aviso = f"Valores incoerentes: com C={c:.2f} e θ={angulo_graus:.2f}°, B esperado ≈ {b_esperado:.2f}."
                elif b is not None:
                    a = math.tan(ang) * b

            if b is None:
                if c is not None:
                    b = math.cos(ang) * c
                elif a is not None:
                    b = a / math.tan(ang)

            if c is None and a is not None:
                c = a / math.sin(ang)
            if c is None and b is not None:
                c = b / math.cos(ang)

        if c is not None and a is not None and b is not None:
            if not (c > a and c > b):
                erro = "A hipotenusa (C) deve ser maior que os catetos (A e B)."

        resultado = {
            "a": formatar_com_raiz(a),
            "b": formatar_com_raiz(b),
            "c": formatar_com_raiz(c),
            "angulo": f"{angulo_graus:.2f}°" if angulo_graus is not None else "Não informado",
            "erro": erro,
            "aviso": aviso
        }

    return render_template("index.html", resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)  # Aqui está a inicialização do servidor Flask
