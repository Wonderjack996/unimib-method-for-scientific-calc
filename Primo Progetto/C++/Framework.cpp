#include "Framework.h"

#if defined(_MSC_VER)
#include <Windows.h>
#include <Psapi.h>
#elif defined(__GNUC__)

#include "stdlib.h"
#include "stdio.h"
#include "string.h"

int parseLine(char* line) {
	// This assumes that a digit will be found and the line ends in " Kb".
	int i = strlen(line);
	const char* p = line;
	while (*p <'0' || *p > '9') p++;
	line[i - 3] = '\0';
	i = atoi(p);
	return i;
}

int getValue() { //Note: this value is in KB!
	FILE* file = fopen("/proc/self/status", "r");
	int result = -1;
	char line[128];

	while (fgets(line, 128, file) != NULL) {
		if (strncmp(line, "VmRSS:", 6) == 0) {
			result = parseLine(line);
			break;
		}
	}
	fclose(file);
	return result;
}
#endif

bool Framework::chol() {

	//Esclusione memoria programma
#if defined(_MSC_VER)
	PROCESS_MEMORY_COUNTERS pmc;
	GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc));
	double programMemory = pmc.WorkingSetSize / (1024.0 * 1024.0);
#elif defined(__GNUC__)
	double programMemory = getValue() / 1024;
#endif

	// Inizializzazione Matrice Simmetrica
	spMatrix resultMatrix = SparseMatrix.selfadjointView<Eigen::Lower>();
	SparseMatrix.data().clear();
	resultMatrix.makeCompressed();

	// Memoria Iniziale Matrice
#if defined(_MSC_VER)
	GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc));
	double initialMemory = pmc.WorkingSetSize / (1024.0 * 1024.0);
#elif defined(__GNUC__)
	double initialMemory = getValue() / 1024;
#endif

	initialMemory -= programMemory;
	InitialMemoryUsage = initialMemory;

	// Vettori soluzione esatta e termini noti
	VectorXd xe = VectorXd::Ones(resultMatrix.rows());
	VectorXd b = resultMatrix * xe;

	//Inizializzazione Solver
	PardisoLLT<spMatrix>  solver;

	// Inizio timer Choleksy
	auto start = std::chrono::high_resolution_clock::now();

	// Preparazione fattorizzazione matrice
	solver.analyzePattern(resultMatrix);

	// Fattorizzazione matrice
	solver.factorize(resultMatrix);

	// Calcolo soluzione
	VectorXd x = solver.solve(b);

	// Memoria Finale Matrice
#if defined(_MSC_VER)
	GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc));
	double finalMemory = pmc.WorkingSetSize / (1024.0 * 1024.0);
#elif defined(__GNUC__)
	double finalMemory = getValue() / 1024;
#endif

	// Calcolo memoria utilizzata Matrice fattorizzata
	MatrixMemoryUsage = finalMemory - initialMemory;

	// Fine timer Cholesky
	auto end = std::chrono::high_resolution_clock::now();
	std::chrono::duration<double> duration = end - start;

	// Tempo esecuzione cholesky in secondi
	ElapsedTime = duration.count();

	// Calcolo errore relativo
	RelativeError = (x - xe).norm() / xe.norm();
		
	return true;
}

void Framework::results() {

	// Metodo per print dei risulati ottenuti
	std::cout << "=== " << getMatrixName() << " === "  << std::endl;
	std::cout << "[>] Elapsed Time: " << ElapsedTime << " s" << std::endl;
	std::cout << "[>] Relative Error: " << RelativeError << std::endl;
	std::cout << "[>] Matrix Initial Memory Usage: " << InitialMemoryUsage << " MB" << std::endl;
	std::cout << "[>] Matrix Final Memory Usage: " << MatrixMemoryUsage << " MB" << std::endl;
}
