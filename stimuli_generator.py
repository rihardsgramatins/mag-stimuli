import warnings
import random
import os
from PIL import Image, ImageDraw, ImageFont

FONT = "Inter-Regular.ttf"
DARKGRAY = (150, 150, 150)
LIGHTGRAY = (200, 200, 200)
BACKGROUND = (250, 250, 250)

# Function to generate a random matrix
def generate_matrix(rows, cols, special_element):
    matrix = []
    for i in range(rows):
        row = []
        for j in range(cols):
            if (i, j) == special_element:
                row.append(28)
            else:
                while True:
                    num = random.randint(10, 99)
                    if num != 28 and num not in row:
                        row.append(num)
                        break
        matrix.append(row)
    return matrix

# Function for drawing matrix with No Grouping (Default)
def draw_no_grouping(matrix, width, height, font_size):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(FONT, font_size)
        num_rows, num_cols = len(matrix), len(matrix[0])
        cell_width = 109
        cell_height = 54
        grid_width = num_cols * cell_width + (num_cols + 1) * 110
        grid_height = num_rows * cell_height + (num_rows + 1) * 110
        start_x = (width - grid_width) // 2
        start_y = (height - grid_height) // 2

        for i in range(num_rows):
            for j in range(num_cols):
                text = str(matrix[i][j])
                text_width, text_height = draw.textsize(text, font=font)
                rect_x0 = start_x + j * cell_width + (j + 1) * 110
                rect_y0 = start_y + i * cell_height + (i + 1) * 110
                rect_x1 = rect_x0 + cell_width
                rect_y1 = rect_y0 + cell_height
                fill = DARKGRAY
                draw.rectangle([rect_x0, rect_y0, rect_x1, rect_y1], fill=fill, outline=None)
                text_x = rect_x0 + (cell_width - text_width) // 2
                text_y = rect_y0 + (cell_height - text_height) // 2
                text_y -= 5
                draw.text((text_x, text_y), text, fill="black", font=font)
        return image

# Function for drawing matrix with Similarity principle
def draw_similarity(matrix, quadrant, width, height, font_size):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(FONT, font_size)
        num_rows, num_cols = len(matrix), len(matrix[0])
        cell_width = 109
        cell_height = 54
        grid_width = num_cols * cell_width + (num_cols + 1) * 110
        grid_height = num_rows * cell_height + (num_rows + 1) * 110
        start_x = (width - grid_width) // 2
        start_y = (height - grid_height) // 2
        quadrant_color = LIGHTGRAY

        for i in range(num_rows):
            for j in range(num_cols):
                text = str(matrix[i][j])
                text_width, text_height = draw.textsize(text, font=font)
                rect_x0 = start_x + j * cell_width + (j + 1) * 110
                rect_y0 = start_y + i * cell_height + (i + 1) * 110
                rect_x1 = rect_x0 + cell_width
                rect_y1 = rect_y0 + cell_height
                fill = DARKGRAY
                if quadrant == 1 and j < num_cols // 2 and i < num_rows // 2:
                    fill = quadrant_color
                elif quadrant == 2 and j >= num_cols // 2 and i < num_rows // 2:
                    fill = quadrant_color
                elif quadrant == 3 and j < num_cols // 2 and i >= num_rows // 2:
                    fill = quadrant_color
                elif quadrant == 4 and j >= num_cols // 2 and i >= num_rows // 2:
                    fill = quadrant_color
                draw.rectangle([rect_x0, rect_y0, rect_x1, rect_y1], fill=fill, outline=None)
                text_x = rect_x0 + (cell_width - text_width) // 2
                text_y = rect_y0 + (cell_height - text_height) // 2
                text_y -= 5
                draw.text((text_x, text_y), text, fill="black", font=font)
        return image

