"""
@Author: Mina Sameh Wadie
Cairo Higher Institute
Assignment by Dr Ahmed Negm

This is a file for Liner Congruential Method

Special Thanks to
Dr Ahmed Negm
Eng Omar
Eng Mohammed

LCM uses the formula: X_(i+1) = (a . X_i + c) mod m
R_1 = X/m

X0 is the seed element
a is the multiplier
c is the increment
m is the module

if c == 0 => Multiplicative LCM
   c != 0 => Mixed LCM

Functions:
    main: In case this file was called as Main program
    get_lcm: returns R values using given constants
    chi2_test: a hand made way to do the chi square test
    chi2_test_using_lib: Uses a ready lib to do the CHI Square Test
    draw_graph: Draws the relation between elements as graph, really fun to look at

Misc Variables:
    logging: Used to log data for review
"""

import logging # used to log data to see it later
import sys # to exit
import csv # To open chi table
from scipy.stats import chi2_contingency # a test
import matplotlib.pyplot as plt # Plot graphs for fun :P

def get_lcm( seed : int, constant_multiplier : int, increment: int, modulus: int ) -> list:
    """ this will generate LCM based on the inputs for the equations
    parameters:
        seed : the seed element
        a : the multiplier
        c : the increment
        m : the modulus
    returns:
        R values as a list
    """
    list_of_seed : list = []
    list_of_r : list = []
    for _ in range(modulus):
        seed = ( constant_multiplier * seed + increment ) % modulus
        #Stop cuz the numbers will just repeat themselves, just an optimization move
        # Log the output
        #logging.debug("new seed = %s", ( constant_multiplier  * seed + increment ) % modulus )
        #removed as per Eng Omar supervision and for the CHI test
        #the idea was that we have all the numbers constants except X, if X is the same
        #as the first one then the output will repeat itself.
        #if( len(list_of_seed) > 1 and seed == list_of_seed[0] ):
        #    break
        list_of_r.append( float(seed/modulus) )
        list_of_seed.append(seed)
    # Show them as graph
    #draw_graph(list_of_r)
    print(list_of_r)
    logging.debug("VALUES OF SEEDS -------------------")
    logging.debug(list_of_seed)
    logging.debug("VALUES OF R -------------------")
    logging.debug(list_of_r)
    return list_of_r

def chi2_test( lst : list, number_of_classes : int ,
        significance_level : float , modulus : int ) -> bool:
    """
    This is a function that checks independence
    parameters:
                lst: data that we will check
                significance_level: the level that is required
    returns:
            boolean value if there is null hypothesis or not
            if we Rejct the null hypothesis means that its independent
    """
    # divide it to equal intervels and count elements in classes
    lst_of_classes_count : list = []
    logging.debug("Counting ---------------------------------------")
    for counter in range(1, len(lst) , number_of_classes ):
        elements : list = []
        # Get elements for example between 20 and 20+10 so between 20 and 30 :P
        elements = [ i for i in lst
                # First time learning about chained ands in python, neat
                if (counter/modulus) < i <= ((counter + number_of_classes)/modulus) #Chained And :D
                ]
        logging.debug(
                "Found %s elements between %s and %s ",
                len(elements), counter, counter+number_of_classes
                )
        logging.debug("Counter is %s",counter)
        logging.debug("Elements are %s",elements)
        lst_of_classes_count.append(len(elements))
    expected = len(lst) / number_of_classes
    chi_square_statistic = 0
    for observed in lst_of_classes_count :
        chi_square_statistic += ( (( observed - expected )**2) / expected )
    logging.debug("Found --------------------- Last O-E/E is equal %s",
                            chi_square_statistic)
    # Get the chi squared distribution table
    with open('./chitable.csv','r', newline='', encoding="utf8") as chitest:
        csv_rows = csv.reader(chitest)
        csv_rows = list(csv_rows)
        chi_distribution_value : float = 0.0
        if significance_level == 0.05:
            chi_distribution_value = float(csv_rows[len(lst_of_classes_count)][1].replace("\t",""))
        elif significance_level == 0.01:
            chi_distribution_value = float(csv_rows[len(lst_of_classes_count)][2].replace("\t",""))
        elif significance_level == 0.001:
            chi_distribution_value = float(csv_rows[len(lst_of_classes_count)][3].replace("\t",""))
        logging.debug("Using %s", chi_distribution_value)
        if chi_square_statistic < chi_distribution_value:
            return True
        return False

def chi2_test_using_lib( lst : list, modulus : int = 100,
        significance_level : float = 0.05 , number_of_classes :int = 10 ) -> bool:
    """
    This is a function that checks independence
    parameters:
                lst: data that we will check
                significance_level: the level that is required
    returns:
            boolean value if there is null hypothesis or not
    """
    lst_of_classes_count : list = []
    for counter in range(1, len(lst) , number_of_classes ):
        elements : list = []
        elements = [ i for i in lst
                if (counter/modulus) < i <= ((counter + number_of_classes)/modulus) #Chained And :D
                ]
        lst_of_classes_count.append(len(elements))
    lst = lst_of_classes_count
    logging.debug("lst ----------------------\n  %s \n -------------", lst)
    chistat, p_value, dof, _= chi2_contingency( lst )
    logging.debug("dof ----------------------  %s", dof)
    logging.debug("chistat ----------------------  %s", chistat)
    logging.debug("p_value ----------------------  %s", p_value)
    if p_value <= significance_level:
        return True
    return False

def draw_graph(lst : list ) -> None:
    """ Draws the points as graphs
        parameters:
                 lst: The points that will be drawn
        return : Void
    """
    plt.plot( lst )
    plt.ylabel('Relation between X and R')
    plt.show()


def main():
    """ Main Function that will run"""
    # seed :int = 27
    # constant_multiplier :int = 17
    # increment :int = 43
    # modulus :int = 100
    # number_of_classes : int = 10
    # significance_level : float = 0.05
    seed : int = int(input("Enter X:"))
    constant_multiplier : int = int(input("Enter a:"))
    increment : int = int(input("Enter C:"))
    modulus : int = int(input("Enter M:"))
    number_of_classes  = int(input("Enter k:"))
    significance_level = float(input("Enter Significance Level:"))
    logging.debug("first seed = %s", seed)
    lst_of_r =  get_lcm( seed, constant_multiplier, increment, modulus )
    if chi2_test(lst_of_r, number_of_classes, significance_level, modulus):
        print("Rejected Null Hypothesis")
    else : print("Accepted Null Hypothesis")
    if chi2_test_using_lib(lst_of_r, modulus, significance_level , number_of_classes):
        print("Rejected Null Hypothesis")
    else : print("Accepted Null Hypothesis")
    sys.exit(0)

if __name__ == "__main__":
    # Set the log file to data.log
    logging.basicConfig(filename='data.log', level=logging.DEBUG)
    logging.debug("Starting -------------------------------------------------")
    main()
