def create_single_image(message):
    if message == "random":
        res_image = [
                {
                    "type": "image",
                    "originalContentUrl": "https://unsplash.it/630/400",
                    "previewImageUrl": "https://unsplash.it/630/400"
                }
            ]
    else:
        res_image = [
                {
                    "type": "image",
                    "originalContentUrl": "http://e-village.main.jp/gazou/image_gazou/gazou_0138.jpg",
                    "previewImageUrl": "http://e-village.main.jp/gazou/image_gazou/gazou_0138.jpg"
                }
            ]
    return res_image