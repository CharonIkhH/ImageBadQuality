import os
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

# Папки для входных и выходных изображений
input_folder = 'venv\\undone'  # Используем raw string для Windows путей
output_folder = 'venv\\done'

# Создаем выходную папку, если она не существует
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def add_noise(image):
    """Добавляем случайный шум к изображению."""
    noise = np.random.normal(0, 25, image.shape).astype(np.uint8)
    noisy_image = cv2.add(image, noise)
    return noisy_image

def save_image(image, filename, suffix):
    """Сохраняем изображение с указанным суффиксом."""
    output_path = os.path.join(output_folder, f"{filename}_{suffix}.jpg")
    cv2.imwrite(output_path, image)

def process_image(input_path):
    """Обрабатываем изображение с добавлением различных фильтров и сохраняем результат."""
    filename = os.path.splitext(os.path.basename(input_path))[0]
    image = cv2.imread(input_path)
    
    # 1. Черно-белое изображение
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    save_image(gray_image, filename, "1")

    # 2. Добавление шума
    noisy_image = add_noise(image)
    save_image(noisy_image, filename, "2")

    # 3. Комбинация черно-белого и шума
    noisy_gray_image = add_noise(gray_image)
    save_image(noisy_gray_image, filename, "3")

    # 4. Размытие
    blurred_image = cv2.GaussianBlur(image, (9, 9), 0)
    save_image(blurred_image, filename, "4")

    # 5. Уменьшение резкости
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    low_sharpness_image = pil_image.filter(ImageFilter.SMOOTH)
    save_image(cv2.cvtColor(np.array(low_sharpness_image), cv2.COLOR_RGB2BGR), filename, "5")

    # 6. Повышенная контрастность
    enhancer = ImageEnhance.Contrast(pil_image)
    high_contrast_image = enhancer.enhance(2.0)  # Увеличиваем контрастность в 2 раза
    save_image(cv2.cvtColor(np.array(high_contrast_image), cv2.COLOR_RGB2BGR), filename, "6")

    # 7. Низкая контрастность
    low_contrast_image = enhancer.enhance(0.5)  # Понижаем контрастность
    save_image(cv2.cvtColor(np.array(low_contrast_image), cv2.COLOR_RGB2BGR), filename, "7")

    # 8. Уменьшение яркости
    brightness_enhancer = ImageEnhance.Brightness(pil_image)
    low_brightness_image = brightness_enhancer.enhance(0.5)  # Понижаем яркость
    save_image(cv2.cvtColor(np.array(low_brightness_image), cv2.COLOR_RGB2BGR), filename, "8")

    # 9. Высокая яркость
    high_brightness_image = brightness_enhancer.enhance(1.5)  # Повышаем яркость
    save_image(cv2.cvtColor(np.array(high_brightness_image), cv2.COLOR_RGB2BGR), filename, "9")

    # 10. Инверсия цветов
    inverted_image = cv2.bitwise_not(image)
    save_image(inverted_image, filename, "10")

# Обрабатываем все изображения в папке undone
for image_name in os.listdir(input_folder):
    if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        input_path = os.path.join(input_folder, image_name)
        process_image(input_path)
