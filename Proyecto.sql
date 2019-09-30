CREATE TABLE personas(
perid INT PRIMARY KEY,
pernombre VARCHAR(50),
perapellido VARCHAR(50),
pertelefonofijo VARCHAR(20),
perfechanacimiento VARCHAR(20),
percedula VARCHAR(20)
);

CREATE TABLE linea(
linumerolinea VARCHAR(30) PRIMARY KEY,
perid INT,
linestado VARCHAR(20),
FOREIGN KEY linea(perid) REFERENCES personas(perid)
);

CREATE TABLE equipo(
equserial INT PRIMARY KEY,
linumerolinea VARCHAR(30),
equmarca VARCHAR(50),
equdescripcion VARCHAR(50),
equestado VARCHAR(50),
FOREIGN KEY equipo(linumerolinea) REFERENCES linea(linumerolinea)
);

CREATE TABLE factura(
facnumero INT PRIMARY KEY,
linumerolinea VARCHAR(30),
facfechaemision DATE,
facvalor DOUBLE,
FOREIGN KEY factura(linumerolinea) REFERENCES linea(linumerolinea)
);