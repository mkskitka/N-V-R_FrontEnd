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

.gradio-container {background-color: black !important}

/* Title left-aligned */
h1 {
    text-align: left !important; /* Left-align the title */
}

.gradio-app, .gradio-container {
    background-color: 'black' !important
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
    padding: 20px; /* Increase padding to make the dropdown bigger */
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