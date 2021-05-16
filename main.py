import re

regex = r'[XY].\d+.\d+'


def gcode_to_coordinates(file_name, output_file_name, num_of_dots: int):
    x_coordinates = []
    y_coordinates = []
    temp_x = []
    temp_y = []

    coordinates = []

    with open(file_name) as gcode:
        for line in gcode:
            coordinate = re.findall(regex, line, re.MULTILINE)
            if not coordinate:
                continue
            x_str, y_str = tuple(coordinate)
            x_str, y_str = x_str.replace('X', ''), y_str.replace('Y', '')
            x, y = float(x_str), float(y_str)
            x_coordinates.append(x)
            y_coordinates.append(y)

    print("Found", len(x_coordinates), "of X coordinates")
    print("Found", len(y_coordinates), "of Y coordinates")

    # Get minimum coordinates
    x_min = min(x_coordinates)
    y_min = min(y_coordinates)

    # Offset coordinates by minimum X & Y values
    for x in x_coordinates:
        temp_x.append(x - x_min)
    for y in y_coordinates:
        temp_y.append(y - y_min)
    x_coordinates, y_coordinates = temp_x, temp_y

    temp_x = []
    temp_y = []

    # Get maximum coordinates value
    x_max = max(x_coordinates)
    y_max = max(y_coordinates)

    # Scale by maximum dimension
    scale_by_maximum = 0
    if x_max > y_max:
        scale_by_maximum = x_max
    elif y_max >= x_max:
        scale_by_maximum = y_max

    for x in x_coordinates:
        temp_x.append(int(x / scale_by_maximum * 255))
    for y in y_coordinates:
        temp_y.append(int(y / scale_by_maximum * 255))
    x_coordinates, y_coordinates = temp_x, temp_y

    for n in range(0, num_of_dots):
        coordinates.append((x_coordinates[n], y_coordinates[n]))

    print("Parsed", len(coordinates), "coordinates")

    embd_code = \
"#ifndef GRAPHIC_H\n" \
"#define GRAPHIC_H\n\n"

    embd_code += f'#define DOT_ARRAY_SIZE {num_of_dots}\n\n'
    embd_code += f'const unsigned char dot[DOT_ARRAY_SIZE][2] PROGMEM = ' + '{\n\t'
    n = 1
    for x, y in coordinates:
        embd_code += "0x%02x, 0x%02x, " % (x, y)

        if n >= 20:
            embd_code += '\n\t'
            n = 0
        n += 1

    embd_code += '\n};\n#endif\n'

    f = open(output_file_name, "w")
    f.write(embd_code)
    f.close()


if __name__ == '__main__':
    gcode_to_coordinates('gear-34.gcode', "./src/graphic.h", 6500)

