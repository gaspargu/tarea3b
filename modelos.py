"""
Este archivo generaría todos los modelos que tiene la aplicación. En programas más complicados
tendríamos una cosa así:

src/models/actor/chansey.py
src/models/actor/egg.py
src/models/factory/eggcreator.py

...
Y este archivo sería algo como
src/models/model.py --> sólo importaría los objetos que usa el resto de la aplicación, sin tocar el detalle mismo

from src.models.actor.chansey import Chansey
from src.models.actor.factory import EggCreator
...

Pero aquí, como nuestra app es sencilla, definimos todas las clases aquí mismo.
1. Chansey
2. Los huevos
"""

import math
import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es



from OpenGL.GL import *
import random
import numpy as np
from typing import List

d = 1

class Persona(object):
    def __init__(self):

        self.pos = None
        self.estado = 'Sana'

        gpu_triangulo_cian = es.toGPUShape(bs.createColorTriangle(0, 0.5, 0.95))  
          
        triangulo_cian = sg.SceneGraphNode('triangulo')
        triangulo_cian.transform = tr.uniformScale(0.05)
        triangulo_cian.childs = [gpu_triangulo_cian]

        persona = sg.SceneGraphNode('persona') 
        persona.childs = [triangulo_cian]

        self.model = persona
        
      
        
    def draw(self, pipeline):

        sg.drawSceneGraphNode(self.model, pipeline, 'transform')

    # funcion que revisa si una persona está al alcance de otra
    def esta_en_radio(self, p: 'Persona', radio):
        distancia = np.sqrt((self.pos[0]-p.pos[0])**2+(self.pos[1]-p.pos[1])**2)
        return distancia<radio


    def enfermar(self):
        gpu_triangulo_rojo = es.toGPUShape(bs.createColorTriangle(1, 0, 0))

        self.estado = 'Enferma'
        triangulo = sg.findNode(self.model, 'triangulo')
        triangulo.childs = [gpu_triangulo_rojo]

class PersonaCreator(object):
    def __init__(self, estadisticas: 'Estadísiticas', radio, prob):
        personas: List['Persona']
        self.personas = []
        self.est = estadisticas
        self.radio = radio
        self.prob = prob
       

    def draw(self, pipeline):
        for k in self.personas:
            k.draw(pipeline)
    

    def crear_persona(self):
        p = Persona()
        p.pos = [random.uniform(-0.95,0.95), random.uniform(-0.95,0.95)]
        p.model.transform = tr.translate(p.pos[0], p.pos[1],0)
        self.personas.append(p)


    def pasa_dia(self):

        print('Día',self.est.dias[-1])
        self.est.dias.append(self.est.dias[-1]+1)
        numero_enfermos = 0
        for k in self.personas:
            if k.estado == 'Enferma':
                for e in self.personas:
                    if e.estado == 'Sana' and k.esta_en_radio(e, self.radio) and random.random()<self.prob:
                        e.estado = 'Contagiada'
                        e.enfermar()
                        numero_enfermos += 1

        

            x = k.pos[0]+0.2*random.uniform(-1,1)
            y = k.pos[1]+0.2*random.uniform(-1,1)
            if x > 0.95:
                x = 0.95
            if x < -0.95:
                x = -0.95
            if y > 0.95:
                y = 0.95
            if y < -0.95:
                y = -0.95
            
            k.model.transform = tr.translate(x, y,0)
            k.pos = [x, y]

        for k in self.personas:
            if k.estado == 'Contagiada':
                k.estado = 'Enferma'

        self.est.enfermos.append(self.est.enfermos[-1]+numero_enfermos)





class Estadísticas(object): 
    def __init__(self):
        self.dias = [1]
        self.muertos = [0]
        self.enfermos = [2]

    










