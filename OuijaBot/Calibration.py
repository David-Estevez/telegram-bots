ouijamap = {'a':(0,0),
            'b':(0,0),
            'c':(0,0),
            'd':(0,0),
            'e':(0,0),
            'f':(0,0),
            'g':(0,0),
            'h':(0,0),
            'i':(0,0),
            'j':(0,0),
            'k':(0,0),
            'l':(0,0),
            'm':(0,0),
            'n':(0,0),
            'o':(0,0),
            'p':(0,0),
            'q':(0,0),
            'r':(0,0),
            's':(0,0),
            't':(0,0),
            'u':(0,0),
            'v':(0,0),
            'w':(0,0),
            'x':(0,0),
            'y':(0,0),
            'z':(150,260),
            '0':(0,0),
            '1':(0,0),
            '2':(0,0),
            '3':(0,0),
            '4':(0,0),
            '5':(0,0),
            '6':(0,0),
            '7':(0,0),
            '8':(0,0),
            '9':(0,0),
            'yes':(57.00, 96.00),
            'no':(57.00, 256.00)
            }

def parse_string(string):
    x_start = string.find('X:')
    y_start = string.find('Y:')
    z_start = string.find('Z:')
    return '(' + string[x_start+2:y_start-1] + ', ' + string[y_start+2:z_start-1] + ')'


if __name__ == '__main__':
    test_str = 'X:150.00 Y:260.00 Z:0.00 E:0.00 Count X: 410.00 Y:-110.00 Z:0.00'
    result_str = parse_string(test_str)
    if result_str == '(150.00, 260.00)':
        print 'Success'
    else:
        print 'Fail! Result: ' + result_str
