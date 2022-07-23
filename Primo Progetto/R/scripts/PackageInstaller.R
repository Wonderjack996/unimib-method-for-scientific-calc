##############################
## Istallazione Package     ##
##############################

## Ottenimento di tutti i package al momento istallati nell'ambiente corrente
allPackageInstalled = installed.packages()[, 1]

## rstudioapi
if (!("rstudioapi" %in% allPackageInstalled)) {
  install.packages("rstudioapi")
}

## R.matlab
if (!("R.matlab" %in% allPackageInstalled)) {
  install.packages("R.matlab")
}

## spam
if (!("spam" %in% allPackageInstalled)) {
  install.packages("spam")
}

## spam64
if (!("spam64" %in% allPackageInstalled)) {
  install.packages("spam64")
}

## tictoc
if (!("tictoc" %in% allPackageInstalled)) {
  install.packages("tictoc")
}

## Matrix
if (!("Matrix" %in% allPackageInstalled)) {
  install.packages("Matrix")
}

## matrixcalc
if (!("matrixcalc" %in% allPackageInstalled)) {
  install.packages('matrixcalc')
}

## RMark
if (!("RMark" %in% allPackageInstalled)) {
  install.packages("RMark")
}

## Settaggio wd
library(rstudioapi)
filePath = getSourceEditorContext()$path
setwd(dirname(filePath))

## Eliminazione della variabile non piu' utile
rm(allPackageInstalled)
rm(filePath)