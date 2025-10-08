# Taller Práctico #2

## Caso de Estudio: Optimización de la Atención al Cliente en una Empresa de E-commerce - Implementación de un Sistema RAG para IA Generativa

El objetivo de este taller es analizar un caso de estudio enfocado en la implementación de un sistema RAG (Retrieval-Augmented Generation) para optimizar la atención al cliente de una empresa de comercio electrónico.

En este caso, EcoMarket busca superar las limitaciones de los modelos de lenguaje de propósito general, los cuales tienden a generar respuestas incompletas o imprecisas al no contar con información específica y actualizada de la compañía. La idea es integrar un mecanismo de recuperación de documentos internos que permita que las respuestas sean precisas, coherentes y fundamentadas en datos reales de la organización. De esta manera, el sistema podrá atender consultas frecuentes relacionadas con pedidos, devoluciones, inventario y políticas de la empresa, reduciendo los tiempos de respuesta, mejorando la experiencia del cliente y fortaleciendo la confianza en el canal de soporte automatizado.

---

## Fase 1: Selección de Componentes Clave del Sistema RAG

Para la implementación del sistema RAG en EcoMarket es necesario seleccionar cuidadosamente los componentes que permitirán garantizar precisión, escalabilidad y eficiencia en el manejo de consultas de los clientes. En cuanto al modelo de embeddings, se opta por utilizar **Sentence Transformers multilingües de Hugging Face**, como *paraphrase-multilingual-MiniLM-L12-v2*, ya que ofrecen un buen equilibrio entre costo y rendimiento. Estos modelos son de código abierto, funcionan de manera eficiente en el idioma español y pueden ejecutarse localmente, lo que evita la dependencia exclusiva de servicios propietarios y reduce gastos operativos. Esta elección asegura que la representación semántica de los documentos de la empresa sea adecuada para realizar búsquedas precisas y rápidas en el sistema de recuperación.

Respecto a la base de datos vectorial, la propuesta inicial es utilizar **ChromaDB**, dado que es open-source, ligera y de fácil integración con frameworks como LangChain. Esto facilita su uso en un entorno académico o de prototipado, donde los recursos suelen ser limitados. Sin embargo, también se contempla la posibilidad de migrar a una solución más robusta como **Pinecone** en escenarios de producción, debido a su capacidad de manejar millones de vectores, escalabilidad en la nube y tiempos de respuesta óptimos. Aunque Pinecone implica un costo adicional, su facilidad de uso y soporte en entornos empresariales lo convierten en una opción viable a futuro. Con esta combinación de componentes se logra un sistema flexible que puede adaptarse tanto a un entorno de pruebas como a uno de despliegue real, respondiendo a las necesidades de EcoMarket de contar con un servicio de atención al cliente confiable, actualizado y eficiente.


