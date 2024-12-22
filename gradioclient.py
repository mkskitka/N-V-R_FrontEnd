import gradio as gr
import requests
import pathlib
from PIL import Image
from io import BytesIO
import tempfile
from PIL import Image
import io 
import base64

# Define custom CSS to use Lato font
# custom_css = """
# @import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap');

# body {
#     font-family: 'Lato', sans-serif;
# }
# """
# custom_css = "footer {visibility: hidden}"

custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap');

body, button, input, select, textarea, h1, h2, h3, h4, h5, h6, p, span, label {
    font-family: 'Lato', sans-serif !important;
    font-weight: 400;
    text-transform: uppercase;
    background-color: black !important;
}

/* Bold headings */
h1, h2, h3, h4, h5, h6, strong {
    font-weight: 400;
    text-transform: uppercase; /* Ensure bold text is also uppercase */
}

/* Make all divs black */
div {
    background-color: black !important;
    color: white !important; /* Ensure text remains visible */
    border: 0px solid white !important;
}

/* Title left-aligned */
h1 {
    text-align: left !important; /* Left-align the title */
}


/* Add a white thin border to dropdowns, buttons, and form inputs */
button {
    border: 1px solid white !important;
    background-color: black !important; /* Ensure inputs have black background */
    color: white !important; /* Ensure text inside is visible */

    border-radius: 4px;
}
input {
    background-color: #111 !important;
    padding: 10px; /* Increase padding to make the dropdown bigger */
    border-radius: 4px;
    font-size: 16px; /* Increase font size */
    width: 100% !important;
    position: relative !important;
}

/* Hide the footer */
footer {
    visibility: hidden;
}
"""

# Paint Names 
BLACK_HEX = "Black Hex"
BLACK_MAT = "Black Mat Paint"
BLACK = "Black Paint"
BLUE_PAINT = "Blue Paint"
CAMO_ONE = "Camo 01"
CAMO_TWO = "Camo 02"
CAMO_THREE = "Camo 03"
RED_PAINT = "Red Paint"
PEARL_ONE = "Pearl 01"
PEARL_TWO = "Pearl 02"
GOLD = "Gold Iridescent Paint"
RUSTED = "Rusted Paint"
WHITE_MAT =  "White Mat Paint"
TIGER = "Tiger"
RED_IRIDESCENT =  "Red Iridescent Paint"

# Background Names 
NTNSTY = "1960"
ANIME = "Anime"
TUNING = "Tuning"
UNDERGROUND_GARAGE = "Underground Garage"
UNDERWATER = "Underwater"
COMIC = "Comic"
DREAMSCAPE = "Dreamscape Clouds"
FILM_NOIR = "Film Noir"
JUNGLE = "Jungle"
MIAMI_NIGHTS = "Miami Nights"
NEON = "Neon"
POST_APO = "Post Apo"


paintNames = {
    "None": "None",
    BLACK_HEX: "Black_Hex_Paint",
    BLACK_MAT: "Black_Mat_Paint",
    BLACK: "Black_Paint",
    BLUE_PAINT: "Blue_Paint",
    CAMO_ONE: "Camo_Paint", 
    CAMO_TWO: "Camouflage2", 
    CAMO_THREE: "Camouflage3", 
    RED_PAINT: "Red_Paint",
    PEARL_ONE: "Pearl",
    PEARL_TWO: "Pearl02",
    GOLD: "Gold_Iridescent_Paint",
    RUSTED: "Rusted_Paint",
   WHITE_MAT: "White_Mat_Paint",
   TIGER: "Tiger",
   RED_IRIDESCENT: "Red_Iridescent_Paint",
}

backgroundNames = {
    "None": "None",
    NTNSTY: "1960",
    ANIME: "Anime", 
    TUNING: "Tuning",
    UNDERGROUND_GARAGE: "UndergroundGarage",
    UNDERWATER: "Underwater",
    COMIC: "Comic",
    DREAMSCAPE: "Dreamscape_Clouds",
    FILM_NOIR: "Film_Noir",
    JUNGLE: "Jungle",
    MIAMI_NIGHTS: "MiamiNights",
    NEON:  "Neon",
    POST_APO: "PostApo",
}


def slugify(s: str) -> str:
    return s.lower().replace(" ", "-").replace(".", "-").replace("/", "-")[:32]


# Define the function to handle the form and make a POST request
def send_post_request(Car, Paint, Background, Password ):
    # Dev
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

# Define a custom theme
# custom_theme = gr.themes.Base(
#     primary_hue="gray",  # Primary color
#     secondary_hue="gray"  # Secondary color
# )
# Create the Gradio interface
interface = gr.Interface(
    fn=send_post_request, 
    theme="Base",
    # (primary_hue="red", secondary_hue="pink")
    title = "N-V-R | DREAM CAR",
    inputs= [
        gr.Image(type="pil", label="Car"),
        gr.Dropdown(
            ["None", BLACK_HEX, BLACK_MAT, BLACK, BLUE_PAINT, RED_PAINT, CAMO_ONE, CAMO_TWO, CAMO_THREE, PEARL_ONE, PEARL_TWO, GOLD, RUSTED,WHITE_MAT,TIGER,RED_IRIDESCENT], 
            value="None", multiselect=False, label="Paint", info=""
        ),

        gr.Dropdown(
                ["None",NTNSTY, ANIME, TUNING, UNDERGROUND_GARAGE, UNDERWATER, COMIC, DREAMSCAPE, FILM_NOIR, JUNGLE, MIAMI_NIGHTS, NEON, POST_APO], 
                value="None", multiselect=False, label="Background", info=""
        ),
        gr.Textbox(label="Password", type="password"),  # Masked input for password
        # gr.Button(value="Render")  # Custom submit button
    ],
    # outputs=gr.Image()
    outputs=gr.Image(label="Generated Image", type="filepath", format='png'),
    css=custom_css,  # Apply the custom CSS
    # outputs=gr.File(),
    flagging_mode="never"  # Disable the flag button
)

# Manually create a custom submit button with "Render"
# submit_button = gr.Button(value="Render")

# Adding the submit button
# interface.add_component(submit_button)

# Launch the app
interface.launch(server_name="0.0.0.0", server_port=8080)




