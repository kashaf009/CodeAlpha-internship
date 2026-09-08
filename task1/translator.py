import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator
import pyperclip
import threading
from typing import Optional


# ============================================================================
# Configuration
# ============================================================================

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Urdu": "ur",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh-CN",
    "Arabic": "ar",
    "Russian": "ru"
}

MAX_CHAR_LIMIT = 500

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
WINDOW_MIN_WIDTH = 700
WINDOW_MIN_HEIGHT = 600


# ============================================================================
# Translator
# ============================================================================

class TranslatorWorker:
    """Handles translation using GoogleTranslator."""

    @staticmethod
    def translate(
        text: str,
        source_lang: str,
        target_lang: str
    ) -> Optional[str]:

        if source_lang == target_lang:
            return text

        try:
            translator = GoogleTranslator(
                source=source_lang,
                target=target_lang
            )

            result = translator.translate(text)

            if not result:
                raise Exception("Translation service returned an empty result.")

            return result

        except Exception as e:
            raise Exception(f"Translation failed: {str(e)}")


# ============================================================================
# Main Application
# ============================================================================

class TranslatorApp:

    def __init__(self, root: tk.Tk):

        self.root = root

        self.root.title("Language Translator Pro")
        self.root.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
        )

        self.root.minsize(
            WINDOW_MIN_WIDTH,
            WINDOW_MIN_HEIGHT
        )

        self.root.configure(bg="#f4f6f8")

        self.is_translating = False

        # Keyboard shortcuts
        self.root.bind(
            "<Control-Return>",
            lambda event: self.translate_text()
        )

        self.root.bind(
            "<Control-c>",
            lambda event: self.copy_translation()
        )

        self.setup_ui()

    # ========================================================================
    # UI
    # ========================================================================

    def setup_ui(self):

        self._create_title()
        self._create_language_selector()
        self._create_text_areas()
        self._create_character_counter()
        self._create_buttons()
        self._create_footer()

    # ========================================================================
    # Title
    # ========================================================================

    def _create_title(self):

        title = tk.Label(
            self.root,
            text="🌐 Language Translator Pro",
            font=("Arial", 28, "bold"),
            bg="#f4f6f8",
            fg="#222222"
        )

        title.pack(pady=(20, 5))

        subtitle = tk.Label(
            self.root,
            text="Fast and accurate translations",
            font=("Arial", 11),
            bg="#f4f6f8",
            fg="#666666"
        )

        subtitle.pack(pady=(0, 15))

    # ========================================================================
    # Language Selection
    # ========================================================================

    def _create_language_selector(self):

        language_frame = tk.Frame(
            self.root,
            bg="#f4f6f8"
        )

        language_frame.pack(pady=10)

        # Source language

        self.source_language = ttk.Combobox(
            language_frame,
            values=list(LANGUAGES.keys()),
            state="readonly",
            width=18,
            font=("Arial", 11)
        )

        self.source_language.set("English")

        self.source_language.grid(
            row=0,
            column=0,
            padx=15
        )

        # Swap

        swap_button = tk.Button(
            language_frame,
            text="⇄ Swap",
            font=("Arial", 11, "bold"),
            command=self.swap_languages,
            bg="#ffffff",
            fg="#2563eb",
            relief="flat",
            padx=15,
            cursor="hand2"
        )

        swap_button.grid(
            row=0,
            column=1,
            padx=10
        )

        # Target language

        self.target_language = ttk.Combobox(
            language_frame,
            values=list(LANGUAGES.keys()),
            state="readonly",
            width=18,
            font=("Arial", 11)
        )

        self.target_language.set("Hindi")

        self.target_language.grid(
            row=0,
            column=2,
            padx=15
        )

    # ========================================================================
    # Text Areas
    # ========================================================================

    def _create_text_areas(self):

        text_frame = tk.Frame(
            self.root,
            bg="#f4f6f8"
        )

        text_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=20
        )

        # --------------------------------------------------------------------
        # Input
        # --------------------------------------------------------------------

        input_frame = tk.Frame(
            text_frame,
            bg="white",
            highlightbackground="#dddddd",
            highlightthickness=1
        )

        input_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        input_label = tk.Label(
            input_frame,
            text="Enter Text",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#333333"
        )

        input_label.pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )

        self.input_text = tk.Text(
            input_frame,
            wrap="word",
            font=("Arial", 12),
            bg="white",
            fg="#222222",
            relief="flat",
            padx=15,
            pady=10
        )

        self.input_text.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        self.input_text.bind(
            "<KeyRelease>",
            self.update_char_count
        )

        # --------------------------------------------------------------------
        # Output
        # --------------------------------------------------------------------

        output_frame = tk.Frame(
            text_frame,
            bg="white",
            highlightbackground="#dddddd",
            highlightthickness=1
        )

        output_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        output_label = tk.Label(
            output_frame,
            text="Translation",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#333333"
        )

        output_label.pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )

        self.output_text = tk.Text(
            output_frame,
            wrap="word",
            font=("Arial", 12),
            bg="white",
            fg="#2563eb",
            relief="flat",
            padx=15,
            pady=10,
            state="disabled"
        )

        self.output_text.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

    # ========================================================================
    # Character Counter
    # ========================================================================

    def _create_character_counter(self):

        counter_frame = tk.Frame(
            self.root,
            bg="#f4f6f8"
        )

        counter_frame.pack(
            padx=35,
            fill="x"
        )

        self.char_label = tk.Label(
            counter_frame,
            text="Characters: 0 / 500",
            font=("Arial", 9),
            bg="#f4f6f8",
            fg="#888888"
        )

        self.char_label.pack(
            anchor="e"
        )

    # ========================================================================
    # Buttons
    # ========================================================================

    def _create_buttons(self):

        button_frame = tk.Frame(
            self.root,
            bg="#f4f6f8"
        )

        button_frame.pack(pady=15)

        self.translate_button = tk.Button(
            button_frame,
            text="🚀 Translate (Ctrl+Enter)",
            command=self.translate_text,
            font=("Arial", 12, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            padx=25,
            pady=10,
            cursor="hand2"
        )

        self.translate_button.grid(
            row=0,
            column=0,
            padx=8
        )

        copy_button = tk.Button(
            button_frame,
            text="📋 Copy",
            command=self.copy_translation,
            font=("Arial", 11),
            bg="white",
            fg="#333333",
            relief="solid",
            padx=20,
            pady=9,
            cursor="hand2"
        )

        copy_button.grid(
            row=0,
            column=1,
            padx=8
        )

        clear_button = tk.Button(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_text,
            font=("Arial", 11),
            bg="white",
            fg="#333333",
            relief="solid",
            padx=20,
            pady=9,
            cursor="hand2"
        )

        clear_button.grid(
            row=0,
            column=2,
            padx=8
        )

    # ========================================================================
    # Footer
    # ========================================================================

    def _create_footer(self):

        footer = tk.Label(
            self.root,
            text="⌨️ Ctrl+Enter to translate | Ctrl+C to copy | Max 500 characters",
            font=("Arial", 9),
            bg="#f4f6f8",
            fg="#888888"
        )

        footer.pack(
            pady=(0, 15)
        )

    # ========================================================================
    # Character Count
    # ========================================================================

    def update_char_count(self, event=None):

        text = self.input_text.get(
            "1.0",
            tk.END
        ).strip()

        char_count = len(text)

        if char_count > MAX_CHAR_LIMIT:

            color = "#e74c3c"

        elif char_count > MAX_CHAR_LIMIT * 0.8:

            color = "#f39c12"

        else:

            color = "#888888"

        self.char_label.config(
            text=f"Characters: {char_count} / {MAX_CHAR_LIMIT}",
            fg=color
        )

    # ========================================================================
    # Translation
    # ========================================================================

    def translate_text(self):

        if self.is_translating:
            return

        text = self.input_text.get(
            "1.0",
            tk.END
        ).strip()

        source = self.source_language.get()
        target = self.target_language.get()

        # Validation

        if not text:

            messagebox.showwarning(
                "Input Error",
                "Please enter some text to translate."
            )

            return

        if len(text) > MAX_CHAR_LIMIT:

            messagebox.showwarning(
                "Input Error",
                f"Text exceeds {MAX_CHAR_LIMIT} characters."
            )

            return

        if source == target:

            self.show_translation(text)

            return

        # Start translation

        self.is_translating = True

        self.translate_button.config(
            state="disabled",
            text="⏳ Translating..."
        )

        thread = threading.Thread(
            target=self._translate_worker,
            args=(text, source, target),
            daemon=True
        )

        thread.start()

    # ========================================================================
    # Translation Worker
    # ========================================================================

    def _translate_worker(
        self,
        text: str,
        source: str,
        target: str
    ):

        try:

            translated = TranslatorWorker.translate(
                text,
                LANGUAGES[source],
                LANGUAGES[target]
            )

            # IMPORTANT:
            # Send result back to Tkinter main thread

            self.root.after(
                0,
                self.translation_success,
                translated
            )

        except Exception as e:

            self.root.after(
                0,
                self.translation_error,
                str(e)
            )

    # ========================================================================
    # Translation Success
    # ========================================================================

    def translation_success(self, translated):

        self.show_translation(translated)

        self.is_translating = False

        self.translate_button.config(
            state="normal",
            text="🚀 Translate (Ctrl+Enter)"
        )

    # ========================================================================
    # Translation Error
    # ========================================================================

    def translation_error(self, error):

        self.is_translating = False

        self.translate_button.config(
            state="normal",
            text="🚀 Translate (Ctrl+Enter)"
        )

        messagebox.showerror(
            "Translation Error",
            error
        )

    # ========================================================================
    # Show Translation
    # ========================================================================

    def show_translation(self, text):

        self.output_text.config(
            state="normal"
        )

        self.output_text.delete(
            "1.0",
            tk.END
        )

        self.output_text.insert(
            tk.END,
            text
        )

        self.output_text.config(
            state="disabled"
        )

    # ========================================================================
    # Swap Languages
    # ========================================================================

    def swap_languages(self):

        source = self.source_language.get()
        target = self.target_language.get()

        self.source_language.set(target)
        self.target_language.set(source)

        input_content = self.input_text.get(
            "1.0",
            tk.END
        ).strip()

        self.output_text.config(
            state="normal"
        )

        output_content = self.output_text.get(
            "1.0",
            tk.END
        ).strip()

        self.output_text.config(
            state="disabled"
        )

        self.input_text.delete(
            "1.0",
            tk.END
        )

        self.input_text.insert(
            tk.END,
            output_content
        )

        self.show_translation(
            input_content
        )

        self.update_char_count()

    # ========================================================================
    # Copy
    # ========================================================================

    def copy_translation(self):

        self.output_text.config(
            state="normal"
        )

        translated = self.output_text.get(
            "1.0",
            tk.END
        ).strip()

        self.output_text.config(
            state="disabled"
        )

        if not translated:

            messagebox.showwarning(
                "No Translation",
                "Nothing to copy. Translate first!"
            )

            return

        try:

            pyperclip.copy(
                translated
            )

            messagebox.showinfo(
                "Copied",
                "Translation copied to clipboard!"
            )

        except Exception as e:

            messagebox.showerror(
                "Copy Error",
                str(e)
            )

    # ========================================================================
    # Clear
    # ========================================================================

    def clear_text(self):

        self.input_text.delete(
            "1.0",
            tk.END
        )

        self.output_text.config(
            state="normal"
        )

        self.output_text.delete(
            "1.0",
            tk.END
        )

        self.output_text.config(
            state="disabled"
        )

        self.update_char_count()


# ============================================================================
# Application Entry Point
# ============================================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = TranslatorApp(root)

    root.mainloop()