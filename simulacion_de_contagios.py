"""
Esta sería la clase vista. Contiene el ciclo de la aplicación y ensambla
las llamadas para obtener el dibujo de la escena.
"""

import json
import math
import glfw
from OpenGL.GL import *
import sys

from modelos import *
from controller import Controller

## Lectura de datos

nombre_archivo = sys.argv[1]

data = open(nombre_archivo, 'r').read()

datos = json.loads(data)

Radius = datos["Radius"]
Contagious_prob = datos["Contagious_prob"]
Death_rate = datos["Death_rate"]
Initial_population = datos["Initial_population"]
Days_to_heal = datos["Days_to_heal"]



if __name__ == '__main__':

    # Initialize glfw
    if not glfw.init():
        sys.exit()
   
    width = 900
    height = 900

    window = glfw.create_window(width, height, 'Pandemia', None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    controlador = Controller()

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, controlador.on_key)

    # Assembling the shader program (pipeline) with both shaders
    pipeline1 = es.SimpleTransformShaderProgram()
    pipeline2 = es.SimpleTextureTransformShaderProgram()


    # Telling OpenGL to use our shader program
    glUseProgram(pipeline1.shaderProgram)
    

    # Setting up the clear screen color
    glClearColor(0.25, 0.25, 0.25, 1.0)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Hacemos el fondo
    #esquina = es.toGPUShape(bs.createColorQuad(0, 0, 0))

    # HACEMOS LOS OBJETOS
    
    #manzana = Manzana(tamaño)
    
    estadisticas = Estadísticas()
    personas = PersonaCreator(estadisticas, Radius, Contagious_prob)
    for i in range(10):
        personas.crear_persona()
    
    personas.personas[3].enfermar()
    personas.personas[4].enfermar()

    controlador.set_personas(personas)

    

    contador = 0

    while not glfw.window_should_close(window):  # Dibujando --> 1. obtener el input
        
        t = glfw.get_time()

        # Using GLFW to check for input events
        glfw.poll_events()  # OBTIENE EL INPUT --> CONTROLADOR --> MODELOS

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)
        





   

        # DIBUJAR LOS MODELOS
        
        #snake.draw(pipeline1)
        personas.draw(pipeline1)
        #p.draw(pipeline1)
       
  

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
