import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from matplotlib.figure import Figure



# Import our graph-related modules
from graph import *
from node import *
from segment import *


from graph import DeleteNode


from tkinter import simpledialog

from graph import DeleteSegment



def delete_segment_interface(interface):
    segment_id = simpledialog.askstring("Delete Segment", "Enter Segment ID:")
    if not segment_id:
        return

    if DeleteSegment(interface.graph, segment_id):
        interface.status_var.set(f"Segment '{segment_id}' deleted.")
    else:
        interface.status_var.set(f"Segment '{segment_id}' not found.")



# Graph creation functions
def create_example_graph():
   """Creates and returns an example graph with nodes and segments."""
   graph = Graph()


   # Create nodes for the example graph
   node_a = Node("A", 0, 0)
   node_b = Node("B", 5, 5)
   node_c = Node("C", 10, 0)
   node_d = Node("D", 5, -5)


   # Add nodes to the graph
   AddNode(graph, node_a)
   AddNode(graph, node_b)
   AddNode(graph, node_c)
   AddNode(graph, node_d)


   # Add segments to the graph
   AddSegment(graph, "1", "A", "B")
   AddSegment(graph, "2", "B", "C")
   AddSegment(graph, "3", "C", "D")
   AddSegment(graph, "4", "D", "A")
   AddSegment(graph, "5", "A", "C")


   return graph




def create_custom_graph():
   """Creates and returns a custom graph with nodes and segments."""
   graph = Graph()


   # Create nodes for the custom graph
   node_p = Node("P", 0, 0)
   node_q = Node("Q", 8, 6)
   node_r = Node("R", 10, 0)
   node_s = Node("S", 5, -5)
   node_t = Node("T", 15, 5)


   # Add nodes to the graph
   AddNode(graph, node_p)
   AddNode(graph, node_q)
   AddNode(graph, node_r)
   AddNode(graph, node_s)
   AddNode(graph, node_t)


   # Add segments to the graph
   AddSegment(graph, "1", "P", "Q")
   AddSegment(graph, "2", "Q", "R")
   AddSegment(graph, "3", "R", "S")
   AddSegment(graph, "4", "S", "P")
   AddSegment(graph, "5", "P", "R")
   AddSegment(graph, "6", "Q", "T")
   AddSegment(graph, "7", "R", "T")


   return graph




# Visualization functions
def plot_single_node_view(ax, graph, node_name):
   """Plots a view showing a single node and its neighbors on the given axes."""
   # Find the target node
   target_node = None
   for node in graph.nodes:
       if node.name == node_name:
           target_node = node
           break


   if target_node is None:
       return False


   # Clear the current plot
   ax.clear()


   # Plot all nodes
   for node in graph.nodes:
       ax.plot(node.x, node.y, marker='o', linestyle='', color='black', markersize=5)
       ax.text(node.x, node.y, node.name,
               horizontalalignment='left',
               verticalalignment='bottom',
               color='red')


   # Plot the selected node's neighbors and connections
   for neighbor in target_node.neighbors:
       for segment in graph.segments:
           if (segment.origin == target_node and segment.destination == neighbor) or \
                   (segment.origin == neighbor and segment.destination == target_node):
               # Draw the segment
               ax.plot([segment.origin.x, segment.destination.x],
                       [segment.origin.y, segment.destination.y], 'blue')


               # Draw an arrow
               ax.arrow(segment.origin.x, segment.origin.y,
                        segment.destination.x - segment.origin.x,
                        segment.destination.y - segment.origin.y,
                        head_width=0.5, head_length=0.5, fc='blue', ec='blue',
                        length_includes_head=True)


               # Display the cost
               midpoint_x = (segment.origin.x + segment.destination.x) / 2
               midpoint_y = (segment.origin.y + segment.destination.y) / 2
               ax.text(midpoint_x, midpoint_y, round(segment.cost, 2))


   # Set the title to indicate which node's neighbors are being shown
   ax.set_title(f"Neighbors of node '{node_name}'")
   ax.grid(True)


   return True




