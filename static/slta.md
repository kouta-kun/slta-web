# SLTA

El Sistema de gestión Logística de Transporte Automotriz (SLTA) es una solución confiable para contabilidad y
trazabilidad logística en el mercado automobiliario, con un enfoque en la escalabilidad y consistencia de la estructura
interna de datos.

## Capacidades del producto

### Extensibilidad

La base de datos _Informix_ del SLTA está modelada de manera extensible, de tal manera que se pueden implementar nuevas
clases de lugares y medios de transporte simplemente manipulando un par de tablas. Por ejemplo, es posible agregar
una ciudad flotante mecánica simplemente ejecutando
```sql
insert into TipoTransporte (nombre) values ('Aerobote');
insert into lugar(nombre, capacidad, geox, geoy, usuariocreador, fecharegistro, tipo) values ('Patio de Isla del cielo',
20, -33,-51, 1, "1998-03-01 12:00:00", "Patio");
insert into habilitado(idlugar, idtipo) values ((select idlugar from lugar where nombre='Patio de Isla del cielo'),
                                                (select idtipo from TipoTransporte where nombre='Aerobote'));
insert into habilitado(idlugar, idtipo) values ((select idlugar from lugar where nombre='Puerto de Montevideo'),
 (select idtipo from TipoTransporte where nombre='Aerobote'));
```
y agregando vehículos de tipo Aerobote.

### Irredundancia e inmutabilidad parcial de datos

En nuestra base de datos intentamos no eliminar información; aquello que se marca como erróneo (informes, lotes
cancelados, etc) no se elimina sino que se marca como invalidado por otro acontecimiento en la base de datos (informe
que lo remplaza, lote al que se reasigna, baja del sistema, etc) para asegurar la transparencia acerca del estado del
vehículo.