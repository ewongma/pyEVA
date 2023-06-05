import glob
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
import os
import shutil

from LoadCSV import LoadCSV


class PlotData:

    def __init__(self, level: int):
        self.files = []
        self.level = level
        self._find_all_xml("input/*.mz*ML")



    def _find_all_xml(self, path: str):
        for name in glob.glob(path):
            self.files.append(name)

    def plot_eic(self):
        if len(self.files) == 1:
            robjects.r('''
                library(dplyr)
                library(xcms)
                library(ggplot2)
                library(scales)
                peak_smooth <- function(x,level){
                    n <- level
                    if(length(x) < 2*n){
                      return(x)
                    } else if(length(unique(x))==1){
                      return(x)
                    } else{
                      y <- vector(length=length(x))
                      for(i in 1:n){
                        y[i] <- sum(c((n-i+2):(n+1),n:1)*x[1:(i+n)])/sum(c((n-i+2):(n+1),n:1))
                      }
                      for(i in (n+1):(length(y)-n)){
                        y[i] <-  sum(c(1:(n+1),n:1)*x[(i-n):(i+n)])/sum(c(1:(n+1),n:1))
                      }
                      for(i in (length(y)-n+1):length(y)){
                        y[i] <- sum(c(1:n,(n+1):(n+i-length(x)+1))*x[(i-n):length(x)])/sum(c(1:n,(n+1):(n+i-length(x)+1)))
                      }
                      return(y)
                    }
                }
                oneObject <- function(featureTable, input.files, level) {
                    xraw <- xcmsRaw(toString(input.files), profstep=0, mslevel = 1)
                    plot.matrix <- featureTable
                    plotmz.tol <- 0.01
                    plotrt.tol <- 60
                    if(nrow(plot.matrix)!=0){
                        for(k in 1:nrow(plot.matrix)){
                            rt.lower.limit <- plot.matrix$rt[k] - plotrt.tol
                            rt.upper.limit <- plot.matrix$rt[k] + plotrt.tol
                            mass.lower.limit <- plot.matrix$mz[k] - plotmz.tol
                            mass.upper.limit <- plot.matrix$mz[k] + plotmz.tol
                            mzRange <- as.double(cbind(mass.lower.limit, mass.upper.limit))
                            RTRange <- as.integer(cbind(rt.lower.limit, rt.upper.limit))
                            eeic <- rawEIC(xraw, mzrange=mzRange, rtrange=RTRange) #extracted EIC object
                            points <- cbind(xraw@scantime[eeic$scan], peak_smooth(eeic$intensity, level))
                            png(file = paste0(rownames(plot.matrix)[k], ".png"),
                                width = 480, height = 480)
                            eic <- plot(points, type="l", main="      ", xlab="Seconds",
                                    ylab="Intensity", xlim=RTRange)
                            dev.off()
                        }
                    }
                }
            ''')
            pandas2ri.activate()
            one_object = robjects.r['oneObject']
            one_object(LoadCSV().featureTable, self.files, self.level)
        else:
            robjects.r('''
                library(dplyr)
                library(xcms)
                library(ggplot2)
                library(scales)
                peak_smooth <- function(x,level){
                    n <- level
                    if(length(x) < 2*n){
                      return(x)
                    } else if(length(unique(x))==1){
                      return(x)
                    } else{
                      y <- vector(length=length(x))
                      for(i in 1:n){
                        y[i] <- sum(c((n-i+2):(n+1),n:1)*x[1:(i+n)])/sum(c((n-i+2):(n+1),n:1))
                      }
                      for(i in (n+1):(length(y)-n)){
                        y[i] <-  sum(c(1:(n+1),n:1)*x[(i-n):(i+n)])/sum(c(1:(n+1),n:1))
                      }
                      for(i in (length(y)-n+1):length(y)){
                        y[i] <- sum(c(1:n,(n+1):(n+i-length(x)+1))*x[(i-n):length(x)])/sum(c(1:n,(n+1):(n+i-length(x)+1)))
                      }
                      return(y)
                    }
                }
                moreObject <- function(featureTable, input.files, level) {
                    xraws <- list()
                    for(j in 1:length(input.files)){
                        xraws[[j]] <- xcmsRaw(toString(input.files[j]),profstep=0, mslevel = 1)
                    }
                    plot.matrix <- featureTable
                    plotmz.tol <- 0.01
                    plotrt.tol <- 60
                    if(nrow(plot.matrix)!=0){
                        for(k in 1:nrow(plot.matrix)){
                            rt.lower.limit <- plot.matrix$rt[k] - plotrt.tol
                            rt.upper.limit <- plot.matrix$rt[k] + plotrt.tol
                            mass.lower.limit <- plot.matrix$mz[k] - plotmz.tol
                            mass.upper.limit <- plot.matrix$mz[k] + plotmz.tol
                            mzRange <- as.double(cbind(mass.lower.limit, mass.upper.limit))
                            RTRange <- as.integer(cbind(rt.lower.limit, rt.upper.limit))
                            eeic <- rawEIC(xraws[[plot.matrix$sample[k]]], mzrange=mzRange, rtrange=RTRange) #extracted EIC object
                            points <- cbind(xraws[[plot.matrix$sample[k]]]@scantime[eeic$scan], peak_smooth(eeic$intensity, level))
                            png(file = paste0(rownames(plot.matrix)[k], ".png"),
                                width = 480, height = 480)
                            eic <- plot(points, type="l", main="      ", xlab="Seconds",
                                        ylab="Intensity", xlim=RTRange)
                            dev.off()
                        }
                    }
                }
            ''')
            pandas2ri.activate()
            more_object = robjects.r['moreObject']
            more_object(LoadCSV().featureTable, self.files, self.level)
        # all the eic images will be stored under classifier/dataset/test and will overwrite
        print("EICs are plotting now")
        if len(os.listdir('classifier/EICplots')) != 0:
            print("The test folder is not empty; re-running will replace all the existing EICs")
            for image in glob.glob('classifier/EICplots/*.png'):
                os.remove(image)
        for image in glob.glob("*.png"):
            new_path = "classifier/EICplots/" + image
            shutil.move(image, new_path)


if __name__ == '__main__':
    userinput = int(input("Enter a smoothing level (e.g., 0, 1, or 2. ‘0’ means no smoothing.):\n"))
    a = PlotData(level=userinput)
    a.plot_eic()

