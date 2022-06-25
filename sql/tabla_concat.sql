CREATE TABLE IF NOT EXISTS public.tabla_concat
(
"cod_localidad" integer NOT NULL,
"id_provincia"   integer NOT NULL,
"id_departamento" integer NOT NULL,
"categoría"  character varying(50)[] NOT NULL,
"provincia"  character varying(50)[] NOT NULL,
"localidad"  character varying(50)[] NOT NULL,
"nombre"     character varying(50)[] NOT NULL,
"domicilio"  character varying(50)[] NOT NULL,
"número de teléfono" integer,
"mail"   character varying(50)[],
"código postal"  integer NOT NULL,
"web" character varying(50)[],
"fecha de carga" DATE
);