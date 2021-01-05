from subprocess import Popen, PIPE, STDOUT
from classes.Analysis import Analysis
from utils.readTool import readToolOutput
import itertools
import os
import time


class WALA(Analysis):

    def __init__(self, config=None):
        super().__init__([])

        self.baseCommand = [
            'java', '-classpath', '/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/jre/lib/charsets.jar:/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/jre/lib/ext/cldrdata.jar:/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/jre/lib/ext/dnsns.jar:/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/jre/lib/ext/jaccess.jar:/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/jre/lib/ext/localedata.jar:/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/jre/lib/ext/nashorn.jar:/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/jre/lib/ext/sunec.jar:/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/jre/lib/ext/sunjce_provider.jar:/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/jre/lib/ext/sunpkcs11.jar:/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/jre/lib/ext/zipfs.jar:/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/jre/lib/jce.jar:/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/jre/lib/jsse.jar:/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/jre/lib/management-agent.jar:/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/jre/lib/resources.jar:/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/jre/lib/rt.jar:/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/lib/dt.jar:/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/lib/jconsole.jar:/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/lib/sa-jdi.jar:/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/lib/tools.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/out/production/main:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/com.ibm.wala.cast-1.5.4.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/com.ibm.wala.cast.java-1.5.4.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/com.ibm.wala.cast.java.ecj-1.5.4.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/com.ibm.wala.cast.js-1.5.4.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/com.ibm.wala.cast.js.rhino-1.5.4.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/com.ibm.wala.core-1.5.4.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/com.ibm.wala.dalvik-1.5.4.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/com.ibm.wala.scandroid-1.5.4.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/com.ibm.wala.shrike-1.5.4.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/com.ibm.wala.util-1.5.4.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/commons-cli-1.4.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/commons-io-2.4.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/dexlib2-2.2.6.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/guava-18.0.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/jericho-html-3.2.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/jsr305-1.3.9.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/org.eclipse.core.commands-3.6.0.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/org.eclipse.core.contenttype-3.4.100.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/org.eclipse.core.expressions-3.4.300.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/org.eclipse.core.filesystem-1.3.100.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/org.eclipse.core.jobs-3.5.100.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/org.eclipse.core.resources-3.7.100.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/org.eclipse.core.runtime-3.7.0.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/org.eclipse.equinox.app-1.3.100.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/org.eclipse.equinox.common-3.6.0.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/org.eclipse.equinox.preferences-3.4.1.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/org.eclipse.equinox.registry-3.5.101.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/org.eclipse.jdt.core-3.10.0.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/org.eclipse.osgi-3.7.1.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/org.eclipse.text-3.5.101.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/rhino-1.7.10.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/slf4j-api-1.7.2.jar:/Users/aliahsan/Documents/Research/WALA/WALA-start/build/distributions/WALA-start-0.1/lib/WALA-start-0.1.jar:/Users/aliahsan/Downloads/org.json.jar',
            'com/ibm/wala/examples/drivers/JSCallGraphDriver']

        # self.flags = ["-uneval", "-determinacy",
        #               ("-blended-analysis", "-generate-log", "-log-file", "log-file.log"), ("-unsound", "X")]
        self.combinations = []
        self.timeTaken = 0.0
        # for L in range(0, len(self.flags)+1):
        #     for subset in itertools.combinations(self.flags, L):
        #         self.combinations.append(subset)

    # def runAllCombinations(self):
    #     for combination in self.combinations:
    #         self.run(*combination)

    def run(self, *flags):
        print(">>>>> Running WALA on JS Program <<<<< ")
        command = self.baseCommand.copy()
        for arg in flags:
            if isinstance(arg, tuple):
                for a in arg:
                    command.append(a)
            else:
                command.append(arg)

        command.append(self.analysisFile)
        command.append(self.outputFile)
        tic = time.perf_counter()
        walaOutput = Popen(command, stdout=PIPE, stderr=STDOUT)
        toc = time.perf_counter()
        self.timeTaken = toc - tic
        print(f"WALA performed analysis in {self.timeTaken: 0.4f} seconds")
        pipeOutput = walaOutput.communicate()[0][:9].decode()
        if pipeOutput == 'Exception':
            print("WALA didn't terminate, resulted in exception")
            return
        return readToolOutput(wala=True)
