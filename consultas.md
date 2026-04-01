
---

### 🎯 Preguntas de Competencia (Competency Questions)

1. **¿Qué propiedades están disponibles en una determinada ubicación (ej. Santa Cruz o Cochabamba)?**
   `Propiedad and (ubicadaEn value Zona_SCZ or ubicadaEn value Zona_CBBA)`

2. **¿Qué propiedades son adecuadas para un perfil específico (ej. grupos de amigos)?**
   `Propiedad and (compatibleCon value Amigos)`

3. **¿Qué propiedades tienen políticas que admiten mascotas?**
   `Propiedad and (tienePolitica value PoliticaPetFriendly)`

4. **¿Qué alojamientos se encuentran dentro de un rango de precio específico (ej. entre 30 y 60 por noche)?**
   `Propiedad and (precioNoche some xsd:decimal[>= 30.0]) and (precioNoche some xsd:decimal[<= 60.0])`

5. **¿Qué alojamientos tienen capacidad para 3 o más personas?**
   `Propiedad and (capacidadMaxima some xsd:int[>= 3])`

6. **¿Qué propiedades ofrecen simultáneamente Piscina y Parqueo?**
   `Propiedad and (tieneAmenidad value Piscina) and (tieneAmenidad value Parking)`

7. **¿Qué perfiles de huéspedes viajan con un propósito de trabajo?**
   `PerfilHuesped and (tienePropositoViaje value ViajeTrabajo)`

8. **¿Qué propiedades tienen buena relación calidad-precio (alta calificación y bajo costo)?**
   `Propiedad and (calificacionPromedio some xsd:decimal[>= 4.5]) and (precioNoche some xsd:decimal[<= 45.0])`

9. **¿Qué alojamientos se consideran de "lujo" / alta gama (Villas muy caras)?**
   `Villa and (precioNoche some xsd:decimal[>= 200.0])`

10. **¿Cuáles alojamientos ofrecen política de cancelación "Flexible"?**
    `Propiedad and (tienePolitica value PoliticaFlexible)`

11. **¿Qué propiedades están cerca del centro de la ciudad / puntos de interés (ej. cerca del Cristo Redentor)?**
    `Propiedad and (ubicadaEn some (ZonaGeografica and tienePuntoInteres value CristoRedentor))`

12. **¿Cuáles habitaciones privadas tienen baño privado en suite?**
    `HabitacionPrivada and (tipoBano value "EnSuite")`

13. **¿Qué alojamientos (Casas o Apartamentos) tienen 2 o más dormitorios disponibles?**
    `(Casa or Apartamento) and (numeroDormitorios some xsd:int[>= 2])`

14. **¿Existen habitaciones compartidas exclusivas para personas individuales (sin necesidad de ir en grupo)?**
    `HabitacionCompartida and (compatibleCon value Individual)`

15. **¿Qué alojamientos tienen un sistema de acceso moderno (Llave Electrónica / Código numérico)?**
    `Propiedad and (tipoAcceso value "LlaveElectronica" or tipoAcceso value "CodigoNumerico")`

16. **¿Qué apartamentos ubicados en La Paz tienen ascensor y están en un piso alto (> piso 3)?**
    `Apartamento and (ubicadaEn value Zona_LP) and (tieneAscensor value "true"^^xsd:boolean) and (numeroPiso some xsd:int[>= 3])`

---

### 🟢 1. Nivel Básico (Instancias Directas)
Sirven para listar todos los individuos que pertenecen directamente a una jerarquía o clase de la ontología.

1.  **Todas las casas registradas:**
    `Casa`
2.  **Todos los apartamentos:**
    `Apartamento`
3.  **Cualquier propiedad (Llamará a villas, casas, habitaciones, etc.):**
    `Propiedad`
4.  **Cualquier tipo de Alojamiento Completo (Casas, Departamentos, Villas):**
    `AlojamientoCompleto`
5.  **Lista de todos los propósitos de viaje definidos:**
    `PropositoViaje`

---

### 🟡 2. Nivel Intermedio (Propiedades de Objeto simples)
Buscan qué propiedades tienen ciertas relaciones (`ObjectProperties`) específicas con otras clases o valores.

