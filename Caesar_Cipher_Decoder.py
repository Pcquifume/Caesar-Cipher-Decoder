#!/usr/bin/env python3
"""
Ultimate Caesar Cipher Decoder - Fast and elegant decoding application
Supports: raw text, files, frequency analysis, automatic decoding
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import time
import string
from collections import Counter
import os
import re

class CaesarDecoder:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔓 Ultimate Caesar Cipher Decoder")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e1e')
        
        # Variables
        self.input_text = tk.StringVar()
        self.shift_value = tk.IntVar(value=0)
        self.auto_decode = tk.BooleanVar(value=True)
        self.case_sensitive = tk.BooleanVar(value=False)
        self.preserve_spaces = tk.BooleanVar(value=True)
        
        # English letter frequencies
        self.english_freq = {
            'e': 12.7, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7.0, 'n': 6.7,
            's': 6.3, 'h': 6.1, 'r': 6.0, 'd': 4.3, 'l': 4.0, 'c': 2.8,
            'u': 2.8, 'm': 2.4, 'w': 2.4, 'f': 2.2, 'g': 2.0, 'y': 2.0,
            'p': 1.9, 'b': 1.3, 'v': 1.0, 'k': 0.8, 'j': 0.15, 'x': 0.15,
            'q': 0.10, 'z': 0.07
        }
        
        self.setup_ui()
        self.center_window()
        
    def setup_ui(self):
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        colors = {
            'bg': '#1e1e1e',
            'fg': '#ffffff',
            'accent': '#007acc',
            'success': '#28a745',
            'warning': '#ffc107',
            'error': '#dc3545',
            'input_bg': '#2d2d30',
            'button_bg': '#007acc'
        }
        
        style.configure('Title.TLabel', background=colors['bg'], foreground=colors['accent'], 
                       font=('Helvetica', 16, 'bold'))
        style.configure('Subtitle.TLabel', background=colors['bg'], foreground=colors['fg'], 
                       font=('Helvetica', 10))
        style.configure('Custom.TButton', background=colors['button_bg'], foreground=colors['fg'],
                       font=('Helvetica', 10, 'bold'), relief='flat')
        style.configure('Success.TButton', background=colors['success'], foreground=colors['fg'])
        style.configure('Warning.TButton', background=colors['warning'], foreground='black')
        
        # Main container
        main_frame = tk.Frame(self.root, bg=colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=colors['bg'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="🔓 ULTIMATE CAESAR CIPHER DECODER", style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame, text="Fast & Intelligent Decoding • Frequency Analysis • File Support", 
                                 style='Subtitle.TLabel')
        subtitle_label.pack(pady=(5, 0))
        
        # Input section
        input_frame = tk.LabelFrame(main_frame, text=" 📝 INPUT ", bg=colors['bg'], 
                                   fg=colors['accent'], font=('Helvetica', 12, 'bold'))
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Input methods frame
        input_methods_frame = tk.Frame(input_frame, bg=colors['bg'])
        input_methods_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # File button
        file_btn = tk.Button(input_methods_frame, text="📁 LOAD FILE", 
                           command=self.load_file, bg=colors['button_bg'], fg=colors['fg'],
                           font=('Helvetica', 10, 'bold'), relief='flat', padx=15, pady=8)
        file_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear button
        clear_btn = tk.Button(input_methods_frame, text="🗑️ CLEAR ALL", 
                            command=self.clear_all, bg=colors['error'], fg=colors['fg'],
                            font=('Helvetica', 10, 'bold'), relief='flat', padx=15, pady=8)
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Auto decode button
        auto_btn = tk.Button(input_methods_frame, text="🤖 AUTO DECODE", 
                           command=self.auto_decode_text, bg=colors['success'], fg=colors['fg'],
                           font=('Helvetica', 10, 'bold'), relief='flat', padx=15, pady=8)
        auto_btn.pack(side=tk.RIGHT)
        
        # Text input area
        text_input_frame = tk.Frame(input_frame, bg=colors['bg'])
        text_input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        tk.Label(text_input_frame, text="Text to decode:", bg=colors['bg'], 
                fg=colors['fg'], font=('Helvetica', 10, 'bold')).pack(anchor=tk.W)
        
        self.text_input = scrolledtext.ScrolledText(text_input_frame, height=6, 
                                                   bg=colors['input_bg'], fg=colors['fg'],
                                                   font=('Consolas', 11), insertbackground=colors['fg'])
        self.text_input.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        self.text_input.bind('<KeyRelease>', self.on_text_change)
        
        # Controls section
        controls_frame = tk.LabelFrame(main_frame, text=" ⚙️ CONTROLS ", bg=colors['bg'], 
                                     fg=colors['accent'], font=('Helvetica', 12, 'bold'))
        controls_frame.pack(fill=tk.X, pady=(0, 15))
        
        controls_inner = tk.Frame(controls_frame, bg=colors['bg'])
        controls_inner.pack(fill=tk.X, padx=10, pady=10)
        
        # Shift control
        shift_frame = tk.Frame(controls_inner, bg=colors['bg'])
        shift_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(shift_frame, text="Shift:", bg=colors['bg'], fg=colors['fg'], 
                font=('Helvetica', 10, 'bold')).pack(side=tk.LEFT)
        
        self.shift_scale = tk.Scale(shift_frame, from_=-25, to=25, orient=tk.HORIZONTAL,
                                   variable=self.shift_value, bg=colors['input_bg'], fg=colors['fg'],
                                   troughcolor=colors['accent'], activebackground=colors['accent'],
                                   highlightthickness=0, command=self.on_shift_change)
        self.shift_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        self.shift_label = tk.Label(shift_frame, text="0", bg=colors['bg'], fg=colors['accent'], 
                                   font=('Helvetica', 12, 'bold'), width=4)
        self.shift_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Options
        options_frame = tk.Frame(controls_inner, bg=colors['bg'])
        options_frame.pack(side=tk.RIGHT, padx=(20, 0))
        
        case_cb = tk.Checkbutton(options_frame, text="Preserve case", variable=self.case_sensitive,
                               bg=colors['bg'], fg=colors['fg'], selectcolor=colors['input_bg'],
                               activebackground=colors['bg'], activeforeground=colors['fg'],
                               command=self.decode_text)
        case_cb.pack(anchor=tk.W)
        
        space_cb = tk.Checkbutton(options_frame, text="Keep spaces", variable=self.preserve_spaces,
                                bg=colors['bg'], fg=colors['fg'], selectcolor=colors['input_bg'],
                                activebackground=colors['bg'], activeforeground=colors['fg'],
                                command=self.decode_text)
        space_cb.pack(anchor=tk.W)
        
        # Results section
        results_frame = tk.LabelFrame(main_frame, text=" 🔍 RESULTS ", bg=colors['bg'], 
                                    fg=colors['accent'], font=('Helvetica', 12, 'bold'))
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        results_inner = tk.Frame(results_frame, bg=colors['bg'])
        results_inner.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Results tabs
        self.notebook = ttk.Notebook(results_inner)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Decoded text tab
        decoded_frame = tk.Frame(self.notebook, bg=colors['bg'])
        self.notebook.add(decoded_frame, text="📄 Decoded Text")
        
        decoded_header = tk.Frame(decoded_frame, bg=colors['bg'])
        decoded_header.pack(fill=tk.X, pady=(0, 10))
        
        self.result_info = tk.Label(decoded_header, text="Ready to decode", bg=colors['bg'], 
                                   fg=colors['fg'], font=('Helvetica', 10))
        self.result_info.pack(side=tk.LEFT)
        
        save_btn = tk.Button(decoded_header, text="💾 SAVE RESULT", command=self.save_result,
                           bg=colors['button_bg'], fg=colors['fg'], font=('Helvetica', 9, 'bold'),
                           relief='flat', padx=10, pady=5)
        save_btn.pack(side=tk.RIGHT)
        
        self.result_text = scrolledtext.ScrolledText(decoded_frame, bg=colors['input_bg'], 
                                                    fg=colors['fg'], font=('Consolas', 11),
                                                    state=tk.DISABLED)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Analysis tab
        analysis_frame = tk.Frame(self.notebook, bg=colors['bg'])
        self.notebook.add(analysis_frame, text="📊 Analysis")
        
        self.analysis_text = scrolledtext.ScrolledText(analysis_frame, bg=colors['input_bg'], 
                                                      fg=colors['fg'], font=('Consolas', 10),
                                                      state=tk.DISABLED)
        self.analysis_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # All possibilities tab
        possibilities_frame = tk.Frame(self.notebook, bg=colors['bg'])
        self.notebook.add(possibilities_frame, text="🎯 All Possibilities")
        
        self.possibilities_text = scrolledtext.ScrolledText(possibilities_frame, bg=colors['input_bg'], 
                                                          fg=colors['fg'], font=('Consolas', 9),
                                                          state=tk.DISABLED)
        self.possibilities_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status bar
        self.status_bar = tk.Label(main_frame, text="Ready", bg=colors['input_bg'], fg=colors['fg'],
                                  relief=tk.SUNKEN, anchor=tk.W, font=('Helvetica', 9))
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        
    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) // 2
        y = (self.root.winfo_screenheight() - self.root.winfo_reqheight()) // 2
        self.root.geometry(f"+{x}+{y}")
        
    def update_status(self, message, color='#ffffff'):
        self.status_bar.config(text=message, fg=color)
        self.root.update_idletasks()
        
    def load_file(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Select a file",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if file_path:
                self.update_status("Loading file...", '#ffc107')
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    
                self.text_input.delete('1.0', tk.END)
                self.text_input.insert('1.0', content)
                
                filename = os.path.basename(file_path)
                self.update_status(f"File loaded: {filename} ({len(content)} characters)", '#28a745')
                
                if self.auto_decode.get():
                    threading.Thread(target=self.auto_decode_text, daemon=True).start()
                    
        except Exception as e:
            messagebox.showerror("Error", f"Unable to load file:\n{str(e)}")
            self.update_status("Loading error", '#dc3545')
            
    def clear_all(self):
        self.text_input.delete('1.0', tk.END)
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        self.result_text.config(state=tk.DISABLED)
        
        self.analysis_text.config(state=tk.NORMAL)
        self.analysis_text.delete('1.0', tk.END)
        self.analysis_text.config(state=tk.DISABLED)
        
        self.possibilities_text.config(state=tk.NORMAL)
        self.possibilities_text.delete('1.0', tk.END)
        self.possibilities_text.config(state=tk.DISABLED)
        
        self.shift_value.set(0)
        self.result_info.config(text="Ready to decode")
        self.update_status("Interface cleared", '#28a745')
        
    def caesar_cipher(self, text, shift):
        result = []
        
        for char in text:
            if char.isalpha():
                ascii_offset = ord('A') if char.isupper() else ord('a')
                shifted = (ord(char) - ascii_offset + shift) % 26
                result.append(chr(shifted + ascii_offset))
            else:
                if self.preserve_spaces.get() or not char.isspace():
                    result.append(char)
                    
        return ''.join(result)
        
    def calculate_frequency_score(self, text):
        if not text:
            return 0
            
        # Count letters
        letter_count = Counter()
        total_letters = 0
        
        for char in text.lower():
            if char.isalpha():
                letter_count[char] += 1
                total_letters += 1
                
        if total_letters == 0:
            return 0
            
        # Calculate score based on English frequencies
        score = 0
        for letter, count in letter_count.items():
            frequency = (count / total_letters) * 100
            expected_freq = self.english_freq.get(letter, 0.01)
            score += abs(frequency - expected_freq)
            
        return 1000 / (score + 1)  # Lower score is better
        
    def find_best_shift(self, text):
        if not text.strip():
            return 0
            
        self.update_status("Performing frequency analysis...", '#ffc107')
        
        best_shift = 0
        best_score = 0
        scores = []
        
        for shift in range(26):
            decoded = self.caesar_cipher(text, -shift)
            score = self.calculate_frequency_score(decoded)
            scores.append((shift, score, decoded))
            
            if score > best_score:
                best_score = score
                best_shift = shift
                
        return best_shift, scores
        
    def auto_decode_text(self):
        text = self.text_input.get('1.0', tk.END).strip()
        if not text:
            return
            
        try:
            self.update_status("Auto-decoding in progress...", '#ffc107')
            
            best_shift, all_scores = self.find_best_shift(text)
            self.shift_value.set(-best_shift if best_shift > 0 else 26 - best_shift)
            
            # Update display
            self.decode_text()
            self.show_analysis(all_scores)
            self.show_all_possibilities(all_scores)
            
            self.update_status(f"Auto-decode complete - Optimal shift: {-best_shift}", '#28a745')
            
        except Exception as e:
            self.update_status(f"Auto-decode error: {str(e)}", '#dc3545')
            
    def show_analysis(self, scores):
        self.analysis_text.config(state=tk.NORMAL)
        self.analysis_text.delete('1.0', tk.END)
        
        analysis = "=== FREQUENCY ANALYSIS ===\n\n"
        
        # Sort by score
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        
        analysis += "Top 5 most probable shifts:\n"
        analysis += "-" * 50 + "\n"
        
        for i, (shift, score, decoded) in enumerate(sorted_scores[:5]):
            analysis += f"#{i+1} - Shift: -{shift:2d} | Score: {score:6.2f}\n"
            preview = decoded[:100].replace('\n', ' ')
            if len(decoded) > 100:
                preview += "..."
            analysis += f"     Preview: {preview}\n\n"
            
        # Statistics
        text = self.text_input.get('1.0', tk.END).strip()
        analysis += "\n=== TEXT STATISTICS ===\n"
        analysis += f"Total length: {len(text)} characters\n"
        
        letters = sum(1 for c in text if c.isalpha())
        analysis += f"Letters: {letters}\n"
        
        if letters > 0:
            analysis += f"Spaces: {text.count(' ')}\n"
            analysis += f"Digits: {sum(1 for c in text if c.isdigit())}\n"
            analysis += f"Punctuation: {len(text) - letters - text.count(' ') - sum(1 for c in text if c.isdigit())}\n"
            
            # Letter frequency in original text
            letter_freq = Counter(c.lower() for c in text if c.isalpha())
            analysis += "\nLetter frequencies (top 10):\n"
            for letter, count in letter_freq.most_common(10):
                freq = (count / letters) * 100
                analysis += f"{letter.upper()}: {count:3d} ({freq:5.2f}%)\n"
                
        self.analysis_text.insert('1.0', analysis)
        self.analysis_text.config(state=tk.DISABLED)
        
    def show_all_possibilities(self, scores):
        self.possibilities_text.config(state=tk.NORMAL)
        self.possibilities_text.delete('1.0', tk.END)
        
        content = "=== ALL DECODING POSSIBILITIES ===\n\n"
        
        # Sort by shift
        sorted_by_shift = sorted(scores, key=lambda x: x[0])
        
        for shift, score, decoded in sorted_by_shift:
            content += f"Shift -{shift:2d} (Score: {score:6.2f}):\n"
            content += "-" * 60 + "\n"
            
            # Limit display to avoid overload
            preview = decoded[:200]
            if len(decoded) > 200:
                preview += "... [truncated]"
                
            content += preview + "\n\n"
            
        self.possibilities_text.insert('1.0', content)
        self.possibilities_text.config(state=tk.DISABLED)
        
    def on_shift_change(self, value=None):
        self.shift_label.config(text=str(self.shift_value.get()))
        self.decode_text()
        
    def on_text_change(self, event=None):
        # Real-time decoding if text changes
        if self.auto_decode.get():
            # Delay to avoid too many calls
            self.root.after(500, self.decode_text)
        else:
            self.decode_text()
            
    def decode_text(self):
        text = self.text_input.get('1.0', tk.END).strip()
        if not text:
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete('1.0', tk.END)
            self.result_text.config(state=tk.DISABLED)
            self.result_info.config(text="No text to decode")
            return
            
        try:
            shift = self.shift_value.get()
            decoded = self.caesar_cipher(text, shift)
            
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert('1.0', decoded)
            self.result_text.config(state=tk.DISABLED)
            
            # Result info
            info = f"Decoded with shift {shift} • {len(decoded)} characters"
            self.result_info.config(text=info)
            
        except Exception as e:
            self.result_info.config(text=f"Error: {str(e)}")
            
    def save_result(self):
        decoded_text = self.result_text.get('1.0', tk.END).strip()
        if not decoded_text:
            messagebox.showwarning("Warning", "No result to save")
            return
            
        try:
            file_path = filedialog.asksaveasfilename(
                title="Save result",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(decoded_text)
                    
                filename = os.path.basename(file_path)
                self.update_status(f"Result saved: {filename}", '#28a745')
                messagebox.showinfo("Success", f"Result saved to:\n{file_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Unable to save:\n{str(e)}")
            self.update_status("Save error", '#dc3545')
            
    def run(self):
        self.root.mainloop()

def main():
    """Main entry point of the application"""
    try:
        app = CaesarDecoder()
        app.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()