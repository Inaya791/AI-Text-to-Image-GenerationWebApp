from flask import Flask, request, jsonify, render_template
import openai
import base64
import os

app = Flask(__name__)

# Configure OpenAI client
client = openai.OpenAI(
    base_url="https://api.deepinfra.com/v1/openai",
    api_key="your api key"  # Replace with your actual API key aIsh: 
)

UPLOAD_FOLDER = "static/images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        response = client.images.generate(
            prompt=prompt,
            model="black-forest-labs/FLUX-1-schnell",
            n=4,
            size="1024x1024",
        )

        image_urls = []
        for i, img_data in enumerate(response.data):
            base64_data = img_data.b64_json
            image_data = base64.b64decode(base64_data)

            image_path = os.path.join(UPLOAD_FOLDER, f"generated_{i}.png")
            with open(image_path, "wb") as file:
                file.write(image_data)

            image_urls.append(f"/{image_path}")

        return jsonify({"images": image_urls})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
