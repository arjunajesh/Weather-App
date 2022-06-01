import tkinter as tk;
from tkinter import font
from matplotlib.pyplot import*
import requests
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

HEIGHT = 500
WIDTH = 600
ft = True
root = tk.Tk()

def get_weather(city):
    weather_key = '3cb84c2df62f062c4c904c0577d5e2be'
    url = 'https://api.openweathermap.org/data/2.5/forecast'
    params = {'APPID': weather_key, 'q':city, 'units':'imperial'}
    response = requests.get(url, params=params)  #Requests 3 hour 
    weather = response.json()
    list = []
    print(weather)
    for forecast in weather['list']: #iterates through each forecast
        x = forecast['dt_txt'] #finds date-time of the forecast
        x = x[11:13] #cut the string to just the time of the forecast
        if x == str(12):#only add forecast if time of day is 12 (so there will be 5 total) 
            tempDate = [forecast['main']['temp_max'], forecast['dt_txt']]
            list.append(tempDate)
    createPlot(list, weather['city']['name'])


canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

background = ImageTk.PhotoImage(Image.open('WeatherBg.jpg'))
background_label = tk.Label(root, image = background)
background_label.place(relwidth=1, relheight=1)

frame = tk.Frame(root, bg='#80c1ff', bd = 5)
frame.place(relx = 0.5, rely = 0.1, relwidth=0.85, relheight=0.1, anchor='n')

#SEARCH BAR
entry = tk.Entry(frame, font = 40)
entry.place(relwidth=0.65, relheight=1)

#GET WEATHER BUTTON
button = tk.Button(frame, text="Get Weather", font = 40, command=lambda:get_weather(entry.get()))
button.place(relx=0.7, relwidth=0.3, relheight = 1)

lower_frame = tk.Frame(root, bg='#80c1ff', bd = 5)
lower_frame.place(relx=0.5,rely=0.22, relwidth=0.85, relheight=0.6, anchor='n')

f = Figure(figsize=(5,5), dpi= 100)
canvas = FigureCanvasTkAgg(f, master = lower_frame) 
def createPlot(l, city):
    f.clear(True)
    y = []
    x = []
    for i in l:
        y.append(i[0])
        s = i[1]
        s = s[5:10]
        x.append(s)
    plot1 = f.add_subplot(111)
    title = '5-Day Forecast for ' + city
    plot1.title.set_text(title)
    plot1.set_ylabel('Temperature(F)')
    plot1.plot(x,y)
    
    canvas.draw()
    canvas.get_tk_widget().pack()


root.mainloop()