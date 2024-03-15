< !DOCTYPE html >
    <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta http-equiv="X-UA-Compatible" content="IE=edge" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>Colorify</title>
            <link rel="stylesheet" href="./index.css" />
            <script src="./index.js" defer></script>
        </head>
        <body>
            <div class="container">
                <h1>Colorify</h1>
                <p class="subheading">
                    With colorify we want to start
                    learning JavaScript.
                </p>
                <div class="circle" id="circleID"></div>
                <div class="action">
                    <button onclick="paint('red')">Red</button>
                    <button onclick="paint('green')">Green</button>
                    <button onclick="paint('yellow')">Yellow</button>
                </div>
            </div>
        </body>
    </html>