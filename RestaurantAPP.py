from __future__ import annotations
from dataclasses import dataclass, field
import tkinter as tk
from tkinter import ttk

@dataclass(eq=False)
class DecisionNode:
    name: str
    children: dict[str, DecisionNode] = field(default_factory=dict)

    def add_child(self, branch_name: str, child: DecisionNode) -> None:
        if not branch_name:
            raise ValueError("Branch name cannot be empty.")
        if branch_name in self.children:
            raise ValueError(f"Branch '{branch_name}' already exists.")
        self.children[branch_name] = child

    def get_child(self, branch_name: str) -> DecisionNode | None:
        return self.children.get(branch_name)

    def is_leaf(self) -> bool:
        return not self.children

def build_restaurant_tree() -> DecisionNode:
    root = DecisionNode("Restaurant System")

    customer = DecisionNode("Customer Operations")
    staff = DecisionNode("Staff Operations")
    menu_node = DecisionNode("Menu Management")

    root.add_child("customer", customer)
    root.add_child("staff", staff)
    root.add_child("menu", menu_node)

    m_foods = DecisionNode("Food Categories")
    m_drinks = DecisionNode("Drink Categories")
    m_desserts = DecisionNode("Dessert Categories")

    menu_node.add_child("foods", m_foods)
    menu_node.add_child("drinks", m_drinks)
    menu_node.add_child("desserts", m_desserts)

    m_foods.add_child("lentil_soup", DecisionNode("Lentil Soup ($6)"))
    m_foods.add_child("tomato_soup", DecisionNode("Tomato Soup ($7)"))
    m_foods.add_child("beef_steak", DecisionNode("Beef Steak ($25)"))
    m_foods.add_child("caesar_salad", DecisionNode("Caesar Salad ($9)"))

    m_drinks.add_child("turkish_tea", DecisionNode("Turkish Tea ($3)"))
    m_drinks.add_child("espresso", DecisionNode("Espresso ($4)"))

    m_desserts.add_child("baklava", DecisionNode("Pistachio Baklava ($8)"))
    m_desserts.add_child("magnolia", DecisionNode("Strawberry Magnolia ($7)"))

    waiter_ops = DecisionNode("Waiter Assignment")
    chef_ops = DecisionNode("Kitchen Duty")
    staff.add_child("waiters", waiter_ops)
    staff.add_child("chefs", chef_ops)

    for w_idx in [1, 2, 3]:
        w_node = DecisionNode(f"Waiter {w_idx}")
        waiter_ops.add_child(f"waiter_{w_idx}", w_node)
        for t_idx in [1, 2, 3]:
            w_node.add_child(f"table_{t_idx}", DecisionNode(f"Waiter {w_idx} is at table {t_idx}"))

    foods_list = [("lentil_soup", "Lentil Soup"), ("tomato_soup", "Tomato Soup"), ("beef_steak", "Beef Steak"), ("baklava", "Baklava")]
    for c_idx in [1, 2, 3]:
        c_node = DecisionNode(f"Chef {c_idx}")
        chef_ops.add_child(f"chef_{c_idx}", c_node)
        for f_key, f_name in foods_list:
            c_node.add_child(f_key, DecisionNode(f_type := f"Chef {c_idx} is preparing {f_name}"))

    dine_in = DecisionNode("Dine-In Orders")
    takeaway = DecisionNode("Takeaway Orders")
    customer.add_child("dine_in", dine_in)
    customer.add_child("takeaway", takeaway)

    customer_foods = [("lentil_soup", "Tomato Soup", 7), ("tomato_soup", "Tomato Soup", 7), ("beef_steak", "Beef Steak", 25), ("baklava", "Baklava", 8)]

    for t_idx in [1, 2, 3]:
        t_node = DecisionNode(f"Table {t_idx}")
        dine_in.add_child(f"table_{t_idx}", t_node)
        for f_key, f_name, f_price in customer_foods:
            f_node = DecisionNode(f"{f_name} (${f_price})")
            t_node.add_child(f_key, f_node)
            f_node.add_child("cash", DecisionNode(f"Customer at table {t_idx} will have {f_name}, {f_price}$, with cash"))
            f_node.add_child("card", DecisionNode(f"Customer at table {t_idx} will have {f_name}, {f_price}$, with card"))

    for f_key, f_name, f_price in customer_foods:
        f_node = DecisionNode(f"{f_name} (${f_price})")
        takeaway.add_child(f_key, f_node)
        f_node.add_child("cash", DecisionNode(f"Customer will have a takeaway meal,{f_name},{f_price}$,with cash"))
        f_node.add_child("card", DecisionNode(f"Customer will have a takeaway meal,{f_name},{f_price}$,with card"))

    return root

