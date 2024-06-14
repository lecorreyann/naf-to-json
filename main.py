import pandas as pd
import threading
import time

# Function to download the file


def download_file(url, done_event):
    global df
    df = pd.read_excel(url, header=0)
    df = df.iloc[:, [1, 2]]
    df = df.dropna()
    df = df[df.iloc[:, 0].str.match(r'^\d{2}\.\d{2}[A-Z]$')]
    done_event.set()

# Function to animate the loading message


def animate_loading(done_event):
    load_message = ""
    while not done_event.is_set():
        print(
            f"\rLoading file \"Nomenclature d’activités française – NAF rév. 2\" {load_message}", end="")
        time.sleep(0.5)
        load_message += "." if len(load_message) < 4 else ""
        load_message = "" if len(load_message) == 4 else load_message


# URL to download the file from
url = 'https://www.insee.fr/fr/statistiques/fichier/2120875/int_courts_naf_rev_2.xls'

# Event to signal when the download is done
done_event = threading.Event()

# Start the download in a separate thread
download_thread = threading.Thread(
    target=download_file, args=(url, done_event))
download_thread.start()

# Start the loading animation in the main thread
animate_loading(done_event)

# Wait for the download to finish
download_thread.join()

print("\nDownload complete!")

# Rename columns
df.columns = ['code', 'legend']

# Save the dataframe to a json file
df.to_json('naf.json', orient='records')
