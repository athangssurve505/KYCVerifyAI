import base64

with open("Face5.jpg", "rb") as img:
    encoded = base64.b64encode(img.read()).decode("utf-8")

with open("b64.txt", "w") as f:
    f.write(encoded)

print("Base64 saved to b64.txt")
