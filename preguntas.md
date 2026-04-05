# Preguntas de competencia resueltas con SPARQL

Estas consultas están alineadas con el contexto boliviano modelado en la ontología. Las ciudades y zonas usadas en los datos incluyen `La Paz`, `Cochabamba`, `Santa Cruz de la Sierra`, `Sucre` y `Tarija`, con barrios o áreas como `Sopocachi`, `Achumani`, `Cala Cala`, `Tiquipaya`, `Equipetrol`, `Urubo`, `La Recoleta`, `Centro Historico`, `San Bernardo` y `San Roque`. También se consideran referencias bolivianas como `Universidad Mayor de San Andres`, `Cristo de la Concordia`, `Fexpocruz`, `Plaza 25 de Mayo`, `Terminal de Buses de Tarija` y `Mercado Campesino`.

Prefijos base para todas las consultas:

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
```

Nota: algunas preguntas no están modeladas de forma exacta en la ontología actual. En esos casos se deja una aproximación SPARQL coherente con el contexto boliviano de la base, usando los barrios, ciudades, perfiles de huésped y puntos de interés que sí están representados.

---

## 1. ¿Qué propiedades están disponibles en una determinada ciudad?

Contexto Bolivia: la ciudad objetivo puede cambiarse por `La Paz`, `Cochabamba`, `Santa Cruz de la Sierra`, `Sucre` o `Tarija`. En el ejemplo se consulta `Cochabamba`.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?prop ?nombre ?ciudad
WHERE {
  VALUES ?ciudadBuscada { "Cochabamba" }
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :ubicadaEn ?zona .
  ?zona :ciudad ?ciudad .
  FILTER(?ciudad = ?ciudadBuscada)
}
ORDER BY ?nombre
```

## 2. ¿Qué alojamientos están cerca del centro de la ciudad?

Aproximación: la ontología no modela un predicado explícito de "centro". Para el contexto boliviano se asume cercanía al eje urbano principal o casco histórico de cada ciudad, usando puntos de interés en la misma zona con distancia menor o igual a 1500 metros.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?prop ?nombre ?puntoNombre ?distancia
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :ubicadaEn ?zona .
  ?zona :tienePuntoInteres ?punto .
  ?punto :nombrePunto ?puntoNombre ;
         :distanciaMetros ?distancia .
  FILTER(?distancia <= 1500)
}
ORDER BY ?distancia ?nombre
```

## 3. ¿Qué propiedades se encuentran cerca de universidades o centros de estudio?

La ontología ya incluye puntos de interés educativos bolivianos, como universidades y centros de estudio, para responder esta consulta.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?prop ?nombre ?puntoNombre
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :ubicadaEn ?zona .
  ?zona :tienePuntoInteres ?punto .
  ?punto :tipoPunto "Educacion" ;
         :nombrePunto ?puntoNombre .
}
ORDER BY ?nombre
```

## 4. ¿Qué alojamientos están cerca de transporte público?

La ontología ya incluye puntos de interés de transporte bolivianos, como terminales o estaciones urbanas, para responder esta consulta.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?prop ?nombre ?puntoNombre
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :ubicadaEn ?zona .
  ?zona :tienePuntoInteres ?punto .
  ?punto :tipoPunto "Transporte" ;
         :nombrePunto ?puntoNombre .
}
ORDER BY ?nombre
```

## 5. ¿Qué propiedades se encuentran en zonas tranquilas?

Aproximación: se consideran tranquilas las zonas bolivianas con densidad urbana `Baja`, `Media` o `Rural`, por ejemplo áreas residenciales o periurbanas como `Achumani`, `Tiquipaya`, `Urubo` o `San Roque`.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?prop ?nombre ?ciudad ?densidad
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :ubicadaEn ?zona .
  ?zona :ciudad ?ciudad ;
        :densidadUrbana ?densidad .
  FILTER(
    ?densidad = "Baja"^^xsd:string ||
    ?densidad = "Media"^^xsd:string ||
    ?densidad = "Rural"^^xsd:string
  )
}
ORDER BY ?ciudad ?nombre
```

## 6. ¿Qué alojamientos se encuentran dentro de un rango de precio específico?

Contexto Bolivia: el rango de ejemplo puede interpretarse como alojamiento de presupuesto medio dentro del mercado representado para ciudades como Cochabamba, Sucre o Tarija.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?prop ?nombre ?precio
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :precioNoche ?precio .
  FILTER(?precio >= 30.0 && ?precio <= 60.0)
}
ORDER BY ?precio ?nombre
```

## 7. ¿Qué propiedades pueden considerarse económicas?

Contexto Bolivia: aquí se consideran económicas las propiedades con precio nocturno igual o menor a `50.0`, umbral útil para comparar opciones accesibles dentro del dataset boliviano.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?prop ?nombre ?precio
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :precioNoche ?precio .
  FILTER(?precio <= 50.0)
}
ORDER BY ?precio ?nombre
```

## 8. ¿Qué alojamientos ofrecen descuentos por estadías largas?