6.  **Alojamientos que están en Cochabamba:**
    `Propiedad and (ubicadaEn value Zona_CBBA)`
7.  **Propiedades que contienen una Piscina:**
    `Propiedad and (tieneAmenidad value Piscina)`
8.  **Propiedades específicamente orientadas a Perfil Familiar:**
    `Propiedad and (compatibleCon value Familiar)`
9.  **Villas ubicadas en Santa Cruz:**
    `Villa and (ubicadaEn value Zona_SCZ)`
10. **Propiedades que han declarado explícitamente tener alguna política de cancelación:**
    `Propiedad and (tienePolitica some Politica)`

---

### 🟠 3. Nivel Avanzado (Intersección de Relaciones Múltiples)
Combinan lógicamente múltiples variables semánticas usando sentencias como `and` / `or`.

11. **Propiedades en La Paz que tienen "Wifi":**
    `Propiedad and (ubicadaEn value Zona_LP) and (tieneAmenidad value Wifi)`
12. **Propiedades que ofrecen "AireAcondicionado" Y "Parking" al mismo tiempo:**
    `Propiedad and (tieneAmenidad value AireAcondicionado) and (tieneAmenidad value Parking)`
13. **Casas o Apartamentos acordes con grupo de "Amigos":**
    `(Casa or Apartamento) and (compatibleCon value Amigos)`
14. **Zonas que tienen algún Punto de Interés registrado:**
    `ZonaGeografica and (tienePuntoInteres some PuntoInteres)`
15. **Alojamiento que NO es una habitación de ningún tipo y permite mascotas:**
    `Propiedad and not (AlojamientoHabitacion) and (tienePolitica value PoliticaPetFriendly)`

---

### 🔵 4. Nivel Especialista (Propiedades de Datos - Valores Exactos)
Aquí se consulta directamente el comportamiento interno de los individuos a nivel metadatos (booleanos, literales).

16. **Alojamientos con acceso configurado vía Llave Electrónica:**
    `Propiedad and (tipoAcceso value "LlaveElectronica")`
17. **Casas que tienen jardín:**
    `Casa and (tieneJardin value "true"^^xsd:boolean)`
18. **Apartamentos que declaran tener Ascensor:**
    `Apartamento and (tieneAscensor value "true"^^xsd:boolean)`
19. **Habitaciones privadas con Baño en suite:**
    `HabitacionPrivada and (tipoBano value "EnSuite")`
20. **Políticas específicas que permiten mascotas:**
    `Politica and (reglaMascotas value "Permitido")`

---

### 🟣 5. Nivel Maestro (Propiedades de Datos Numéricos - Facetas y Rangos)
Protégé permite que el motor semántico pueda deducir y realizar consultas comparativas sobre rangos int, double y decimal. 

21. **Alojamientos que pueden albergar 4 huéspedes o más:**
    `Propiedad and (capacidadMaxima some xsd:int[>= 4])`
22. **Alojamientos de alta gama (calificación promedio por encima de 4.5):**
    `Propiedad and (calificacionPromedio some xsd:decimal[> 4.5])`
23. **Cualquier tipo de propiedad económica (Cuesta menos o igual de 50 la noche):**
    `Propiedad and (precioNoche some xsd:decimal[<= 50.0])`
24. **Villas gigantes para eventos (Capacidad para más de 30 personas):**
    `Villa and (capacidadEventos some xsd:int[>= 30])`
25. **Una "Súper Consulta": Apartamentos en el centro con más de 1 baño y precios menores a 100:**
    `Apartamento and (numeroBanos some xsd:int[> 1]) and (precioNoche some xsd:decimal[< 100.0])`

**✏️ Tip para ejecutarlas:** En Protégé puedes usar atajos de teclado para autocompletado en el cuadro de DL Query. Si pones `tieneAm` y aprietas la tecla `Tab`, la interfaz se autocompletará a `tieneAmenidad`, lo que es ideal para evitar errores tipográficos de mayúsculas/minúsculas o espacios.