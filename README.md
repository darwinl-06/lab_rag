# Taller Práctico #2

## Caso de Estudio: Optimización de la Atención al Cliente en una Empresa de E-commerce - Implementación de un Sistema RAG para IA Generativa

El objetivo de este taller es analizar un caso de estudio enfocado en la implementación de un sistema RAG (Retrieval-Augmented Generation) para optimizar la atención al cliente de una empresa de comercio electrónico.

En este caso, EcoMarket busca superar las limitaciones de los modelos de lenguaje de propósito general, los cuales tienden a generar respuestas incompletas o imprecisas al no contar con información específica y actualizada de la compañía. La idea es integrar un mecanismo de recuperación de documentos internos que permita que las respuestas sean precisas, coherentes y fundamentadas en datos reales de la organización. De esta manera, el sistema podrá atender consultas frecuentes relacionadas con pedidos, devoluciones, inventario y políticas de la empresa, reduciendo los tiempos de respuesta, mejorando la experiencia del cliente y fortaleciendo la confianza en el canal de soporte automatizado.

---

## Fase 1: Selección de Componentes Clave del Sistema RAG

Para la implementación del sistema RAG en EcoMarket es necesario seleccionar cuidadosamente los componentes que permitirán garantizar precisión, escalabilidad y eficiencia en el manejo de consultas de los clientes. En cuanto al modelo de embeddings, se opta por utilizar **Sentence Transformers multilingües de Hugging Face**, como *paraphrase-multilingual-MiniLM-L12-v2*, ya que ofrecen un buen equilibrio entre costo y rendimiento. Estos modelos son de código abierto, funcionan de manera eficiente en el idioma español y pueden ejecutarse localmente, lo que evita la dependencia exclusiva de servicios propietarios y reduce gastos operativos. Esta elección asegura que la representación semántica de los documentos de la empresa sea adecuada para realizar búsquedas precisas y rápidas en el sistema de recuperación.

Respecto a la base de datos vectorial, la propuesta inicial es utilizar **ChromaDB**, dado que es open-source, ligera y de fácil integración con frameworks como LangChain. Esto facilita su uso en un entorno académico o de prototipado, donde los recursos suelen ser limitados. Sin embargo, también se contempla la posibilidad de migrar a una solución más robusta como **Pinecone** en escenarios de producción, debido a su capacidad de manejar millones de vectores, escalabilidad en la nube y tiempos de respuesta óptimos. Aunque Pinecone implica un costo adicional, su facilidad de uso y soporte en entornos empresariales lo convierten en una opción viable a futuro. Con esta combinación de componentes se logra un sistema flexible que puede adaptarse tanto a un entorno de pruebas como a uno de despliegue real, respondiendo a las necesidades de EcoMarket de contar con un servicio de atención al cliente confiable, actualizado y eficiente.

---

## Fase 2: Creación de la Base de Conocimiento de Documentos

El éxito de un sistema RAG depende directamente de la calidad y organización de la información que se pone a disposición del modelo. En el caso de EcoMarket, resulta fundamental construir una base de conocimiento que contenga los documentos más relevantes para el proceso de atención al cliente. Para este propósito, se identifican tres fuentes clave: **la política de devoluciones y garantías en formato PDF**, ya que representa uno de los temas más consultados por los clientes; **un archivo de inventario de productos en Excel o CSV**, que permite acceder de manera actualizada a la disponibilidad, precios y características de los artículos; y **un documento JSON con preguntas frecuentes (FAQ)**, que recopila respuestas a dudas comunes en torno a envíos, pagos y procesos de compra. Estos documentos constituyen la base mínima que garantizará que el asistente pueda ofrecer respuestas fundamentadas y alineadas con la información oficial de la empresa.

Para asegurar un buen desempeño en la búsqueda semántica, es necesario dividir cada documento en fragmentos o *chunks* que puedan ser procesados por el modelo de embeddings. En este caso, se propone aplicar una **estrategia de segmentación recursiva**, que combina la separación por secciones naturales (como títulos y párrafos) con un control de tamaño máximo en tokens (ejemplo: 500 tokens con un solapamiento de 50). Este enfoque resulta más adecuado que una segmentación fija, ya que evita romper frases o apartados importantes y mantiene la coherencia del contenido. Finalmente, cada fragmento será convertido en un vector utilizando el modelo de embeddings seleccionado y cargado en la base de datos vectorial. De esta manera, cuando un cliente formule una pregunta, el sistema podrá recuperar los fragmentos más relevantes y construir una respuesta precisa y contextualizada.

