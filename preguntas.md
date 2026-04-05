# Preguntas de competencia resueltas con SPARQL

Prefijos base para todas las consultas:

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
```

Nota: algunas preguntas no están modeladas de forma exacta en la ontología actual. En esos casos se deja una aproximación SPARQL o una consulta que hoy devolvería vacío hasta que se agreguen más datos.

---

## 1. ¿Qué propiedades están disponibles en una determinada ciudad?

```sparql
PREFIX : <http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?prop ?nombre ?ciudad
WHERE {
  ?prop rdf:type/rdfs:subClassOf* :Propiedad ;
        :nombrePropiedad ?nombre ;
        :ubicadaEn ?zona .
  ?zona :ciudad ?ciudad .
  FILTER(?ciudad = "Cochabamba")
}
ORDER BY ?nombre
```

## 2. ¿Qué alojamientos están cerca del centro de la ciudad?

Aproximación: la ontología no modela "centro de la ciudad" explícitamente. Se usa la existencia de un punto de interés en la zona con distancia menor o igual a 1500 metros.

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

La ontología ya incluye un punto de interés educativo para responder esta consulta.

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

La ontología ya incluye un punto de interés de transporte para responder esta consulta.

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

Aproximación: se consideran tranquilas las zonas con densidad urbana `Baja`, `Media` o `Rural`.

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

La ontología no modela descuentos. Se deja una aproximación para alojamientos que aceptan estancias largas mediante políticas con `:maximoNoches >= 30`.

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

Aproximación: se interpreta como propiedades con `:numeroDormitorios >= 2`.

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

La ontología ya incluye la amenidad `Desayuno`.

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

La ontología ya incluye la amenidad `Limpieza`.

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

La ontología ya incluye la amenidad `Lavanderia`.

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

La ontología modela el costo del estacionamiento como una amenidad de transporte con costo adicional igual a `0`.

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

Aproximación: se consideran turísticos los alojamientos compatibles con perfiles vacacionales o ubicados en zonas con puntos de interés de tipo `Turismo`.

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

Ejemplo de consulta multicriterio: se puntúan propiedades por cumplir varias preferencias a la vez. Aquí se usan como ejemplo `Wifi`, `AireAcondicionado`, `Parking`, política pet-friendly, capacidad para al menos 4 personas y precio máximo de 60.

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
