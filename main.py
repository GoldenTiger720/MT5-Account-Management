import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
from typing import Dict, Any
import json
from datetime import datetime

class ModalWindow(tk.Toplevel):
    def __init__(self, parent, title, width=400, height=300):
        super().__init__(parent)
        self.setup_modal(title, width, height)
        
    def setup_modal(self, title, width, height):
        self.title(title)
        # Center window
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        # Modal properties
        self.transient(self.master)
        self.grab_set()
        self.resizable(False, False)
        self.configure(bg='#f0f0f0')

class MATModal(ModalWindow):
    def __init__(self, parent):
        super().__init__(parent, "MAT Settings", 400, 400)
        
        # Main frame with padding
        frame = ttk.Frame(self, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(
            frame,
            text="MAT Settings",
            font=('Arial', 12, 'bold')
        ).pack(pady=(0, 20))
        
        # MAT Options
        options = [
            ("View Master Accounts", self.view_master_accounts),
            ("Create New Master Account", self.create_master_account),
            ("Manage Account Templates", self.manage_templates),
            ("Account Settings", self.account_settings),
            ("Security Settings", self.security_settings),
            ("Trade Settings", self.trade_settings),
            ("Reports", self.show_reports)
        ]
        
        for text, command in options:
            btn = ttk.Button(
                frame,
                text=text,
                width=30,
                command=command
            )
            btn.pack(pady=5)
        
        # Close button
        ttk.Button(
            frame,
            text="Close",
            command=self.destroy,
            width=20
        ).pack(pady=(20, 0))
    
    def view_master_accounts(self):
        messagebox.showinfo("Info", "Opening Master Accounts view...")
        self.destroy()
    
    def create_master_account(self):
        self.destroy()
        AddAccountModal(self.master, is_demo=False)
    
    def manage_templates(self):
        messagebox.showinfo("Info", "Opening Template Management...")
        self.destroy()
    
    def account_settings(self):
        messagebox.showinfo("Info", "Opening Account Settings...")
        self.destroy()
    
    def security_settings(self):
        messagebox.showinfo("Info", "Opening Security Settings...")
        self.destroy()
    
    def trade_settings(self):
        messagebox.showinfo("Info", "Opening Trade Settings...")
        self.destroy()
    
    def show_reports(self):
        messagebox.showinfo("Info", "Opening Reports...")
        self.destroy()

class ServerModal(ModalWindow):
    def __init__(self, parent):
        super().__init__(parent, "Server Settings", 500, 400)
        
        # Server settings content
        frame = ttk.Frame(self, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Connection Settings
        ttk.Label(frame, text="Connection Settings", font=('Arial', 12, 'bold')).pack(pady=10)
        
        settings = [
            ("Server Address:", "localhost"),
            ("Port:", "443"),
            ("Timeout (ms):", "5000"),
            ("Max Connections:", "100")
        ]
        
        for label, default in settings:
            setting_frame = ttk.Frame(frame)
            setting_frame.pack(fill=tk.X, pady=5)
            ttk.Label(setting_frame, text=label).pack(side=tk.LEFT, padx=5)
            ttk.Entry(setting_frame, width=30).pack(side=tk.RIGHT, padx=5)
            
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Apply", command=self.apply_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)
        
    def apply_settings(self):
        messagebox.showinfo("Success", "Server settings updated successfully!")
        self.destroy()

class AddAccountModal(ModalWindow):
    def __init__(self, parent, is_demo=False):
        super().__init__(parent, "Add Master Account" if not is_demo else "Add Demo Master Account", 400, 500)
        
        frame = ttk.Frame(self, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Account Details
        ttk.Label(frame, text="Account Details", font=('Arial', 12, 'bold')).pack(pady=10)
        
        fields = [
            "Login ID:",
            "Password:",
            "Confirm Password:",
            "Group:",
            "Leverage:",
            "Initial Balance:"
        ]
        
        self.entries = {}
        for field in fields:
            field_frame = ttk.Frame(frame)
            field_frame.pack(fill=tk.X, pady=5)
            ttk.Label(field_frame, text=field).pack(side=tk.LEFT, padx=5)
            entry = ttk.Entry(field_frame, width=30)
            entry.pack(side=tk.RIGHT, padx=5)
            self.entries[field] = entry
            
        # Demo account checkbox
        self.is_demo = tk.BooleanVar(value=is_demo)
        ttk.Checkbutton(frame, text="Demo Account", variable=self.is_demo).pack(pady=10)
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Create", command=self.create_account).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)
        
    def create_account(self):
        # Validate input
        if not all(entry.get() for entry in self.entries.values()):
            messagebox.showerror("Error", "All fields are required!")
            return
            
        messagebox.showinfo("Success", "Account created successfully!")
        self.destroy()

class FilterDialog(ModalWindow):
    def __init__(self, parent, columns):
        super().__init__(parent, "Filter Data", 300, 400)
        
        frame = ttk.Frame(self, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Filter options
        ttk.Label(frame, text="Filter By:", font=('Arial', 10, 'bold')).pack(pady=5)
        
        self.column_var = tk.StringVar()
        column_combo = ttk.Combobox(frame, textvariable=self.column_var, values=columns)
        column_combo.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text="Value:").pack(pady=5)
        self.value_entry = ttk.Entry(frame)
        self.value_entry.pack(fill=tk.X, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Apply", command=self.apply_filter).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_filter).pack(side=tk.LEFT, padx=5)
        
    def apply_filter(self):
        # Filter logic to be implemented
        self.destroy()
        
    def clear_filter(self):
        # Clear filter logic
        self.destroy()

class MT5AdminDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MT5 Admin Dashboard")
        self.state('zoomed')
        
        # Initialize variables
        self.current_sort_column = None
        self.sort_ascending = True
        
        self.setup_styles()
        self.setup_ui()
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load sample data into the table"""
        sample_data = [
            (False, '12345', 'Standard', '100%', '1:100', 
            '10000.00', '0.00', '1000.00', '9000.00', True),
            (False, '12346', 'Pro', '100%', '1:200', 
            '25000.00', '0.00', '2000.00', '23000.00', False),
            (True, '12347', 'VIP', '100%', '1:500', 
            '50000.00', '1000.00', '5000.00', '46000.00', False)
        ]
        
        for item in sample_data:
            self.tree.insert('', 'end', values=item)
    def setup_ui(self):
        # Menu Bar
        self.menu_frame = ttk.Frame(self, style='MenuBar.TFrame')
        self.menu_frame.pack(fill='x', padx=0, pady=0)
        self.create_menu_bar()
        
        # Tab Bar
        self.tab_frame = ttk.Frame(self)
        self.tab_frame.pack(fill='x', padx=5, pady=2)
        ttk.Label(
            self.tab_frame,
            text="MAT - Master accounts ×",
            background='lightgray',
            padding='5 3'
        ).pack(side='left')
        
        # Button Bar (Toolbar)
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(fill='x', padx=5, pady=2)
        self.create_toolbar()
        
        # Main Table Frame
        self.table_frame = ttk.Frame(self)
        self.table_frame.pack(fill='both', expand=True, padx=5, pady=5)
        self.setup_table()
        
    def setup_styles(self):
        style = ttk.Style()
        
        # Configure global styles
        style.configure("TFrame", background="#f5f5f5")
        style.configure("TLabel", background="#f5f5f5", font=('Arial', 9))
        style.configure("TButton", padding=5, font=('Arial', 9))
        
        # Table styles
        style.configure("Treeview",
                       background="white",
                       fieldbackground="white",
                       rowheight=25,
                       font=('Arial', 9))
        
        style.configure("Treeview.Heading",
                       background="#e1e1e1",
                       font=('Arial', 9, 'bold'),
                       relief='flat')
        
        style.map("Treeview.Heading",
                 background=[('active', '#d1d1d1')])
                 
        # Menu styles
        style.configure("Menu.TLabel",
                       padding='10 5',
                       background="#f0f0f0",
                       font=('Arial', 9))
        
        # Button styles
        style.configure("Toolbar.TButton",
                       padding='5 3',
                       font=('Arial', 9))

    def create_menu_bar(self):
        menus = {
            'Server': self.show_server_modal,
            'Binary Options': self.show_binary_options,
            'MAT': self.show_mat_modal,
            'Language': self.show_language_options,
            'Help': self.show_help
        }
        
        for text, command in menus.items():
            label = ttk.Label(self.menu_frame, text=text, style='Menu.TLabel', cursor='hand2')
            label.pack(side='left')
            label.bind('<Button-1>', lambda e, cmd=command: cmd())
            label.bind('<Enter>', lambda e: e.widget.configure(background='#e0e0e0'))
            label.bind('<Leave>', lambda e: e.widget.configure(background='#f0f0f0'))

    def create_toolbar(self):
        buttons = [
            # ('Refresh', self.refresh_data),
            ('Add master account', lambda: self.show_add_account(False)),
            ('Add demo master account', lambda: self.show_add_account(True)),
            ('Template demo master account', self.show_template_dialog)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(self.button_frame, text=text, command=command, style='Toolbar.TButton')
            btn.pack(side='left', padx=2)

    def setup_table(self):
        # Enhanced table setup with sorting and filtering
        columns = ('Locked', 'Login', 'Group', 'Allocation', 'Leverage', 
                  'Balance', 'Credit', 'Margin', 'Free margin', 'Is demo')
                  
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show='headings')
        
        # Configure columns with sorting
        for col in columns:
            self.tree.heading(col, text=col,
                            command=lambda c=col: self.sort_column(c))
            self.tree.column(col, width=100)
            
        # Add right-click menu
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Edit", command=self.edit_row)
        self.context_menu.add_command(label="Delete", command=self.delete_row)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Filter", command=self.show_filter_dialog)
        
        self.tree.bind("<Button-3>", self.show_context_menu)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        self.tree.grid(column=0, row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')
        
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=1)

    def sort_column(self, col):
        """Sort tree contents when a column header is clicked"""
        # Get all items in the tree
        data = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        
        # If the column is clicked again, reverse the sort order
        if self.current_sort_column == col:
            self.sort_ascending = not self.sort_ascending
        else:
            self.sort_ascending = True
            self.current_sort_column = col
            
        # Sort the data
        data.sort(reverse=not self.sort_ascending)
        
        # Rearrange items in sorted positions
        for index, (_, item) in enumerate(data):
            self.tree.move(item, '', index)
            
        # Add the arrows in the column header
        for column in self.tree['columns']:
            if column == col:
                self.tree.heading(column, text=f"{column} {'↑' if self.sort_ascending else '↓'}")
            else:
                self.tree.heading(column, text=column)

    def show_context_menu(self, event):
        """Display the context menu on right click"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def edit_row(self):
        """Edit the selected row"""
        selected = self.tree.selection()
        if not selected:
            return
            
        # Show edit dialog
        item = selected[0]
        values = self.tree.item(item)['values']
        # Implement edit dialog here

    def delete_row(self):
        """Delete the selected row"""
        selected = self.tree.selection()
        if not selected:
            return
            
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this item?"):
            for item in selected:
                self.tree.delete(item)

    def show_filter_dialog(self):
        """Show the filter dialog"""
        FilterDialog(self, self.tree['columns'])

    # Modal window methods
    def show_server_modal(self):
        ServerModal(self)

    def show_binary_options(self):
        messagebox.showinfo("Binary Options", "Binary Options settings dialog (to be implemented)")

    def show_mat_modal(self):
        MATModal(self)

    def show_language_options(self):
        languages = ['English', 'Spanish', 'French', 'German', 'Russian', 'Chinese']
        dialog = ModalWindow(self, "Select Language", 300, 200)
        for lang in languages:
            ttk.Button(dialog, text=lang, command=lambda l=lang: self.change_language(l, dialog)).pack(pady=5)

    def show_help(self):
        help_text = """
        MT5 Administrator Help
        
        1. Account Management
        - Add new master accounts
        - Monitor account status
        - Manage permissions
        
        2. Server Settings
        - Configure connection
        - Set up security
        
        3. Support
        Visit: help.metaquotes.net
        """
        dialog = ModalWindow(self, "Help", 400, 300)
        text = tk.Text(dialog, wrap=tk.WORD, padx=20, pady=20)
        text.pack(fill=tk.BOTH, expand=True)
        text.insert('1.0', help_text)
        text.config(state='disabled')

    def show_add_account(self, is_demo):
        AddAccountModal(self, is_demo)

    def show_template_dialog(self):
        messagebox.showinfo("Template", "Template creation dialog (to be implemented)")

    def change_language(self, language, dialog):
        messagebox.showinfo("Language", f"Language changed to {language}")
        dialog.destroy()

def main():
    app = MT5AdminDashboard()
    app.mainloop()

if __name__ == "__main__":
    main()