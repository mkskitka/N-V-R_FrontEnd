import gradio as gr
import requests
import pathlib
from PIL import Image
from io import BytesIO
import tempfile
from PIL import Image
import io 
import base64
from custom_css import custom_css
from constants import paintNames
from constants import backgroundNames
from constants import BLACK_HEX, BLACK_MAT, BLACK, BLUE_PAINT, RED_PAINT, CAMO_ONE, CAMO_TWO, CAMO_THREE, PEARL_ONE, PEARL_TWO, GOLD, RUSTED,WHITE_MAT, TIGER,RED_IRIDESCENT, NTNSTY, ANIME, TUNING, UNDERGROUND_GARAGE,UNDERWATER, COMIC, DREAMSCAPE, FILM_NOIR, JUNGLE, MIAMI_NIGHTS, NEON, POST_APO


def slugify(s: str) -> str:
    return s.lower().replace(" ", "-").replace(".", "-").replace("/", "-")[:32]


# Define the function to handle the form and make a POST request
def send_post_request(Car, Background, Paint, Password ):
    # url = "https://n-v-r--n-v-r-dream-car-comfyui-api-dev.modal.run"  # Replace with your actual endpoint
            # Convert the image (PIL format) to bytes
    buffered = io.BytesIO()
    Car.save(buffered, format="PNG")
    buffered.seek(0)

     # Encode the image in Base64
    image_base64 = base64.b64encode(buffered.read()).decode("utf-8")

    # Deployment 
    url = "https://n-v-r--n-v-r-dream-car-comfyui-api.modal.run"
    payload = {
        "password": Password,
        "paint": paintNames[Paint], 
        "background": backgroundNames[Background],
        "car": image_base64
    }
    
    try:
        response = requests.post(url, json=payload)
        print("\n\n response code: ", response.status_code)
        # print("\n\n response text: ", response.text)
        # Process the response from the API
        if response.status_code == 200:
            
            # Get the system's temporary directory
            temp_dir = tempfile.gettempdir()
            # print(response.content)
            print(f"Temporary directory: {temp_dir}")
            filename1= Paint+"_"+Background
            filename = pathlib.Path(temp_dir) / f"{slugify(filename1)}.png"
            filename.write_bytes(response.content)
            print(f"saved to '{filename}'")

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
    theme="Base",
    # (primary_hue="red", secondary_hue="pink")
    title = "N-V-R | DREAM CAR",
    inputs= [
        gr.Image(type="pil"),
        gr.Dropdown(
            [NTNSTY, ANIME, TUNING, UNDERGROUND_GARAGE,
                UNDERWATER, COMIC, DREAMSCAPE, FILM_NOIR, 
                JUNGLE, MIAMI_NIGHTS, NEON, POST_APO], 
            value=NTNSTY, multiselect=False, label="Pick a Style", info=""
        ),
        gr.Dropdown(
            [BLACK_HEX, BLACK_MAT, BLACK, BLUE_PAINT,
              RED_PAINT, CAMO_ONE, CAMO_TWO, CAMO_THREE, 
              PEARL_ONE, PEARL_TWO, GOLD, RUSTED,WHITE_MAT,
              TIGER,RED_IRIDESCENT], 
            value=BLACK_MAT, multiselect=False, label="Pick a Paint", info=""
        ),
        gr.Textbox(label="Password", type="password"),  # Masked input for password
        # gr.Button(value="Render")  # Custom submit button
    ],
    # outputs=gr.Image()
    outputs=gr.Image(type="filepath", format='png'),
    css=custom_css,  # Apply the custom CSS
    # outputs=gr.File(),
    flagging_mode="never"  # Disable the flag button
)

# Launch the app
interface.launch(server_name="0.0.0.0", server_port=8080)




