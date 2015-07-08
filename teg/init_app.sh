#! /usr/bin/env bash

if [ -f db.sqlite3 ]
then
    echo -e "\n\n- Eliminando base de datos de desarrollo..."
    rm db.sqlite3 
    
fi

Sinconizamos y migramos la BD
echo -e "\n\n- Haciendo las migraciones para la base de datos..."
#/usr/bin/env python2.7 manage.py makemigrations

# Sinconizamos y migramos la BD
echo -e "\n\n- Aplicando las migraciones para la base de datos..."
/usr/bin/env python2.7 manage.py migrate

echo -e "\n\n- Cargando fixtures: Cuentas - RolSgt"
/usr/bin/env python2.7 manage.py loaddata fixtures/cuentas_rolsgt.json

echo -e "\n\n- Cargando fixtures: Cuentas - SgtUsuario"
/usr/bin/env python2.7 manage.py loaddata fixtures/cuentas_sgtusuario.json

echo -e "\n\n- Cargando fixtures: Sgt - Estado"
/usr/bin/env python2.7 manage.py loaddata fixtures/venezuela_estados.json

echo -e "\n\n- Cargando fixtures: Sgt - Municipio"
/usr/bin/env python2.7 manage.py loaddata fixtures/venezuela_municipios.json

echo -e "\n\n- Cargando fixtures: Sgt - TipoInspeccion"
/usr/bin/env python2.7 manage.py loaddata fixtures/sgt_tipoinspeccion.json

echo -e "\n\n- Cargando fixtures: Sgt - Perito"
/usr/bin/env python2.7 manage.py loaddata fixtures/sgt_perito.json

echo -e "\n\n- Cargando fixtures: Sgt - CentroInspeccion"
/usr/bin/env python2.7 manage.py loaddata fixtures/sgt_centroinspeccion.json

echo -e "\n\n- Cargando fixtures: Sgt - Estatus"
/usr/bin/env python2.7 manage.py loaddata fixtures/sgt_estatus.json

echo -e "\n\n- Cargando fixtures: Sgt - TipoRespuesta"
/usr/bin/env python2.7 manage.py loaddata fixtures/sgt_tiporespuesta.json

echo -e "\n\n- Cargando fixtures: Sgt - TipoEncuesta"
/usr/bin/env python2.7 manage.py loaddata fixtures/sgt_tipoencuesta.json

