import numpy as np
import imageio.v3 as iio
import matplotlib.pyplot as plt

def encode_lsb(image_path, secret_text, output_path):
    img = iio.imread(image_path)
    stego_img = img.astype(np.uint8).copy() 
    
    secret_text += "###"
    bin_secret = ''.join([format(ord(i), '08b') for i in secret_text])
    
    data_index = 0
    total_bits = len(bin_secret)
    rows, cols, channels = stego_img.shape
    
    for r in range(rows):
        for c in range(cols):
            for ch in range(channels):
                if data_index < total_bits:
                    pixel_val = int(stego_img[r, c, ch])
                    
                    new_bit = int(bin_secret[data_index])
                   
                    new_pixel_val = (pixel_val & ~1) | new_bit
                    
                    stego_img[r, c, ch] = np.clip(new_pixel_val, 0, 255)
                    data_index += 1
                else:
                    break
    

    iio.imwrite(output_path, stego_img)
    return img, stego_img


try:
    path_asli = 'input.jpg' 
    path_hasil = 'stego_result.png' 
    pesan = "AKU"
    
    original, stego = encode_lsb(path_asli, pesan, path_hasil)
    
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1); plt.imshow(original); plt.title("Citra Asli"); plt.axis('off')
    plt.subplot(1, 2, 2); plt.imshow(stego); plt.title(f"Citra Stego (Pesan: {pesan})"); plt.axis('off')
    plt.tight_layout()
    plt.show()
    
    print(f"Berhasil! File disimpan sebagai: {path_hasil}")

except Exception as e:
    print(f"Terjadi kesalahan: {e}")