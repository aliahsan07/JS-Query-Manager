from dataclasses import dataclass, field
from typing import List


@dataclass
class SafeConfig:

    callSiteSensitivity: int = 20
    loopDepth: int = 10
    loopIter: int = 100

    options: list = field(
        default_factory=lambda: [10, 20, 50, 100, 500])

    def calculateCallSiteSen(self, option):

        upper = self.callSiteSensitivity * ((100 + option)/100)
        lower = self.callSiteSensitivity * ((100 - option)/100)

        if lower < 0:
            lower = 0
        return [int(upper), int(lower)]

    def makeHeapBuilderCombos(self):
        callSiteOptions = [0, 1, 2, 5, 10, 12, 20, 50, 100, 500]
        loopDepthOptions = [0, 1, 2, 3, 5, 7, 10, 15, 20, 50]
        loopIterOptions = [0, 1, 2, 10, 50, 100, 200, 500, 100, 10000]

        for i in callSiteOptions:
            for j in loopDepthOptions:
                for k in loopIterOptions:
                    # invoke with every option

                    # store and compute result
                    print(i, j, k)
