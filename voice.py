"""
Voice module — text-to-speech output for Sentinel.
Uses pyttsx3 (offline, no internet required).

If TTS is unavailable for any reason the module falls back silently
to printing the text in the terminal instead.
"""

from sentinel.modules import BaseModule


class VoiceModule(BaseModule):
    name = "voice"

    def __init__(self) -> None:
        self._engine = None
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty("rate", 165)    # words per minute
            engine.setProperty("volume", 1.0)  # 0.0 – 1.0
            self._engine = engine
        except Exception:
            # TTS unavailable (missing driver, headless env, etc.)
            pass

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def say(self, text: str) -> None:
        """Speak a line of text.  Falls back to print() if TTS is unavailable."""
        if self._engine is not None:
            try:
                # Suppress ALSA/aplay error spam on headless systems
                import os
                devnull_fd = os.open(os.devnull, os.O_WRONLY)
                saved_stderr = os.dup(2)
                os.dup2(devnull_fd, 2)
                try:
                    self._engine.say(text)
                    self._engine.runAndWait()
                finally:
                    os.dup2(saved_stderr, 2)
                    os.close(saved_stderr)
                    os.close(devnull_fd)
                return
            except Exception:
                pass
        # Fallback — always visible in the terminal
        print(f"[Sentinel] {text}")

    @property
    def tts_available(self) -> bool:
        return self._engine is not None

    def run(self) -> None:
        """Called by the registry on startup — reserved for future use."""
        pass
