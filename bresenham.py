"""
This is just breseham line drawing algo
"""

from dataclasses import dataclass
import logging
import sys
import tkinter


@dataclass
class Pixel:
    """
    A class representing Pixels

    ...

    Attributes
    ----------
    point_x:
        the X coordinate value

    point_Y:
        the Y coordinate value

    Methods
    -------
    get_points:
        returns a list with the X,Y points
    """
    point_x: float
    point_y: float

    def __init__(self, point_x: float, point_y: float):
        self.point_x = point_x
        self.point_y = point_y

    def get_points(self) -> list[float]:
        """ Returns point(x,y) as list of floats  """
        return [self.point_x, self.point_y]


def breseham(point: Pixel, point1: Pixel) -> list[Pixel]:
    """ It calculates Pixels for bresenham

    :point: First Point
    :point2: Second Point
    :returns: A list of `Pixel`s that will be drawn :)

    """
    points_to_be_drawn: list[Pixel] = []
    # First GET dX and dY
    delta_x: float = point1.point_x - point.point_x
    delta_y: float = point1.point_y - point.point_y
    # Get P!
    p_value = (2*delta_y) - delta_x
    logging.debug("Value of dX: %f, , dY: %f ", delta_x, delta_y)
    logging.debug("Value of P: %f ", p_value)
    while point.point_y != point1.point_y:
        if points_to_be_drawn is not None and len(points_to_be_drawn) > 30:
            # Stops the program from destroying your hard disk with large
            # data.log file.
            logging.error("ERROR Reached Max number EXITTING!")
            print("Something went wrong, logging..............")
            sys.exit(1)
        if p_value < 0:
            point.point_x += 1
            points_to_be_drawn.append(Pixel(point.point_x, point.point_y))
            p_value = p_value + (2*delta_y)
            logging.debug("Value of P: %i", p_value)
            logging.debug("POINT = XVal: %f, YVal: %f",
                          point.point_x, point.point_y)
        else:
            point.point_x += 1
            point.point_y += 1
            points_to_be_drawn.append(Pixel(point.point_x, point.point_y))
            p_value = p_value + (2*delta_y) - (2*delta_x)
            logging.debug("Value of P: %i", p_value)
            logging.debug("POINT = XVal: %f, YVal: %f",
                          point.point_x, point.point_y)
    return points_to_be_drawn


def draw(lst_of_points: list[Pixel], scale: int) -> None:
    """ Will draw the line and points on a tkinter window

    :point: First point that will be used to draw the line
    :point2: Second point end of the line
    :lst_of_points: the list of points that will be drawn
    :returns: None
    """
    # Creates an instance window
    win = tkinter.Tk()
    win.title("Points")
    win.geometry("1000x700")
    # The canvas we will draw on
    canvas = tkinter.Canvas(win, width=1000, height=700)
    # The points
    for pixel in lst_of_points:
        # There is no way to draw a Point except using line or oval
        canvas.create_line(pixel.point_x*scale, pixel.point_y*scale,
                           pixel.point_x*scale + 1, pixel.point_y*scale,
                           fill="red", width=4
                           )
    point: Pixel = lst_of_points[0]
    point1: Pixel = lst_of_points[-1]
    # The line that is drawn
    canvas.create_line(point1.point_x*scale, point1.point_y*scale,
                       point.point_x*scale, point.point_y*scale,
                       fill="green", width=5
                       )
    canvas.pack()
    # Start the gui
    win.mainloop()


def main():
    """Main"""
    point0: Pixel = Pixel(2, 3)
    point1: Pixel = Pixel(15, 8)
    lst: list[Pixel] = breseham(point0, point1)
    print(lst)
    draw(lst, 40)


if __name__ == "__main__":
    logging.basicConfig(filename='data.log', level=logging.DEBUG)
    logging.debug("Starting -------------------------------------------------")
    main()
    logging.debug("Finished -------------------------------------------------")
    sys.exit(0)
