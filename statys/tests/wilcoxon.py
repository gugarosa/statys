from scipy.stats import wilcoxon as w
from scipy.stats import ranksums as r


def wilcoxon_signed_rank(dist, alpha=0.05):
    """
    """

    #
    output = {}

    #
    for (attr, value) in dist.attrs:
        for (attr2, value2) in dist.attrs:
            if attr == attr2:
                pass
            else:
                # print(value, value2)
                _, p = w(value, value2)
                
                if p >= alpha:
                    h = 0
                else:
                    h = 1

                print(h, p)


def wilcoxon_rank_sum(dist, alpha=0.05):
    """
    """

    #
    output = {}

    #
    for (attr, value) in dist.attrs:
        for (attr2, value2) in dist.attrs:
            if attr == attr2:
                pass
            else:
                # print(value, value2)
                _, p = r(value, value2)
                
                if p >= alpha:
                    h = 0
                else:
                    h = 1

                print(h, p)