def plot_full_graph(ax, graph):
   """Plots the full graph on the given axes."""
   # Clear the current plot
   ax.clear()


   # Plot all segments
   for segment in graph.segments:
       ax.plot([segment.origin.x, segment.destination.x],
               [segment.origin.y, segment.destination.y], 'blue')


       # Calculate the midpoint of the segment
       midpoint_x = segment.origin.x + (segment.destination.x - segment.origin.x) / 2
       midpoint_y = segment.origin.y + (segment.destination.y - segment.origin.y) / 2


       # Display the segment cost
       ax.text(midpoint_x, midpoint_y, round(segment.cost, 2))


       # Add an arrow to indicate direction
       ax.arrow(segment.origin.x, segment.origin.y,
                segment.destination.x - segment.origin.x,
                segment.destination.y - segment.origin.y,
                head_width=0.5, head_length=0.5, fc='blue', ec='blue',
                length_includes_head=True)


   # Plot all nodes
   for node in graph.nodes:
       ax.plot(node.x, node.y, marker='o', linestyle='', color='black', markersize=5)
       ax.text(node.x, node.y, node.name,
               horizontalalignment='left',
               verticalalignment='bottom',
               color='red',
               fontsize=7)


   # Set labels and title
   ax.set_xlabel('X')
   ax.set_ylabel('Y')
   ax.set_title("Graph Visualization")
   ax.grid(True)




# UI setup functions
def setup_ui(interface):
   """Sets up all UI components."""
   # Create frames for organizing the UI
   interface.controls_frame = tk.Frame(interface.root, padx=10, pady=10)
   interface.controls_frame.pack(side=tk.LEFT, fill=tk.Y)


   interface.plot_frame = tk.Frame(interface.root, padx=10, pady=10)
   interface.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


   # Title label
   title_label = tk.Label(interface.controls_frame, text="Graph Operations", font=("Arial", 14, "bold"))
   title_label.pack(pady=10)


   # Buttons for graph operations
   interface.example_graph_btn = tk.Button(
       interface.controls_frame,
       text="Show Example Graph",
       command=lambda: show_example_graph(interface),
       width=20,
       padx=5, pady=5
   )
   interface.example_graph_btn.pack(pady=5)


   interface.custom_graph_btn = tk.Button(
       interface.controls_frame,
       text="Show Custom Graph",
       command=lambda: show_custom_graph(interface),
       width=20,
       padx=5, pady=5
   )
   interface.custom_graph_btn.pack(pady=5)


   interface.load_graph_btn = tk.Button(
       interface.controls_frame,
       text="Load Graph from File",
       command=lambda: load_graph_from_file(interface),
       width=20,
       padx=5, pady=5
   )
   interface.load_graph_btn.pack(pady=5)


   # Node selection section
   interface.node_selection_label = tk.Label(interface.controls_frame, text="Node Selection",
                                             font=("Arial", 12, "bold"))
   interface.node_selection_label.pack(pady=(20, 5))


   interface.node_listbox_frame = tk.Frame(interface.controls_frame)
   interface.node_listbox_frame.pack(fill=tk.X, pady=5)


   interface.node_listbox = tk.Listbox(interface.node_listbox_frame, height=10, selectmode=tk.SINGLE)
   interface.node_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


   interface.node_scrollbar = tk.Scrollbar(interface.node_listbox_frame, orient=tk.VERTICAL)
   interface.node_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


   interface.node_listbox.config(yscrollcommand=interface.node_scrollbar.set)
   interface.node_scrollbar.config(command=interface.node_listbox.yview)


   interface.show_neighbors_btn = tk.Button(
       interface.controls_frame,
       text="Show Node Neighbors",
       command=lambda: show_node_neighbors(interface),
       width=20,
       padx=5, pady=5
   )
   interface.show_neighbors_btn.pack(pady=5)
   interface.add_segment_btn = tk.Button(
       interface.controls_frame,
       text="Add Segment",
       command=lambda: add_segment_interface(interface),
       width=20, padx=5, pady=5
   )
   interface.add_segment_btn.pack(pady=5)
   interface.add_node_btn = tk.Button(
       interface.controls_frame,
       text="Add Node",
       command=lambda: add_node_interface(interface),
       width=20, padx=5, pady=5
   )
   interface.add_node_btn.pack(pady=5)
   interface.delete_node_btn = tk.Button(
       interface.controls_frame,
       text="Delete Node",
       command=lambda: delete_selected_node(interface),
       width=20, padx=5, pady=5
   )
   interface.delete_node_btn.pack(pady=5)

   # Status bar
   interface.status_var = tk.StringVar()
   interface.status_var.set("Ready")
   interface.status_bar = tk.Label(interface.root, textvariable=interface.status_var, bd=1, relief=tk.SUNKEN,
                                   anchor=tk.W)
   interface.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
   interface.delete_segment_btn = tk.Button(
       interface.controls_frame,
       text="Delete Segment",
       command=lambda: delete_segment_interface(interface),
       width=20, padx=5, pady=5
   )
   interface.delete_segment_btn.pack(pady=5)
   interface.segment_selection_label = tk.Label(interface.controls_frame, text="Segment Selection",
                                                font=("Arial", 12, "bold"))
   interface.segment_selection_label.pack(pady=(20, 5))

   interface.segment_listbox_frame = tk.Frame(interface.controls_frame)
   interface.segment_listbox_frame.pack(fill=tk.X, pady=5)

   interface.segment_listbox = tk.Listbox(interface.segment_listbox_frame, height=10, selectmode=tk.SINGLE)
   interface.segment_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

   interface.segment_scrollbar = tk.Scrollbar(interface.segment_listbox_frame, orient=tk.VERTICAL)
   interface.segment_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

   interface.segment_listbox.config(yscrollcommand=interface.segment_scrollbar.set)
   interface.segment_scrollbar.config(command=interface.segment_listbox.yview)
   interface.new_graph_btn = tk.Button(
       interface.controls_frame,
       text="Create Empty Graph",
       command=lambda: create_empty_graph(interface),
       width=20, padx=5, pady=5
   )
   interface.new_graph_btn.pack(pady=5)
   interface.save_graph_btn = tk.Button(
       interface.controls_frame,
       text="Save Graph to File",
       command=lambda: save_graph_to_file(interface),
       width=20, padx=5, pady=5
   )
   interface.save_graph_btn.pack(pady=5)


