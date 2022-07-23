## Settaggio wd
allPackageInstalled = installed.packages()[, 1]
if (!("rstudioapi" %in% allPackageInstalled)) {
  install.packages("rstudioapi")
}
library(rstudioapi)
setwd(dirname(getSourceEditorContext()$path))
rm(allPackageInstalled)

## Installazione di tutte le librerie necessarie

source(paste(getwd(), "/PackageInstaller.R", sep = ""))

## Import funzioni necessarie

source(paste(getwd(), "/Functions.R", sep = ""))

#### Import librerie necessarie

library(R.matlab)
library(spam)
library(spam64)
library(tictoc)
library(Matrix)

#### Fattorizzazione di Cholesky

## Matrix ex15

load(paste(dirname(getwd()),"/data/ex15.Rdata", sep = ""))

myChol(ex15)

rm(ex15)
gc()

## Matrix shallow_water1

load(paste(dirname(getwd()),"/data/shallow_water1.Rdata", sep = ""))

myChol(shallow_water1)

rm(shallow_water1)
gc()

## Matrix apache2

load(paste(dirname(getwd()),"/data/apache2.Rdata", sep = ""))

myChol(apache2)

rm(apache2)
gc()

## Matrix parabolic_fem

load(paste(dirname(getwd()),"/data/parabolic_fem.Rdata", sep = ""))

myChol(parabolic_fem)

rm(parabolic_fem)
gc()

## Matrix cfd1

load(paste(dirname(getwd()),"/data/cfd1.Rdata", sep = ""))

myChol(cfd1)

rm(cfd1)
gc()

## Matrix G3_circuit

load(paste(dirname(getwd()),"/data/G3_circuit.Rdata", sep = ""))

myChol(G3_circuit)

rm(G3_circuit)
gc()

## Matrix cfd2

load(paste(dirname(getwd()),"/data/cfd2.Rdata", sep = ""))

myChol(cfd2)

rm(cfd2)
gc()

## Matrix Flan_1565

load(paste(dirname(getwd()),"/data/Flan_1565.Rdata", sep = ""))

myChol(Flan_1565)

rm(Flan_1565)
gc()

## Matrix StocF_1465

load(paste(dirname(getwd()),"/data/StocF_1465.Rdata", sep = ""))

myChol(StocF_1465)

rm(StocF_1465)

rm(myChol)

gc()