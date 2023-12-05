import networkx as nx

class Graph:
    def __init__(self):
        # Inicialización de un grafo no dirigido utilizando NetworkX
        self.graph = nx.Graph()
        # Contador para asignar códigos a los aeropuertos
        self.airport_counter = 1

    def add_airport(self, airport, location):
        # Añadir un aeropuerto al grafo con un código único y atributos de nombre y ubicación
        airport_code = self.airport_counter
        self.graph.add_node(airport_code, name=airport, location=location)
        self.airport_counter += 1
        return airport_code

    def get_airports_list(self):
        # Obtener una lista de diccionarios con información de los aeropuertos en el grafo
        airports_list = []
        for node, data in self.graph.nodes(data=True):
            airport_info = {
                'code': node,
                'name': data.get('name', 'No Name'),
                'location': data.get('location', 'No Location')
            }
            airports_list.append(airport_info)
        return airports_list

    def add_route(self, source, destination, distance, flight_time):
        # Añadir una ruta al grafo con atributos de distancia y tiempo de vuelo
        self.graph.add_edge(source, destination, distance=distance, flight_time=flight_time)

    def get_shortest_path_dis(self, source, destination):
        try:
            # Calcular la ruta más corta y su longitud utilizando el algoritmo de Dijkstra
            path = nx.dijkstra_path(self.graph, source, destination, weight='distance')
            distance = nx.dijkstra_path_length(self.graph, source, destination, weight='distance')
            return path, distance
        except nx.NetworkXNoPath:
            # Manejar la excepción si no hay ruta disponible
            return None
        
    def get_shortest_path(self, source, destination):
        try:
            # Calcular la ruta más corta y su longitud utilizando el algoritmo de Dijkstra
            path = nx.dijkstra_path(self.graph, source, destination, weight='flight_time')
            flight_time = nx.dijkstra_path_length(self.graph, source, destination, weight='flight_time')
            return path, flight_time
        except nx.NetworkXNoPath:
            # Manejar la excepción si no hay ruta disponible
            return None

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Application(tk.Tk):
    def __init__(self):
        # Inicialización de la aplicación y configuración de la ventana principal
        super().__init__()

        self.title("Gestión de Rutas Aéreas")
        self.geometry("800x580")
        self.configure(bg="#FFFFFF")

        # Inicialización de la instancia de la clase Graph
        self.graph = Graph()

        # Creación de widgets en la ventana principal
        self.create_widgets()

        # Configuración del lienzo para visualizar el grafo
        self.figure = plt.figure(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def create_widgets(self):
        # Creación de widgets en la ventana principal

        # Título
        title_label = tk.Label(self, text="      RUTAS AÉREAS      ", bg="#E4F4FD", fg="black", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        # Cuadro de color azul claro
        frame = tk.Frame(self, bg="lightblue", bd=1, relief="solid", padx=25, pady=25)
        frame.pack()

        # Botones dentro del cuadro
        button_width = 20  # Ancho deseado para los botones

        airport_button = tk.Button(frame, text="Registrar Aeropuerto", bg="#E4F4FD", command=self.register_airport, width=button_width)
        airport_button.pack(pady=5)

        route_button = tk.Button(frame, text="Crear Ruta", bg="#E4F4FD", command=self.create_route, width=button_width)
        route_button.pack(pady=5)

        edit_button = tk.Button(frame, text="Editar Ruta", bg="#E4F4FD", command=self.edit_route, width=button_width)
        edit_button.pack(pady=5)

        visualize_button = tk.Button(frame, text="Visualizar Rutas por Distancia", bg="#E4F4FD", command=self.visualize_routes, width=button_width)
        visualize_button.pack(pady=5)

        visualize_time_routes_button = tk.Button(frame, text="Visualizar Rutas por Tiempo", bg="#E4F4FD", command=self.visualize_time_routes, width=button_width)
        visualize_time_routes_button.pack(pady=5)


        airports_button = tk.Button(frame, text="Lista de Aeropuertos", bg="#E4F4FD", command=self.display_airports, width=button_width)
        airports_button.pack(pady=5)

        # Título
        title_label = tk.Label(self, text=" BÚSQUEDA DE RUTAS ", bg="#E4F4FD", fg="black", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        # Cuadro de color azul claro
        frame = tk.Frame(self, bg="lightblue", bd=1, relief="solid", padx=25, pady=25)
        frame.pack()

        # Botones dentro del cuadro
        label_width = 20  # Ancho deseado para los botones

        origin_label = tk.Label(frame, text="Aeropuerto de Origen", width=label_width, bg=frame.cget("bg"))
        origin_label.pack(pady=5)
        self.origin_entry = tk.Entry(frame)
        self.origin_entry.pack()

        destination_label = tk.Label(frame, text="Aeropuerto de Destino", width=label_width, bg=frame.cget("bg"))
        destination_label.pack(pady=10)
        self.destination_entry = tk.Entry(frame)
        self.destination_entry.pack()

        search_button = tk.Button(frame, text="Buscar Ruta por Distancia", bg="#E4F4FD", command=self.search_route, width=label_width)
        search_button.pack(pady=10)

        search_shortest_time_button = tk.Button(frame, text="Buscar Ruta por Tiempo Corto", bg="#E4F4FD", command=self.search_shortest_time_route, width=button_width)
        search_shortest_time_button.pack(pady=5)


    def register_airport(self):
        # Crear una nueva ventana superior para registrar aeropuertos
        register_window = tk.Toplevel(self)
        register_window.title("Registrar Aeropuerto")

        # Crear campos de entrada para el nombre y la ubicación del aeropuerto
        self.create_input_field(register_window, "Nombre:", "name_entry")
        self.create_input_field(register_window, "Ubicación:", "location_entry")

        # Agregar un botón de guardar que llama a la función 'save_airport' cuando se presiona
        save_button = tk.Button(register_window, text="Guardar", command=self.save_airport)
        save_button.pack()

    def create_input_field(self, window, label_text, entry_name):
        # Crear una etiqueta con el texto proporcionado y agregarla a la ventana
        label = tk.Label(window, text=label_text)
        label.pack()

        # Crear un campo de entrada utilizando ttk.Entry y agregarlo a la ventana
        entry = ttk.Entry(window)
        entry.pack()

        # Establecer el atributo de la instancia con el nombre proporcionado para referenciar el campo de entrada
        setattr(self, entry_name, entry)

    def save_airport(self):
        name = self.name_entry.get()
        location = self.location_entry.get()

        if name and location:
            if not any('name' in node_data and node_data['name'] == name for _, node_data in self.graph.graph.nodes(data=True)):
                airport_code = self.graph.add_airport(name, location)
                messagebox.showinfo("Aeropuerto registrado", f"Aeropuerto '{name}' registrado exitosamente con código {airport_code}.")
                self.update_graph()
                self.name_entry.delete(0, tk.END)
                self.location_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Ya existe un aeropuerto con este nombre.")
        else:
            messagebox.showerror("Error", "Todos los campos son requeridos.")

    def create_route(self):
        create_route_window = tk.Toplevel(self)
        create_route_window.title("Crear Ruta")

        source_label = tk.Label(create_route_window, text="Código de Aeropuerto de Origen:")
        source_entry = tk.Entry(create_route_window)
        source_label.pack()
        source_entry.pack()

        destination_label = tk.Label(create_route_window, text="Código de Aeropuerto de Destino:")
        destination_entry = tk.Entry(create_route_window)
        destination_label.pack()
        destination_entry.pack()

        distance_label = tk.Label(create_route_window, text="Distancia:")
        distance_entry = tk.Entry(create_route_window)
        distance_label.pack()
        distance_entry.pack()

        flight_time_label = tk.Label(create_route_window, text="Tiempo de vuelo:")
        flight_time_entry = tk.Entry(create_route_window)
        flight_time_label.pack()
        flight_time_entry.pack()

        save_button = tk.Button(create_route_window, text="Guardar",
                                command=lambda: self.save_route(source_entry.get(), 
                                                                destination_entry.get(), 
                                                                distance_entry.get(), 
                                                                flight_time_entry.get(),
                                                                create_route_window))
        save_button.pack()

    def save_route(self, source_code, destination_code, distance, flight_time, window):
        try:
            source_code = int(source_code)
            destination_code = int(destination_code)
            self.graph.add_route(source_code, destination_code, float(distance), float(flight_time))
            messagebox.showinfo("Ruta creada", "Ruta creada exitosamente.")
            window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Códigos de aeropuerto, distancia y tiempo de vuelo deben ser números válidos.")
        except nx.NodeNotFound:
            messagebox.showerror("Error", "Aeropuerto no encontrado. Por favor, registra los aeropuertos primero.")

    def edit_route(self):
        edit_route_window = tk.Toplevel(self)
        edit_route_window.title("Editar Ruta")

        source_label = tk.Label(edit_route_window, text="Aeropuerto de Origen:")
        source_entry = tk.Entry(edit_route_window)
        source_label.pack()
        source_entry.pack()

        destination_label = tk.Label(edit_route_window, text="Aeropuerto de Destino:")
        destination_entry = tk.Entry(edit_route_window)
        destination_label.pack()
        destination_entry.pack()

        distance_label = tk.Label(edit_route_window, text="Nueva Distancia:")
        distance_entry = tk.Entry(edit_route_window)
        distance_label.pack()
        distance_entry.pack()

        flight_time_label = tk.Label(edit_route_window, text="Nuevo Tiempo de Vuelo:")
        flight_time_entry = tk.Entry(edit_route_window)
        flight_time_label.pack()
        flight_time_entry.pack()

        save_button = tk.Button(edit_route_window, text="Guardar",
                                command=lambda: self.update_route(source_entry.get(), destination_entry.get(),
                                                                  distance_entry.get(), flight_time_entry.get(),
                                                                  edit_route_window))
        save_button.pack()

    def visualize_routes(self):
        graph_window = tk.Toplevel(self)
        graph_window.title("Visualizar Rutas")

        # Crear un nuevo lienzo para mostrar el grafo
        figure = plt.figure(figsize=(10, 6))
        canvas = FigureCanvasTkAgg(figure, master=graph_window)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Obtener la información del nodo para etiquetar los nodos con el nombre del aeropuerto
        node_labels = {node: self.graph.graph.nodes[node]['name'] for node in self.graph.graph.nodes}

        # Dibujar el grafo en el lienzo con los nombres de los aeropuertos
        pos = nx.spring_layout(self.graph.graph)
        nx.draw(self.graph.graph, pos, with_labels=True, labels=node_labels, node_color='skyblue', node_size=800)
        labels = nx.get_edge_attributes(self.graph.graph, 'distance')
        nx.draw_networkx_edge_labels(self.graph.graph, pos, edge_labels=labels)

        # Actualizar el lienzo
        canvas.draw()

        # Añadido para mostrar la ventana
        graph_window.mainloop()

    def visualize_time_routes(self):
        graph_window = tk.Toplevel(self)
        graph_window.title("Visualizar Rutas por Tiempo de Vuelo")

        figure = plt.figure(figsize=(10, 6))
        canvas = FigureCanvasTkAgg(figure, master=graph_window)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        node_labels = {node: self.graph.graph.nodes[node]['name'] for node in self.graph.graph.nodes}
        pos = nx.spring_layout(self.graph.graph)
        nx.draw(self.graph.graph, pos, with_labels=True, labels=node_labels, node_color='skyblue', node_size=800)
        labels = nx.get_edge_attributes(self.graph.graph, 'flight_time')
        nx.draw_networkx_edge_labels(self.graph.graph, pos, edge_labels=labels)

        canvas.draw()

    def update_graph(self):
        self.figure.clear()
        pos = nx.spring_layout(self.graph.graph)
        nx.draw(self.graph.graph, pos, with_labels=True, node_color='skyblue', node_size=800)
        labels = nx.get_edge_attributes(self.graph.graph, 'distance')
        nx.draw_networkx_edge_labels(self.graph.graph, pos, edge_labels=labels)

    def update_route(self, source, destination, distance, flight_time, window):
        if source and destination and distance and flight_time:
            try:
                source = int(source)
                destination = int(destination)

                if self.graph.graph.has_edge(source, destination):
                    self.graph.graph[source][destination]['distance'] = float(distance)
                    self.graph.graph[source][destination]['flight_time'] = float(flight_time)
                    self.update_graph()  # Asegúrate de llamar correctamente al método update_graph
                    messagebox.showinfo("Ruta actualizada", "Ruta actualizada exitosamente.")
                    window.destroy()
                else:
                    messagebox.showerror("Error", "La ruta especificada no existe.")
            except ValueError:
                messagebox.showerror("Error", "Códigos de aeropuerto deben ser números válidos.")
        else:
            messagebox.showerror("Error", "Todos los campos son requeridos.")

    def search_route(self):
        # Obtener referencias a las entradas de origen y destino
        origin_entry = self.origin_entry
        destination_entry = self.destination_entry

        # Verificar si las entradas están en la ventana principal o en una ventana secundaria
        if not self.origin_entry.winfo_ismapped():
            # Si no están mapeadas, buscar en la ventana secundaria
            origin_entry = self.origin_entry.in_toplevel()
            destination_entry = self.destination_entry.in_toplevel()

        # Verificar si la ventana secundaria aún existe
        if origin_entry.winfo_exists() and destination_entry.winfo_exists():
            origin_code = origin_entry.get()
            destination_code = destination_entry.get()

            if origin_code and destination_code:
                try:
                    origin_code = int(origin_code)
                    destination_code = int(destination_code)
                    result = self.graph.get_shortest_path_dis(origin_code, destination_code)
                    if result:
                        path, distance = result
                        airport_names = [self.graph.graph.nodes[node]['name'] for node in path]
                        messagebox.showinfo("Ruta encontrada", f"Ruta encontrada:\n\n"
                                                            f"Ruta: {' -> '.join(map(str, airport_names))}\n"
                                                            f"Distancia: {distance} km\n")
                    else:
                        messagebox.showerror("Error", "No se encontró una ruta entre los aeropuertos especificados.")
                except ValueError:
                    messagebox.showerror("Error", "Códigos de aeropuerto deben ser números válidos.")
            else:
                messagebox.showerror("Error", "Todos los campos son requeridos.")
        else:
            messagebox.showerror("Error", "La ventana de edición de rutas ha sido cerrada.")

    def search_shortest_time_route(self):
        # Obtener referencias a las entradas de origen y destino
        origin_entry = self.origin_entry
        destination_entry = self.destination_entry

        # Verificar si las entradas están en la ventana principal o en una ventana secundaria
        if not self.origin_entry.winfo_ismapped():
            # Si no están mapeadas, buscar en la ventana secundaria
            origin_entry = self.origin_entry.in_toplevel()
            destination_entry = self.destination_entry.in_toplevel()

        # Verificar si la ventana secundaria aún existe
        if origin_entry.winfo_exists() and destination_entry.winfo_exists():
            origin_code = origin_entry.get()
            destination_code = destination_entry.get()

            if origin_code and destination_code:
                try:
                    origin_code = int(origin_code)
                    destination_code = int(destination_code)
                    result = self.graph.get_shortest_path(origin_code, destination_code)
                    if result:
                        path, flight_time = result
                        airport_names = [self.graph.graph.nodes[node]['name'] for node in path]
                        messagebox.showinfo("Ruta encontrada", f"Ruta encontrada:\n\n"
                                                            f"Ruta: {' -> '.join(map(str, airport_names))}\n"
                                                            f"Tiempo de vuelo: {flight_time} horas")
                    else:
                        messagebox.showerror("Error", "No se encontró una ruta entre los aeropuertos especificados.")
                except ValueError:
                    messagebox.showerror("Error", "Códigos de aeropuerto deben ser números válidos.")
            else:
                messagebox.showerror("Error", "Todos los campos son requeridos.")
        else:
            messagebox.showerror("Error", "La ventana de edición de rutas ha sido cerrada.")

    def display_airports(self):
        # Obtener la lista de aeropuertos y crear una nueva ventana para mostrarla
        airports_list = self.graph.get_airports_list()
        airports_window = tk.Toplevel(self)
        airports_window.title("Lista de Aeropuertos")

        # Crear un nuevo marco para mostrar la lista de aeropuertos
        frame = tk.Frame(airports_window, bg="white", bd=1, relief="solid", padx=25, pady=25)
        frame.pack()

        # Crear etiquetas para mostrar la lista de aeropuertos
        for airport in airports_list:
            airport_info = f"Código: {airport['code']}, Nombre: {airport['name']}, Ubicación: {airport['location']}"
            airport_label = tk.Label(frame, text=airport_info, bg=frame.cget("bg"))
            airport_label.pack()
        
if __name__ == "__main__":
    app = Application()
    app.mainloop()