import requests
from PIL import Image, ImageDraw, ImageTk
import os
import tkinter as tk
import zipfile

"""
    HACKATHON 2024 GROUP GUPTA'S GOONS - Charlie VandenBosch and Dylan Clements
    Please run 'pip install requests' and 'pip install Pillow' in your terminal before running program
    Also make sure the two images in the zip file are in the same place as this python file
"""

# This is for zipping the files
def zip():
    python_filename = 'LeafyLessons.py'
    image1_filename = 'heatMap.png'
    image2_filename = 'treeMap.png'
    zip_filename = 'unzipme.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        zip_file.write(python_filename)
    with zipfile.ZipFile(zip_filename, 'a') as zip_file:
        zip_file.write(image1_filename)
    with zipfile.ZipFile(zip_filename, 'a') as zip_file:
        zip_file.write(image2_filename)

# Returns the user's ip address
def get_ip_from_user():
    response = requests.get('https://httpbin.org/ip')
    data = response.json()
    user_ip_address = data['origin']
    return user_ip_address

# Uses ip-api to extract the city and lat&long from the input ip address
# Also makes sure the user is in Worcester
def get_lat_long(ip_address):
    response = requests.get(f'http://ip-api.com/json/{ip_address}')
    data = response.json()
    city = data['city']
    if city != 'Worcester':
        print('Sorry, you are outside of Worcester, therefore, not on this map')
        return None
    else:
        lat = data['lat']
        lon = data['lon']
        lat_plus_lon = str(lat) + '#' + str(lon)
        return lat_plus_lon

# Handles user location and image information
def images(user_pixel_info):
    # Split pixel info
    user_split_pixel = user_pixel_info.split('#')
    user_pixel_x = int(user_split_pixel[0])
    user_pixel_y = int(user_split_pixel[1])

    # Get the full path to the image file
    path = str(os.path.dirname(os.path.abspath(__file__)))
    heat_image_path = path + '/heatMap.png'
    tree_image_path = path + '/treeMap.png'

    # Load the images
    image1 = Image.open(heat_image_path)
    image2 = Image.open(tree_image_path)
    
    # Define the color and size of the marker
    marker_color = (255, 0, 0)  # Red color
    marker_size = 10

    # Create a drawing object
    draw = ImageDraw.Draw(image1)
    draw2 = ImageDraw.Draw(image2)
    # Draw a marker at the user's pixel coordinates on both maps
    draw.ellipse((user_pixel_x - marker_size, user_pixel_y - marker_size,
                    user_pixel_x + marker_size, user_pixel_y + marker_size),
                    fill=marker_color)
    draw2.ellipse((user_pixel_x - marker_size, user_pixel_y - marker_size,
                    user_pixel_x + marker_size, user_pixel_y + marker_size),
                    fill=marker_color)

    # Convert image to Tkinter-compatible objects
    img1 = ImageTk.PhotoImage(image1)
    img2 = ImageTk.PhotoImage(image2)

    # Display images in labels
    label1.configure(image=img1)
    label2.configure(image=img2)
    label1.image = img1
    label2.image = img2

# Runs the correct functions in the right order
def update_images():
    ip_address = get_ip_from_user()
    lat_long = get_lat_long(ip_address)
    user_pixel_info = get_pixel_coords(lat_long)
    images(user_pixel_info)

# Calculates the user's pixel coordinates from their lat long
def get_pixel_coords(lat_plus_lon):
    # Split lat long
    split_latlon = lat_plus_lon.split('#')
    lat = split_latlon[0]
    long = split_latlon[1]

    # Dimensions of the maps (in pixels)
    map_width = 635
    map_height = 738

    # Boundary coordinates of map (lat long of corners)
    map_top_left_latlon = (42.341181, -71.884035)
    map_bottom_right_latlon = (42.210027, -71.731253)

    # Convert lat and long to pixel coordinates
    user_pixel_x = int((float(long) - map_top_left_latlon[1]) / (map_bottom_right_latlon[1] - map_top_left_latlon[1]) * map_width)
    user_pixel_y = int((float(lat) - map_top_left_latlon[0]) / (map_bottom_right_latlon[0] - map_top_left_latlon[0]) * map_height)

    # return pixel info
    user_pixel_info = str(user_pixel_x) + '#' + str(user_pixel_y)
    return user_pixel_info

