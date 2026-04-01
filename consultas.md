---

### 🎯 Preguntas de Competencia (Competency Questions)

**P1: ¿Qué propiedades están disponibles en una determinada ubicación (ej. Santa Cruz o Cochabamba)?**
```text
Propiedad and (ubicadaEn value Zona_SCZ or ubicadaEn value Zona_CBBA)
```

**P2: ¿Qué propiedades son adecuadas para un perfil específico (ej. grupos de amigos)?**
```text
Propiedad and (compatibleCon value Amigos)
```

**P3: ¿Qué propiedades tienen políticas que admiten mascotas?**
```text
Propiedad and (tienePolitica value PoliticaPetFriendly)
```

**P4: ¿Qué alojamientos se encuentran dentro de un rango de precio específico (ej. entre 30 y 60 por noche)?**
```text
Propiedad and (precioNoche some xsd:decimal[>= 30.0]) and (precioNoche some xsd:decimal[<= 60.0])
```

**P5: ¿Qué alojamientos tienen capacidad para 3 o más personas?**
```text
Propiedad and (capacidadMaxima some xsd:int[>= 3])
```

**P6: ¿Qué propiedades ofrecen simultáneamente Piscina y Parqueo?**
```text
Propiedad and (tieneAmenidad value Piscina) and (tieneAmenidad value Parking)
```

**P7: ¿Qué perfiles de huéspedes viajan con un propósito de trabajo?**
```text
PerfilHuesped and (tienePropositoViaje value ViajeTrabajo)
```

**P8: ¿Qué propiedades tienen buena relación calidad-precio (alta calificación y bajo costo)?**
```text
Propiedad and (calificacionPromedio some xsd:decimal[>= 4.5]) and (precioNoche some xsd:decimal[<= 45.0])
```

**P9: ¿Qué alojamientos se consideran de "lujo" / alta gama (Villas muy caras)?**
```text
Villa and (precioNoche some xsd:decimal[>= 200.0])
```

**P10: ¿Cuáles alojamientos ofrecen política de cancelación "Flexible"?**
```text
Propiedad and (tienePolitica value PoliticaFlexible)
```

**P11: ¿Qué propiedades están cerca del centro de la ciudad / puntos de interés (ej. cerca del Cristo Redentor)?**
```text
Propiedad and (ubicadaEn some (ZonaGeografica and tienePuntoInteres value CristoRedentor))
```

**P12: ¿Cuáles habitaciones privadas tienen baño privado en suite?**
```text
HabitacionPrivada and (tipoBano value "EnSuite")
```

**P13: ¿Qué alojamientos (Casas o Apartamentos) tienen 2 o más dormitorios disponibles?**
```text
(Casa or Apartamento) and (numeroDormitorios some xsd:int[>= 2])
```

**P14: ¿Existen habitaciones compartidas exclusivas para personas individuales (sin necesidad de ir en grupo)?**
```text
HabitacionCompartida and (compatibleCon value Individual)
```

**P15: ¿Qué alojamientos tienen un sistema de acceso moderno (Llave Electrónica / Código numérico)?**
```text
Propiedad and (tipoAcceso value "LlaveElectronica" or tipoAcceso value "CodigoNumerico")
```

**P16: ¿Qué apartamentos ubicados en La Paz tienen ascensor y están en un piso alto (> piso 3)?**
```text
Apartamento and (ubicadaEn value Zona_LP) and (tieneAscensor value "true"^^xsd:boolean) and (numeroPiso some xsd:int[>= 3])
```

---

### 🟢 1. Nivel Básico (Instancias Directas)

**P1: Todas las casas registradas:**
```text
Casa
```

**P2: Todos los apartamentos:**
```text
Apartamento
```

**P3: Cualquier propiedad (Llamará a villas, casas, habitaciones, etc.):**
```text
Propiedad
```

**P4: Cualquier tipo de Alojamiento Completo (Casas, Departamentos, Villas):**
```text
AlojamientoCompleto
```