# Function for drawing matrix with Common Ground principle
def draw_common_ground(matrix, quadrant, width, height, font_size):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(FONT, font_size)
        num_rows, num_cols = len(matrix), len(matrix[0])
        cell_width = 110
        cell_height = 55
        grid_width = num_cols * cell_width + (num_cols - 1) * 110  # Calculate total grid width
        grid_height = num_rows * cell_height + (num_rows - 1) * 110  # Calculate total grid height
        start_x = (width - grid_width) // 2  # Calculate starting X position
        start_y = (height - grid_height) // 2  # Calculate starting Y position

        # Calculate the coordinates for the quadrant area
        if quadrant == 1:
            quadrant_x0 = start_x - 55
            quadrant_y0 = start_y - 55
            quadrant_x1 = start_x + num_cols // 2 * cell_width + (num_cols // 2 - 1) * 110 + 55
            quadrant_y1 = start_y + num_rows // 2 * cell_height + (num_rows // 2 - 1) * 110 + 55
        elif quadrant == 2:
            quadrant_x0 = start_x + num_cols // 2 * cell_width + (num_cols // 2) * 110 - 55
            quadrant_y0 = start_y - 55
            quadrant_x1 = start_x + grid_width + 55
            quadrant_y1 = start_y + num_rows // 2 * cell_height + (num_rows // 2 - 1) * 110 + 55
        if quadrant == 3:
            quadrant_x0 = start_x - 55
            quadrant_y0 = start_y + num_rows // 2 * cell_height + (num_rows // 2) * 110 - 55
            quadrant_x1 = start_x + num_cols // 2 * cell_width + (num_cols // 2 - 1) * 110 + 55
            quadrant_y1 = start_y + grid_height + 55
        elif quadrant == 4:
            quadrant_x0 = start_x + num_cols // 2 * cell_width + (num_cols // 2) * 110 - 55
            quadrant_y0 = start_y + num_rows // 2 * cell_height + (num_rows // 2) * 110 - 55
            quadrant_x1 = start_x + grid_width + 55
            quadrant_y1 = start_y + grid_height + 55

        # Draw the lighter gray background only within the quadrant area
        draw.rectangle([quadrant_x0, quadrant_y0, quadrant_x1, quadrant_y1], fill=BACKGROUND, outline=None)

        # Draw matrix elements
        for i in range(num_rows):
            for j in range(num_cols):
                text = str(matrix[i][j])
                text_width, text_height = draw.textsize(text, font=font)
                rect_x0 = start_x + j * (cell_width + 110)
                rect_y0 = start_y + i * (cell_height + 110)
                rect_x1 = rect_x0 + cell_width
                rect_y1 = rect_y0 + cell_height
                fill = DARKGRAY
                draw.rectangle([rect_x0, rect_y0, rect_x1, rect_y1], fill=fill, outline=None)
                text_x = rect_x0 + (cell_width - text_width) // 2
                text_y = rect_y0 + (cell_height - text_height) // 2
                text_y -= 5
                draw.text((text_x, text_y), text, fill="black", font=font)

        return image

# Function for drawing matrix with Proximity principle
def draw_proximity(matrix, quadrant, width, height, font_size):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(FONT, font_size)
        num_rows, num_cols = len(matrix), len(matrix[0])
        cell_width = 110
        cell_height = 55
        grid_width = num_cols * cell_width + (num_cols - 1) * 110  # Calculate total grid width
        grid_height = num_rows * cell_height + (num_rows - 1) * 110  # Calculate total grid height
        start_x = (width - grid_width) // 2  # Calculate starting X position
        start_y = (height - grid_height) // 2  # Calculate starting Y position

        # Divide the quadrant into two rows
        num_rows_quadrant = num_rows // 2 if quadrant in [1, 2] else (num_rows + 1) // 2
        row_height = grid_height // num_rows_quadrant

        num_cols_quadrant = num_cols // 2
        offset = 110

        # Draw matrix elements
        for i in range(num_rows):
            for j in range(num_cols):
                text = str(matrix[i][j])
                text_width, text_height = draw.textsize(text, font=font)
                if quadrant == 1 and i < num_rows_quadrant and j < num_cols // 2:
                    # Calculate Y position based on row index and apply offset
                    rect_y0 = start_y + i * (cell_height + 55) + (row_height - cell_height) // 2 + 27.5  - offset
                    rect_x0 = start_x + j * (cell_width + 55) + ((num_cols_quadrant - 1) * 27.5)
                elif quadrant == 2 and i < num_rows_quadrant and j >= num_cols // 2:
                    rect_y0 = start_y + i * (cell_height + 55) + (row_height - cell_height) // 2 + 27.5 - offset
                    rect_x0 = start_x + j * (cell_width + 55) + ((num_cols_quadrant - 1) * 55) + 55 + ((num_cols_quadrant - 1) * 27.5)
                elif quadrant == 3 and i >= num_rows_quadrant and j < num_cols // 2:
                    rect_y0 = start_y + i * (cell_height + 55) + (row_height - cell_height) // 2 + 110 + 27.5 - offset
                    rect_x0 = start_x + j * (cell_width + 55) + ((num_cols_quadrant - 1) * 27.5)
                elif quadrant == 4 and i >= num_rows_quadrant and j >= num_cols // 2:
                    rect_y0 = start_y + i * (cell_height + 55) + (row_height - cell_height) // 2 + 110 + 27.5  - offset
                    rect_x0 = start_x + j * (cell_width + 55) + ((num_cols_quadrant - 1) * 55) + 55 + ((num_cols_quadrant - 1) * 27.5)
                else:
                    # For elements outside the quadrant, use original positions
                    rect_y0 = start_y + i * (cell_height + 110) + (row_height - cell_height) // 2  - offset
                    rect_x0 = start_x + j * (cell_width + 110)
                
                rect_x1 = rect_x0 + cell_width
                rect_y1 = rect_y0 + cell_height
                fill = DARKGRAY
                draw.rectangle([rect_x0, rect_y0, rect_x1, rect_y1], fill=fill, outline=None)
                text_x = rect_x0 + (cell_width - text_width) // 2
                text_y = rect_y0 + (cell_height - text_height) // 2
                text_y -= 5
                draw.text((text_x, text_y), text, fill="black", font=font)

        return image