# Creates and manages the second window
def show_additional_window():
    # Create the window
    additional_window = tk.Toplevel(root)
    additional_window.title("Additional Information")

    # Add text to the new window
    text = tk.Text(additional_window, wrap=tk.WORD)
    text.pack(expand=True, fill=tk.BOTH)

    # Insert text
    text.insert(tk.END, 
                "Cities tend to be 1-7°F hotter than their suburban counterparts. This is primarily due to the abundance of heat absorbing materials such as asphalt and concrete, alongside the lack of vegetation." + '\n' + 
                '\n' + 
                "Every road, sidewalk, parking lot, and concrete building is a magnet for heat and slowly seeps it into the air close to the ground. This artificial rise in heat causes two main issues:" + '\n' + 
                '\n' + 
                "One is the quality of life of residents, extreme high temperatures can make going outside dangerous and day to day activities harder." + '\n' + 
                "The second is the environmental impact, the hotter it is the more people have to do to cool down. Air conditioning is responsible for nearly four percent of the world's greenhouse gas emissions, so this problem is self-fulfilling." + '\n' +
                '\n' +
                "The hotter it gets, the more AC units are used, the more they are used, the worse Global Warming gets. So tackling artificial heat at the roots is key." + '\n' + 
                '\n' +
                "Researchers from the Urban Climate Lab at the Georgia Institute of Technology conducted a Heat Risk assessment for Worcester, in which they created an up to date heat map of the city." + '\n' + 
                "The consensus was that much of Worcester is at medium or even high risk of serious heat crisis in the future. Crisis level is determined by amount of tree coverage, air conditioning, and heat-related mortality." + '\n' +
                '\n' +
                "Find your district's city councilor/your district here:" + '\n' + 
                "https://geospatial.worcesterma.gov/FindMyCityCouncilor/" + '\n' + 
                '\n' + 
                "Write to the mayor or your Worcester district city councilor:" + '\n' + 
                "https://www.worcesterma.gov/elections/elected-officials" + '\n' + 
                '\n' + "Request planting of trees through Worcester 311:" + '\n' + 
                "https://www7.worcesterma.gov/Applications/OCSC/Home/RequestGeneral?sDisplayAs=Tree%20Planting" + '\n' + 
                '\n' + 
                "Contact your representatives to voice your beliefs and push for policies to incentivize property owners to keep trees or plant to replace removed ones!" + '\n' +
                '\n' +
                "Tree Coverage Map: (https://commons.clarku.edu/cgi/viewcontent.cgi?article=2713&co ntext=asdff)" + '\n' +
                "Heat map: (https://www.worcesterma.gov/uploads/b3/49/b349ee5fb569021ece3ed3c914625074/gwac-urban-climate-consulting-presentation.pdf)")

    # Button to go back to the main window
    back_button = tk.Button(additional_window, text="Back to Main Window", command=additional_window.destroy)
    back_button.pack()

if __name__ == '__main__':
    # zip
    zip()
    
    # Sets the title and gui
    root = tk.Tk()
    root.title("LeafyLessons")

    # Adjust the size of the main window
    root.geometry("1280x950")

    # Create a frame to hold the images and buttons
    frame = tk.Frame(root)
    frame.pack(expand=True, fill=tk.BOTH)
    
    # Button to update images
    button = tk.Button(root, text="Mark where you are on the map (allow location services)", command=update_images)
    button.config(width=40, height=3)
    button.pack(side=tk.BOTTOM, pady=10)

    # Button to show additional window
    additional_button = tk.Button(root, text="Additional Window", command=show_additional_window)
    additional_button.config(width=40, height=3)
    additional_button.pack(side=tk.BOTTOM, pady=10)

    # Load images
    image1 = Image.open("heatMap.png")
    image2 = Image.open("treeMap.png")
    img1 = ImageTk.PhotoImage(image1)
    img2 = ImageTk.PhotoImage(image2)

    # Display images in labels
    label1 = tk.Label(frame, image=img1)
    label1.grid(row=0, column=0)
    label2 = tk.Label(frame, image=img2)
    label2.grid(row=0, column=1)

    # Keep the window open
    root.mainloop()