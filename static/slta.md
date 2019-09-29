# SLTA

El Sistema de gestión Logística de Transporte Automotriz (SLTA) es una solución confiable para contabilidad y
trazabilidad logística en el mercado automobiliario, con un enfoque en la escalabilidad y consistencia de la estructura
interna de datos.

## Funcionalidades del producto

### Gestión de lugares

El sistema administrará un conjunto de lugares (puertos, patios, etc) por donde pasarán los vehículos.
Estos tendrán zonas y subzonas, en los cuales se posicionarán los vehículos

### Gestión de informes

El sistema le permitirá ingresar informes de estado de los vehículos

### Gestión de lotes

El sistema le permitirá administrar lotes en los cuales se trasladen vehículos

### Extensibilidad

La base de datos _Informix_ del SLTA está modelada de manera extensible, de tal manera que se pueden implementar nuevas
clases de lugares y medios de transporte simplemente manipulando un par de tablas.

Vea el [blog](blog?tags=sql) para ejemplos de esto.

### Irredundancia e inmutabilidad parcial de datos

En nuestra base de datos intentamos no eliminar información; aquello que se marca como erróneo (informes, lotes
cancelados, etc) no se elimina sino que se marca como invalidado por otro acontecimiento en la base de datos (informe
que lo remplaza, lote al que se reasigna, baja del sistema, etc) para asegurar la transparencia acerca del estado del
vehículo.