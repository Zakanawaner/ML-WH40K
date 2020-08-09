Flujo de la aplicación:

Interactive Board (IB)
    A. Generación de los ejércitos.
        1. Arranca el escenario.
        2. Preguntar por las opciones de juego (puntos, etc.)
        3. Te pide que metas tu battlescribe.
        4. Submit y te genera los muñecos.
        5. Elegir el ejército de BigPapa.
        6. Generación del ejército tipo que corresponda con el modelo entrenado.

    B. Visualización de estadíasticas (fuera del flujo, constante durante toda la partida)
        1. CP, Objetivos, turno actual, fase actual, etc.
        2. Opcional: que te cante los bonus actuales por proximidad, etc.

Intelligent Agent (IA)
    A. Inicialización del agente.
        1. Inicialización de la imagen del tablero (se actualizará cada vez que sea necesario).
        2. Información del tablero en TTS (terreno, unidades amigas, enemigas...)
        3. Asigna las estadísticas a cada modelo que hay en el tablero.
        4. Asigna escuadrones.

    B. Comienza la partida.
        1. Evaluación del tablero.
        2. Toma de decisiones.
        3. Órdenes a sus escuadrones.
        4. Actualización del tablero.
        5. Aprendizaje tras cada decisión.

Intelligent Troops (IT)
    A. Inicialización.
        1. Agente más básico que ejecute las decisiones del IA.

    B. Durante la partida.
        2. Saber interpretar las órdenes del IA.
        3. Ejecutarlas de la forma más optimizada posible.
        4. Aprendizaje de sus acciones.