# Function for drawing matrix with All Grouping principles
def draw_all_grouping(matrix, quadrant, width, height, font_size):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(FONT, font_size)

        num_rows, num_cols = len(matrix), len(matrix[0])
        cell_width = 110
        cell_height = 55
        grid_width = num_cols * cell_width + (num_cols - 1) * 110  # Calculate total grid width
        grid_height = num_rows * cell_height + (num_rows - 1) * 110  # Calculate total grid height
        start_x = (width - grid_width) // 2  # Calculate starting X position
        start_y = (height - grid_height) // 2  # Calculate starting Y position

        # Calculate the coordinates for the quadrant area
        if quadrant == 1:
            quadrant_x0 = start_x - 55
            quadrant_y0 = start_y - 55
            quadrant_x1 = start_x + num_cols // 2 * cell_width + (num_cols // 2 - 1) * 110 + 55
            quadrant_y1 = start_y + num_rows // 2 * cell_height + (num_rows // 2 - 1) * 110 + 55
        elif quadrant == 2:
            quadrant_x0 = start_x + num_cols // 2 * cell_width + (num_cols // 2) * 110 - 55
            quadrant_y0 = start_y - 55
            quadrant_x1 = start_x + grid_width + 55
            quadrant_y1 = start_y + num_rows // 2 * cell_height + (num_rows // 2 - 1) * 110 + 55
        if quadrant == 3:
            quadrant_x0 = start_x - 55
            quadrant_y0 = start_y + num_rows // 2 * cell_height + (num_rows // 2) * 110 - 55
            quadrant_x1 = start_x + num_cols // 2 * cell_width + (num_cols // 2 - 1) * 110 + 55
            quadrant_y1 = start_y + grid_height + 55
        elif quadrant == 4:
            quadrant_x0 = start_x + num_cols // 2 * cell_width + (num_cols // 2) * 110 - 55
            quadrant_y0 = start_y + num_rows // 2 * cell_height + (num_rows // 2) * 110 - 55
            quadrant_x1 = start_x + grid_width + 55
            quadrant_y1 = start_y + grid_height + 55

        # Draw the lighter gray background only within the quadrant area
        draw.rectangle([quadrant_x0, quadrant_y0, quadrant_x1, quadrant_y1], fill=BACKGROUND, outline=None)
        
        # Divide the quadrant into two rows
        num_rows_quadrant = num_rows // 2 if quadrant in [1, 2] else (num_rows + 1) // 2
        row_height = grid_height // num_rows_quadrant

        num_cols_quadrant = num_cols // 2
        offset = 110
        quadrant_color = LIGHTGRAY
        # Draw matrix elements
        for i in range(num_rows):
            for j in range(num_cols):
                text = str(matrix[i][j])
                text_width, text_height = draw.textsize(text, font=font)
                if quadrant == 1 and i < num_rows_quadrant and j < num_cols // 2:
                    # Calculate Y position based on row index and apply offset
                    rect_y0 = start_y + i * (cell_height + 55) + (row_height - cell_height) // 2 + 27.5  - offset
                    rect_x0 = start_x + j * (cell_width + 55) + ((num_cols_quadrant - 1) * 27.5)
                    fill = quadrant_color
                elif quadrant == 2 and i < num_rows_quadrant and j >= num_cols // 2:
                    rect_y0 = start_y + i * (cell_height + 55) + (row_height - cell_height) // 2 + 27.5 - offset
                    rect_x0 = start_x + j * (cell_width + 55) + ((num_cols_quadrant - 1) * 55) + 55 + ((num_cols_quadrant - 1) * 27.5)
                    fill = quadrant_color
                elif quadrant == 3 and i >= num_rows_quadrant and j < num_cols // 2:
                    rect_y0 = start_y + i * (cell_height + 55) + (row_height - cell_height) // 2 + 110 + 27.5 - offset
                    rect_x0 = start_x + j * (cell_width + 55) + ((num_cols_quadrant - 1) * 27.5)
                    fill = quadrant_color
                elif quadrant == 4 and i >= num_rows_quadrant and j >= num_cols // 2:
                    rect_y0 = start_y + i * (cell_height + 55) + (row_height - cell_height) // 2 + 110 + 27.5  - offset
                    rect_x0 = start_x + j * (cell_width + 55) + ((num_cols_quadrant - 1) * 55) + 55 + ((num_cols_quadrant - 1) * 27.5)
                    fill = quadrant_color
                else:
                    # For elements outside the quadrant, use original positions
                    rect_y0 = start_y + i * (cell_height + 110) + (row_height - cell_height) // 2  - offset
                    rect_x0 = start_x + j * (cell_width + 110)
                    fill = DARKGRAY
                
                rect_x1 = rect_x0 + cell_width
                rect_y1 = rect_y0 + cell_height
                
                draw.rectangle([rect_x0, rect_y0, rect_x1, rect_y1], fill=fill, outline=None)
                text_x = rect_x0 + (cell_width - text_width) // 2
                text_y = rect_y0 + (cell_height - text_height) // 2
                text_y -= 5
                draw.text((text_x, text_y), text, fill="black", font=font)

    return image

