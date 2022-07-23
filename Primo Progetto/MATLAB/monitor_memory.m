% Questa funzione usa il comando WHOS per individuare gli elementi
% all'interno del BASE workspace. Dopodiché somma i byte di ciascun
% elemento e restituisce la somma in MB.
function [memory_in_use] = monitor_memory()
elements_in_memory = evalin('base','whos');
if size(elements_in_memory,1) > 0

    for i = 1:size(elements_in_memory,1)
        array_of_elements(i) = elements_in_memory(i).bytes;
    end
    memory_in_use = sum(array_of_elements);
    memory_in_use = memory_in_use/1048576;

else
    memory_in_use = 0;
end
