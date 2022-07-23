#pragma once

#include <Eigen/Sparse>
#include <Eigen/PardisoSupport>
#include <unsupported/Eigen/SparseExtra>
#include <string>
#include <chrono>

using namespace Eigen;
using namespace std::chrono;

typedef SparseMatrix<double> spMatrix;

class Framework {

public:
	
	void printDBG(const char* error) { printf("[ERROR] %s\n", error); }

	bool isMatrixLoaded() { if (SparseMatrix.valuePtr()) return true; return false; }

	bool chol();

	void results();
	
	Framework(const char* fileName) {

		std::string input = fileName;

		if (input.empty()) { printDBG("Please provide a valid matrix file");  return; }

#if defined(_MSC_VER)
		MatrixName = input.substr(input.find_last_of("\\") + 1);
#elif defined(__GNUC__)
		MatrixName = input.substr(input.find_last_of("/") + 1);
		#endif
		loadMarket(SparseMatrix, input);
	}

	const char* getMatrixName() { return MatrixName.c_str(); }

private:
	spMatrix	SparseMatrix;
	double		RelativeError;
	double		ElapsedTime;
	double		MatrixMemoryUsage;
	double		InitialMemoryUsage;
	std::string	MatrixName;
};
