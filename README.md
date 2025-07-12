# LocalAiChat

A simple Python-based Telegram bot that uses a locally running Large Language Model (LLM) to answer your questions. It's built with `aiogram` and uses `llama-cpp-python` to run an OpenAI-compatible server out of the box.

## Features

- **Run Locally**: All processing happens on your machine. The internet is only needed for the Telegram Bot API.
- **Easy to Start**: A `Makefile` helps you set up and run the project with just a few commands.
- **GGUF Support**: Works with models in the popular GGUF format.
- **Context-Aware**: Remembers the last few messages in a conversation.
- **Async Powered**: Built with `asyncio` for better performance.
- **GPU Acceleration**: Optional support for NVIDIA (CUDA) and Apple Silicon (Metal) GPUs.

## How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/LocalAiChat.git
cd LocalAiChat
```

### 2. Set Up Environment and Install Dependencies

Just run this command:

```bash
make setup
```

It will create a virtual environment in the `.venv` folder and install all the required libraries from `requirements.txt`.

### 3. Configure Environment Variables

Copy the example file to create your own configuration:

```bash
cp env.example .env
```

Now, open the `.env` file in a text editor and fill in the following:

- `BOT_TOKEN`: Your Telegram bot token. You can get one from [@BotFather](https://t.me/BotFather).
- `MODEL_PATH`: The path to your model file.

### 4. Download a Model

This project needs a model in the `.gguf` format. You can download a suitable model from [Hugging Face](https://huggingface.co/models?search=gguf).

We recommend using models designed for chat or instructions, like [Hermes-2-Pro-Llama-3-8B-GGUF](https://huggingface.co/NousResearch/Hermes-2-Pro-Llama-3-8B-GGUF).

After downloading the model:

1.  Create a `models` folder in the project's root directory.
2.  Place the model file (e.g., `Hermes-2-Pro-Llama-3-8B-Q4_K_M.gguf`) inside the `models` folder.
3.  Make sure the `MODEL_PATH` in your `.env` file is correct (e.g., `models/your_model_name.gguf`).

### 5. Run the Project

```bash
make run
```

This command starts both the AI server and the Telegram bot. You can now open a chat with your bot in Telegram and start talking!

## GPU Acceleration (Optional)

If you have a supported GPU, you can make the model run faster.

- **For NVIDIA (CUDA)**:
  Uncomment the line `CMAKE_ARGS="-DGGML_CUDA=on"` in the `Makefile` and run `make setup` again. You need to have the NVIDIA CUDA Toolkit installed.

- **For Apple Silicon (Metal)**:
  Metal support is usually enabled by default. If it's not working, uncomment `CMAKE_ARGS="-DLLAMA_METAL=on"` in the `Makefile` and run `make setup` again to reinstall dependencies.