def setup_figure(interface):
    """Sets up the matplotlib figure and canvas."""
    # Create a figure for the plots
    interface.fig = Figure(figsize=(6, 5), dpi=100)
    interface.ax = interface.fig.add_subplot(111)

    # ✅ Crear el canvas ANTES de usarlo
    interface.canvas = FigureCanvasTkAgg(interface.fig, master=interface.plot_frame)
    interface.canvas.draw()
    interface.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # ✅ Ahora sí puedes usar mpl_connect
    interface.canvas.mpl_connect("button_press_event", lambda event: on_canvas_click(interface, event))


def on_canvas_click(interface, event):
    if event.inaxes:
        x, y = event.xdata, event.ydata
        name = simpledialog.askstring("Node Name", "Enter a name for this node:")
        if name:
            if interface.graph.GetNodeByName(name):
                messagebox.showerror("Error", "A node with that name already exists.")
                return
            new_node = Node(name, x, y)
            AddNode(interface.graph, new_node)
            update_node_listbox(interface)
            plot_full_graph(interface.ax, interface.graph)
            interface.canvas.draw()
            interface.status_var.set(f"Node '{name}' added at ({x:.2f}, {y:.2f})")


def update_node_listbox(interface):
   """Updates the node listbox with the names of all nodes in the graph."""
   # Clear the listbox
   interface.node_listbox.delete(0, tk.END)


   # Add nodes to the listbox
   for node in interface.graph.nodes:
       interface.node_listbox.insert(tk.END, node.name)




# Button command functions
def show_example_graph(interface):
   """Displays the example graph."""
   # Use the external function to create an example graph
   interface.graph = create_example_graph()


   # Update the node listbox
   update_node_listbox(interface)



   # Plot the graph using the external function
   plot_full_graph(interface.ax, interface.graph)
   interface.canvas.draw()


   # Update status
   interface.status_var.set("Example graph loaded")

def add_segment_interface(interface):
    origin = simpledialog.askstring("Segment", "Origin node name:")
    dest = simpledialog.askstring("Segment", "Destination node name:")
    seg_id = simpledialog.askstring("Segment", "Segment ID (optional):")

    if not origin or not dest:
        return

    if not seg_id:
        seg_id = f"{origin}{dest}"  # por si no quieren poner ID

    try:
        AddSegment(interface.graph, seg_id, origin, dest)


        interface.segment_listbox.insert(tk.END, seg_id)


        plot_full_graph(interface.ax, interface.graph)
        interface.canvas.draw()
        interface.status_var.set(f"Segment {seg_id} added")
    except:
        messagebox.showerror("Error", "Failed to add segment")

