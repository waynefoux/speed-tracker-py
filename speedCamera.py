import sys
import getopt
import videoProcessor



def main(argv):

    inputstream = None

    try:
        opts, argv = getopt.getopt(argv, "hi:", ["iinput="])
    except getopt.GetoptError:
        print('speedCamera.py -i inputstream')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('speedCamera.py -i <inputstream>')
            sys.exit()
        elif opt in ("-i", "--istream"):
            inputstream = arg



            speed_calculator = videoProcessor.SpeedCalculator(inputstream)

            speed_calculator.start()


if __name__ == "__main__":
    main(sys.argv[1:])
