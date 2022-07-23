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

#### Import librerie necessarie

library(R.matlab)
library(spam)
library(spam64)
library(tictoc)
library(Matrix)
library(matrixcalc)

#### Funzione per risoluzione con Cholesky

myChol = function(matrix) {
  
  name = deparse(substitute(matrix))
  
  ## Inizio Analisi
  print(paste("--------- ", name, " ---------", sep = ""))
  
  ## Calcolo dimensione della matrice
  matrix_size = object.size(matrix)
  print(matrix_size, units = "MB", standard = "SI", digits = 4L)
  print(paste("-> ", name, " - matrix size: ", matrix_size, sep = ""))
  
  ## Calcolo numero di non zeri
  matrix_nonzero = Matrix::nnzero(matrix)
  print(paste("-> ", name, " - matrix non zeros: ", matrix_nonzero, sep = ""))
  
  ## Check simmetria perché, se non lo è, non posso fare la fattorizzazione
  if (isSymmetric.spam(matrix) == F)
    return ("Matrix not Symmetric!")
  
  ## Calcolo della soluzione esatta (tutti 1) e del termine noto associato
  xe = rep(1, nrow(matrix))
  b = matrix %*% xe
  
  print("----------------------------------------------------")
  ## Esecuzione della decomposizione di Cholesky pivot MMD
  i = Sys.time()
  R = tryCatch(
    {
      chol.spam(matrix, pivot = "MMD")
    },
    error = function(e){
      ## Errore sollevato se la matrice non è definitiva positiva. Se non fosse
      ## stata simmetrica ci saremmo fermati al controllo di riga 50
      return (e)
    }
  )
  chol_time = difftime(Sys.time(), i, units = "secs")
  print(chol_time, digits = 4L)
  print(paste("-> ", name, " - chol time pivot MMD: ", chol_time, sep = ""))
  chol_size = object.size(R)
  print(chol_size, units = "MB", standard = "SI", digits = 4L)
  print(paste("-> ", name, " - chol size pivot MMD: ", chol_size, sep = ""))
  
  ## Risoluzione sistema lineare pivot MMD
  i = Sys.time()
  x = solve.spam(R,b)
  solve_time = difftime(Sys.time(), i, units = "secs")
  print(solve_time, digits = 4L)
  print(paste("-> ", name, " - solve time pivot MMD: ", solve_time, sep = ""))
  print(chol_time+solve_time, digits = 4L)
  print(paste("-> ", name, " - tot time pivot MMD: ", solve_time+chol_time, sep = ""))
  print("Total size: ")
  print(chol_size + object.size(x), units = "MB", standard = "SI", digits = 4L)
  
  ## Calcolo errore relativo
  rel_error = norm(xe - x, type = "2") / norm(xe, type = "2")
  print(rel_error, digits = 4L)
  print(paste("-> ", name, " - relative error pivot MMD: ", rel_error, sep = ""))
}