---

## Fase 3: Implementación del Sistema RAG

En esta fase se integró un sistema de **Retrieval-Augmented Generation (RAG)** al chatbot de EcoMarket. Para ello se implementó un módulo de ingesta que carga documentos relevantes (política de devoluciones, catálogo de productos y FAQs), los indexa en una base vectorial y permite recuperar fragmentos útiles durante la interacción. Estos fragmentos se incorporan como contexto en las respuestas, mejorando la precisión y el respaldo documental del asistente.

Durante la implementación de la Fase 3 se presentaron varias limitaciones y se establecieron ciertas suposiciones para comprender mejor el alcance de la arquitectura RAG desarrollada. En primer lugar, el proyecto depende de recursos locales limitados: al ejecutarse con un modelo vía Ollama, la capacidad de cómputo condiciona la velocidad y la calidad de las respuestas frente a modelos más potentes en la nube. El sistema funciona únicamente con los documentos que fueron indexados mediante rag/ingest.py, por lo que la cobertura del conocimiento depende totalmente de los archivos almacenados en la carpeta data; si un SKU o número de pedido no aparece en esas fuentes, el asistente no puede ofrecer respuesta. Tampoco existe actualización automática: cualquier cambio en los documentos requiere volver a construir el índice manualmente. Además, la extracción de texto desde archivos PDF o Excel puede perder estructura en casos complejos, y el modelo de embeddings multilingüe empleado, aunque ligero y eficiente, no siempre captura todos los matices del lenguaje. También se reconoce que, aunque el prompt limita al modelo a responder solo con información del contexto, pueden ocurrir pequeñas alucinaciones o variaciones semánticas debido a la naturaleza probabilística del LLM. Se asume que los archivos en data/ representan la verdad organizacional (catálogos, políticas, pedidos) y que mantienen un formato estable, con identificadores como TRK-0003 o SKU-004.
---

### 📂 Estructura del proyecto

```

├─ app.py                 
├─ rag/
│  └─ ingest.py           # Ingesta/indexación de documentos en Chroma
│  └─ retriever.py
├─ settings.toml          # Modelo/temperatura y prompt(s)
├─ requirements.txt
└─ data/
   ├─ returns_policy.pdf  # Política de devoluciones
   ├─ faq.pdf             # Preguntas frecuentes
   ├─ orders.xls          # Datos de pedidos (tracking, estado, etc.)
   └─ producs.xls         # Datos de productos (SKU, categoría, retornable, etc.)
```

---

### ⚙️ Requisitos e instalación

1. Crear entorno virtual:

   ```bash
   python -m venv venv  
   venv\Scripts\activate      
   ```

2. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   pip install langchain langchain-community langchain-openai langchain-chroma
   ```

3. Construir el índice de documentos:

   ```bash
   python -m rag.ingest
   ```

---

### Uso del programa

El script `app.py` funciona desde la línea de comandos con dos subcomandos:  

#### 1. Consultar estado de pedido
```bash
python app.py order --tracking {NUMERO_DE_SEGUIMIENTO}
```

#### 2. Solicitar devolución de producto
```bash
python app.py return --sku {IDENTIFICADOR_DEL_PREFUCTO} --days_since_delivery {DIAS} --opened
```

#### 3. Preguntas frecuentes
```bash
python .\app.py faq --question {PREGUNTA}
```


Parámetros:  
- `--tracking`: número de seguimiento del pedido.  
- `--sku`: identificador del producto.  
- `--days_since_delivery`: días transcurridos desde la entrega.  
- `--opened`: indicar si el producto fue abierto (opcional, por defecto es cerrado).
- `-question`: indica pregunta

---

### 📌 Ejemplos

#### Ejemplo 1: Estado de pedido con retraso
```bash
python app.py order --tracking TRK-0003
```

Salida esperada:
```
Hola, antes que nada quiero agradecerte profundamente por haberte puesto en contacto con nosotros y por confiar en EcoMarket para tu compra. 

