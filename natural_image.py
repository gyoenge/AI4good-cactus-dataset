import requests 
import uuid 

def download_images(fileroot, img_size, img_num):
    lorempicsum_url = f"https://picsum.photos/{img_size[0]}/{img_size[1]}" 
    
    for i in range(img_num):
        try: 
            response = requests.get(lorempicsum_url) 
            if response.status_code == 200:
                img_filename = fileroot + f"{uuid.uuid4()}.jpg"  
                with open(img_filename, 'wb') as file:
                    file.write(response.content)
            else:
                print(f"Failed to get image : {response.status_code}")
        except Exception as e:
            print(f'Failed to download image : {e}')

if __name__ == '__main__':
    download_images("dataset/natural_image/", (250,250), 50)
    