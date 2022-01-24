"""
@Author: Mina Sameh Wadie
Cairo Higher Institute
Assignment by Dr Ahmed Negm

This is a file for autocorrelation testing random numbers

Special Thanks to
Dr Ahmed Negm
Eng Omar
Eng Mohammed

R_XX = 1/N-k ( Sum(Xi-X-)^2* (Xi+k - X-)^2 )
                    ------------------
                        Sx Sx

Sx = sqrt(1/n-1 (xi-x)^2)

"""

import sys  # To grecifully exit the program :D
import logging  # Log stuff for easy access
from math import sqrt
from lcm_and_chitest import get_lcm  # Our random numbers generator


def autocorrelation(random_nums: list) -> float:
    """
        param:
            RandomNumbers: List of numbers to be tested
        return:
            if its correlated or not i guess
    """
    logging.debug('------ AUTOCORRELATION ------------')
    # N the number of numbers
    big_n: int = len(random_nums)
    logging.debug('Using %s \n and N = %s', random_nums, big_n)
    # Get X Mean
    big_x_mean: float = sum(random_nums) / big_n
    # get the sum of xi minus xmean power 2
    sum_xi_minus_x = sum([(i-big_x_mean)**2 for i in random_nums])

    # finally get the sx
    big_s_underscore_x: float = sqrt(1/(big_n-1) * sum_xi_minus_x)

    logging.debug('sx = %s, x^-=%s', big_s_underscore_x, big_x_mean)
    # r(k) will be diveded by sx * sx, so in order to save some time
    # set to a constant
    sx_2 = big_s_underscore_x ** 2
    # k will eq 1-n-1
    r_xx = []
    for big_k in range(1, big_n):
        sum_xi_xmean_times_xik_xmean = sum([
            (random_nums[i]-big_x_mean)*(random_nums[i+big_k]-big_x_mean)
            for i in range(big_n-big_k)
        ])
        logging.debug('sum of xi-xmean * xi+k = %s',
                      sum_xi_xmean_times_xik_xmean)
        r_xx.append((1/(big_n-big_k)) * (sum_xi_xmean_times_xik_xmean / sx_2))
    logging.debug('rxx = %s', r_xx)
    logging.debug('abs sum rxx = %s', abs(sum(r_xx)))
    return abs(sum(r_xx))


def main() -> None:
    """Main Function"""
    logging.basicConfig(filename='autocorrelation.log', level=logging.DEBUG)
    logging.debug("------- Starting -----------------------------------------")

    # Get our random numbers
    list_of_r = get_lcm(1, 2, 1, 51)
    # To make things easier only take the numbers in .2f format(0.00)
    list_of_r = [float(f'{i:.2f}') for i in list_of_r]
    logging.debug('as a .2F:%s', list_of_r)

    autocorrelation(list_of_r)
    logging.debug("------- Ending -----------------------------------------")
    sys.exit(0)


if __name__ == "__main__":
    main()
