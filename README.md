Dataset para análisis correlación entre la valoración del bitcoin y valores NASDAQ
    "El caso al que pretendemos dar respuesta trata de generar un set de datos que permita, posteriormente, entrenar algún modelo estadístico para evaluar si un subconjunto de valores bursátiles de empresas tecnológicas cotizadas mantienen correlación con la valoración del Bitcoin (BTC).  "

1- Diseño del prototipo de producto
    Partiendo de que el objetivo es proveer de un buen producto para su posterior análisis, el requisito principal que este impone es básicamente el formato. En este caso, una tabla con variables predictoras, variable objetivo y con un registro para cada instancia de la unidad observacional a tratar. Vamos a intentar mapear estos requisitos formales a nuestro caso:

Unidad observacional

Cada registro de nuestra tabla corresponderá a un día en el cual se tomará una muestra de la valoración de cada empresa en NASDAQ y el valor del BTC.
2025-04-01 | `... variables predictoras ...` | `variable objetivo`
Por lo tanto, la `columna índice` será el propio día en el que se tome la muestra.

Variables predictoras

En este caso, será información relacionada con la valoración de las empresas del NASDAQ del estudio durante el día del muestreo. Para cada empresa cotizada se quiere obtener:
    - Valoración al cierre de la jornada,
    - Diferencia entre apertura y cierre,
    - Tendencia de la jornada,
    - Rango del día

Variable objetivo
La variable objetivo en este caso será el valor del Bitcoin en el momento de la consulta.

2- Extracción
¿De dónde obtenemos los datos?
Existen varias fuentes de datos disponibles para este tipo de valores. Sin embargo, hemos elegido los siguientes:
Para los valores de las empresas a consultar en NASDAQ
En este caso, una de las fuentes más usadas en Yahoo Finance. Para presentar una nueva tipología de fuentes de datos, presentaremos `yfinance`, una librería que hace de *wrapper* para Python de la API de Yahoo Finance.
Este tipo de librerías nos facilitan mucho el trabajar con APIs puesto que implementan con clases y métodos el tipo de interacciones que solemos hacer. Otro ejemplo de este tipo podría ser `tweepy`, que permite interaccionar con la API de Twitter.

Para los valores de BTC
Usaremos la API REST \"directa\" en este caso de coinbase.

¿Con qué frecuencia obtenemos los datos?
Las valoraciones de BTC se van actualizando de forma continuada, sin embargo, NASDAQ tiene un calendario y horario para operar. En este caso, nos interesa obtener los datos de las jornadas en que se haya operado en NASDAQ una vez estas hayan finalizado (para poder obtener todas las variables que nos interesan)
    *Fuente*: http://www.nasdaqtrader.com/trader.aspx?id=calendar

¿Qué partición consultamos?

Para los valores de las empresas a consultar en NASDAQ 
Vemos si `yfinance` permite:
    - consultar datos para una empresa determinada
    - obtener los datos solamente del último día de operación
    - ver sobre qué variables nos devuelve los datos

Vemos si podemos consultar para solo una empresa y el último día:
Concluimos lo siguiente:
    - `yfinance` permite consultas por índice bursátil, por lo que vamos a trabajar con un dataframe por empresa como fuente de datos (lista de dataframes). Esto nos obliga a agregarlas para obtener el tablón que deseamos.
    - la librería permite obtener una partición bastante próxima a nuestro producto deseado.
    - Existen variables que habrá ingeniar a partir de las existentes.

Para los valores de BTC
El enfoque de la API de Coinbase es distinto, puesto que obtiene el valor del BTC en ese preciso momento. Por lo tanto, vamos a tener que consultarlo en un momento determinado y obtener su valor.
{'data': {'base': 'BTC', 'currency': 'USD', 'amount': '61618.41'}}

Ingeniería de características

Realizamos la ingeniería de variables previa al agregado de forma que el conjunto pueda programarse más eficientemente,
Como hemos visto las variables que esperamos obtener son básicamente relacionadas con los índices bursátiles y el valor del BTC
 Entonces, habría que evalaur cuales de estas vienen directamente obtenidas de las fuentes de datos y cuales hay que ingeniar a partir de las otras. Vamos entonces a examinar qué variables pueden ser directamente obtenibles desde las fuentes de datos y qué variables hay que ingeniar. Para las que caigan en esa categoría, vamos a estudiar cómo generarlas.
    variables índices bursátiles
    - [indicebursatil]_cierre: obtenible directamente a través de la consulta a `yfinance`. Campo `Close`.
    - [indicebursatil]_dif: hay que ingenierla desde el dataframe obtenido con `yfinance`: `Open` - `Close`.
    - [indicebursatil]_tend: hay que ingeniarla. Podemos aprovechar el resultado de la variable superior y simplemente evaluar su símbolo.
    - [indicebursatil]_rango: hay que ingeniarla desde el dataframe obtenido con `yfinance`: `High` - `Low`.
    - valor_btc: obtenible directamente a través del fichero JSON de respuesta de la API de Coinbase.

Agregado
De la extracción e ingeniería de características, vamos a obtener lo siguiente:
    - Un listado de dataframes con la información bursátil de cada índice.
    - Un dataframe con el valor del BTC.
Para agregarlos, deberemos concatenar los dataframes. Si el valor de BTC podemos formatearlo a dataframe, nos será más fácil de llevarlo a cabo puesto que usaremos solo ese tipo y nos serviremos de métodos de Pandas.
Con todo esto, deberiamos poder generar nuestro tablón final.

  4- Load
    Sólamente nos quedará resolver dónde guardamos el tablón.
    La aproximación que propongo en el caso es guardarlo en una base de datos cloud basada en SQL.
    De tal forma tendremos los siguientes beneficios:
•	Datos de forma consistente por usar un RDBMS.
•	Flexibilidad en el tamaño de nuestro data.