La ontología no modela descuentos explícitos. Se deja una aproximación para alojamientos que aceptan estadías largas mediante políticas con `:maximoNoches >= 30`, algo pertinente para trabajo, estudios o reubicación temporal en ciudades bolivianas.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?prop ?nombre ?politica ?maxNoches
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :tienePolitica ?politica .
  ?politica :maximoNoches ?maxNoches .
  FILTER(?maxNoches >= 30)
}
ORDER BY DESC(?maxNoches) ?nombre
```

## 9. ¿Qué propiedades tienen buena relación precio–calidad?

Contexto Bolivia: la consulta combina precio moderado con calificación alta para identificar opciones competitivas dentro del mercado local modelado.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?prop ?nombre ?precio ?calificacion
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :precioNoche ?precio ;
        :calificacionPromedio ?calificacion .
  FILTER(?precio <= 45.0 && ?calificacion >= 4.5)
}
ORDER BY DESC(?calificacion) ?precio
```

## 10. ¿Qué alojamientos son considerados de lujo?

Contexto Bolivia: en esta ontología el segmento de lujo se aproxima con `Villa` y precio nocturno alto, algo coherente con zonas como `Urubo`, `Tiquipaya` o sectores residenciales consolidados.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>

SELECT DISTINCT ?prop ?nombre ?precio
WHERE {
  ?prop rdf:type :Villa ;
        :nombrePropiedad ?nombre ;
        :precioNoche ?precio .
  FILTER(?precio >= 200.0)
}
ORDER BY DESC(?precio)
```

## 11. ¿Qué alojamientos incluyen cocina?

Contexto Bolivia: esta consulta es útil para identificar estadías aptas para viajes familiares, laborales o prolongados en ciudades bolivianas.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?prop ?nombre
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :tieneAmenidad :Cocina .
}
ORDER BY ?nombre
```

## 12. ¿Qué propiedades tienen garaje o estacionamiento?

Contexto Bolivia: se incluyen opciones útiles para ciudades con uso intensivo de vehículo particular, como Santa Cruz de la Sierra, Tarija o zonas periurbanas de Cochabamba.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?prop ?nombre ?tipoEstacionamiento
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :tipoEstacionamiento ?tipoEstacionamiento .
  FILTER(?tipoEstacionamiento != "NoDisponible")
}
ORDER BY ?nombre
```

## 13. ¿Qué alojamientos cuentan con piscina?

Contexto Bolivia: esta consulta suele destacar propiedades recreativas o de clima más cálido, especialmente en Santa Cruz de la Sierra y algunas zonas residenciales amplias.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?prop ?nombre
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :tieneAmenidad :Piscina .
}
ORDER BY ?nombre
```

## 14. ¿Qué propiedades tienen aire acondicionado?

Contexto Bolivia: esta preferencia es especialmente relevante para alojamientos en Santa Cruz de la Sierra y otros contextos de clima cálido dentro del dataset.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?prop ?nombre
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :tieneAmenidad :AireAcondicionado .
}
ORDER BY ?nombre
```

## 15. ¿Qué propiedades tienen capacidad para más de cuatro personas?

Contexto Bolivia: ayuda a ubicar propiedades aptas para grupos, turismo interno o viajes familiares extendidos.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?prop ?nombre ?capacidad
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :capacidadMaxima ?capacidad .
  FILTER(?capacidad > 4)
}
ORDER BY DESC(?capacidad) ?nombre
```

## 16. ¿Qué alojamientos son adecuados para parejas?

Contexto Bolivia: se basa en la compatibilidad con el perfil `Pareja` ya modelado en la ontología.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?prop ?nombre
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :compatibleCon :Pareja .
}
ORDER BY ?nombre
```

## 17. ¿Qué propiedades son adecuadas para familias?

Contexto Bolivia: se basa en la compatibilidad con el perfil `Familiar`, útil para viajes vacacionales, reubicación o estancias con hijos.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?prop ?nombre
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :compatibleCon :Familiar .
}
ORDER BY ?nombre
```

## 18. ¿Qué alojamientos son adecuados para viajeros individuales?

Contexto Bolivia: se apoya en el perfil `Individual`, frecuente en viajes de estudio, trabajo o turismo de corta estancia.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?prop ?nombre
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :compatibleCon :Individual .
}
ORDER BY ?nombre
```

## 19. ¿Qué propiedades tienen varias habitaciones disponibles?

Aproximación: se interpreta como propiedades con `:numeroDormitorios >= 2`, una lectura razonable para casas, apartamentos amplios o villas del contexto boliviano.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?prop ?nombre ?dormitorios
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :numeroDormitorios ?dormitorios .
  FILTER(?dormitorios >= 2)
}
ORDER BY DESC(?dormitorios) ?nombre
```

## 20. ¿Qué propiedades admiten mascotas?

Contexto Bolivia: se usa la política declarada de mascotas y no una inferencia por tipo de alojamiento o zona.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?prop ?nombre ?politica
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :tienePolitica ?politica .
  ?politica :reglaMascotas "Permitido" .
}
ORDER BY ?nombre
```

## 21. ¿Qué alojamientos incluyen desayuno?

La ontología ya incluye la amenidad `Desayuno`, útil para estancias urbanas o turísticas en el contexto boliviano.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?prop ?nombre
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :tieneAmenidad ?amenidad .
  ?amenidad :nombreAmenidad "Desayuno" .
}
ORDER BY ?nombre
```

