# Análisis de Estructura de Datos - rt-feed-record

## 📊 Resumen Ejecutivo

- **Total de registros procesados**: 8,451
- **Total de campos únicos**: 82
- **Tipos de datos encontrados**: 4 (string, integer, float, null)
- **Fecha de análisis**: 30 de septiembre de 2025

## 🗂️ Archivos Generados

1. **rt-feed-record-formatted.json** - Archivo JSON formateado y legible
2. **rt-feed-record-analysis.json** - Análisis detallado en formato JSON
3. **rt-feed-record-summary.txt** - Resumen completo en texto plano

## 📈 Estadísticas Principales

### Distribución de Tipos de Datos
- **String (str)**: Textos, códigos, nombres, fechas
- **Integer (int)**: Contadores, índices, relevancia, sentimientos binarios
- **Float (float)**: Valores de sentimiento, confianza, scores
- **Null**: Valores vacíos o no aplicables

### Campos Críticos (Siempre Poblados - 0% nulos)
- `TIMESTAMP_UTC` - Marca temporal del registro
- `RP_DOCUMENT_ID` - Identificador único del documento
- `RP_ENTITY_ID` - Identificador único de la entidad
- `ENTITY_TYPE` - Tipo de entidad (EVNT, SPOR, PLCE, etc.)
- `ENTITY_NAME` - Nombre de la entidad
- `COUNTRY_CODE` - Código de país
- `DOCUMENT_TYPE` - Tipo de documento (ej: FULL-ARTICLE)
- `TITLE` - Título del documento
- `SOURCE_NAME` - Nombre de la fuente
- `PRODUCT_KEY` - Clave del producto (ej: EDGE)

### Campos Ocasionales (Alto porcentaje de nulos)
- `MATURITY` - 100% nulos
- `RP_TERRITORY_ID` - 100% nulos
- `TERRITORY_NAME` - 100% nulos
- `EVALUATION_METHOD` - 99.9% nulos
- `RP_POSITION_ID` - 99.9% nulos
- `POSITION_NAME` - 99.9% nulos

## 🎯 Tipos de Entidades Identificadas

Basándose en los ejemplos encontrados:

### Eventos (EVNT)
- Super Bowl
- Eventos deportivos y de entretenimiento

### Deportes (SPOR)
- Sport (categoría general)

### Lugares (PLCE) 
- State of Indiana, US
- State of Alabama, US
- Cincinnati, US
- United States

### Equipos (TEAM)
- Cincinnati Bengals
- Detroit Lions
- Los Angeles Rams
- Pittsburgh Steelers
- Tampa Bay Buccaneers
- Buffalo Bills
- Baltimore Ravens
- etc.

### Productos (PRDT/PROD)
- Pizza
- Food
- Meat
- Instagram
- Motion Picture

### Compañías (COMP)
- Meta Platforms Inc.
- MyPizza Technologies Inc.
- Instagram Inc.

### Organizaciones (ORGA/ORGT)
- NFL
- Championship

### Conceptos y Emociones
- Love (EMOT)
- Calm (EMOT)
- Talent (SOCI)
- Leadership (SOCI)
- Award (CEPT)
- Challenge (CEPT)

## 📋 Campos de Sentimiento y Análisis

El dataset incluye múltiples métricas de análisis de sentimiento:

### Sentimientos Principales
- `ENTITY_SENTIMENT` - Sentimiento de la entidad (-1 a 1)
- `ENTITY_SENTIMENT_CONFIDENCE` - Confianza del sentimiento (0 a 1)
- `DOCUMENT_SENTIMENT` - Sentimiento del documento
- `COMPOSITE_SENTIMENT_SCORE` - Score compuesto

### Sentimientos Específicos
- `SUSTAINABILITY_SENTIMENT` - Sentimiento sobre sostenibilidad
- `CREDIT_SENTIMENT` - Sentimiento crediticio
- `INTEREST_RATE_SENTIMENT` - Sentimiento sobre tasas de interés
- `STOCK_TONE_SENTIMENT` - Tono sobre acciones
- `EARNINGS_TONE_SENTIMENT` - Tono sobre ganancias

## 🔍 Campos de Metadatos

### Identificadores y Referencias
- `RP_DOCUMENT_ID` - ID único del documento
- `RP_ENTITY_ID` - ID único de la entidad
- `RP_PARENT_ID` - ID de entidad padre
- `PROVIDER_DOCUMENT_ID` - ID del proveedor
- `RP_SOURCE_ID` - ID de la fuente

### Información de Jerarquía
- `ENTITY_HIERARCHY_LEVEL` - Nivel en jerarquía (1, 2, etc.)
- `PARENT_NAME` - Nombre del elemento padre
- `ENTITY_DETECTION_TYPE` - Tipo de detección (direct, indirect)

### Métricas de Contenido
- `WORD_COUNT` - Número de palabras
- `PARAGRAPH_COUNT` - Número de párrafos  
- `BYTE_COUNT` - Tamaño en bytes
- `DOCUMENT_RECORD_COUNT` - Total de registros del documento

## 💡 Recomendaciones de Uso

1. **Para análisis de sentimiento**: Usar campos `ENTITY_SENTIMENT` y `DOCUMENT_SENTIMENT`
2. **Para filtrado por relevancia**: Usar `ENTITY_RELEVANCE` (valores 0-100)
3. **Para análisis temporal**: Usar `TIMESTAMP_UTC`
4. **Para categorización**: Usar `ENTITY_TYPE`, `GROUP`, `CATEGORY`
5. **Para análisis geográfico**: Usar `COUNTRY_CODE` y entidades de tipo PLCE

## ⚠️ Consideraciones Importantes

- Muchos campos tienen altos porcentajes de valores nulos
- Los datos parecen ser de análisis de noticias/medios con enfoque en sentimiento
- Las fechas están en formato UTC timestamp
- Los IDs son strings hexadecimales únicos
- Los valores de sentimiento van de -1 (negativo) a +1 (positivo)