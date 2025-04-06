import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt




class Node:
   """Clase para representar un nodo en el grafo."""


   def __init__(self, name, x, y):
       self.name = name
       self.x = x
       self.y = y
       self.neighbors = []




class Segment:
   """Clase para representar un segmento entre dos nodos en el grafo."""


   def __init__(self, origin, destination, name, cost=0):
       self.origin = origin
       self.destination = destination
       self.name = name
       self.cost = cost




class Graph:
   """Clase para representar un grafo."""


   def __init__(self):
       self.nodes = []  # Lista de nodos
       self.segments = []  # Lista de segmentos


   def reset_graph(self):
       """Reinicia los nodos y segmentos del grafo."""
       self.nodes.clear()
       self.segments.clear()


   def add_node(self, node):
       """Agrega un nodo al grafo."""
       self.nodes.append(node)


   def add_segment(self, segment):
       """Agrega un segmento al grafo."""
       self.segments.append(segment)


   def remove_node(self, node):
       """Elimina un nodo del grafo y todos los segmentos asociados a él."""
       self.nodes = [n for n in self.nodes if n != node]
       self.segments = [s for s in self.segments if s.origin != node and s.destination != node]


   def save_to_file(self, file_path):
       """Guarda el grafo en un archivo (formato: NODOS y SEGMENTOS)."""
       with open(file_path, "w") as f:
           for node in self.nodes:
               f.write(f"NODE {node.name} {node.x} {node.y}\n")
           for segment in self.segments:
               f.write(f"SEGMENT {segment.name} {segment.origin.name} "
                       f"{segment.destination.name} {segment.cost}\n")




class GraphApp:
   """Aplicación gráfica para interactuar con el grafo."""


   def __init__(self, root):
       self.root = root
       self.root.title("Graph Interface")
       self.graph = Graph()


       # Canvas para dibujar el grafo
       self.canvas = tk.Canvas(self.root, width=600, height=400, bg="white")
       self.canvas.pack()


       # Variables para interactividad
       self.selected_nodes = []  # Para agregar segmentos


       # Crear controles
       self.create_controls()


   def create_controls(self):
       """Crea los botones y controles de la interfaz."""
       control_frame = tk.Frame(self.root)
       control_frame.pack()


       # Botón: Agregar nodo
       btn_add_node = tk.Button(control_frame, text="Agregar Nodo", command=self.enable_add_node)
       btn_add_node.grid(row=0, column=0, padx=5, pady=5)


       # Botón: Agregar segmento
       btn_add_segment = tk.Button(control_frame, text="Agregar Segmento", command=self.enable_add_segment)
       btn_add_segment.grid(row=0, column=1, padx=5, pady=5)


       # Botón: Eliminar nodo
       btn_remove_node = tk.Button(control_frame, text="Eliminar Nodo", command=self.enable_remove_node)
       btn_remove_node.grid(row=0, column=2, padx=5, pady=5)


       # Botón: Rediseñar grafo
       btn_design_new_graph = tk.Button(control_frame, text="Nuevo Grafo", command=self.design_new_graph)
       btn_design_new_graph.grid(row=0, column=3, padx=5, pady=5)


       # Botón: Guardar grafo
       btn_save_graph = tk.Button(control_frame, text="Guardar Grafo", command=self.save_graph_to_file)
       btn_save_graph.grid(row=0, column=4, padx=5, pady=5)


   def enable_add_node(self):
       """Habilita el modo para agregar nodos."""
       self.canvas.bind("<Button-1>", self.add_node_with_click)


   def add_node_with_click(self, event):
       """Agrega un nodo al dar clic en el canvas."""
       x, y = event.x, event.y
       name = f"Nodo_{len(self.graph.nodes) + 1}"  # Nombre del nodo
       new_node = Node(name, x, y)
       self.graph.add_node(new_node)
       self.draw_graph()


   def enable_add_segment(self):
       """Habilita el modo para agregar segmentos entre dos nodos."""
       self.selected_nodes = []
       self.canvas.bind("<Button-1>", self.add_segment_with_click)


   def add_segment_with_click(self, event):
       """Crea un segmento seleccionando dos nodos consecutivamente."""
       for node in self.graph.nodes:
           if abs(node.x - event.x) < 10 and abs(node.y - event.y) < 10:  # Selección con tolerancia
               self.selected_nodes.append(node)
               break


       if len(self.selected_nodes) == 2:
           origin, destination = self.selected_nodes
           name = f"{origin.name}-{destination.name}"
           cost = ((origin.x - destination.x) ** 2 + (origin.y - destination.y) ** 2) ** 0.5  # Distancia euclidiana
           new_segment = Segment(origin, destination, name, cost)
           self.graph.add_segment(new_segment)
           self.selected_nodes = []
           self.draw_graph()


   def enable_remove_node(self):
       """Habilita el modo para eliminar nodos."""
       self.canvas.bind("<Button-1>", self.remove_node_with_click)


   def remove_node_with_click(self, event):
       """Elimina un nodo (y sus segmentos) al dar clic sobre él."""
       for node in self.graph.nodes:
           if abs(node.x - event.x) < 10 and abs(node.y - event.y) < 10:  # Tolerancia de selección
               self.graph.remove_node(node)
               self.draw_graph()
               break


   def design_new_graph(self):
       """Reinicia el grafo para comenzar desde cero."""
       self.graph.reset_graph()
       self.draw_graph()


   def save_graph_to_file(self):
       """Guarda el grafo actual en un archivo."""
       file_path = filedialog.asksaveasfilename(
           title="Guardar grafo como",
           filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
       )
       if file_path:
           self.graph.save_to_file(file_path)


   def draw_graph(self):
       """Dibuja el grafo completo en la ventana."""
       self.canvas.delete("all")  # Limpiar el canvas
       for segment in self.graph.segments:
           self.canvas.create_line(segment.origin.x, segment.origin.y,
                                   segment.destination.x, segment.destination.y, fill="blue")
           mid_x = (segment.origin.x + segment.destination.x) / 2
           mid_y = (segment.origin.y + segment.destination.y) / 2
           self.canvas.create_text(mid_x, mid_y, text=f"{segment.cost:.1f}", fill="blue")


       for node in self.graph.nodes:
           self.canvas.create_oval(node.x - 10, node.y - 10, node.x + 10, node.y + 10, fill="red")
           self.canvas.create_text(node.x, node.y - 15, text=node.name, fill="black")




if __name__ == "__main__":
   root = tk.Tk()
   app = GraphApp(root)
   root.mainloop()