def add_node_interface(interface):
    name = simpledialog.askstring("Node Name", "Enter a name for the new node:")
    if not name:
        return

    if interface.graph.GetNodeByName(name):
        messagebox.showerror("Error", "A node with that name already exists.")
        return

    x = simpledialog.askfloat("Node X", "Enter X coordinate:")
    y = simpledialog.askfloat("Node Y", "Enter Y coordinate:")

    if x is None or y is None:
        return

    new_node = Node(name, x, y)
    AddNode(interface.graph, new_node)
    update_node_listbox(interface)
    plot_full_graph(interface.ax, interface.graph)
    interface.canvas.draw()
    interface.status_var.set(f"Node '{name}' added at ({x}, {y})")


def show_custom_graph(interface):
   """Displays the custom graph."""
   # Use the external function to create a custom graph
   interface.graph = create_custom_graph()


   # Update the node listbox
   update_node_listbox(interface)



   # Plot the graph using the external function
   plot_full_graph(interface.ax, interface.graph)
   interface.canvas.draw()


   # Update status
   interface.status_var.set("Custom graph loaded")




def load_graph_from_file(interface):
   """Loads a graph from a file selected by the user."""
   # Open file dialog to select a graph file
   file_path = filedialog.askopenfilename(
       title="Select Graph File",
       filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
   )


   if file_path:
       # Load the graph from the file
       loaded_graph = LoadGraphFromFile(file_path)


       if loaded_graph:
           interface.graph = loaded_graph


           # Update the node listbox
           update_node_listbox(interface)



           # Plot the graph using the external function
           plot_full_graph(interface.ax, interface.graph)
           interface.canvas.draw()


           # Update status
           interface.status_var.set(f"Graph loaded from {file_path}")
       else:
           messagebox.showerror("Error", "Failed to load graph from file")

def create_empty_graph(interface):
    interface.graph = Graph()
    update_node_listbox(interface)
    update_segment_listbox(interface)
    plot_full_graph(interface.ax, interface.graph)
    interface.canvas.draw()
    interface.status_var.set("Empty graph created.")

def save_graph_to_file(interface):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        SaveGraphToFile(interface.graph, file_path)
        interface.status_var.set(f"Graph saved to {file_path}")


def delete_selected_node(interface):
    selection = interface.node_listbox.curselection()
    if not selection:
        messagebox.showinfo("Info", "Select a node to delete.")
        return

    name = interface.node_listbox.get(selection[0])
    DeleteNode(interface.graph, name)
    update_node_listbox(interface)
    plot_full_graph(interface.ax, interface.graph)
    interface.canvas.draw()
    interface.status_var.set(f"Node '{name}' and its segments deleted.")



def delete_selected_segment(interface):
    selection = interface.segment_listbox.curselection()
    if not selection:
        interface.status_var.set("No segment selected.")
        return

    index = selection[0]
    segment_id = interface.segment_listbox.get(index)

    if DeleteSegment(interface.graph, segment_id):
        interface.segment_listbox.delete(index)
        interface.status_var.set(f"Segment '{segment_id}' deleted.")
    else:
        interface.status_var.set(f"Segment '{segment_id}' could not be deleted.")

def show_node_neighbors(interface):
   """Displays the neighbors of the selected node."""
   # Get the selected node
   selected_indices = interface.node_listbox.curselection()


   if not selected_indices:
       messagebox.showinfo("Information", "Please select a node first")
       return


   selected_node_name = interface.node_listbox.get(selected_indices[0])


   # Use the external function to plot the node view
   success = plot_single_node_view(interface.ax, interface.graph, selected_node_name)


   if success:
       interface.canvas.draw()
       # Update status
       interface.status_var.set(f"Showing neighbors of node '{selected_node_name}'")
   else:
       messagebox.showerror("Error", f"Node '{selected_node_name}' not found in the graph")




# Main class for storing application state
class GraphInterface:
   def __init__(self, root):
       # Store references to important objects
       self.root = root
       self.root.title("Graph Visualization Tool")
       self.root.geometry("1000x750")

       # Create the main graph object
       self.graph = Graph()

       # ✅ Primero configura la UI (esto crea plot_frame y controls_frame)
       setup_ui(self)

       # ✅ Luego configura el canvas de matplotlib
       setup_figure(self)







def main():
   root = tk.Tk()
   app = GraphInterface(root)
   root.mainloop()




if __name__ == "__main__":
   main()

def update_segment_listbox(interface):
    """Updates the segment listbox with all segment IDs in the graph."""
    interface.segment_listbox.delete(0, tk.END)
    for segment in interface.graph.segments:
        interface.segment_listbox.insert(tk.END, segment.id)