class Fondo(object):

    def __init__(self, tamaño):
        self.tamaño = tamaño

        # Figuras básicas
        gpu_esquina_quad = es.toGPUShape(bs.createColorQuad(0, 0, 0))  # negro
        gpu_grilla_quad = es.toGPUShape(bs.createColorQuad(0.9, 0.9, 0.9))  # gris
        gpu_gameover = es.toGPUShape(bs.createColorQuad(0, 0, 1)) # azul

        gameover = sg.SceneGraphNode('gameover')
        gameover.transform = tr.uniformScale(2)
        gameover.child = [gpu_gameover]

        esquina_vertical = sg.SceneGraphNode('esquinaVertical')
        esquina_vertical.transform = tr.scale(d*4/self.tamaño,2,1)
        esquina_vertical.childs += [gpu_esquina_quad]

        esquina_horizontal = sg.SceneGraphNode('esquinaHorizontal')
        esquina_horizontal.transform = tr.scale(2,d*4/self.tamaño,1)
        esquina_horizontal.childs += [gpu_esquina_quad]

        esquina_der = sg.SceneGraphNode('esquinaDerecha')
        esquina_der.transform = tr.translate(1,0,0)
        esquina_der.childs += [esquina_vertical]

        esquina_izq = sg.SceneGraphNode('esquinaIzquierda')
        esquina_izq.transform = tr.translate(-1,0,0)
        esquina_izq.childs += [esquina_vertical]

        esquina_sup = sg.SceneGraphNode('esquinaIzquierda')
        esquina_sup.transform = tr.translate(0,1,0)
        esquina_sup.childs += [esquina_horizontal]

        esquina_inf = sg.SceneGraphNode('esquinaIzquierda')
        esquina_inf.transform = tr.translate(0,-1,0)
        esquina_inf.childs += [esquina_horizontal]

        cuadrado = sg.SceneGraphNode('cuadrado')
        cuadrado.transform = tr.uniformScale(d*2/self.tamaño)
        cuadrado.childs += [gpu_grilla_quad]

        grilla = sg.SceneGraphNode('grilla')
        grilla.transform = tr.translate(-1+d*3/self.tamaño, 1-d*3/self.tamaño,1)
        grilla.childs += [cuadrado]

        fondo = sg.SceneGraphNode('fondo')

        baseName = "cuadrado"
        for i in range(math.ceil(tamaño/2)-1):
            for j in range(tamaño):
                if j%2==0:
                    x = -1 + d*(3/self.tamaño + 4*i/self.tamaño)
                    y = -1 + d*(3/self.tamaño + 2*j/self.tamaño)
                else:
                    x = -1 + d*(5/self.tamaño + 4*i/self.tamaño)
                    y = -1 + d*(3/self.tamaño + 2*j/self.tamaño)
                newNode = sg.SceneGraphNode(baseName + str(i))
                newNode.transform = tr.translate(x ,y , 1)
                newNode.childs += [cuadrado]
                fondo.childs += [newNode]
        
        fondo.childs += [esquina_der, esquina_izq, esquina_sup, esquina_inf]

        self.model = fondo

    
    def choca_esquina(self, snake: 'Snake'):
        condicionx = snake.pos[0][0] > 1 - d*2/snake.tamaño or snake.pos[0][0] < -1 + d*2/snake.tamaño 
        condiciony = snake.pos[0][1] > 1 - d*2/snake.tamaño or snake.pos[0][1] < -1 + d*2/snake.tamaño
        condicion_come_cola = snake.comio_cola
        if condicionx or condiciony or condicion_come_cola:
            gpu_gameover = es.toGPUShape(bs.createTextureQuad('gameover.png'), GL_REPEAT, GL_NEAREST) # azul

            gameover = sg.SceneGraphNode('gameover')
            gameover.transform = tr.uniformScale(2)
            gameover.childs += [gpu_gameover]

            self.model = gameover
            snake.die = True

    def draw(self, pipeline1, pipeline2, snake: 'Snake'):
        self.choca_esquina(snake)
        if snake.die:
            glUseProgram(pipeline2.shaderProgram)
            sg.drawSceneGraphNode(self.model, pipeline2, 'transform')
        else:
            glUseProgram(pipeline1.shaderProgram)
            sg.drawSceneGraphNode(self.model, pipeline1, 'transform')
        

