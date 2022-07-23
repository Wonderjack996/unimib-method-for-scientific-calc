// Cholesky-Eigen.cpp : Questo file contiene la funzione 'main', in cui inizia e termina l'esecuzione del programma.
//

#include <iostream>
#include "Framework.h"

#if defined(_MSC_VER)
#include <direct.h>
#define getcwd _getcwd
#elif defined(__GNUC__)
#include <unistd.h>
#endif

int main()
{
	std::cout << "[INFO] Please enter matrix file name (file must be inside a data folder): ";
	std::string fileName = "";

	std::cin >> fileName;

	while (fileName.empty() || fileName.find(".mtx") == std::string::npos) {
		std::cout << "[INFO] Please insert a valid mtx file: ";
		std::cin >> fileName;
	}

	char buff[FILENAME_MAX];

	if (getcwd(buff, FILENAME_MAX)) {

		std::string current_path = std::string(buff);

#if defined(_MSC_VER)
		current_path += "\\data\\" + fileName;
#elif defined(__GNUC__)
		current_path += "/data/" + fileName;
#endif

		Framework fChol = Framework(current_path.c_str());

		if (fChol.isMatrixLoaded()) {

			printf("[SUCCESS] Loaded Matrix\n");

			if (fChol.chol()) fChol.results();
		}
		else fChol.printDBG("File not found");
	}
	else std::cout << "[ERROR] Failed to parse current folder!" << std::endl;

#if defined(_MSC_VER)
	system("pause");
#elif defined(__GNUC__)
	std::cin.get();
#endif
	return 0;
}

