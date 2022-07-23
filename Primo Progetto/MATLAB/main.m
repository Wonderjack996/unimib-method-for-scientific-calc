clear all, close all, clc;

% Caricamento matrici dalla cartella "matrixes".
matrixes = dir('matrixes\*.mat');

% Creazione delle variabili in cui salvare i risultati.
table_variables = {'name'; 'time (in seconds)'; 'relative error'; ...
    'initial memory usage (in MB)'; 'condition number'};
table_column_name = {};
table_column_time = [];
table_column_error = [];
table_column_initial_memory = [];
table_column_condition = [];

% Risoluzione di un sistem lineare con la fattorizzazione di Cholesky
% per ogni matrice.
for i=1:length(matrixes)

    % Caricamento della singola matrice A.
    matrix = load(['matrixes\', matrixes(i).name]);
    A = matrix.Problem.A;

    % Abilitazione della scrittura su file dell'output del terminale.
    diary on;
    
    % Stampa a schermo del nome della matrice.
    disp(matrix.Problem.name);

    % Calcolo della memoria occupata prima della risoluzione del sistema
    % lineare.
    memory_start = monitor_memory();
    memory_start
    
    % Calcolo del numero di condizionamento della matrice.
    k = condest(A);
   
    % Impostazione della soluzione esatta formata solo da 1.
    xe = ones(length(A),1);

    % Calcolo del vettore dei termini noti a partire dalla matrice A e
    % dalla soluzione esatta.
    b = A*xe;

    % Abilitazione della stampa a schermo di informazioni dettagliate
    % sulla risoluzione di sistemi lineari per matrici sparse.
    spparms('spumoni', 2);
   
    % Inizio del calcolo del tempo di risoluzione del sistema lineare.
    tic;

    % Risoluzione del sistema lineare con metodo di Cholesky.
    x = A\b;

    % Termine del calcolo del tempo di risoluzione del sistema lineare.
    time = toc;

    % Disabilitazione di diary.
    diary off;
    
    % Calcolo dell'errore relativo (come norma Euclidea) fra la soluzione 
    % calcolata e la soluzione esatta.
    error = norm(x-xe,2)/norm(xe,2);

    % Salvataggio dei risultati.
    table_column_name = [table_column_name, matrix.Problem.name];
    table_column_time = [table_column_time, time];
    table_column_error = [table_column_error, error];
    table_column_initial_memory = [table_column_initial_memory, memory_start];
    table_column_condition = [table_column_condition, k];

    % Rimozione delle variabili temporanee allocate. 
    clear memory_start;
    clear k, clear xe, clear b, clear x, clear time, clear error;
end

% Apertura del file csv per memorizzare i risultati su disco.
fileID = fopen('matlab.csv', 'w');

% Scrittura dei nomi delle variabili nel file csv.
for i = 1:length(table_variables)
    if i == length(table_variables)
        fprintf(fileID, '%s', table_variables{i}); 
    else
        fprintf(fileID, '%s,', table_variables{i});
    end
end

% Scrittura dei risultati nel file csv.
fprintf(fileID, '\n');
for i = 1: length(matrixes)
    fprintf(fileID, '%s,%d,%d,%d,%d\n', table_column_name{i}, ...
        table_column_time(i), table_column_error(i), ...
        table_column_initial_memory(i), table_column_condition(i));
end
fclose(fileID);

