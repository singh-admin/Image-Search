import requests
import io
from flask import Flask, request, Response
from flask_restx import Api, Resource
from urllib.parse import quote
from PIL import Image



app = Flask(__name__)



api = Api(app, title="Image Search API", description="An API to perform image searches")


# Replace with your API key and Custom Search Engine ID
API_KEY = "AIzSyDS-V1wpMDddYItrmAuFXnnwmsC9eMpAWa"
CSE_ID = "065ef161f3b8f4ac7"


# Endpoint to perform an image search
@api.route("/imageSearch")
class ImageSearch(Resource):
    def get(self):
        try:
            query = request.args.get("query")
            encoded_query = quote(query)
            params = {"key": API_KEY, "cx": CSE_ID, "q": encoded_query, "searchType": "image"}
            response = requests.get("https://www.googleapis.com/customsearch/v1", params=params)
            data = response.json()
            if "items" in data:
                for item in data["items"]:
                    image_url = item["link"]
                    image_data = requests.get(image_url).content
                    img = Image.open(io.BytesIO(image_data))
                    # Resize the image
                    new_size = (370, 370)
                    img_resized = img.resize(new_size)
                    # Convert the resized image back to bytes
                    img_resized_bytes = io.BytesIO()
                    img_resized.save(img_resized_bytes, format="JPEG")
                    img_resized_data = img_resized_bytes.getvalue()
                    response = Response(img_resized_data, content_type="image/jpeg")
                    return response
            return {"status_code": 400, "message": "image not found"}
        except (IOError, OSError) as image_exc:
            print("Image processing exception:", image_exc)
            return {"status_code": 500, "message": "internal server error"}
    

if __name__ == "__main__":
    app.run(debug=True)

