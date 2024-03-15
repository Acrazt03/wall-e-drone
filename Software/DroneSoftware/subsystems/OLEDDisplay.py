import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

from threading import Thread
from collections import deque
import logging
import time

time.sleep(5)

logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
logging.info("OLED display ran!")

class OLEDDisplay:
    WIDTH = 128
    HEIGHT = 64 

    def __init__(self, addr=0x3C):
        logging.info('Init i2c')

        try:
            self.i2c = busio.I2C(board.SCL_1, board.SDA_1)
            self.oled = adafruit_ssd1306.SSD1306_I2C(self.WIDTH, self.HEIGHT, self.i2c, addr=addr)
            print('OLED Display initiated!')
            self.clear()
            logging.info('i2c Initiated!')

        except Exception as e:
            logging.info(f'OLED Display had this Exception: {str(e)}')

        self.printRequests = deque()

        self.thread = Thread(target=self.handleRequests)
        self.thread.start()

    def handleRequests(self):
        while True:
            
            #self.clear()

            if len(self.printRequests) > 0:
                request_info, request_type = self.printRequests.pop()

                if request_type == 'line':
                    request_text = request_info[0]
                    request_duration = request_info[1]
                    self.print(request_text)
                    time.sleep(request_duration)

                elif request_type == 'lines':

                    request_texts = request_info[0]
                    request_durations = request_info[1]

                    for request_text, request_duration in zip(request_texts, request_durations):
                        self.print(request_text)
                        time.sleep(request_duration)
            else:
                self.clear()

    def clear(self):
        self.oled.fill(0)
        self.oled.show()

    #TODO: Personalize print
    def print(self, text: str=''):
        BORDER = 5

        image = Image.new("1", (self.WIDTH, self.HEIGHT))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Draw a white background
        draw.rectangle((0, 0, self.WIDTH, self.HEIGHT), outline=255, fill=255)

        # Draw a smaller inner rectangle
        draw.rectangle(
            (BORDER, BORDER, self.WIDTH- BORDER - 1, self.HEIGHT - BORDER - 1),
            outline=0,
            fill=0,
        )

        # Load default font.
        font = ImageFont.load_default()

        # Draw Some Text
        (font_width, font_height) = font.getsize(text)
        draw.text(
            (self.WIDTH // 2 - font_width // 2, self.HEIGHT // 2 - font_height // 2),
            text,
            font=font,
            fill=255,
        )

        # Display image
        self.oled.image(image)
        self.oled.show()

import uvicorn
from optparse import OptionParser
from fastapi import FastAPI
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()

app.display = OLEDDisplay()
logging.info("OLED display initiated!")

@app.get("/print")
async def getPrints():
    return app.display.printRequests

class PrintLineRequest(BaseModel):
    text: str
    duration: Optional[float] = 0.5 #If duration is not specified then show fo only one second

@app.post("/printLine")
async def printOnScreen(printRequest: PrintLineRequest):
    #logging.info(f"OLED display said: {printRequest.text} for {printRequest.duration} secs.!")
    app.display.printRequests.append(((printRequest.text, printRequest.duration), 'line'))
    return printRequest

class PrintSequenceRequest(BaseModel):
    texts: List[str] = ["lines"]
    durations: List[float] = [0.5]

@app.post("/printSequence")
async def printOnScreen(printRequest: PrintSequenceRequest):
    app.display.printRequests.append(((printRequest.texts, printRequest.durations), 'lines'))
    return printRequest

if __name__ == '__main__':
    parser = OptionParser("oled_dispaly.py [options]")

    parser.add_option("--port", dest="port", action="store", default=5001, type="int", help="The web port for the API")

    (opts, args) = parser.parse_args()

    uvicorn.run(app, port=opts.port)

    