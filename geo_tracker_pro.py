import requests
import folium
import tkinter as tk
from tkinter import messagebox
import webbrowser

# Detect user's IP automatically
def get_my_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        data = response.json()
        ip = data["ip"]

        ip_entry.delete(0, tk.END)
        ip_entry.insert(0, ip)

    except Exception as e:
        messagebox.showerror("Error", "Could not detect IP")


# Track IP address
def track_ip():
    ip = ip_entry.get().strip()

    if ip == "":
        messagebox.showwarning("Input Error", "Please enter an IP Address")
        return

    try:
        # Reliable geolocation API
        url = f"http://ip-api.com/json/{ip}"

        response = requests.get(url)
        data = response.json()

        if data["status"] != "success":
            messagebox.showerror("Error", "Invalid IP Address or API error")
            return

        city = data.get("city")
        region = data.get("regionName")
        country = data.get("country")
        latitude = data.get("lat")
        longitude = data.get("lon")
        isp = data.get("isp")

        result = f"""
IP Address: {ip}
City: {city}
Region: {region}
Country: {country}
ISP: {isp}
Latitude: {latitude}
Longitude: {longitude}
"""

        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, result)

        # Create map
        map_obj = folium.Map(location=[latitude, longitude], zoom_start=10)

        folium.Marker(
            [latitude, longitude],
            popup=f"{city}, {country}",
            tooltip=ip
        ).add_to(map_obj)

        map_obj.save("ip_location_map.html")

        webbrowser.open("ip_location_map.html")

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong\n{e}")


# GUI Window
root = tk.Tk()
root.title("GeoLocation Tracker Pro")
root.geometry("500x450")
root.resizable(False, False)

# Title
title = tk.Label(root, text="IP Geolocation Tracker", font=("Arial", 16, "bold"))
title.pack(pady=10)

# IP Entry
ip_label = tk.Label(root, text="Enter IP Address")
ip_label.pack()

ip_entry = tk.Entry(root, width=40)
ip_entry.pack(pady=5)

# Buttons
detect_btn = tk.Button(root, text="Detect My IP", command=get_my_ip)
detect_btn.pack(pady=5)

track_btn = tk.Button(root, text="Track Location", command=track_ip)
track_btn.pack(pady=5)

# Result box
result_text = tk.Text(root, height=15, width=55)
result_text.pack(pady=10)

root.mainloop()