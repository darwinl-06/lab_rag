# Taller Práctico #2

## Caso de Estudio: Optimización de la Atención al Cliente en una Empresa de E-commerce - Implementación de un Sistema RAG para IA Generativa

El objetivo de este taller es analizar un caso de estudio enfocado en la implementación de un sistema RAG (Retrieval-Augmented Generation) para optimizar la atención al cliente de una empresa de comercio electrónico.

En este caso, EcoMarket busca superar las limitaciones de los modelos de lenguaje de propósito general, los cuales tienden a generar respuestas incompletas o imprecisas al no contar con información específica y actualizada de la compañía. La idea es integrar un mecanismo de recuperación de documentos internos que permita que las respuestas sean precisas, coherentes y fundamentadas en datos reales de la organización. De esta manera, el sistema podrá atender consultas frecuentes relacionadas con pedidos, devoluciones, inventario y políticas de la empresa, reduciendo los tiempos de respuesta, mejorando la experiencia del cliente y fortaleciendo la confianza en el canal de soporte automatizado.

---

## Fase 1: Selección de Componentes Clave del Sistema RAG

Para la implementación del sistema RAG en EcoMarket es necesario seleccionar cuidadosamente los componentes que permitirán garantizar precisión, escalabilidad y eficiencia en el manejo de consultas de los clientes. En cuanto al modelo de embeddings, se opta por utilizar **Sentence Transformers multilingües de Hugging Face**, como *paraphrase-multilingual-MiniLM-L12-v2*, ya que ofrecen un buen equilibrio entre costo y rendimiento. Estos modelos son de código abierto, funcionan de manera eficiente en el idioma español y pueden ejecutarse localmente, lo que evita la dependencia exclusiva de servicios propietarios y reduce gastos operativos. Esta elección asegura que la representación semántica de los documentos de la empresa sea adecuada para realizar búsquedas precisas y rápidas en el sistema de recuperación.

Respecto a la base de datos vectorial, la propuesta inicial es utilizar **ChromaDB**, dado que es open-source, ligera y de fácil integración con frameworks como LangChain. Esto facilita su uso en un entorno académico o de prototipado, donde los recursos suelen ser limitados. Sin embargo, también se contempla la posibilidad de migrar a una solución más robusta como **Pinecone** en escenarios de producción, debido a su capacidad de manejar millones de vectores, escalabilidad en la nube y tiempos de respuesta óptimos. Aunque Pinecone implica un costo adicional, su facilidad de uso y soporte en entornos empresariales lo convierten en una opción viable a futuro. Con esta combinación de componentes se logra un sistema flexible que puede adaptarse tanto a un entorno de pruebas como a uno de despliegue real, respondiendo a las necesidades de EcoMarket de contar con un servicio de atención al cliente confiable, actualizado y eficiente.

Perfecto 🙌, sigamos con la **Fase 2: Creación de la Base de Conocimiento**. Te lo redacto en forma de explicación narrativa (como en tu Lab 1), para que quede listo en el README del Taller 2:

---

## Fase 2: Creación de la Base de Conocimiento de Documentos

El éxito de un sistema RAG depende directamente de la calidad y organización de la información que se pone a disposición del modelo. En el caso de EcoMarket, resulta fundamental construir una base de conocimiento que contenga los documentos más relevantes para el proceso de atención al cliente. Para este propósito, se identifican tres fuentes clave: **la política de devoluciones y garantías en formato PDF**, ya que representa uno de los temas más consultados por los clientes; **un archivo de inventario de productos en Excel o CSV**, que permite acceder de manera actualizada a la disponibilidad, precios y características de los artículos; y **un documento JSON con preguntas frecuentes (FAQ)**, que recopila respuestas a dudas comunes en torno a envíos, pagos y procesos de compra. Estos documentos constituyen la base mínima que garantizará que el asistente pueda ofrecer respuestas fundamentadas y alineadas con la información oficial de la empresa.

Para asegurar un buen desempeño en la búsqueda semántica, es necesario dividir cada documento en fragmentos o *chunks* que puedan ser procesados por el modelo de embeddings. En este caso, se propone aplicar una **estrategia de segmentación recursiva**, que combina la separación por secciones naturales (como títulos y párrafos) con un control de tamaño máximo en tokens (ejemplo: 500 tokens con un solapamiento de 50). Este enfoque resulta más adecuado que una segmentación fija, ya que evita romper frases o apartados importantes y mantiene la coherencia del contenido. Finalmente, cada fragmento será convertido en un vector utilizando el modelo de embeddings seleccionado y cargado en la base de datos vectorial. De esta manera, cuando un cliente formule una pregunta, el sistema podrá recuperar los fragmentos más relevantes y construir una respuesta precisa y contextualizada.

---




