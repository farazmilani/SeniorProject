def convert_to_array(text):
    unknown = []
    text_file = open(text,"r")
    for line in text_file.readlines():
        for i in line.split():
            unknown.append(int(round(float(i))))

    text_file.close()
    return unknown

MACBOOK = convert_to_array('macbook\mb_avg.txt')
LAMP = convert_to_array('lamp\lamp_avg.txt')

# do the same for other devices to store




