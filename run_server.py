import os
import uvicorn
from llama_cpp.server.app import create_app, Settings

def main():
    model_path = os.getenv("MODEL_PATH")
    if not model_path or not os.path.exists(model_path):
        print("Error: MODEL_PATH is not set or the file does not exist.")
        print("Please set MODEL_PATH in your .env file.")
        return

    settings = Settings(
        model=model_path,
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("LLAMA_PORT", "8000")),
        n_ctx=int(os.getenv("N_CTX", "2048")),
        n_gpu_layers=-1,
    )
    
    app = create_app(settings=settings)

    print(f"Starting LLaMA server on {settings.host}:{settings.port}...")
    
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
    )

if __name__ == "__main__":
    main() 