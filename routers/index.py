from fastapi.responses import HTMLResponse

from . import router


@router.get("/", response_class=HTMLResponse)
async def home_page():
    return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="robots" content="noindex,nofollow" />
            <meta
                property="og:image"
                content="https://ik.imagekit.io/ykidmzssaww/Hungry-Baby/site-images/thubb-icon_zoCbYRVTO.png"
            />
            <meta property="og:image:width" content="256" />
            <meta property="og:image:height" content="256" />
            <meta
                property="og:title"
                content="Recipes for Toddlers & Beyond"
            />
            <meta
                property="og:description"
                content="Meal ideas for toddlers and beyond. Make mealtime fun with our easy, healthy and delicious recipes. Explore breakfast, lunch, dinner, snack or dessert ideas for your child. While a lot of the posts focus on Indian recipes for toddlers, you will also find a whole bunch of easy and fun meal ideas that you can try no matter where you are."
            />
            <title>Recipes for Toddlers & Beyond</title>
            <link rel="icon" href="https://ik.imagekit.io/ykidmzssaww/Hungry-Baby/site-images/thubb-icon_zoCbYRVTO.png" />
            <style>
                html {
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                }

                body {
                    text-align: center;
                    background-color: #FDF2F8;
                }

                img {
                    margin-top: 150px;
                }

                p {
                    font-family: 'Franklin Gothic Medium', Arial, sans-serif;
                    font-size: 2em;
                    padding: 10px;
                    margin: 10px 20px;
                }

                span {
                    color: #DB2777;
                }

                a {
                    text-decoration: none;
                    color: #DB2777;
                }
            </style>
        </head>
        <body>
            <img src="https://ik.imagekit.io/ykidmzssaww/Hungry-Baby/site-images/thubb-icon_zoCbYRVTO.png" height="200px" alt="Brand Icon"/>
            <p>Welcome to <span><strong>The Hungry Baby Blog</strong></span></p>
            <p>Proceed to the website - <a href="https://hungrybabyblog.com">hungrybabyblog.com</a></p>
        </body>
        </html>
    """
