import gradio as gr
import requests
import pathlib
from PIL import Image
from io import BytesIO
import tempfile




def slugify(s: str) -> str:
    return s.lower().replace(" ", "-").replace(".", "-").replace("/", "-")[:32]

# def predict(···) -> np.ndarray | PIL.Image.Image | str | Path | None
# 	return value

# Define the function to handle the form and make a POST request
def send_post_request(PositivePrompt, Seed, Steps, Password):
    url = "https://n-v-r--n-v-r-endpoint-comfyui-api.modal.run"  # Replace with your actual endpoint
    payload = {
        "prompt": PositivePrompt, 
        "seed": Seed, 
        "steps": Steps,
        "password": Password 
    }
    
    try:
        response = requests.post(url, json=payload)
        # print("Response Status Code:", response.status_code)
        # print("Response Text:", response.text)
        # Process the response from the API
        if response.status_code == 200:
            
            # Get the system's temporary directory
            temp_dir = tempfile.gettempdir()

            print(f"Temporary directory: {temp_dir}")
            filename = pathlib.Path(temp_dir) / f"{slugify(PositivePrompt)}.png"
            filename.write_bytes(response.content)
            print(f"saved to '{filename}'")
            # print(response.content)
            # Convert the raw bytes to a PIL Image
            # image = Image.open(BytesIO(response.content))

            # image.save(filename, format="PNG")  # Save explicitly as PNG
            return filename  # Return the PIL Image to Gradio
        else:
            print(f"Error: {response.status_code}, {response.text}")
            gr.Warning(f"Error: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Failed to connect: {str(e)}")
        return None

# Create the Gradio interface
interface = gr.Interface(
    fn=send_post_request, 
    theme="soft",
    title = "Dream Car",
    inputs= [
        gr.Textbox(label="PositivePrompt"), 
        gr.Number(label="Seed", precision=0, value=1),  # Integer input 1
        gr.Number(label="Steps", precision=0, value=20),  # Integer input 2
        gr.Textbox(label="Password", type="password")  # Masked input for password
    ],
    # outputs=gr.Image()
    outputs=gr.Image(label="Generated Image", type="filepath", format='png'),
    css="footer {visibility: hidden}",
    # outputs=gr.File(),
    
    flagging_mode="never"  # Disable the flag button
)

# Launch the app
interface.launch(server_name="0.0.0.0", server_port=8080)




