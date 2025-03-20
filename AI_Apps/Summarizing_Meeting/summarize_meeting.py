from transformers import pipeline
import gradio as gr


# Function to transcribe audio using the OpenAI Whisper model
def transcript_audio(audio_file):
    pipe = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-tiny.en",
        chunk_length_s=30,
    )

    # Perform speech recognition on the audio file
    # The `batch_size=8` parameter indicates how many chunks are processed at a time
    # The result is stored in `prediction` with the key "text" containing the transcribed text
    prediction = pipe(audio_file, batch_size=8)["text"]

    return prediction


# Set up Gradio interface
audio_input = gr.Audio(sources="upload", type="filepath")  # Audio input
output_text = gr.Textbox()  # Text output

# Create the Gradio interface with the function, inputs, and outputs
iface = gr.Interface(
    fn=transcript_audio,
    inputs=audio_input,
    outputs=output_text,
    title="Audio Transcription App",
    description="Upload the audio file",
)

# Launch the Gradio app
iface.launch(server_name="127.0.0.1", server_port=8080)