**P5: Lista de todos los propósitos de viaje definidos:**
```text
PropositoViaje
```

---

### 🟡 2. Nivel Intermedio (Propiedades de Objeto simples)

**P6: Alojamientos que están en Cochabamba:**
```text
Propiedad and (ubicadaEn value Zona_CBBA)
```

**P7: Propiedades que contienen una Piscina:**
```text
Propiedad and (tieneAmenidad value Piscina)
```

**P8: Propiedades específicamente orientadas a Perfil Familiar:**
```text
Propiedad and (compatibleCon value Familiar)
```

**P9: Villas ubicadas en Santa Cruz:**
```text
Villa and (ubicadaEn value Zona_SCZ)
```

**P10: Propiedades que han declarado explícitamente tener alguna política de cancelación:**
```text
Propiedad and (tienePolitica some Politica)
```

---

### 🟠 3. Nivel Avanzado (Intersección de Relaciones Múltiples)

**P11: Propiedades en La Paz que tienen "Wifi":**
```text
Propiedad and (ubicadaEn value Zona_LP) and (tieneAmenidad value Wifi)
```

**P12: Propiedades que ofrecen "AireAcondicionado" Y "Parking" al mismo tiempo:**
```text
Propiedad and (tieneAmenidad value AireAcondicionado) and (tieneAmenidad value Parking)
```

**P13: Casas o Apartamentos acordes con grupo de "Amigos":**
```text
(Casa or Apartamento) and (compatibleCon value Amigos)
```

**P14: Zonas que tienen algún Punto de Interés registrado:**
```text
ZonaGeografica and (tienePuntoInteres some PuntoInteres)
```

**P15: Alojamiento que NO es una habitación de ningún tipo y permite mascotas:**
```text
Propiedad and not (AlojamientoHabitacion) and (tienePolitica value PoliticaPetFriendly)
```

---

### 🔵 4. Nivel Especialista (Propiedades de Datos - Valores Exactos)

**P16: Alojamientos con acceso configurado vía Llave Electrónica:**
```text
Propiedad and (tipoAcceso value "LlaveElectronica")
```

**P17: Casas que tienen jardín:**
```text
Casa and (tieneJardin value "true"^^xsd:boolean)
```

**P18: Apartamentos que declaran tener Ascensor:**
```text
Apartamento and (tieneAscensor value "true"^^xsd:boolean)
```

**P19: Habitaciones privadas con Baño en suite:**
```text
HabitacionPrivada and (tipoBano value "EnSuite")
```

**P20: Políticas específicas que permiten mascotas:**
```text
Politica and (reglaMascotas value "Permitido")
```

---

### 🟣 5. Nivel Maestro (Propiedades de Datos Numéricos - Facetas y Rangos)

**P21: Alojamientos que pueden albergar 4 huéspedes o más:**
```text
Propiedad and (capacidadMaxima some xsd:int[>= 4])
```

**P22: Alojamientos de alta gama (calificación promedio por encima de 4.5):**
```text
Propiedad and (calificacionPromedio some xsd:decimal[> 4.5])
```

**P23: Cualquier tipo de propiedad económica (Cuesta menos o igual de 50 la noche):**
```text
Propiedad and (precioNoche some xsd:decimal[<= 50.0])
```

**P24: Villas gigantes para eventos (Capacidad para más de 30 personas):**
```text
Villa and (capacidadEventos some xsd:int[>= 30])
```

**P25: Una "Súper Consulta": Apartamentos en el centro con más de 1 baño y precios menores a 100:**
```text
Apartamento and (numeroBanos some xsd:int[> 1]) and (precioNoche some xsd:decimal[< 100.0])
```

**✏️ Tip para ejecutarlas:** En Protégé puedes usar atajos de teclado para autocompletado en el cuadro de DL Query. Si pones `tieneAm` y aprietas la tecla `Tab`, la interfaz se autocompletará a `tieneAmenidad`, lo que es ideal para evitar errores tipográficos de mayúsculas/minúsculas o espacios.