## 22. ¿Qué propiedades ofrecen servicio de limpieza?

La ontología ya incluye la amenidad `Limpieza`, relevante sobre todo para estadías ejecutivas o prolongadas.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?prop ?nombre
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :tieneAmenidad ?amenidad .
  ?amenidad :nombreAmenidad "Limpieza" .
}
ORDER BY ?nombre
```

## 23. ¿Qué alojamientos cuentan con servicio de lavandería?

La ontología ya incluye la amenidad `Lavanderia`, especialmente útil para viajes de estudio, trabajo o permanencias largas.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?prop ?nombre
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :tieneAmenidad ?amenidad .
  ?amenidad :nombreAmenidad "Lavanderia" .
}
ORDER BY ?nombre
```

## 24. ¿Qué propiedades ofrecen estacionamiento gratuito?

La ontología modela el costo del estacionamiento como una amenidad de transporte con costo adicional igual a `0`, algo importante para ciudades bolivianas con movilidad basada en vehículo propio.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?prop ?nombre ?amenidadNombre ?costo
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :tieneAmenidad ?amenidad .
  ?amenidad :categoriaAmenidad "Transporte" ;
            :nombreAmenidad ?amenidadNombre ;
            :costoAdicional ?costo .
  FILTER(?costo = "0.0"^^xsd:decimal)
}
ORDER BY ?nombre
```

## 25. ¿Qué propiedades son adecuadas para estudiar o trabajar?

Contexto Bolivia: esta consulta combina perfiles y propósitos de viaje ligados a `Estudios` o trabajo `Remoto`, algo coherente con estancias cercanas a universidades o zonas urbanas consolidadas.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?prop ?nombre ?perfil ?proposito
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :compatibleCon ?perfil .
  ?perfil :tienePropositoViaje ?proposito .
  {
    ?proposito :tipoPropositoViaje "Estudios" .
  }
  UNION
  {
    ?proposito :modalidadTrabajo "Remoto" .
  }
}
ORDER BY ?nombre
```

## 26. ¿Qué alojamientos son adecuados para estadías largas?

Contexto Bolivia: puede interpretarse como alojamiento apto para pasantías, trabajo temporal, tratamientos médicos, reubicación o estudio en otra ciudad del país.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?prop ?nombre ?politica ?maxNoches
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :tienePolitica ?politica .
  ?politica :maximoNoches ?maxNoches .
  FILTER(?maxNoches >= 30)
}
ORDER BY DESC(?maxNoches) ?nombre
```

## 27. ¿Qué propiedades son recomendadas para viajes familiares?

Contexto Bolivia: se apoya en la relación entre perfiles compatibles y el propósito `ViajeFamiliar`.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?prop ?nombre
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :compatibleCon ?perfil .
  ?perfil :tienePropositoViaje :ViajeFamiliar .
}
ORDER BY ?nombre
```

## 28. ¿Qué alojamientos son ideales para turistas?

Aproximación: se consideran turísticos los alojamientos compatibles con perfiles vacacionales o ubicados en zonas con puntos de interés de tipo `Turismo`, como referencias urbanas y patrimoniales bolivianas ya presentes en la ontología.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?prop ?nombre
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre .
  {
    ?prop :compatibleCon ?perfil .
    ?perfil :tienePropositoViaje :ViajeVacacional .
  }
  UNION
  {
    ?prop :ubicadaEn ?zona .
    ?zona :tienePuntoInteres ?punto .
    ?punto :tipoPunto "Turismo" .
  }
}
ORDER BY ?nombre
```

## 29. ¿Qué propiedades cumplen múltiples preferencias del huésped?

Ejemplo de consulta multicriterio: se puntúan propiedades por cumplir varias preferencias a la vez. Aquí se usan `Wifi`, `AireAcondicionado`, `Parking`, política pet-friendly, capacidad para al menos 4 personas y precio máximo de 60, un escenario razonable para comparar alojamientos urbanos bolivianos.

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?prop ?nombre (COUNT(*) AS ?criteriosCumplidos)
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre .
  {
    ?prop :tieneAmenidad :Wifi .
  }
  UNION
  {
    ?prop :tieneAmenidad :AireAcondicionado .
  }
  UNION
  {
    ?prop :tieneAmenidad :Parking .
  }
  UNION
  {
    ?prop :tienePolitica ?politica .
    ?politica :reglaMascotas "Permitido" .
  }
  UNION
  {
    ?prop :capacidadMaxima ?capacidad .
    FILTER(?capacidad >= 4)
  }
  UNION
  {
    ?prop :precioNoche ?precio .
    FILTER(?precio <= 60.0)
  }
}
GROUP BY ?prop ?nombre
HAVING(COUNT(*) >= 3)
ORDER BY DESC(?criteriosCumplidos) ?nombre
```
