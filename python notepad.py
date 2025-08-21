import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, scrolledtext
import re

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Notepad+")
        self.root.geometry("1000x700")
        
        # Current file and settings
        self.current_file = None
        self.dark_mode = tk.BooleanVar(value=False)
        self.font_size = tk.IntVar(value=12)
        self.font_family = tk.StringVar(value="Consolas")
        
        # Setup UI components
        self.setup_menu()
        self.setup_toolbar()
        self.setup_text_area()
        self.setup_statusbar()
        
        # Apply initial theme
        self.toggle_theme()
        
        # Bind events
        self.text_area.bind('<KeyRelease>', self.on_key_release)
        self.text_area.bind('<Button-1>', self.update_statusbar)
        self.text_area.bind('<<Modified>>', self.on_text_modified)
        
    def setup_menu(self):
        # Create menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_app)
        
        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut, accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Copy", command=self.copy, accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Paste", command=self.paste, accelerator="Ctrl+V")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Find", command=self.find_text, accelerator="Ctrl+F")
        self.edit_menu.add_command(label="Replace", command=self.replace_text, accelerator="Ctrl+H")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        
        # View menu
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_checkbutton(label="Dark Mode", variable=self.dark_mode, command=self.toggle_theme)
        
        # Theme submenu
        self.theme_menu = tk.Menu(self.view_menu, tearoff=0)
        self.view_menu.add_cascade(label="Themes", menu=self.theme_menu)
        self.theme_menu.add_command(label="Light", command=lambda: self.change_theme("light"))
        self.theme_menu.add_command(label="Dark", command=lambda: self.change_theme("dark"))
        self.theme_menu.add_command(label="Blue", command=lambda: self.change_theme("blue"))
        
        # Font size submenu
        self.font_menu = tk.Menu(self.view_menu, tearoff=0)
        self.view_menu.add_cascade(label="Font Size", menu=self.font_menu)
        for size in [8, 10, 12, 14, 16, 18, 20, 24]:
            self.font_menu.add_command(label=str(size), command=lambda s=size: self.change_font_size(s))
        
        # Syntax highlighting submenu
        self.syntax_menu = tk.Menu(self.view_menu, tearoff=0)
        self.view_menu.add_cascade(label="Syntax Highlighting", menu=self.syntax_menu)
        self.syntax_menu.add_command(label="Plain Text", command=lambda: self.set_syntax_highlighting("plain"))
        self.syntax_menu.add_command(label="Python", command=lambda: self.set_syntax_highlighting("python"))
        self.syntax_menu.add_command(label="JavaScript", command=lambda: self.set_syntax_highlighting("javascript"))
        self.syntax_menu.add_command(label="HTML", command=lambda: self.set_syntax_highlighting("html"))
        self.syntax_menu.add_command(label="CSS", command=lambda: self.set_syntax_highlighting("css"))
        
        # Keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-Shift-S>', lambda e: self.save_as_file())
        self.root.bind('<Control-f>', lambda e: self.find_text())
        self.root.bind('<Control-h>', lambda e: self.replace_text())
        self.root.bind('<Control-a>', lambda e: self.select_all())
        
    def setup_toolbar(self):
        # Create toolbar frame
        self.toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Toolbar buttons
        new_icon = tk.PhotoImage(width=1, height=1)  # Placeholder for actual icons
        open_icon = tk.PhotoImage(width=1, height=1)
        save_icon = tk.PhotoImage(width=1, height=1)
        
        new_btn = tk.Button(self.toolbar, image=new_icon, command=self.new_file, 
                           relief=tk.FLAT, compound=tk.TOP, text="New", width=50)
        new_btn.image = new_icon
        new_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        open_btn = tk.Button(self.toolbar, image=open_icon, command=self.open_file, 
                            relief=tk.FLAT, compound=tk.TOP, text="Open", width=50)
        open_btn.image = open_icon
        open_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        save_btn = tk.Button(self.toolbar, image=save_icon, command=self.save_file, 
                            relief=tk.FLAT, compound=tk.TOP, text="Save", width=50)
        save_btn.image = save_icon
        save_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Separator
        sep = tk.Frame(self.toolbar, height=2, width=2, bd=1, relief=tk.SUNKEN)
        sep.pack(side=tk.LEFT, padx=4, pady=4)
        
        # Font size selector
        font_frame = tk.Frame(self.toolbar)
        font_frame.pack(side=tk.LEFT, padx=5)
        tk.Label(font_frame, text="Font:").pack(side=tk.LEFT)
        font_spinbox = tk.Spinbox(font_frame, from_=8, to=72, width=5, 
                                 textvariable=self.font_size, command=self.update_font)
        font_spinbox.pack(side=tk.LEFT, padx=5)
        
    def setup_text_area(self):
        # Create main frame for text area and line numbers
        text_frame = tk.Frame(self.root)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Line numbers
        self.line_numbers = tk.Text(text_frame, width=4, padx=5, pady=5, takefocus=0, 
                                   border=0, background='lightgray', state='disabled')
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Text area with scrollbar
        self.text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, undo=True, 
                                                  font=(self.font_family.get(), self.font_size.get()))
        self.text_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Add scrollbar to line numbers
        line_scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.sync_scroll)
        line_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.line_numbers.config(yscrollcommand=line_scrollbar.set)
        
        # Configure tags for syntax highlighting
        self.setup_syntax_highlighting()
        
    def setup_statusbar(self):
        self.status_bar = tk.Label(self.root, text="Ln 1, Col 1", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def setup_syntax_highlighting(self):
        # Configure text tags for different syntax elements
        self.text_area.tag_configure("keyword", foreground="blue")
        self.text_area.tag_configure("comment", foreground="green")
        self.text_area.tag_configure("string", foreground="red")
        self.text_area.tag_configure("number", foreground="purple")
        self.text_area.tag_configure("function", foreground="darkorange")
        
        self.current_language = "plain"
        
    def set_syntax_highlighting(self, language):
        self.current_language = language
        self.highlight_syntax()
        
    def highlight_syntax(self):
        if self.current_language == "plain":
            return
            
        # Remove previous highlighting
        for tag in ["keyword", "comment", "string", "number", "function"]:
            self.text_area.tag_remove(tag, "1.0", tk.END)
            
        # Get the entire text content
        content = self.text_area.get("1.0", tk.END)
        
        if self.current_language == "python":
            # Python syntax patterns
            keywords = ["and", "as", "assert", "break", "class", "continue", "def", "del", 
                       "elif", "else", "except", "False", "finally", "for", "from", "global", 
                       "if", "import", "in", "is", "lambda", "None", "nonlocal", "not", "or", 
                       "pass", "raise", "return", "True", "try", "while", "with", "yield"]
            
            self.highlight_patterns(keywords, "keyword")
            self.highlight_pattern(r'#.*', "comment")
            self.highlight_pattern(r'(\"\"\"[\s\S]*?\"\"\"|\'\'\'[\s\S]*?\'\'\'|\".*?\"|\'.*?\')', "string")
            self.highlight_pattern(r'\b\d+\b', "number")
            self.highlight_pattern(r'\bdef\s+(\w+)', "function", group=1)
            
        elif self.current_language == "javascript":
            # JavaScript syntax patterns
            keywords = ["break", "case", "catch", "class", "const", "continue", "debugger", 
                       "default", "delete", "do", "else", "export", "extends", "finally", 
                       "for", "function", "if", "import", "in", "instanceof", "new", "return", 
                       "super", "switch", "this", "throw", "try", "typeof", "var", "void", 
                       "while", "with", "yield"]
            
            self.highlight_patterns(keywords, "keyword")
            self.highlight_pattern(r'//.*', "comment")
            self.highlight_pattern(r'/\*[\s\S]*?\*/', "comment")
            self.highlight_pattern(r'(\".*?\"|\'.*?\')', "string")
            self.highlight_pattern(r'\b\d+\b', "number")
            self.highlight_pattern(r'\bfunction\s+(\w+)', "function", group=1)
            
        elif self.current_language == "html":
            # HTML syntax patterns
            self.highlight_pattern(r'&lt;/?[^&gt;]+&gt;', "keyword")
            self.highlight_pattern(r'&lt;!--[\s\S]*?--&gt;', "comment")
            self.highlight_pattern(r'(\".*?\"|\'.*?\')', "string")
            
        elif self.current_language == "css":
            # CSS syntax patterns
            self.highlight_pattern(r'\.\w+', "keyword")
            self.highlight_pattern(r'#\w+', "keyword")
            self.highlight_pattern(r'/\*[\s\S]*?\*/', "comment")
            self.highlight_pattern(r'(\".*?\"|\'.*?\')', "string")
            self.highlight_pattern(r'\b\d+\b', "number")
            
    def highlight_patterns(self, patterns, tag):
        for pattern in patterns:
            self.highlight_pattern(r'\b' + pattern + r'\b', tag)
            
    def highlight_pattern(self, pattern, tag, group=0):
        content = self.text_area.get("1.0", tk.END)
        for match in re.finditer(pattern, content):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.text_area.tag_add(tag, start, end)
            
    def sync_scroll(self, *args):
        # Sync line numbers scroll with text area
        self.line_numbers.yview_moveto(args[0])
        self.text_area.yview_moveto(args[0])
        
    def update_line_numbers(self):
        # Update line numbers based on text content
        lines = self.text_area.get("1.0", "end-1c").split("\n")
        line_count = len(lines)
        
        # Configure line numbers widget
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete("1.0", tk.END)
        
        for i in range(1, line_count + 1):
            self.line_numbers.insert(tk.END, f"{i}\n")
            
        self.line_numbers.config(state=tk.DISABLED)
        
    def update_statusbar(self, event=None):
        # Update status bar with line and column info
        if not event:
            return
            
        # Get current cursor position
        cursor_pos = self.text_area.index(tk.INSERT)
        line, col = cursor_pos.split('.')
        
        # Update status bar
        self.status_bar.config(text=f"Ln {line}, Col {int(col)+1}")
        
    def on_key_release(self, event):
        self.update_line_numbers()
        self.update_statusbar()
        self.highlight_syntax()
        
    def on_text_modified(self, event):
        # Handle text modification events
        if event:
            self.text_area.edit_modified(False)
            
    def update_font(self):
        self.text_area.config(font=(self.font_family.get(), self.font_size.get()))
        
    def change_font_size(self, size):
        self.font_size.set(size)
        self.update_font()
        
    def toggle_theme(self):
        if self.dark_mode.get():
            self.apply_dark_theme()
        else:
            self.apply_light_theme()
            
    def change_theme(self, theme):
        if theme == "dark":
            self.dark_mode.set(True)
            self.apply_dark_theme()
        elif theme == "light":
            self.dark_mode.set(False)
            self.apply_light_theme()
        elif theme == "blue":
            self.apply_blue_theme()
            
    def apply_light_theme(self):
        # Light theme colors
        bg_color = "white"
        fg_color = "black"
        self.text_area.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)
        self.line_numbers.config(bg="lightgray", fg="black")
        self.status_bar.config(bg="lightgray", fg="black")
        
    def apply_dark_theme(self):
        # Dark theme colors
        bg_color = "#2e2e2e"
        fg_color = "#ffffff"
        self.text_area.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)
        self.line_numbers.config(bg="#3c3c3c", fg="white")
        self.status_bar.config(bg="#3c3c3c", fg="white")
        
        # Update syntax highlighting colors for dark theme
        self.text_area.tag_configure("keyword", foreground="#569cd6")
        self.text_area.tag_configure("comment", foreground="#6a9955")
        self.text_area.tag_configure("string", foreground="#ce9178")
        self.text_area.tag_configure("number", foreground="#b5cea8")
        self.text_area.tag_configure("function", foreground="#dcdcaa")
        
    def apply_blue_theme(self):
        # Blue theme colors
        bg_color = "#e6f3ff"
        fg_color = "#000055"
        self.text_area.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)
        self.line_numbers.config(bg="#cce5ff", fg="darkblue")
        self.status_bar.config(bg="#cce5ff", fg="darkblue")
        
    def new_file(self):
        if self.text_area.edit_modified():
            if not messagebox.askokcancel("Notepad+", "Save changes to current file?"):
                return
            self.save_file()
            
        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self.root.title("Notepad+")
        self.text_area.edit_modified(False)
        self.update_line_numbers()
        
    def open_file(self):
        if self.text_area.edit_modified():
            if not messagebox.askokcancel("Notepad+", "Save changes to current file?"):
                return
            self.save_file()
            
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, content)
                    
                self.current_file = file_path
                self.root.title(f"Notepad+ - {file_path}")
                self.text_area.edit_modified(False)
                self.update_line_numbers()
                
                # Try to detect file type for syntax highlighting
                if file_path.endswith(".py"):
                    self.set_syntax_highlighting("python")
                elif file_path.endswith(".js"):
                    self.set_syntax_highlighting("javascript")
                elif file_path.endswith(".html"):
                    self.set_syntax_highlighting("html")
                elif file_path.endswith(".css"):
                    self.set_syntax_highlighting("css")
                else:
                    self.set_syntax_highlighting("plain")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {str(e)}")
                
    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, "w") as file:
                    content = self.text_area.get(1.0, tk.END)
                    file.write(content)
                    
                self.text_area.edit_modified(False)
                messagebox.showinfo("Notepad+", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {str(e)}")
        else:
            self.save_as_file()
            
    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            self.current_file = file_path
            self.save_file()
            self.root.title(f"Notepad+ - {file_path}")
            
    def exit_app(self):
        if self.text_area.edit_modified():
            if messagebox.askokcancel("Notepad+", "Save changes before exiting?"):
                self.save_file()
                
        self.root.destroy()
        
    def undo(self):
        try:
            self.text_area.edit_undo()
        except:
            pass
            
    def redo(self):
        try:
            self.text_area.edit_redo()
        except:
            pass
            
    def cut(self):
        self.text_area.event_generate("<<Cut>>")
        
    def copy(self):
        self.text_area.event_generate("<<Copy>>")
        
    def paste(self):
        self.text_area.event_generate("<<Paste>>")
        
    def select_all(self):
        self.text_area.tag_add(tk.SEL, "1.0", tk.END)
        self.text_area.mark_set(tk.INSERT, "1.0")
        self.text_area.see(tk.INSERT)
        
    def find_text(self):
        find_str = simpledialog.askstring("Find", "Enter text to find:")
        if find_str:
            # Remove previous highlights
            self.text_area.tag_remove("found", "1.0", tk.END)
            
            # Search for the text
            start_pos = "1.0"
            while True:
                start_pos = self.text_area.search(find_str, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                    
                end_pos = f"{start_pos}+{len(find_str)}c"
                self.text_area.tag_add("found", start_pos, end_pos)
                start_pos = end_pos
                
            # Configure the highlight
            self.text_area.tag_config("found", background="yellow", foreground="black")
            
    def replace_text(self):
        find_str = simpledialog.askstring("Replace", "Find what:")
        if not find_str:
            return
            
        replace_str = simpledialog.askstring("Replace", "Replace with:")
        if replace_str is None:
            return
            
        # Remove previous highlights
        self.text_area.tag_remove("found", "1.0", tk.END)
        
        # Search and replace
        content = self.text_area.get("1.0", tk.END)
        new_content = content.replace(find_str, replace_str)
        
        if content != new_content:
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", new_content)
            messagebox.showinfo("Replace", "Replacement completed.")
        else:
            messagebox.showinfo("Replace", "Text not found.")


if __name__ == "__main__":
    root = tk.Tk()
    notepad = Notepad(root)
    root.mainloop()