class RestaurantApp:
    def __init__(self, root: tk.Tk, tree_root: DecisionNode):
        self.root = root
        self.root.title("Discrete Structures - Restaurant Graph Visualization V4.0")
        self.root.geometry("1600x950")
        
        self.BG_DARK = "#141419"
        self.BG_PANEL = "#1e1e24"
        self.TEXT_LIGHT = "#ffffff"
        self.TEXT_MUTED = "#6c757d"
        self.ACCENT_BLUE = "#00b4d8"
        self.LEAF_GREEN = "#06d6a0"
        self.NODE_DEFAULT = "#2a2a35"
        self.LINE_DEFAULT = "#3d3d4d"
        
        self.root.configure(bg=self.BG_DARK)
        self.tree_root = tree_root
        self.current_node = tree_root
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.style.configure("PanedWindow", background=self.BG_DARK)
        self.style.configure("TFrame", background=self.BG_DARK)

        self.paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.canvas_frame = tk.Frame(self.paned_window, bg=self.BG_DARK)
        self.paned_window.add(self.canvas_frame, weight=4)
        
        tk.Label(self.canvas_frame, text="Discrete Structure - Live Graph Model", bg=self.BG_DARK, fg=self.ACCENT_BLUE, font=("Segoe UI", 12, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        self.canvas = tk.Canvas(self.canvas_frame, bg=self.BG_DARK, highlightthickness=1, highlightbackground=self.LINE_DEFAULT)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.right_frame = tk.Frame(self.paned_window, bg=self.BG_PANEL)
        self.paned_window.add(self.right_frame, weight=1)
        
        self.title_label = tk.Label(self.right_frame, text="", bg=self.BG_PANEL, fg=self.TEXT_LIGHT, font=("Segoe UI", 14, "bold"), wraplength=280, justify="center")
        self.title_label.pack(pady=(40, 10))
        
        self.path_label = tk.Label(self.right_frame, text="", bg=self.BG_PANEL, fg=self.TEXT_MUTED, font=("Segoe UI", 9), wraplength=280, justify="center")
        self.path_label.pack(pady=(0, 20))
        
        self.line = tk.Frame(self.right_frame, bg=self.ACCENT_BLUE, height=2, width=180)
        self.line.pack(pady=10)

        self.buttons_frame = tk.Frame(self.right_frame, bg=self.BG_PANEL)
        self.buttons_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)
        
        self.restart_btn = tk.Button(self.right_frame, text="RESET GRAPH", bg=self.BG_DARK, fg=self.TEXT_LIGHT, activebackground=self.ACCENT_BLUE, activeforeground=self.TEXT_LIGHT, font=("Segoe UI", 10, "bold"), relief="flat", bd=0, cursor="hand2", padx=20, pady=8, command=self.reset_tree)
        self.restart_btn.pack(side=tk.BOTTOM, pady=40)
        
        self.node_positions = {}
        self._compute_graph_layout()
        self.update_ui()

    def _compute_graph_layout(self):
        leaves = []
        def find_leaves(node):
            if node.is_leaf():
                leaves.append(node)
            for child in node.children.values():
                find_leaves(child)
        find_leaves(self.tree_root)
        
        leaf_y_map = {leaf: idx * 13 + 30 for idx, leaf in enumerate(leaves)}
        
        def calc_coords(node, depth):
            x = depth * 250 + 120
            if node.is_leaf():
                y = leaf_y_map[node]
            else:
                child_ys = []
                for child in node.children.values():
                    calc_coords(child, depth + 1)
                    child_ys.append(self.node_positions[child][1])
                y = sum(child_ys) / len(child_ys)
            self.node_positions[node] = (x, y)

        calc_coords(self.tree_root, 0)

    def _get_active_path(self, current: DecisionNode, target: DecisionNode, path: list[DecisionNode] = []) -> list[DecisionNode] | None:
        path = path + [current]
        if current == target:
            return path
        for child in current.children.values():
            extended_path = self._get_active_path(child, target, path)
            if extended_path:
                return extended_path
        return None

    def draw_graph(self):
        self.canvas.delete("all")
        active_path = self._get_active_path(self.tree_root, self.current_node) or []

        def draw_edges(node):
            for child in node.children.values():
                x1, y1 = self.node_positions[node]
                x2, y2 = self.node_positions[child]
                
                if node in active_path and child in active_path:
                    line_color = self.LEAF_GREEN if child == self.current_node and child.is_leaf() else self.ACCENT_BLUE
                    line_width = 3
                else:
                    line_color = self.LINE_DEFAULT
                    line_width = 1
                    
                self.canvas.create_line(x1, y1, x2, y2, fill=line_color, width=line_width)
                draw_edges(child)
        draw_edges(self.tree_root)

        for node, (x, y) in self.node_positions.items():
            if node == self.current_node:
                bg_color = self.LEAF_GREEN if node.is_leaf() else self.ACCENT_BLUE
                text_color = self.BG_DARK if node.is_leaf() else self.TEXT_LIGHT
                outline_color = self.TEXT_LIGHT
                font_weight = "bold"
            elif node in active_path:
                bg_color = "#1d3557"
                text_color = self.ACCENT_BLUE
                outline_color = self.ACCENT_BLUE
                font_weight = "normal"
            else:
                bg_color = self.NODE_DEFAULT
                text_color = self.TEXT_MUTED
                outline_color = self.LINE_DEFAULT
                font_weight = "normal"

            if node.is_leaf():
                w, h = 120, 10
                font_size = 7
            else:
                w, h = 75, 12
                font_size = 8

            self.canvas.create_rectangle(x-w, y-h, x+w, y+h, fill=bg_color, outline=outline_color, width=1.5, tags=f"node_{id(node)}")
            self.canvas.create_text(x, y, text=node.name, fill=text_color, font=("Segoe UI", font_size, font_weight), width=w*2-10, justify="center")

    def update_ui(self):
        self.title_label.config(text=f"{self.current_node.name}")
        
        active_path = self._get_active_path(self.tree_root, self.current_node) or []
        path_str = " -> ".join([node.name for node in active_path])
        self.path_label.config(text=f"Path Trace:\n{path_str}")
        
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
            
        if self.current_node.is_leaf():
            tk.Label(self.buttons_frame, text="OPERATIONAL OUTPUT", fg=self.LEAF_GREEN, bg=self.BG_PANEL, font=("Segoe UI", 12, "bold")).pack(pady=30)
            tk.Label(self.buttons_frame, text=self.current_node.name, fg=self.TEXT_LIGHT, bg=self.BG_PANEL, font=("Segoe UI", 11, "bold"), wraplength=280, justify="center").pack()
        else:
            tk.Label(self.buttons_frame, text="SELECT NEXT BRANCH", bg=self.BG_PANEL, fg=self.TEXT_MUTED, font=("Segoe UI", 9, "bold")).pack(pady=(0, 15))
            
            for branch_name, child_node in self.current_node.children.items():
                btn_text = f"BRANCH: {branch_name.upper()}"
                btn = tk.Button(self.buttons_frame, 
                                text=btn_text, 
                                bg=self.ACCENT_BLUE, 
                                fg=self.TEXT_LIGHT,
                                activebackground="#2a6fdb",
                                activeforeground=self.TEXT_LIGHT,
                                font=("Segoe UI", 10, "bold"), 
                                relief="flat", 
                                bd=0, 
                                pady=8, 
                                cursor="hand2",
                                command=lambda c=child_node: self.navigate(c))
                btn.pack(pady=5, fill=tk.X)
        
        self.draw_graph()

    def navigate(self, next_node: DecisionNode):
        self.current_node = next_node
        self.update_ui()
        
    def reset_tree(self):
        self.current_node = self.tree_root
        self.update_ui()

if __name__ == "__main__":
    restaurant_root = build_restaurant_tree()
    
    root_window = tk.Tk()
    app = RestaurantApp(root_window, restaurant_root)
    root_window.mainloop()
