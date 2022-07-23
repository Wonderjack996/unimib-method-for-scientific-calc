## Settaggio wd
allPackageInstalled = installed.packages()[, 1]
if (!("rstudioapi" %in% allPackageInstalled)) {
  install.packages("rstudioapi")
}
library(rstudioapi)
setwd(dirname(getSourceEditorContext()$path))
rm(allPackageInstalled)

## Installazione di tutte le librerie necessarie

source(paste(getwd(), "PackageInstaller.R", sep = ""))

#### Import librerie necessarie

library(R.matlab)
library(spam)
library(spam64)
library(tictoc)
library(Matrix)
library(matrixcalc)

ex15 = read.MM(paste(dirname(getwd()), "/data/", "ex15.mtx", sep = ""))
save(ex15, file = "ex15.Rdata")

shallow_water1 = 
  read.MM(paste(dirname(getwd()), "/data/", "shallow_water1.mtx", sep = ""))
save(shallow_water1, file = "shallow_water1.Rdata")

cfd1 = 
  read.MM(paste(dirname(getwd()), "/data/", "cfd1.mtx", sep = ""))
save(cfd1, file = "cfd1.Rdata")

cfd2 = 
  read.MM(paste(dirname(getwd()), "/data/", "cfd2.mtx", sep = ""))
save(cfd2, file = "cfd2.Rdata")

apache2 = 
  read.MM(paste(dirname(getwd()), "/data/", "apache2.mtx", sep = ""))
save(apache2, file = "apache2.Rdata")

parabolic_fem =
  read.MM(paste(dirname(getwd()), "/data/", "parabolic_fem.mtx", sep = ""))
save(parabolic_fem, file = "parabolic_fem.Rdata")

G3_circuit =
  read.MM(paste(dirname(getwd()), "/data/", "G3_circuit.mtx", sep = ""))
save(G3_circuit, file = "G3_circuit.Rdata")

StocF_1465 =
  read.MM(paste(dirname(getwd()), "/data/", "StocF-1465.mtx", sep = ""))
save(StocF_1465, file = "StocF_1465.Rdata")

Flan_1565 =
  read.MM(paste(dirname(getwd()), "/data/", "Flan_1565.mtx", sep = ""))
save(Flan_1565, file = "Flan_1565.Rdata")