Revisé el estado de tu pedido con número de seguimiento TRK-0003 y encontré la siguiente información:  
Estado actual: Retrasado  
Fecha estimada de entrega: 2025-09-26  
Enlace de rastreo: https://track.eco/0003  

He notado que existe un retraso debido a una operación en la empresa de paquetería. Entiendo lo frustrante que puede ser y te pido disculpas sinceras por este inconveniente. Estamos trabajando de cerca con el transportador para garantizar que recibas tu pedido lo antes posible. 

Si necesitas más ayuda, recuerda que puedes escribirnos en el chat 24/7, al correo contacto@ecomarket.com o llamarnos al +1-800-ECOMARKET.
```

---

#### Ejemplo 2: Producto no elegible para devolución
```bash
python app.py return --sku SKU-001 --days_since_delivery 5 --opened
```

Salida esperada:
```
Hola, agradezco mucho que nos hayas contactado y que confíes en EcoMarket para tus compras. 
Revisé la información del producto con SKU SKU-001 y debo informarte con toda transparencia que este artículo no puede devolverse porque pertenece a la categoría de higiene o perecederos, o bien porque ya ha sido abierto. Estas restricciones están establecidas por razones sanitarias y de seguridad.

Entiendo que esta no es la respuesta que esperabas y lamento sinceramente la situación. Como alternativa, podemos ofrecerte un cupón del 10% de descuento en tu próxima compra como muestra de nuestro compromiso contigo. 

Si tienes alguna pregunta o deseas hablar sobre otras opciones, por favor no dudes en comunicarte directamente con nosotros mediante el chat de soporte 24/7, el correo electrónico contacto@ecomarket.com o llamando al +1-800-ECOMARKET. Estoy aquí para apoyarte en todo lo que necesites.
```

---

#### Ejemplo 3: Producto elegible para devolución
```bash
python app.py return --sku SKU-004 --days_since_delivery 10
```

Salida esperada:
```
Hola, muchas gracias por contactarnos y por confiar en EcoMarket con tu compra del producto con SKU SKU-004. 
He revisado tu caso y confirmo que el producto es elegible para devolución.

Para proceder, por favor sigue estos pasos:  
1. Ingresa a tu cuenta en EcoMarket y dirígete a la sección "Mis pedidos".  
2. Solicita la devolución y descarga la etiqueta de envío.  
3. Empaca el producto en su empaque original.  
4. Entrégalo al transportador asignado o en el punto autorizado más cercano.  

En cuanto recibamos el producto, procesaremos tu reembolso en un plazo de 5 a 7 días hábiles. 

Si tienes alguna pregunta o necesitas ayuda durante el proceso, puedes comunicarte con nosotros en cualquier momento mediante el chat de soporte 24/7, escribirnos al correo contacto@ecomarket.com o llamarnos al +1-800-ECOMARKET.
```

#### Ejemplo 4: Preunta frecuente
```bash
python .\app.py faq --question "¿Qué pasa si mi producto llegó dañado?"
```

Salida esperada:
```
Hola, Alex! Gracias por ponerse en contacto con nosotros y confiar en EcoMarket para resolver tus dudas. Aquí está una respuesta clara basada en el contexto que has proporcionado:

Si tu producto llegó dañado, te ofrecemos un reemplazo gratuito o podemos procesar su reembolso completo del dinero. Para recibir esta ayuda especializada, por favor asegúrate de presentar evidencia como una foto o video que muestre el estado actual del producto. Una vez validado tu caso con la documentación necesaria, se llevará a cabo un procesamiento dentro de los 5 a 7 días hábiles siguientes su recepción por parte nuestro equipo especializado en soporte al cliente.

Esperamos que esta información te sea útil y si tiens alguna otra pregunta o necesitas más detalles, no dudes en comunicarte con nosotros a través del chat de soporte 24/7, escribirnos al correo contact@ecomarket.com o llamarnos al +1-800-ECOMARKET. Estamos aquí para ayudar siempre que sea posible y apoyarte en cada paso del proceso de resolución.

Espero poder asistir aún más contigo, Alex.
```

---







