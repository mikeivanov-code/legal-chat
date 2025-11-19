import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from .config import DATA_ROOT
from .ingest import index_client
from .pipeline import answer_question

class LegalChatApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Legal Chat (Local RAG + Ollama)")
        self.geometry("960x720")

        self._history = []

        self._build_widgets()

        self._load_clients()



    # --- UI setup ---

    def _build_widgets(self):

        top = ttk.Frame(self)

        top.pack(fill=tk.X, padx=12, pady=8)



        ttk.Label(top, text="Client:").pack(side=tk.LEFT)

        self.client_combo = ttk.Combobox(top, state="readonly", width=40)

        self.client_combo.pack(side=tk.LEFT, padx=8)

        self.refresh_btn = ttk.Button(top, text="↻", width=3, command=self._load_clients)

        self.refresh_btn.pack(side=tk.LEFT)



        self.index_btn = ttk.Button(top, text="Index", command=self._on_index)

        self.index_btn.pack(side=tk.LEFT, padx=8)

        self.clear_hist_btn = ttk.Button(top, text="Clear History", command=self._clear_history)

        self.clear_hist_btn.pack(side=tk.LEFT)



        self.status_var = tk.StringVar(value="Ready")

        self.status_label = ttk.Label(top, textvariable=self.status_var, foreground="#555")

        self.status_label.pack(side=tk.RIGHT)



        mid = ttk.Frame(self)

        mid.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)



        # Question

        q_frame = ttk.LabelFrame(mid, text="Question")

        q_frame.pack(fill=tk.BOTH, expand=False)

        self.q_text = tk.Text(q_frame, height=5, wrap=tk.WORD)

        self.q_text.pack(fill=tk.BOTH, expand=True)



        # Buttons

        btns = ttk.Frame(self)

        btns.pack(fill=tk.X, padx=12)

        self.ask_btn = ttk.Button(btns, text="Ask", command=self._on_ask)

        self.ask_btn.pack(side=tk.LEFT)



        # Answer

        a_frame = ttk.LabelFrame(self, text="Response")

        a_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        self.a_text = tk.Text(a_frame, height=20, wrap=tk.WORD)

        self.a_text.pack(fill=tk.BOTH, expand=True)



    def _load_clients(self):

        clients = []

        try:

            for p in Path(DATA_ROOT).iterdir():

                if p.is_dir():

                    clients.append(p.name)

        except Exception:

            pass

        if not clients:

            clients = ["client_example"]

        self.client_combo["values"] = clients

        if clients:

            self.client_combo.set(clients[0])



    def _set_status(self, text: str):

        self.status_var.set(text)

        self.update_idletasks()



    def _clear_history(self):

        self._history = []

        self.a_text.delete("1.0", tk.END)

        self._set_status("History cleared")



    # --- Actions ---

    def _on_index(self):

        client = self.client_combo.get()

        if not client:

            messagebox.showwarning("Client not found", "Choose client")

            return

        self._set_status(f"Indexation: {client}…")

        self.index_btn.configure(state=tk.DISABLED)

        threading.Thread(target=self._run_index_bg, args=(client,), daemon=True).start()



    def _run_index_bg(self, client: str):

        try:

            index_client(Path(DATA_ROOT), client)

            self.after(0, lambda: self._set_status("Indexation Complete"))

        except Exception as e:

            self.after(0, lambda: messagebox.showerror("Ошибка индексации", str(e)))

            self.after(0, lambda: self._set_status("Ошибка"))

        finally:

            self.after(0, lambda: self.index_btn.configure(state=tk.NORMAL))



    def _on_ask(self):

        client = self.client_combo.get()

        question = self.q_text.get("1.0", tk.END).strip()

        if not client:

            messagebox.showwarning("Нет клиента", "Выберите клиента")

            return

        if not question:

            messagebox.showwarning("Пустой вопрос", "Введите вопрос")

            return

        self.a_text.delete("1.0", tk.END)

        self._set_status("Генерация ответа…")

        self.ask_btn.configure(state=tk.DISABLED)

        threading.Thread(target=self._run_answer_bg, args=(client, question), daemon=True).start()



    def _append_answer(self, text: str):

        self.a_text.insert(tk.END, text)

        self.a_text.see(tk.END)



    def _run_answer_bg(self, client: str, question: str):

        def on_token(tok: str):

            self.after(0, lambda t=tok: self._append_answer(t))

        try:

            reply, self._history = answer_question(client, question, history=self._history, on_token=on_token)

            self.after(0, lambda: self._set_status("Готово"))

        except Exception as e:

            self.after(0, lambda: messagebox.showerror("Ошибка", str(e)))

            self.after(0, lambda: self._set_status("Ошибка"))

        finally:

            self.after(0, lambda: self.ask_btn.configure(state=tk.NORMAL))



def run_gui():

    app = LegalChatApp()

    app.mainloop()