# Function to save the matrix as an image
def save_matrix_as_image(matrix, filename, quadrant, style, width=1920, height=1080, font_size=48):
    # Call the appropriate function based on the style name
    if style == "No_Grouping":
        image = draw_no_grouping(matrix, width, height, font_size)
    elif style == "Similarity":
        image = draw_similarity(matrix, quadrant, width, height, font_size)
    elif style == "Common_Ground":
        image = draw_common_ground(matrix, quadrant, width, height, font_size)
    elif style == "Proximity":
        image = draw_proximity(matrix, quadrant, width, height, font_size)
    elif style == "All_Grouping":
        image = draw_all_grouping(matrix, quadrant, width, height, font_size)

    # Save the image to the specified filename
    image.save(filename)


def generate_variations(style_names):
    matrix_sizes = [(4, 2), (4, 4), (4, 8)]
    for style_name in style_names:
        for size in matrix_sizes:
            rows, cols = size
            num_elements = rows * cols
            
            # Generate one variant with the special element inside a quadrant
            quadrant_inside = random.randint(1, 4)
            position_inside = (random.randint(0, rows // 2 - 1), random.randint(0, cols // 2 - 1))
            placement_inside = "in_quadrant"
            special_element_inside = position_inside if quadrant_inside == 1 else (position_inside[0], position_inside[1] + cols // 2) if quadrant_inside == 2 else (position_inside[0] + rows // 2, position_inside[1]) if quadrant_inside == 3 else (position_inside[0] + rows // 2, position_inside[1] + cols // 2)
            filename_inside = f"assets/{style_name}_{num_elements}_{quadrant_inside}_{placement_inside}.png"
            matrix_inside = generate_matrix(rows, cols, special_element_inside)
            save_matrix_as_image(matrix_inside, filename_inside, quadrant_inside, style_name)

            # Generate one variant with the special element outside the quadrant
            quadrant_outside = random.randint(1, 4)
            position_outside = (random.randint(0, rows - 1), random.randint(0, cols - 1))
            while (position_outside[0] < rows // 2 and quadrant_outside == 1) or (position_outside[1] < cols // 2 and quadrant_outside == 2) or (position_outside[0] >= rows // 2 and quadrant_outside == 3) or (position_outside[1] >= cols // 2 and quadrant_outside == 4):
                position_outside = (random.randint(0, rows - 1), random.randint(0, cols - 1))
            placement_outside = "outside_quadrant"
            special_element_outside = position_outside
            filename_outside = f"assets/{style_name}_{num_elements}_{quadrant_outside}_{placement_outside}.png"
            matrix_outside = generate_matrix(rows, cols, special_element_outside)
            save_matrix_as_image(matrix_outside, filename_outside, quadrant_outside, style_name)

            # Generate one variant with the special element not in matrix
            quadrant_not_in_matrix = random.randint(1, 4)
            placement_not_in_matrix = "not_in_matrix"
            filename_not_in_matrix = f"assets/{style_name}_{num_elements}_{quadrant_not_in_matrix}_{placement_not_in_matrix}.png"
            matrix_not_in_matrix = generate_matrix(rows, cols, None)
            save_matrix_as_image(matrix_not_in_matrix, filename_not_in_matrix, quadrant_not_in_matrix, style_name)

            # Delete one random picture of the 3 generated for each matrix size
            filenames_to_delete = [filename_inside, filename_outside, filename_not_in_matrix]
            filename_to_delete = random.choice(filenames_to_delete)
            os.remove(filename_to_delete)

# Call the main function to generate variations
style_names = ["No_Grouping", "Similarity", "Common_Ground", "Proximity", "All_Grouping"]
generate_variations(style_names)