class Snake(object):
    def __init__(self, tamaño):
        self.tamaño = tamaño

        #centra la cabeza de la serpiente al comienzo
        if self.tamaño%2 == 0:
            self.pos = [[d/self.tamaño,d/self.tamaño],[d*3/self.tamaño,d/self.tamaño],[d*5/tamaño,d/self.tamaño],[d*7/tamaño,d/self.tamaño]]
            #self.pos = [[1/self.tamaño,1/self.tamaño],[3/self.tamaño,1/self.tamaño],[5/tamaño,1/self.tamaño]]
        else:
            self.pos = [[0,0],[d*2/self.tamaño,0],[d*4/self.tamaño,0],[d*6/self.tamaño,0]]
            #self.pos = [[0,0],[2/self.tamaño,0],[4/self.tamaño,0]]
        #self.dir = [['left','left'],['left','left'],['left','left']]
        self.dir = [['left','left'],['left','left'],['left','left'],['left','left']]

        self.die = False
        self.comio = False
        self.comio_cola = False
        self.comiendo = False

        # Figuras básicas
        #gpu_trozo = es.toGPUShape(bs.createColorQuad(0, 0.3, 0))  # verde
        gpu_trozo = es.toGPUShape(bs.createTextureQuad('cuerpo.png'), GL_REPEAT, GL_NEAREST)
        gpu_trozo_cabeza =  es.toGPUShape(bs.createTextureQuad('cabeza.png'), GL_REPEAT, GL_NEAREST)

        

        trozo = sg.SceneGraphNode('trozo')
        trozo.transform = tr.uniformScale(d*2/self.tamaño)
        trozo.childs += [gpu_trozo]

        trozo_cabeza = sg.SceneGraphNode('trozo')
        trozo_cabeza.transform = tr.uniformScale(d*2/self.tamaño)
        trozo_cabeza.childs += [gpu_trozo_cabeza]
        
        cuerpo = sg.SceneGraphNode('cuerpo')
        cuerpo.childs += [trozo]

        cuerpo2 = sg.SceneGraphNode('cuerpo2')
        cuerpo2.childs += [trozo]

        cola = sg.SceneGraphNode('cola')
        cola.childs += [trozo]

        cabeza = sg.SceneGraphNode('cabeza')
        cabeza.childs += [trozo_cabeza]

        self.serpiente =[cabeza,cuerpo,cuerpo2,cola]
        #self.serpiente =[cabeza,cuerpo,cola]
        
        self.tiempo = 0



    def draw(self, pipeline):
        for i in range(len(self.serpiente)):
            glUseProgram(pipeline.shaderProgram)
            self.serpiente[i].transform = tr.translate(self.pos[i][0], self.pos[i][1], 0)
            sg.drawSceneGraphNode(self.serpiente[i], pipeline, "transform")


    def update(self):
        for i in range(len(self.dir)):
            new_dir = self.dir[i][0]
            if new_dir == 'left':
                self.pos[i][0] -= d*2/self.tamaño
                
            elif new_dir == 'right':
                self.pos[i][0] += d*2/self.tamaño
            
            elif new_dir == 'up':
                self.pos[i][1] += d*2/self.tamaño 
            
            elif new_dir == 'down':
                self.pos[i][1] -= d*2/self.tamaño
               

    def move_left(self):
        old_dir = self.dir[0][1]
        if old_dir != 'right':
            self.dir[0][0] = 'left'  
            
    def move_right(self):
        old_dir = self.dir[0][1]
        if old_dir != 'left':
            self.dir[0][0] = 'right'            

    def move_up(self):
        old_dir = self.dir[0][1]
        if old_dir != 'down':
            self.dir[0][0] = 'up' 

    def move_down(self):
        old_dir = self.dir[0][1]
        if old_dir != 'up':
            self.dir[0][0] = 'down'

    def come_manzana(self, manzana: 'Manzana'):
        #if math.trunc(100*manzana.pos_x) == math.trunc(100*self.pos[0][0]) and math.trunc(100*manzana.pos_y) == math.trunc(100*self.pos[0][1]):
        if abs(manzana.pos_x - self.pos[0][0]) < d*0.5/self.tamaño and abs(manzana.pos_y - self.pos[0][1])< d*0.5/self.tamaño:
            self.comio = True

    def come_cola(self):
        for i in range(1,len(self.pos)):
            if abs(self.pos[0][0] - self.pos[i][0]) < d/self.tamaño and abs(self.pos[0][1] - self.pos[i][1]) < d/self.tamaño:
                self.comio_cola = True


    def crece(self):
        tamaño_snake = len(self.dir)
        direccion_cola = self.dir[-1][1]
        #self.pos += [self.pos[-1]]
        if direccion_cola == 'left':
            self.pos += [[self.pos[-1][0], self.pos[-1][1]]]
        elif direccion_cola == 'right':
            self.pos +=[[self.pos[-1][0], self.pos[-1][1]]]
        elif direccion_cola == 'up':
            self.pos += [[self.pos[-1][0], self.pos[-1][1]]]
        else:
            self.pos += [[self.pos[-1][0], self.pos[-1][1]]]
        self.dir += [['stop','stop']]
  

        gpu_trozo = es.toGPUShape(bs.createTextureQuad('cuerpo.png'), GL_REPEAT, GL_NEAREST)

        trozo = sg.SceneGraphNode('trozo')
        trozo.transform = tr.uniformScale(d*2/self.tamaño)
        trozo.childs += [gpu_trozo]

        aum = sg.SceneGraphNode(str(tamaño_snake))
        aum.childs += [trozo]

        self.serpiente += [aum]
             


class Manzana(object):
    def __init__(self, tamaño):
        self.tamaño = tamaño

        gpu_circulo = es.toGPUShape(bs.createCircle(d/self.tamaño))  # rojo
        gpu_triangulo = es.toGPUShape(bs.createColorTriangle(0, 0.8, 0)) #verde

        coronta = sg.SceneGraphNode('coronta')
        coronta.childs += [gpu_circulo]

        hoja = sg.SceneGraphNode('hoja')
        hoja.transform = tr.matmul([tr.uniformScale(d/self.tamaño),tr.translate(0,0.6,0)])
        hoja.childs += [gpu_triangulo]

        self.pos_x = -1 + d*3/self.tamaño + d*2/self.tamaño*random.randint(0,self.tamaño-3)
        self.pos_y = -1 + d*3/self.tamaño + d*2/self.tamaño*random.randint(0,self.tamaño-3)

        manzana = sg.SceneGraphNode('manzana')
        manzana.childs += [coronta, hoja]
        self.model = manzana


    def draw(self, pipeline):
        self.model.transform = tr.translate(self.pos_x,self.pos_y,0)
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')

    def malpuesta(self, snake: 'Snake'):
        for i in range(len(snake.pos)):
            if abs(self.pos_x - self.pos[i][0]) < d*0.5/self.tamaño and abs(self.pos[i][0] - self.pos[i][0]) < d*0.5/self.tamaño:
                self.comio_cola = True

    def fue_comida(self, snake: 'Snake'):
        self.pos_x = -1 + d*3/self.tamaño + d*2/self.tamaño*random.randint(0,self.tamaño-3)
        self.pos_y = -1 + d*3/self.tamaño + d*2/self.tamaño*random.randint(0,self.tamaño-3)
















