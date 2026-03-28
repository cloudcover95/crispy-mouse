import threading
import time
from llama_cpp import Llama

# ==============================================================================
# SOVEREIGN PREDICTOR: OPTIMIZED LOCAL LLM ENGINE (Phi-3 Mini)
# ==============================================================================

class SovereignPredictor:
    """
    Threaded LLM inference engine for ultra-fast word completion.
    Optimized for Phi-3 Mini (1.4B) quantized model with 512 context window.
    """
    
    def __init__(self, model_path: str = "phi-3-mini-4k-instruct-q4.gguf", n_threads: int = 6):
        """
        Initialize Sovereign tensor engine
        
        Args:
            model_path: Path to .gguf model file (Phi-3 Mini recommended)
            n_threads: CPU threads for inference (should match physical cores)
        """
        print(f"[LLM] Booting Local Tensor Engine: {model_path}")
        try:
            # Optimize n_ctx (context window) to 512 for extreme speed
            # n_threads should map to physical cores of the Windows 11 CPU
            self.llm = Llama(
                model_path=model_path, 
                n_ctx=512, 
                n_threads=n_threads, 
                verbose=False
            )
            self.is_loaded = True
            print(f"[LLM] Model loaded successfully ({n_threads} threads, 512 ctx window)")
        except Exception as e:
            print(f"[LLM] Initialization Failure: {e}")
            self.is_loaded = False

        self.current_task = None
        self.cancel_flag = threading.Event()
        self.latest_predictions = ["...", "...", "..."]

    def _generate_predictions(self, context_buffer, callback):
        """
        Generate 3 word predictions via LLM inference
        
        Args:
            context_buffer: Current text context (word being typed)
            callback: Function to call with results [word1, word2, word3]
        """
        if not self.is_loaded or len(context_buffer.strip()) < 2:
            return

        # Engineered prompt to force 3 discrete comma-separated options
        prompt = f"Complete this text naturally. Reply ONLY with 3 single-word options separated by commas.\nText: {context_buffer}"
        
        try:
            response = self.llm(
                prompt,
                max_tokens=15,
                temperature=0.2,  # Low temperature for deterministic, logical completions
                stop=["\n", ".", "!"],
                echo=False
            )
            
            if self.cancel_flag.is_set():
                return  # User typed a new letter; discard this branch

            output = response['choices'][0]['text'].strip()
            # Clean and split the LLM output tensor
            words = [w.strip() for w in output.split(',') if w.strip()]
            
            # Pad array if model returns fewer than 3 options
            while len(words) < 3: 
                words.append("...")
            
            self.latest_predictions = words[:3]
            callback(self.latest_predictions)

        except Exception as e:
            print(f"[LLM] Inference Vector Error: {e}")

    def request_completion(self, context_buffer, callback):
        """
        Request word predictions (async, non-blocking)
        
        Kill any active inference threads to free CPU cycles for responsiveness.
        
        Args:
            context_buffer: Current text context
            callback: Function to execute with [pred1, pred2, pred3]
        """
        # Kill any active inference threads to free CPU cycles
        if self.current_task and self.current_task.is_alive():
            self.cancel_flag.set()
            self.current_task.join(timeout=0.1)
        
        self.cancel_flag.clear()
        self.current_task = threading.Thread(
            target=self._generate_predictions, 
            args=(context_buffer, callback),
            daemon=True
        )
        self.current_task.start()

# ==============================================================================
# GLOBAL SINGLETON
# ==============================================================================
_predictor: SovereignPredictor = None

def get_predictor(model_path: str = "phi-3-mini-4k-instruct-q4.gguf", 
                  n_threads: int = 6) -> SovereignPredictor:
    """Get or create the global Sovereign Predictor"""
    global _predictor
    if _predictor is None:
        _predictor = SovereignPredictor(model_path=model_path, n_threads=n_threads)
    return _predictor

def initialize_predictor(model_path: str = "phi-3-mini-4k-instruct-q4.gguf",
                        n_threads: int = 6) -> SovereignPredictor:
    """Initialize the Sovereign Predictor engine"""
    return get_predictor(model_path=model_path, n_threads=n_threads)
